
import logging
from typing import Any, Dict, Optional

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add switches for passed config_entry in HA."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = data["coordinator"]
    api = data["api"]

    # coordinator.data가 초기화될 때까지 기다립니다.
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        ZigbangHomeSecurityModeSwitch(coordinator, api, device_id)
        for device_id in coordinator.data
    )

class ZigbangHomeSecurityModeSwitch(CoordinatorEntity, SwitchEntity):
    """Zigbang Home Security Mode Switch."""

    def __init__(self, coordinator: DataUpdateCoordinator, api, device_id: str):
        """Initialize the switch."""
        super().__init__(coordinator)
        self.api = api
        self._device_id = device_id
        
        device = coordinator.data[self._device_id]
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
            "name": device.get("userNick", "Zigbang Doorlock"),
            "manufacturer": "Samsung",
            "model": device.get("modelNm", "SHP-Series"),
        }
        self._attr_unique_id = f"{self._device_id}_home_security_mode"
        self._attr_has_entity_name = True
        self._attr_translation_key = "home_security_mode"
        # Fallback name used when custom integration translations are not loaded yet.
        # Without this, Home Assistant can display only the device name for the switch.
        self._attr_name = "Home Security Mode"


    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self.coordinator.data[self._device_id].get("doorlockStatusVO", {}).get("dummyMode", False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        session = async_get_clientsession(self.hass)
        result = await self.api.set_security_mode(session, self._device_id, True)
        if result:
            self.coordinator.data[self._device_id]["doorlockStatusVO"]["dummyMode"] = True
            self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        session = async_get_clientsession(self.hass)
        result = await self.api.set_security_mode(session, self._device_id, False)
        if result:
            self.coordinator.data[self._device_id]["doorlockStatusVO"]["dummyMode"] = False
            self.async_write_ha_state()
        await self.coordinator.async_request_refresh()
