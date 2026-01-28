"""Water Heater platform for Paradigma."""
from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    WaterHeaterEntityFeature,
)
from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    hub = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ParadigmaWaterHeater(hub, entry.entry_id)])

class ParadigmaWaterHeater(WaterHeaterEntity):
    def __init__(self, hub, uid):
        self._hub = hub
        self._attr_has_entity_name = True
        self._attr_translation_key = "dhw"
        self._attr_unique_id = f"{uid}_wh_ww"
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_supported_features = WaterHeaterEntityFeature.TARGET_TEMPERATURE
        self._attr_min_temp = 30
        self._attr_max_temp = 70
        self._current_temp = None
        self._target_temp = None
        self._attr_operation_list = ["on"] 
        self._attr_current_operation = "on"

    def update(self):
        # Ist-Wert lesen (30004 -> Index 3) [cite: 196]
        c_val = self._hub.read_input_registers(3, 1)
        if c_val and c_val[0] != 0x8000:
            val = c_val[0]
            if val > 32767: val -= 65536
            self._current_temp = val * 0.1

        # Soll-Wert lesen (40009 -> Index 8) [cite: 205]
        t_val = self._hub.read_holding_registers(8, 1)
        if t_val and t_val[0] != 0x8000:
            self._target_temp = t_val[0] * 0.1

    @property
    def current_temperature(self):
        return self._current_temp

    @property
    def target_temperature(self):
        return self._target_temp

    def set_temperature(self, **kwargs):
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp:
            # Wert schreiben in 40009 -> Index 8 [cite: 205]
            val_int = int(temp * 10)
            self._hub.write_register(8, val_int)