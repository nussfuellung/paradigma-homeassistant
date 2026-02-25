"""Sensors for Paradigma."""
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfTemperature, UnitOfEnergy, UnitOfPower, UnitOfTime
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from homeassistant.helpers.entity import DeviceInfo
from datetime import timedelta
import logging
from .const import DOMAIN, CONF_SOLAR, CONF_HK2, CONF_POOL, CONF_ROOM, CONF_BOILER, CONF_WOOD

_LOGGER = logging.getLogger(__name__)



STATUS_HK = { 
    0: "off", 1: "heating", 2: "push", 3: "hold", 
    4: "blocked", 5: "startup", 6: "frost", 7: "screed", 
    8: "cooling_excess", 9: "manual", 10: "emergency", 
    11: "not_installed", 12: "cooling_active" 
}

STATUS_WW = { 
    0: "no_demand", 1: "loading", 2: "frost", 3: "waiting", 
    4: "pump_runon", 5: "buffer_hot", 
    6: "wait_draw", 7: "draw_off", 8: "startup", 
    9: "manual", 10: "circ_active", 11: "circ_runon", 
    12: "circ_lock", 13: "blocked_smarthome" 
}

STATUS_POOL = { 
    0: "no_extension", 1: "off", 2: "blocked", 3: "warm_enough", 
    4: "frost", 5: "heating_normal", 6: "heating_comfort", 
    7: "solar_excess", 8: "blocked_buffer_cold", 
    9: "blocked_ww_prio", 10: "cooling" 
}

STATUS_CIRC = { 
    0: "unused", 1: "runon", 2: "blocked", 3: "off", 
    4: "blocked_sensor", 5: "on", 6: "frost", 7: "blocked_smarthome" 
}

STATUS_BOILER = { 
    0: "off", 1: "on", 2: "on_heating", 3: "loading_buffer", 
    4: "blocked", 5: "cooling_hp", 6: "ww_prep" 
}

STATUS_SOLAR = { 
    0: "waiting", 1: "frost", 2: "push", 3: "delay", 
    4: "loading", 5: "storage_full", 6: "collector_overheat", 
    7: "manual", 8: "measuring", 9: "emergency" 
}

STATUS_WOOD = { 0: "no_boiler", 1: "off", 2: "ignition", 3: "burning", 4: "burnout", 5: "cooling", 6: "shutdown", 7: "pump_push" }
STATUS_PELLET = { 0: "off", 1: "standby", 2: "ignition", 3: "burning", 4: "test", 5: "runon", 6: "cleaning", 7: "error", 8: "unknown" }

