import logging
from homeassistant.components.lock import LockEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, ALERT_TYPE, UNLOCK_TOOL
from .util import rawdt_to_utc, get_unlock_tool_in_raw, get_user_name_in_raw

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """lock 플랫폼 설정"""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    api = data["api"]

    # 코디네이터 데이터(dict)의 key인 deviceId를 순회하며 엔티티 생성
    entities = [
        ZigbangDoorlock(coordinator, api, device_id)
        for device_id in coordinator.data
    ]

    if entities:
        async_add_entities(entities)

class ZigbangDoorlock(CoordinatorEntity, LockEntity):
    """직방 도어락 엔티티 (코디네이터 연동)"""

    def __init__(self, coordinator, api, device_id):
        super().__init__(coordinator)
        self.api = api
        self._device_id = device_id

        device = self.coordinator.data[self._device_id]
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
            "name": device.get("userNick", "Zigbang Doorlock"),
            "model": device.get("modelNm", "SHP-Series"),
            "manufacturer": "Samsung",
        }

        # 고정값 설정
        self._attr_unique_id = f"{device_id}_lock"
        self._attr_has_entity_name = True
        self._attr_translation_key = "zigbang_doorlock"
        self._attr_name = None # 기기 이름은 device_info의 name을 따름

    @property
    def is_locked(self):
        """잠금 상태 반환 (doorlockStatusVO -> locked)"""
        return self.coordinator.data[self._device_id].get("doorlockStatusVO", {}).get("locked", True)

    @property
    def extra_state_attributes(self):
        """도어락의 추가 속성 (최근 이력 정보)"""
        history = self.coordinator.data[self._device_id].get("recentHistoryVOList", {})
        if not history:
            return None

        raw_dt = history.get("rgstDt")
        formatted_dt = rawdt_to_utc(raw_dt)

        msg_cd = history.get("msgCd") or ""
        unlock_tool = get_unlock_tool_in_raw(history)
        if unlock_tool is None:
            tool_code = None
            if msg_cd == "622_OUT":
                tool_code = "INDOOR"
            elif msg_cd == "622_NONE":
                tool_code = None
            elif msg_cd.startswith("622"):
                tool_code = msg_cd[-3:]

            unlock_tool_info = UNLOCK_TOOL.get(tool_code, {}) if tool_code else {}
            unlock_tool = unlock_tool_info.get("name")

        return {
            "last_event_at": formatted_dt,
            "last_message": history.get("msgText"),
            "last_alert_type": ALERT_TYPE.get(msg_cd, msg_cd) if msg_cd else None,
            "last_unlock_tool": unlock_tool,
            "last_user_name": get_user_name_in_raw(history) or history.get("pinNm"),
            "event_id": history.get("eventId")
        }

    async def async_unlock(self, **kwargs):
        """도어락 열기 명령 실행"""
        session = async_get_clientsession(self.coordinator.hass)

        _LOGGER.debug("[Zigbang] %s 기기에 열기 명령을 전송합니다.", self.name)

        # API 호출
        success = await self.api.control_unlock(session, self._device_id)

        if success:
            self.coordinator.data[self._device_id]["doorlockStatusVO"]["locked"] = False
            self.async_write_ha_state()
            # 명령 성공 시 즉시 상태를 업데이트하여 사용자에게 피드백 제공
            # (실제 문이 열린 뒤 다음 30초 주기에서 다시 확인됨)
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error("[Zigbang] 열기 명령 전송에 실패했습니다.")
