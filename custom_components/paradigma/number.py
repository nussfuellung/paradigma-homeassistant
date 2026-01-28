"""Number platform for Paradigma."""
from homeassistant.components.number import NumberEntity
from .const import DOMAIN

# Key, RegisterOffset (zu 40001), Min, Max, Step
# Quellen: HK Soll (Seite 13, Tabelle B3) [cite: 205], Puffer/Kessel Soll (Seite 15, Tabelle B3) [cite: 214]
NUMBERS = [
    ("setpoint_flow_hk1", 2, 20, 80, 1),      # 40003
    ("setpoint_flow_hk2", 3, 20, 80, 1),      # 40004
    ("setpoint_buffer_top", 44, 20, 90, 0.5), # 40045
    ("setpoint_boiler", 45, 20, 90, 0.5),     # 40046
]

async def async_setup_entry(hass, entry, async_add_entities):
    hub = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for n in NUMBERS:
        entities.append(ParadigmaNumber(hub, n[0], n[1], n[2], n[3], n[4], entry.entry_id))
    async_add_entities(entities)

class ParadigmaNumber(NumberEntity):
    def __init__(self, hub, key, address, min_val, max_val, step, uid):
        self._hub = hub
        self._address = address
        self._attr_has_entity_name = True
        self._attr_translation_key = key
        self._attr_unique_id = f"{uid}_num_{address}"
        self._attr_native_min_value = min_val
        self._attr_native_max_value = max_val
        self._attr_native_step = step
        self._attr_native_value = None

    def update(self):
        res = self._hub.read_holding_registers(self._address, 1)
        if res and res[0] != 0x8000:
            self._attr_native_value = res[0] * 0.1

    def set_native_value(self, value):
        val_int = int(value * 10)
        self._hub.write_register(self._address, val_int)
        self._attr_native_value = value