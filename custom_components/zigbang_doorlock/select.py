import logging
from datetime import timedelta
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)


async def async_setup_entry(hass, entry, async_add_entities):
    """select 플랫폼 설정"""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    api = data["api"]

    entities = []
    for device_id in coordinator.data:
        entities.append(ZigbangDoorKeySelect(coordinator, api, device_id, "RFC"))
        entities.append(ZigbangDoorKeySelect(coordinator, api, device_id, "FGP"))

    if entities:
        async_add_entities(entities, True)


class ZigbangDoorKeySelect(SelectEntity):
    """직방 도어락 카드키/지문 선택 엔티티."""

    def __init__(self, coordinator, api, device_id: str, pin_type: str):
        self.coordinator = coordinator
        self.api = api
        self._device_id = device_id
        self._pin_type = pin_type
        self._options: list[str] = []
        self._key_by_option: dict[str, dict[str, Any]] = {}
        self._current_option: str | None = None

        device = coordinator.data[self._device_id]
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
            "name": device.get("userNick", "Zigbang Doorlock"),
            "model": device.get("modelNm", "SHP-Series"),
            "manufacturer": "Samsung",
        }
        suffix = "card_key" if pin_type == "RFC" else "fingerprint"
        self._attr_unique_id = f"{device_id}_{suffix}_selector"
        self._attr_has_entity_name = True
        self._attr_name = "카드키 선택" if pin_type == "RFC" else "지문 선택"
        self._attr_icon = "mdi:card-account-details-outline" if pin_type == "RFC" else "mdi:fingerprint"

    @property
    def available(self) -> bool:
        return self._device_id in self.coordinator.data

    @property
    def options(self) -> list[str]:
        return self._options

    @property
    def current_option(self) -> str | None:
        return self._current_option

    @property
    def extra_state_attributes(self):
        selected = self._key_by_option.get(self._current_option or "", {})
        return {
            "device_id": self._device_id,
            "pin_type": self._pin_type,
            "key_count": len(self._options),
            "selected_pin_id": selected.get("pinId"),
            "selected_pin_name": selected.get("pinName") or selected.get("pinMemberNm"),
            "selected_pin_member_id": selected.get("pinMemberId"),
            "selected_pin": selected.get("pin"),
            "selected_pin_info": selected or None,
        }

    async def async_select_option(self, option: str) -> None:
        if option not in self._key_by_option:
            raise ValueError(f"Unknown Zigbang key option: {option}")
        self._current_option = option
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """카드키/지문 목록을 조회해 UI 선택지를 갱신합니다."""
        session = async_get_clientsession(self.hass)
        if self._pin_type == "RFC":
            keys = await self.api.fetch_card_keys(session, self._device_id)
        else:
            keys = await self.api.fetch_fingerprints(session, self._device_id)

        options: list[str] = []
        key_by_option: dict[str, dict[str, Any]] = {}
        for key in keys:
            label = self._format_option(key)
            options.append(label)
            key_by_option[label] = key

        self._options = options
        self._key_by_option = key_by_option
        if self._current_option not in self._key_by_option:
            self._current_option = self._options[0] if self._options else None

    def _format_option(self, key: dict[str, Any]) -> str:
        pin_id = key.get("pinId")
        name = (
            key.get("pinName")
            or key.get("pinMemberNm")
            or key.get("pinMemberId")
            or ("카드키" if self._pin_type == "RFC" else "지문")
        )
        return f"{name} (ID {pin_id})"
