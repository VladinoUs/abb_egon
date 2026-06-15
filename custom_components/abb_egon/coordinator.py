from __future__ import annotations

from datetime import timedelta
import logging
from xml.etree import ElementTree as ET

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN, MAX_GROUPS, OPTION_SCAN_INTERVAL

LOGGER = logging.getLogger(__name__)


class ABBEgonDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator for ABB Egon."""

    def __init__(self, hass, api, entry) -> None:
        self.api = api
        self.entry = entry
        self.config_loaded = False
        self.elements: list[dict] = []
        self.groups: set[int] = set()
        self.element_to_groups: dict[str, set[int]] = {}

        scan_interval = entry.options.get(OPTION_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

        LOGGER.debug(
            "Coordinator init entryid=%s scaninterval=%s",
            entry.entry_id,
            scan_interval,
        )

        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> dict:
        LOGGER.debug(
            "Coordinator update start configloaded=%s device=%s",
            self.config_loaded,
            self.api.device,
        )

        try:
            if not self.api.device:
                LOGGER.debug("Coordinator no device token, authorizing")
                await self.api.async_authorize()

            if not self.config_loaded:
                LOGGER.debug("Coordinator config not loaded, loading config")
                await self.async_load_config()

            states = await self.async_load_states(self.groups, learn_groups=True)

            payload = {
                "elements": self.elements,
                "states": states,
            }

            LOGGER.debug(
                "Coordinator update success elements=%s states=%s groups=%s",
                len(self.elements),
                len(states),
                sorted(self.groups),
            )
            return payload

        except Exception as err:
            LOGGER.debug("Coordinator update failed err=%s", err, exc_info=True)
            raise UpdateFailed(f"Error communicating with ABB Egon: {err}") from err

    async def async_load_config(self) -> None:
        try:
            xml_text = await self.api.async_get_config()
            LOGGER.debug(
                "Coordinator config raw length=%s snippet=%r",
                len(xml_text),
                xml_text[:500],
            )
            root = ET.fromstring(xml_text)
        except Exception as err:
            LOGGER.debug("Coordinator config load failed err=%s", err, exc_info=True)
            raise UpdateFailed(f"Unable to load ABB Egon config: {err}") from err

        elements_by_id: dict[str, dict] = {}
        groups: set[int] = set()
        element_to_groups: dict[str, set[int]] = {}

        for elem in root.findall(".//elements/element"):
            try:
                element_id = elem.attrib.get("id")
                element_type = elem.attrib.get("type")
                element_name = elem.attrib.get("name", f"Element {element_id}")

                if not element_id or not element_type:
                    LOGGER.debug(
                        "Coordinator skipping config element missing id/type attribs=%s",
                        dict(elem.attrib),
                    )
                    continue

                item = {
                    "id": str(element_id),
                    "type": element_type,
                    "name": element_name,
                    "group": 0,
                }

                elements_by_id[str(element_id)] = item
                element_to_groups[str(element_id)] = set()

                LOGGER.debug("Coordinator parsed base element=%s", item)

            except Exception as err:
                LOGGER.debug(
                    "Coordinator skipping invalid base config element attribs=%s err=%s",
                    dict(elem.attrib),
                    err,
                )

        for group_elem in root.findall(".//groups/group"):
            try:
                group_id_raw = group_elem.attrib.get("id")
                if not group_id_raw:
                    continue

                group_id = int(group_id_raw)
                groups.add(group_id)

                for member in group_elem.findall("./element"):
                    member_id = member.attrib.get("id")
                    if not member_id or member_id == "":
                        continue

                    member_id = str(member_id)
                    element_to_groups.setdefault(member_id, set()).add(group_id)

                    if member_id in elements_by_id and elements_by_id[member_id]["group"] == 0:
                        elements_by_id[member_id]["group"] = group_id

            except Exception as err:
                LOGGER.debug(
                    "Coordinator skipping invalid group attribs=%s err=%s",
                    dict(group_elem.attrib),
                    err,
                )

        if not groups:
            groups = set(range(1, MAX_GROUPS + 1))
            LOGGER.debug(
                "Coordinator no groups in config, using fallback groups=%s",
                sorted(groups),
            )

        self.elements = list(elements_by_id.values())
        self.groups = groups
        self.element_to_groups = element_to_groups
        self.config_loaded = True

        LOGGER.debug(
            "Coordinator config loaded elements=%s groups=%s elementtogroupssample=%s",
            len(self.elements),
            sorted(self.groups),
            {k: sorted(v) for k, v in list(self.element_to_groups.items())[:10]},
        )

    async def async_load_states(
        self,
        groups: set[int],
        learn_groups: bool = False,
    ) -> dict[str, str]:
        try:
            xml_text = await self.api.async_get_all_states()
            LOGGER.debug(
                "Coordinator full state raw length=%s snippet=%r",
                len(xml_text),
                xml_text[:500],
            )
            states = self.parse_state_xml(xml_text)
            LOGGER.debug(
                "Coordinator full state parsed count=%s sample=%s",
                len(states),
                list(states.items())[:10],
            )
            return states
        except Exception as err:
            LOGGER.debug(
                "Coordinator full state load failed err=%s, fallback to groups",
                err,
                exc_info=True,
            )

        states: dict[str, str] = {}
        discovered: dict[str, set[int]] = {}

        for group in sorted(groups):
            try:
                xml_text = await self.api.async_get_state(group)
                LOGGER.debug(
                    "Coordinator state raw group=%s length=%s snippet=%r",
                    group,
                    len(xml_text),
                    xml_text[:500],
                )
                group_states = self.parse_state_xml(xml_text)
                LOGGER.debug(
                    "Coordinator parsed group=%s states=%s",
                    group,
                    group_states,
                )
                states.update(group_states)

                if learn_groups:
                    for element_id in group_states:
                        discovered.setdefault(str(element_id), set()).add(group)

            except Exception as err:
                LOGGER.debug(
                    "Coordinator failed loading group=%s err=%s",
                    group,
                    err,
                    exc_info=True,
                )

        if learn_groups and discovered:
            self.merge_discovered_groups(discovered)

        return states

    def merge_discovered_groups(self, discovered: dict[str, set[int]]) -> None:
        if not discovered:
            return

        element_index = {str(element["id"]): element for element in self.elements}

        for element_id, groups in discovered.items():
            if not groups:
                continue

            current = self.element_to_groups.setdefault(element_id, set())
            before = set(current)
            current.update(groups)

            if element_id in element_index and element_index[element_id].get("group", 0) == 0:
                element_index[element_id]["group"] = min(current)

            if current != before:
                LOGGER.debug(
                    "Coordinator learned groups elementid=%s groups=%s",
                    element_id,
                    sorted(current),
                )

    def parse_state_xml(self, xml_text: str) -> dict[str, str]:
        root = ET.fromstring(xml_text)
        states: dict[str, str] = {}

        for elem in root.iter():
            attrib = {str(key).lower(): value for key, value in elem.attrib.items()}

            element_id = (
                attrib.get("id")
                or attrib.get("elementid")
                or attrib.get("element_id")
            )
            value = (
                attrib.get("value")
                or attrib.get("current")
                or attrib.get("state")
                or attrib.get("val")
            )

            if value is None and elem.text:
                text = elem.text.strip()
                if text:
                    value = text

            if element_id is None:
                continue

            if value in (None, ""):
                continue

            states[str(element_id).strip()] = str(value).strip()

        LOGGER.debug(
            "Coordinator parsestatexml parsedcount=%s sample=%s",
            len(states),
            list(states.items())[:10],
        )
        return states

    async def async_refresh_element(self, element_id: str) -> None:
        element_id = str(element_id)
        groups = self.element_to_groups.get(element_id, set())

        if not groups:
            LOGGER.debug(
                "Coordinator refreshelement id=%s no mapped groups, fallback full refresh",
                element_id,
            )
            await self.async_request_refresh()
            return

        LOGGER.debug(
            "Coordinator refreshelement id=%s groups=%s",
            element_id,
            sorted(groups),
        )

        try:
            partial_states = await self.async_load_states(groups, learn_groups=False)
            current = dict(self.data or {})
            current_states = dict(current.get("states", {}))
            current_states.update(partial_states)

            payload = {
                "elements": current.get("elements", self.elements),
                "states": current_states,
            }
            self.async_set_updated_data(payload)

            LOGGER.debug(
                "Coordinator refreshelement success id=%s updatedstates=%s",
                element_id,
                list(partial_states.keys()),
            )

        except Exception as err:
            LOGGER.debug(
                "Coordinator refreshelement failed id=%s err=%s",
                element_id,
                err,
                exc_info=True,
            )
            await self.async_request_refresh()

    async def async_reload_config(self) -> None:
        LOGGER.debug("Coordinator reloadconfig requested")
        self.config_loaded = False
        self.elements = []
        self.groups = set()
        self.element_to_groups = {}
        await self.async_request_refresh()