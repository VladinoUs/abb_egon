from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    elements = coordinator.data.get("elements", [])
    entities = [
        ABBSwitch(coordinator, element)
        for element in elements
        if element.get("type") == "SW"
    ]
    _LOGGER.debug("Switch setup entities=%s", len(entities))
    async_add_entities(entities)


class ABBSwitch(CoordinatorEntity, SwitchEntity):
    """ABB Egon switch entity."""

    def __init__(self, coordinator, element: dict[str, Any]) -> None:
        super().__init__(coordinator)
        self._element = element
        self._element_id = str(element["id"])
        self._attr_name = element.get("name", f"Switch {self._element_id}")
        self._attr_unique_id = f"abb_egon_switch_{self._element_id}"

        self._optimistic_is_on: bool | None = None

        _LOGGER.debug(
            "Switch init id=%s name=%s group=%s",
            self._element_id,
            self._attr_name,
            element.get("group"),
        )

    def _raw_value(self) -> str | None:
        value = self.coordinator.data.get("states", {}).get(self._element_id)
        if value is not None:
            value = str(value).strip().lower()
        _LOGGER.debug("Switch raw_value id=%s raw=%r", self._element_id, value)
        return value

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    @property
    def is_on(self) -> bool | None:
        if self._optimistic_is_on is not None:
            _LOGGER.debug(
                "Switch is_on optimistic id=%s value=%s",
                self._element_id,
                self._optimistic_is_on,
            )
            return self._optimistic_is_on

        value = self._raw_value()
        if value is None:
            result = None
        else:
            result = value in {"1", "on", "true"}

        _LOGGER.debug(
            "Switch is_on real id=%s raw=%r result=%s",
            self._element_id,
            value,
            result,
        )
        return result

    async def async_turn_on(self, **kwargs: Any) -> None:
        _LOGGER.debug("Switch turn_on id=%s", self._element_id)

        self._optimistic_is_on = True
        self.async_write_ha_state()

        await self.coordinator.api.async_send_action(self._element_id, "on")
        await self.coordinator.async_request_refresh()

        raw_value = self._raw_value()
        if raw_value is not None:
            _LOGGER.debug(
                "Switch turn_on confirmed id=%s raw=%r",
                self._element_id,
                raw_value,
            )
            self._optimistic_is_on = None
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        _LOGGER.debug("Switch turn_off id=%s", self._element_id)

        self._optimistic_is_on = False
        self.async_write_ha_state()

        await self.coordinator.api.async_send_action(self._element_id, "off")
        await self.coordinator.async_request_refresh()

        raw_value = self._raw_value()
        if raw_value is not None:
            _LOGGER.debug(
                "Switch turn_off confirmed id=%s raw=%r",
                self._element_id,
                raw_value,
            )
            self._optimistic_is_on = None
            self.async_write_ha_state()

    def _handle_coordinator_update(self) -> None:
        raw_value = self._raw_value()
        _LOGGER.debug(
            "Switch coordinator_update id=%s raw=%r optimistic=%r",
            self._element_id,
            raw_value,
            self._optimistic_is_on,
        )

        if raw_value is not None:
            self._optimistic_is_on = None

        super()._handle_coordinator_update()