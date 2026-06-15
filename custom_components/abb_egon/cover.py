from __future__ import annotations

import asyncio
import logging
from typing import Any

from homeassistant.components.cover import (
    CoverDeviceClass,
    CoverEntity,
    CoverEntityFeature,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

LOGGER = logging.getLogger(__name__)


def normalize_cover_state(value: str | None) -> str | None:
    if value is None:
        return None

    state = str(value).strip().lower()
    aliases = {
        "up": "uprun",
        "uprun": "uprun",
        "open": "uprun",
        "opening": "uprun",
        "upstop": "upstop",
        "down": "downrun",
        "downrun": "downrun",
        "close": "downrun",
        "closing": "downrun",
        "downstop": "downstop",
        "stop": "stop",
    }
    return aliases.get(state, state)


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[ABBEgonCover] = []

    for element in coordinator.data.get("elements", []):
        if element.get("type") == "ROLL":
            entities.append(ABBEgonCover(coordinator, entry, element))

    LOGGER.debug("Cover setup entities=%s", len(entities))
    async_add_entities(entities)


class ABBEgonCover(CoordinatorEntity, CoverEntity):
    _attr_has_entity_name = True
    _attr_device_class = CoverDeviceClass.SHUTTER
    _attr_supported_features = (
        CoverEntityFeature.OPEN
        | CoverEntityFeature.CLOSE
        | CoverEntityFeature.STOP
    )

    def __init__(self, coordinator, entry, element: dict[str, Any]) -> None:
        super().__init__(coordinator)
        self.entry = entry
        self.api = coordinator.api
        self.id = str(element.get("id"))
        self.type = element.get("type")
        self.group = element.get("group", 0)

        self._attr_unique_id = f"{entry.entry_id}-cover-{self.id}"
        self._attr_name = element.get("name", f"Cover {self.id}")

        self.optimistic_state: str | None = None
        self.last_direction: str | None = None
        self._action_lock = asyncio.Lock()

        LOGGER.debug(
            "Cover init id=%s name=%s group=%s",
            self.id,
            self._attr_name,
            self.group,
        )

    @property
    def assumed_state(self) -> bool:
        return True

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            "abb_id": self.id,
            "abb_type": self.type,
            "abb_group": self.group,
            "abb_real_state": self.real_state,
            "abb_effective_state": self.effective_state,
            "abb_last_direction": self.last_direction,
            "abb_optimistic_state": self.optimistic_state,
        }

    @property
    def raw_value(self) -> str | None:
        data = self.coordinator.data or {}
        states = data.get("states", {})
        return states.get(self.id)

    @property
    def real_state(self) -> str | None:
        raw = self.raw_value
        state = normalize_cover_state(raw)
        LOGGER.debug("Cover real_state id=%s raw=%s normalized=%s", self.id, raw, state)
        return state

    @property
    def effective_state(self) -> str | None:
        optimistic = normalize_cover_state(self.optimistic_state)
        real = self.real_state

        if optimistic and optimistic == real:
            self.optimistic_state = None
            optimistic = None

        effective = optimistic or real
        LOGGER.debug(
            "Cover effective_state id=%s optimistic=%s real=%s effective=%s",
            self.id,
            optimistic,
            real,
            effective,
        )
        return effective

    @property
    def is_opening(self) -> bool | None:
        return self.effective_state == "uprun"

    @property
    def is_closing(self) -> bool | None:
        return self.effective_state == "downrun"

    @property
    def is_closed(self) -> bool | None:
        state = self.effective_state
        if state == "downstop":
            return True
        if state == "upstop":
            return False
        if state in ("uprun", "downrun"):
            return False
        return None

    async def _send_action(self, action: str, optimistic_state: str | None = None) -> None:
        async with self._action_lock:
            normalized_action = normalize_cover_state(action) or action
            normalized_optimistic = normalize_cover_state(optimistic_state)

            LOGGER.debug(
                "Cover send_action id=%s action=%s optimistic_state=%s",
                self.id,
                normalized_action,
                normalized_optimistic,
            )

            if normalized_optimistic:
                self.optimistic_state = normalized_optimistic
                self.async_write_ha_state()

            try:
                if normalized_action == "uprun":
                    await self.api.async_send_action(self.id, "UP")
                elif normalized_action == "downrun":
                    await self.api.async_send_action(self.id, "DOWN")
                else:
                    raise ValueError(f"Unsupported cover action: {action}")

                await self.coordinator.async_refresh()
            except Exception:
                self.optimistic_state = None
                self.async_write_ha_state()
                raise

    async def async_open_cover(self, **kwargs: Any) -> None:
        LOGGER.debug("Cover open id=%s", self.id)
        current = self.effective_state
        self.last_direction = "uprun"

        if current == "uprun":
            await self._send_action("uprun", optimistic_state="upstop")
        else:
            await self._send_action("uprun", optimistic_state="uprun")

    async def async_close_cover(self, **kwargs: Any) -> None:
        LOGGER.debug("Cover close id=%s", self.id)
        current = self.effective_state
        self.last_direction = "downrun"

        if current == "downrun":
            await self._send_action("downrun", optimistic_state="downstop")
        else:
            await self._send_action("downrun", optimistic_state="downrun")

    async def async_stop_cover(self, **kwargs: Any) -> None:
        current = self.effective_state

        if current == "uprun" or self.last_direction == "uprun":
            LOGGER.debug("Cover stop id=%s via UP", self.id)
            await self._send_action("uprun", optimistic_state="upstop")
            return

        if current == "downrun" or self.last_direction == "downrun":
            LOGGER.debug("Cover stop id=%s via DOWN", self.id)
            await self._send_action("downrun", optimistic_state="downstop")
            return

        LOGGER.debug("Cover stop id=%s skipped no known direction", self.id)