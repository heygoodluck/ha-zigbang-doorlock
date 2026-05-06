import logging
from homeassistant.components.event import EventEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, ALERT_TYPE, UNLOCK_TOOL
from .util import rawdt_to_utc

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """event 플랫폼 설정"""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    entities = [
        ZigbangDoorlockEvent(coordinator, device_id)
        for device_id in coordinator.data
    ]

    if entities:
        async_add_entities(entities)


class ZigbangDoorlockEvent(CoordinatorEntity, EventEntity):
    """직방 도어락 이벤트 엔티티"""

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self._device_id = device_id
        self._attr_unique_id = f"{device_id}_event"
        self._attr_has_entity_name = True
        
        # translations 디렉토리를 통한 다국어 처리 지원
        self._attr_translation_key = "doorlock_alert"
        self._attr_icon = "mdi:message-badge-outline"
        self._attr_event_types = ["doorlock_alert"]

        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
        }

    def _handle_coordinator_update(self) -> None:
        """코디네이터 데이터가 업데이트될 때 호출됨"""
        device_data = self.coordinator.data.get(self._device_id, {})
        new_events = device_data.get("new_events", [])

        # __init__.py 에서 수집해준 새 이벤트가 있을 경우, 이를 Home Assistant 엔티티 이벤트로 발송
        for evt in new_events:
            raw_dt = evt.get("rgstDt")
            formatted_dt = rawdt_to_utc(raw_dt)
            self._trigger_event(
                "doorlock_alert",
                {
                    "message": evt.get("msgText"),
                    "alert_type": ALERT_TYPE.get(evt.get("msgCd"), evt.get("msgCd")),
                    "unlock_tool": UNLOCK_TOOL.get(evt.get("msgCd")),
                    "user_name": evt.get("eventMemberNm") if evt.get("msgCd") == "622_IN_SVR" else evt.get("pinNm"),
                    "alert_at": formatted_dt,
                }
            )

        super()._handle_coordinator_update()
