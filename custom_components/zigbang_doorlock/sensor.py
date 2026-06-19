import logging
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
    SensorEntity,
)
from homeassistant.const import PERCENTAGE
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """sensor 플랫폼 설정"""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    entities = [
        ZigbangBatterySensor(coordinator, device_id)
        for device_id in coordinator.data
    ]

    if entities:
        async_add_entities(entities)

class ZigbangBatterySensor(CoordinatorEntity, SensorEntity):
    """직방 도어락 배터리 센서 (코디네이터 연동)"""

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self._device_id = device_id
        
        device = self.coordinator.data[self._device_id]
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
            "name": device.get("userNick", "Zigbang Doorlock"),
            "model": device.get("modelNm", "SHP-Series"),
            "manufacturer": "Samsung",
        }

        self._attr_unique_id = f"{device_id}_battery"
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_has_entity_name = True
        self._attr_translation_key = "battery"

    @property
    def native_value(self):
        """배터리 잔량 반환 (doorlockStatusVO -> battery)"""
        return self.coordinator.data[self._device_id].get("doorlockStatusVO", {}).get("battery")
