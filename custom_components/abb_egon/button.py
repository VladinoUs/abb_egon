from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    elements = coordinator.data.get("elements", [])
    entities = [ABBButton(coordinator, element) for element in elements if element.get("type") == "ACT"]
    _LOGGER.debug("Button setup entities=%s", len(entities))
    async_add_entities(entities)


class ABBButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, element: dict[str, Any]) -> None:
        super().__init__(coordinator)
        self._element = element
        self._element_id = str(element["id"])
        self._attr_name = element.get("name", f"Button {self._element_id}")
        self._attr_unique_id = f"abb_egon_button_{self._element_id}"
        _LOGGER.debug("Button init id=%s name=%s group=%s", self._element_id, self._attr_name, element.get('group'))

    async def async_press(self) -> None:
        _LOGGER.debug("Button press id=%s", self._element_id)
        await self.coordinator.api.async_send_action(self._element_id, "press")
        await self.coordinator.async_request_refresh()
