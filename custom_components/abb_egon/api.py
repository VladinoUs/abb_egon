from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urlencode

import aiohttp

_LOGGER = logging.getLogger(__name__)


class ABBEgonClient:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        session: aiohttp.ClientSession,
        timeout: int = 15,
    ) -> None:
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._session = session
        self._timeout = aiohttp.ClientTimeout(total=timeout)

        self._base_url = f"http://{self._host}:{self._port}"
        self._device: str | None = None

        _LOGGER.debug(
            "ABBEgonClient initialized host=%s port=%s username=%s",
            self._host,
            self._port,
            self._username,
        )

    @property
    def device(self) -> str | None:
        return self._device

    async def _async_http_get(self, path: str, params: dict[str, Any] | None = None) -> str:
        query = urlencode(params or {})
        url = f"{self._base_url}/{path}"
        if query:
            url = f"{url}?{query}"

        _LOGGER.debug("ABB Egon HTTP GET %s", url)

        async with self._session.get(url, timeout=self._timeout) as response:
            text = await response.text(errors="ignore")
            _LOGGER.debug(
                "ABB Egon HTTP response path=%s status=%s length=%s",
                path,
                response.status,
                len(text),
            )
            response.raise_for_status()
            return text

    async def async_authorize(self) -> str:
        _LOGGER.debug(
            "ABB Egon authorize start url=%s/authorize.html username=%s",
            self._base_url,
            self._username,
        )

        text = await self._async_http_get(
            "authorize.html",
            {
                "user": self._username,
                "password": self._password,
            },
        )

        device = text.strip()
        if "=" in device:
            key, value = device.split("=", 1)
            if key.strip().lower() == "device":
                device = value.strip()

        if not device:
            raise ValueError("ABB Egon authorization returned empty device id")

        self._device = device
        _LOGGER.debug(
            "ABB Egon authorize success raw=%s normalized_device=%s",
            text.strip(),
            self._device,
        )
        return self._device

    async def _async_authenticated_get(
        self,
        path: str,
        extra_params: dict[str, Any] | None = None,
    ) -> str:
        if not self._device:
            await self.async_authorize()

        params = dict(extra_params or {})
        params["device"] = self._device

        text = await self._async_http_get(path, params)
        _LOGGER.debug(
            "ABB Egon authenticatedget success path=%s responselength=%s",
            path,
            len(text),
        )
        return text

    async def async_get_config(self) -> str:
        _LOGGER.debug("ABB Egon getconfig device=%s", self._device)
        return await self._async_authenticated_get("config.html")

    async def async_get_state(self, group: int | str) -> str:
        _LOGGER.debug("ABB Egon getstate group=%s device=%s", group, self._device)
        return await self._async_authenticated_get("state.html", {"group": group})

    async def async_get_all_states(self) -> str:
        _LOGGER.debug("ABB Egon getallstates device=%s", self._device)
        return await self._async_authenticated_get("state.html", {"group": 11})

    async def async_send_action(self, element_id: str | int, action: str | int) -> str:
        raw_action = str(action).strip()
        normalized = raw_action.lower()

        if normalized.isdigit():
            abb_action = normalized
        else:
            action_map = {
                "press": "ON",
                "on": "ON",
                "off": "OFF",
                "turn_on": "ON",
                "turn_off": "OFF",
                "up": "UP",
                "uprun": "UP",
                "open": "UP",
                "down": "DOWN",
                "downrun": "DOWN",
                "close": "DOWN",
            }

            abb_action = action_map.get(normalized)
            if abb_action is None:
                raise ValueError(f"Unsupported ABB Egon action: {action}")

        _LOGGER.debug(
            "ABB Egon sendaction id=%s action=%s mapped_action=%s device=%s",
            element_id,
            raw_action,
            abb_action,
            self._device,
        )

        response = await self._async_authenticated_get(
            "action.html",
            {
                "id": str(element_id),
                "action": abb_action,
            },
        )

        _LOGGER.debug(
            "ABB Egon sendaction response id=%s action=%s response=%s",
            element_id,
            abb_action,
            response.strip(),
        )
        return response.strip()