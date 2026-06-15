from __future__ import annotations

from homeassistant.const import Platform

DOMAIN = "abb_egon"
PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.LIGHT,
    Platform.COVER,
    Platform.NUMBER,
    Platform.BUTTON,
]
DEFAULT_NAME = "ABB Egon"
DEFAULT_PORT = 80
DEFAULT_USERNAME = "ABB"
DEFAULT_PASSWORD = "egon"
DEFAULT_SCAN_INTERVAL = 15
MIN_SCAN_INTERVAL = 5
MAX_SCAN_INTERVAL = 300
MAX_GROUPS = 16
OPTION_SCAN_INTERVAL = "scan_interval"