SENSOR_DEFINITIONS = [

    
    ("outdoor_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 0, None),
    ("flow_hk1", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 1, None),
    ("return_hk1", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 2, None),
    ("dhw_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 3, None),
    ("buffer_top", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 4, None),
    ("buffer_bottom", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 5, None),
    ("circ_return_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 6, None),

    ("room_temp_hk1", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 9, CONF_ROOM),
    ("room_temp_hk2", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 10, CONF_ROOM),

    ("flow_hk2", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 7, CONF_HK2),
    ("return_hk2", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 8, CONF_HK2),

    ("boiler_flow", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 12, CONF_BOILER),
    ("boiler_return", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 13, CONF_BOILER),
    ("boiler_hours", UnitOfTime.HOURS, SensorDeviceClass.DURATION, 1.0, "holding_32", 27, CONF_BOILER),
    ("boiler_starts", None, None, 1.0, "holding_32", 29, CONF_BOILER),

    ("wood_flow", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 14, CONF_WOOD),
    ("wood_return", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 15, CONF_WOOD),
    ("wood_buffer_top", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 16, CONF_WOOD),
    ("pellet_hours", UnitOfTime.HOURS, SensorDeviceClass.DURATION, 1.0, "holding_32", 31, CONF_WOOD),
    

    ("collector_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 11, CONF_SOLAR),
    ("solar_power", UnitOfPower.KILO_WATT, SensorDeviceClass.POWER, 0.1, "holding", 19, CONF_SOLAR), 
    ("solar_day", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, 0.1, "holding", 20, CONF_SOLAR),
    ("solar_total", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, 0.1, "holding_32", 21, CONF_SOLAR),

    ("pool_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 19, CONF_POOL),
    ("pool_flow", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 20, CONF_POOL),
    ("pool_return", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 21, CONF_POOL),
    
    ("status_ww", None, None, 1, "holding_status_ww", 34, None),
    ("status_circ", None, None, 1, "holding_status_circ", 35, None),
    ("status_hk1", None, None, 1, "holding_status_hk", 36, None),
    ("status_hk2", None, None, 1, "holding_status_hk", 37, CONF_HK2),
    ("status_solar", None, None, 1, "holding_status_solar", 39, CONF_SOLAR),
    ("status_pool", None, None, 1, "holding_status_pool", 40, CONF_POOL),
    ("status_boiler", None, None, 1, "holding_status_boiler", 41, CONF_BOILER),
    ("status_pellet", None, None, 1, "holding_status_pellet", 42, CONF_WOOD),
    ("status_wood", None, None, 1, "holding_status_wood", 43, CONF_WOOD),
]

async def async_setup_entry(hass, entry, async_add_entities):
    hub = hass.data[DOMAIN][entry.entry_id]
    coordinator = ParadigmaDataCoordinator(hass, hub, entry.data)
    await coordinator.async_config_entry_first_refresh()
    
    entities = []
    for s in SENSOR_DEFINITIONS:
        req_conf = s[6]
        if req_conf and not entry.data.get(req_conf):
            continue
        entities.append(ParadigmaSensor(coordinator, entry, s))
    async_add_entities(entities)

class ParadigmaDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, hub, config):
        super().__init__(hass, _LOGGER, name="ParadigmaSensors", update_interval=timedelta(seconds=30))
        self.hub = hub
        self.config = config

    async def _async_update_data(self):
        data = {}
        
   
        offsets_input = [0, 1, 2, 3, 4, 5, 6]
        if self.config.get(CONF_HK2): offsets_input.extend([7, 8])
        if self.config.get(CONF_ROOM): offsets_input.extend([9, 10])
        if self.config.get(CONF_SOLAR): offsets_input.append(11)
        if self.config.get(CONF_BOILER): offsets_input.extend([12, 13])
        if self.config.get(CONF_WOOD): offsets_input.extend([14, 15, 16])
        if self.config.get(CONF_POOL): offsets_input.extend([19, 20, 21])

        for off in offsets_input:
            val = await self.hass.async_add_executor_job(self.hub.read_input_registers, off, 1)
            if val: data[f"input_{off}"] = val[0]


        offsets_holding_16 = [34, 35, 36]
        if self.config.get(CONF_HK2): offsets_holding_16.append(37)
        if self.config.get(CONF_SOLAR): offsets_holding_16.extend([19, 20, 39])
        if self.config.get(CONF_BOILER): offsets_holding_16.append(41)
        if self.config.get(CONF_WOOD): offsets_holding_16.extend([42, 43])
        if self.config.get(CONF_POOL): offsets_holding_16.append(40)

        for off in offsets_holding_16:
            val = await self.hass.async_add_executor_job(self.hub.read_holding_registers, off, 1)
            if val: data[f"holding_{off}"] = val[0]
            

        offsets_holding_32 = []
        if self.config.get(CONF_SOLAR): offsets_holding_32.append(21)
        if self.config.get(CONF_BOILER): offsets_holding_32.extend([27, 29])
        if self.config.get(CONF_WOOD): offsets_holding_32.append(31)

        for off in offsets_holding_32:
            try:
                val_32 = await self.hass.async_add_executor_job(self.hub.read_holding_registers, off, 2)
                if val_32 and len(val_32) == 2:
                    combined = (val_32[0] << 16) | val_32[1]
                    data[f"holding_32_{off}"] = combined
            except Exception as e:
                _LOGGER.error(f"Fehler beim Lesen des 32-Bit Registers {off}: {e}")
            
        return data

class ParadigmaSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry, definition):
        super().__init__(coordinator)
        self._key = definition[0]
        self._unit = definition[1]
        self._dev_class = definition[2]
        self._factor = definition[3]
        self._type = definition[4]
        self._reg_idx = definition[5]
        self._entry_id = entry.entry_id
        
        self._attr_has_entity_name = True
        self._attr_translation_key = self._key
        self._attr_unique_id = f"{entry.entry_id}_{self._type}_{self._reg_idx}"
        
        if self._dev_class == SensorDeviceClass.ENERGY:
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        elif self._dev_class in [SensorDeviceClass.TEMPERATURE, SensorDeviceClass.POWER]:
            self._attr_state_class = SensorStateClass.MEASUREMENT
        else:
            self._attr_state_class = None

    @property
    def device_info(self):
        return DeviceInfo(identifiers={(DOMAIN, self._entry_id)}, name="Paradigma Heizung", manufacturer="Paradigma", model="SystaSmartC II")

    @property
    def native_value(self):
        if "input" in self._type:
            key = f"input_{self._reg_idx}"
        elif "holding_32" in self._type:
            key = f"holding_32_{self._reg_idx}"
        else:
            key = f"holding_{self._reg_idx}"
            
        raw = self.coordinator.data.get(key)
        
        if raw is None or raw in [0x8000, 0xFFFF]: return None


        if "status_hk" in self._type: return STATUS_HK.get(raw, str(raw))
        if "status_ww" in self._type: return STATUS_WW.get(raw, str(raw))
        if "status_circ" in self._type: return STATUS_CIRC.get(raw, str(raw))
        if "status_solar" in self._type: return STATUS_SOLAR.get(raw, str(raw))
        if "status_boiler" in self._type: return STATUS_BOILER.get(raw, str(raw))
        if "status_wood" in self._type: return STATUS_WOOD.get(raw, str(raw))
        if "status_pellet" in self._type: return STATUS_PELLET.get(raw, str(raw))
        if "status_pool" in self._type: return STATUS_POOL.get(raw, str(raw))

        if self._unit == UnitOfTemperature.CELSIUS:
             if raw > 32767: raw -= 65536
        
        return raw * self._factor

    @property
    def native_unit_of_measurement(self):
        if self._dev_class is None and self._unit is None:
            return None
        return self._unit
    
    @property
    def device_class(self):
        if self._dev_class:
            return self._dev_class

        if self._unit is None and "status" in self._type:
            return SensorDeviceClass.ENUM
        return None
