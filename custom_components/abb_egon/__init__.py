from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ABBEgonClient
from .const import DOMAIN, PLATFORMS, DEFAULT_PASSWORD, DEFAULT_PORT, DEFAULT_USERNAME
from .coordinator import ABBEgonDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


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

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.debug(
        "ABB Egon async_setup_entry done entry_id=%s platforms=%s",
        entry.entry_id,
        PLATFORMS,
    )
    return True


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


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry when options change."""
    _LOGGER.debug("ABB Egon async_reload_entry entry_id=%s", entry.entry_id)
    await hass.config_entries.async_reload(entry.entry_id)
