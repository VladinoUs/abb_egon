from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ABBEgonClient
from .const import DOMAIN, PLATFORMS, DEFAULT_PASSWORD, DEFAULT_PORT, DEFAULT_USERNAME
from .coordinator import ABBEgonDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up ABB Egon integration."""
    hass.data.setdefault(DOMAIN, {})
    _LOGGER.debug("ABB Egon async_setup called")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ABB Egon from a config entry."""
    _LOGGER.debug("ABB Egon async_setup_entry start entry_id=%s", entry.entry_id)

    session = async_get_clientsession(hass)

    api = ABBEgonClient(
        session=session,
        host=entry.data[CONF_HOST],
        port=entry.data.get(CONF_PORT, DEFAULT_PORT),
        username=entry.data.get(CONF_USERNAME, DEFAULT_USERNAME),
        password=entry.data.get(CONF_PASSWORD, DEFAULT_PASSWORD),
    )

    coordinator = ABBEgonDataUpdateCoordinator(hass, api, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    _async_cleanup_stale_entities(hass, entry, coordinator)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.debug(
        "ABB Egon async_setup_entry done entry_id=%s platforms=%s",
        entry.entry_id,
        PLATFORMS,
    )
    return True


def _async_cleanup_stale_entities(
    hass: HomeAssistant,
    entry: ConfigEntry,
    coordinator: ABBEgonDataUpdateCoordinator,
) -> None:
    """Remove entities that are no longer part of the selected elements."""
    if coordinator.selected_element_ids is None:
        _LOGGER.debug("ABB Egon cleanup skipped, no element filter active")
        return

    registry = er.async_get(hass)

    allowed_unique_ids: set[str] = set()
    for element in coordinator.data.get("elements", []):
        element_id = str(element["id"])
        element_type = element.get("type")

        if element_type == "SW":
            allowed_unique_ids.add(f"abb_egon_switch_{element_id}")
        elif element_type == "DIMM":
            allowed_unique_ids.add(f"abb_egon_light_{element_id}")
        elif element_type == "TMPSET":
            allowed_unique_ids.add(f"abb_egon_number_{element_id}")
        elif element_type == "ROLL":
            allowed_unique_ids.add(f"{entry.entry_id}-cover-{element_id}")
        elif element_type == "ACT":
            allowed_unique_ids.add(f"abb_egon_button_{element_id}")
        elif element_type in {"TEMP", "SIG", "LIGHT"}:
            allowed_unique_ids.add(f"abb_egon_sensor_{element_id}")

    entries_to_remove: list[str] = []

    for entity_entry in list(registry.entities.values()):
        if entity_entry.config_entry_id != entry.entry_id:
            continue

        if entity_entry.unique_id not in allowed_unique_ids:
            entries_to_remove.append(entity_entry.entity_id)

    for entity_id in entries_to_remove:
        _LOGGER.debug("ABB Egon removing stale entity=%s", entity_id)
        registry.async_remove(entity_id)

    _LOGGER.debug(
        "ABB Egon cleanup complete allowed=%s removed=%s",
        len(allowed_unique_ids),
        len(entries_to_remove),
    )


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload ABB Egon config entry."""
    _LOGGER.debug("ABB Egon async_unload_entry start entry_id=%s", entry.entry_id)

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    _LOGGER.debug(
        "ABB Egon async_unload_entry done entry_id=%s unload_ok=%s",
        entry.entry_id,
        unload_ok,
    )
    return unload_ok
