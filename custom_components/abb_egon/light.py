from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.light import ATTR_BRIGHTNESS, ColorMode, LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    elements = coordinator.data.get("elements", [])
    entities = [ABBLight(coordinator, element) for element in elements if element.get("type") == "DIMM"]
    _LOGGER.debug("Light setup entities=%s", len(entities))
    async_add_entities(entities)


class ABBLight(CoordinatorEntity, LightEntity):
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}
    _attr_color_mode = ColorMode.BRIGHTNESS

    def __init__(self, coordinator, element: dict[str, Any]) -> None:
        super().__init__(coordinator)
        self._element = element
        self._element_id = str(element["id"])
        self._attr_name = element.get("name", f"Light {self._element_id}")
        self._attr_unique_id = f"abb_egon_light_{self._element_id}"
        self._optimistic_brightness: int | None = None
        self._optimistic_is_on: bool | None = None
        _LOGGER.debug("Light init id=%s name=%s group=%s", self._element_id, self._attr_name, element.get('group'))

    def _raw_value(self) -> str | None:
        value = self.coordinator.data.get("states", {}).get(self._element_id)
        _LOGGER.debug("Light raw_value id=%s raw=%r", self._element_id, value)
        return value

    @property
    def is_on(self) -> bool:
        if self._optimistic_is_on is not None:
            _LOGGER.debug("Light is_on optimistic id=%s value=%s", self._element_id, self._optimistic_is_on)
            return self._optimistic_is_on
        value = self._raw_value()
        try:
            result = value is not None and int(float(value)) > 0
        except (ValueError, TypeError):
            result = False
        _LOGGER.debug("Light is_on real id=%s result=%s", self._element_id, result)
        return result

    @property
    def brightness(self) -> int | None:
        if self._optimistic_brightness is not None:
            _LOGGER.debug("Light brightness optimistic id=%s value=%s", self._element_id, self._optimistic_brightness)
            return self._optimistic_brightness
        value = self._raw_value()
        if value is None:
            return None
        try:
            percent = max(0, min(100, int(float(value))))
            result = round(percent * 255 / 100)
            _LOGGER.debug("Light brightness real id=%s percent=%s brightness=%s", self._element_id, percent, result)
            return result
        except (ValueError, TypeError):
            return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        brightness = kwargs.get(ATTR_BRIGHTNESS)
        if brightness is None:
            percent = 100
            optimistic_brightness = 255
        else:
            percent = max(0, min(100, round(brightness * 100 / 255)))
            optimistic_brightness = brightness
        _LOGGER.debug("Light turn_on id=%s brightness=%s mapped_percent=%s", self._element_id, brightness, percent)
        self._optimistic_is_on = True
        self._optimistic_brightness = optimistic_brightness
        self.async_write_ha_state()
        await self.coordinator.api.async_send_action(self._element_id, str(percent))
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        _LOGGER.debug("Light turn_off id=%s", self._element_id)
        self._optimistic_is_on = False
        self._optimistic_brightness = 0
        self.async_write_ha_state()
        await self.coordinator.api.async_send_action(self._element_id, "0")
        await self.coordinator.async_request_refresh()

    def _handle_coordinator_update(self) -> None:
        _LOGGER.debug("Light coordinator_update id=%s raw=%r", self._element_id, self.coordinator.data.get('states', {}).get(self._element_id))
        if self._raw_value() is not None:
            self._optimistic_is_on = None
            self._optimistic_brightness = None
        super()._handle_coordinator_update()
