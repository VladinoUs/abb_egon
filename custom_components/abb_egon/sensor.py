from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import LIGHT_LUX, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
SENSOR_TYPES = {"TEMP", "SIG", "LIGHT"}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    elements = coordinator.data.get("elements", [])
    entities = [ABBSensor(coordinator, element) for element in elements if element.get("type") in SENSOR_TYPES]
    _LOGGER.debug("Sensor setup entities=%s", len(entities))
    async_add_entities(entities)


class ABBSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, element: dict[str, Any]) -> None:
        super().__init__(coordinator)
        self._element = element
        self._element_id = str(element["id"])
        self._attr_name = element.get("name", f"Sensor {self._element_id}")
        self._attr_unique_id = f"abb_egon_sensor_{self._element_id}"
        element_type = element.get("type")
        name_lower = self._attr_name.lower()
        if element_type == "TEMP" or "teplota" in name_lower or "temp" in name_lower:
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        elif element_type == "LIGHT":
            self._attr_native_unit_of_measurement = LIGHT_LUX
        _LOGGER.debug("Sensor init id=%s name=%s type=%s group=%s", self._element_id, self._attr_name, element.get('type'), element.get('group'))

    @property
    def native_value(self) -> str | float | int | None:
        value = self.coordinator.data.get("states", {}).get(self._element_id)
        _LOGGER.debug("Sensor native_value id=%s raw=%r", self._element_id, value)
        if value is None:
            return None
        try:
            return float(value) if "." in value else int(value)
        except (ValueError, TypeError):
            return value
