"""Water Heater platform for Paradigma."""
import logging
from homeassistant.components.water_heater import WaterHeaterEntity, WaterHeaterEntityFeature
from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE, PRECISION_TENTHS
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    hub = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ParadigmaWaterHeater(hub, entry)])

class ParadigmaWaterHeater(WaterHeaterEntity):
    def __init__(self, hub, entry):
        self._hub = hub
        self._entry_id = entry.entry_id
        self._attr_has_entity_name = True
        self._attr_translation_key = "dhw"
        self._attr_unique_id = f"{entry.entry_id}_wh_ww"
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_precision = PRECISION_TENTHS
        self._attr_supported_features = WaterHeaterEntityFeature.TARGET_TEMPERATURE
        self._attr_min_temp = 30
        self._attr_max_temp = 70
        self._attr_operation_list = ["on"]
        self._attr_current_operation = "on"
        self._current_temp = None
        self._target_temp = None

    @property
    def device_info(self):
        return DeviceInfo(identifiers={(DOMAIN, self._entry_id)}, name="Paradigma Heizung", manufacturer="Paradigma", model="SystaSmartC II")

    @property
    def current_temperature(self): return self._current_temp
    @property
    def target_temperature(self): return self._target_temp

    def update(self):
        try:
            c_val = self._hub.read_input_registers(3, 1)
            if c_val and c_val[0] not in [0x8000, 0xFFFF]:
                val = c_val[0]
                if val > 32767: val -= 65536
                self._current_temp = val * 0.1
        except Exception: pass

        try:
            t_val = self._hub.read_holding_registers(8, 1)
            if t_val and t_val[0] not in [0x8000, 0xFFFF]:
                self._target_temp = t_val[0] * 0.1
        except Exception: pass

    def set_temperature(self, **kwargs):
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp:
            try:
                val_int = int(temp * 10)
                self._hub.write_register(8, val_int)
                self._target_temp = temp
            except Exception: pass