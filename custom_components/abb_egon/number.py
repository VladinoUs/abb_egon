from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    elements = coordinator.data.get("elements", [])
    entities = [ABBNumber(coordinator, element) for element in elements if element.get("type") == "TMPSET"]
    _LOGGER.debug("Number setup entities=%s", len(entities))
    async_add_entities(entities)


class ABBNumber(CoordinatorEntity, NumberEntity):
    _attr_native_min_value = -27
    _attr_native_max_value = 100
    _attr_native_step = 0.5
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator, element: dict[str, Any]) -> None:
        super().__init__(coordinator)
        self._element = element
        self._element_id = str(element["id"])
        self._attr_name = element.get("name", f"Number {self._element_id}")
        self._attr_unique_id = f"abb_egon_number_{self._element_id}"
        self._optimistic_value: float | None = None
        _LOGGER.debug("Number init id=%s name=%s group=%s", self._element_id, self._attr_name, element.get('group'))

    @property
    def native_value(self) -> float | None:
        if self._optimistic_value is not None:
            _LOGGER.debug("Number native_value optimistic id=%s value=%s", self._element_id, self._optimistic_value)
            return self._optimistic_value
        value = self.coordinator.data.get("states", {}).get(self._element_id)
        _LOGGER.debug("Number native_value real id=%s raw=%r", self._element_id, value)
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    async def async_set_native_value(self, value: float) -> None:
        _LOGGER.debug("Number set_value id=%s value=%s", self._element_id, value)
        self._optimistic_value = value
        self.async_write_ha_state()
        await self.coordinator.api.async_send_action(self._element_id, str(value))
        await self.coordinator.async_request_refresh()

    def _handle_coordinator_update(self) -> None:
        _LOGGER.debug("Number coordinator_update id=%s raw=%r", self._element_id, self.coordinator.data.get('states', {}).get(self._element_id))
        if self.coordinator.data.get("states", {}).get(self._element_id) is not None:
            self._optimistic_value = None
        super()._handle_coordinator_update()
