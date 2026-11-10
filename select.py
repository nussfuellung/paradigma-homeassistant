"""Select platform for Paradigma (EMS Tariff)."""
from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.exceptions import HomeAssistantError
from .const import DOMAIN, CONF_EMS

OPTIONS_MAP = {
    0: "no_tariff",
    1: "high_tariff",
    2: "low_tariff"
}
REVERSE_MAP = {v: k for k, v in OPTIONS_MAP.items()}

async def async_setup_entry(hass, entry, async_add_entities):
    hub = hass.data[DOMAIN][entry.entry_id]
    if entry.data.get(CONF_EMS, False):
        async_add_entities([ParadigmaTariffSelect(hub, entry)])

class ParadigmaTariffSelect(SelectEntity):
    def __init__(self, hub, entry):
        self._hub = hub
        self._entry_id = entry.entry_id
        self._attr_has_entity_name = True
        self._attr_translation_key = "ems_tariff"
        self._attr_unique_id = f"{entry.entry_id}_select_tariff_u2"
        self._attr_options = list(OPTIONS_MAP.values())
        self._attr_current_option = None

    @property
    def device_info(self):
        return DeviceInfo(identifiers={(DOMAIN, self._entry_id)})

    async def async_update(self):
        res = await self.hass.async_add_executor_job(self._hub.read_holding_registers, 2, 1, 2)
        if res and res[0] in OPTIONS_MAP:
            self._attr_current_option = OPTIONS_MAP[res[0]]

    async def async_select_option(self, option: str) -> None:
        val_int = REVERSE_MAP[option]
        success = await self.hass.async_add_executor_job(self._hub.write_register, 2, val_int, 2)
        if not success:
            raise HomeAssistantError(f"Fehler beim Senden des Tarifs an die Wärmepumpe.")
        self._attr_current_option = option
