"""Number platform for Paradigma."""
from homeassistant.components.number import NumberEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.const import UnitOfTemperature, UnitOfPower
from homeassistant.exceptions import HomeAssistantError
from .const import DOMAIN, CONF_HK2, CONF_EMS
import logging

_LOGGER = logging.getLogger(__name__)

# Format: (key, address, min_val, max_val, step, req_hk2, req_ems, limit_reg, unit_id)
NUMBERS = [
    ("setpoint_flow_hk1", 2, 20, 80, 1, False, False, 10, 1),
    ("setpoint_flow_hk2", 3, 20, 80, 1, True, False, 11, 1),
    ("ems_pv_surplus", 0, 0, 20000, 100, False, True, None, 2),
    ("ems_grid_limit", 3, 0, 20000, 100, False, True, None, 2),
]

async def async_setup_entry(hass, entry, async_add_entities):
    hub = hass.data[DOMAIN][entry.entry_id]
    entities = []
    hk2_active = entry.data.get(CONF_HK2, False)
    ems_active = entry.data.get(CONF_EMS, False)
    
    for n in NUMBERS:
        if n[5] and not hk2_active: continue
        if n[6] and not ems_active: continue
        entities.append(ParadigmaNumber(hub, n[0], n[1], n[2], n[3], n[4], n[7], n[8], entry))
    async_add_entities(entities)

class ParadigmaNumber(NumberEntity):
    def __init__(self, hub, key, address, min_val, max_val, step, limit_reg, unit_id, entry):
        self._hub = hub
        self._address = address
        self._limit_reg = limit_reg
        self._unit_id = unit_id
        self._entry_id = entry.entry_id
        self._attr_has_entity_name = True
        self._attr_translation_key = key
        self._attr_unique_id = f"{entry.entry_id}_num_{address}_u{unit_id}"
        
        self._attr_native_min_value = min_val
        self._attr_native_max_value = max_val
        self._attr_native_step = step
        self._attr_native_value = None
        
        if "flow" in key:
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        elif "ems" in key:
            self._attr_native_unit_of_measurement = UnitOfPower.WATT

    @property
    def device_info(self):
        return DeviceInfo(identifiers={(DOMAIN, self._entry_id)}, name="Paradigma Heizung", manufacturer="Paradigma", model="SystaSmartC II")

    async def async_update(self):
        # Read the current value
        res = await self.hass.async_add_executor_job(self._hub.read_holding_registers, self._address, 1, self._unit_id)
        if res and res[0] not in [0x8000, 0xFFFF]:
            multiplier = 0.1 if "flow" in self._attr_translation_key else 1.0
            self._attr_native_value = res[0] * multiplier
            
        # Dynamically fetch the max limit if applicable (HK1/HK2)
        if self._limit_reg:
            limit_res = await self.hass.async_add_executor_job(self._hub.read_holding_registers, self._limit_reg, 1, self._unit_id)
            if limit_res and limit_res[0] not in [0x8000, 0xFFFF]:
                self._attr_native_max_value = limit_res[0] * 0.1

    async def async_set_native_value(self, value: float) -> None:
        multiplier = 10 if "flow" in self._attr_translation_key else 1
        val_int = int(value * multiplier)
        success = await self.hass.async_add_executor_job(self._hub.write_register, self._address, val_int, self._unit_id)
        
        if not success:
            raise HomeAssistantError(f"Fehler beim Senden des Wertes {value} an die Heizung.")
            
        self._attr_native_value = value
