"""Sensors for Paradigma (V2.5.0 Mega Update)."""
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfTemperature, UnitOfEnergy, UnitOfPower, UnitOfTime, UnitOfMass
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.entity import DeviceInfo
from datetime import timedelta
import logging
from .const import DOMAIN, CONF_SOLAR, CONF_HK2, CONF_POOL, CONF_ROOM, CONF_BOILER, CONF_WOOD, CONF_EMS

_LOGGER = logging.getLogger(__name__)

STATUS_HK = { 
    0: "off", 1: "outdoor_limit", 2: "room_limit", 3: "buffer_block", 
    4: "dhw_priority", 6: "frost", 7: "solar_excess", 8: "preheat", 
    9: "normal", 10: "comfort", 11: "reduced", 16: "station_dhw", 17: "screed", 25: "control_system"
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

# FIX: Boiler status mapping corrected to spec (states 2-7)
STATUS_BOILER = { 
    0: "off", 1: "on", 2: "on_heating", 3: "loading_buffer", 
    4: "blocked", 5: "cooling_hp", 6: "combi_dhw", 7: "ww_prep" 
}

STATUS_SOLAR = { 
    0: "waiting", 1: "frost", 2: "push", 3: "delay", 
    4: "loading", 5: "storage_full", 6: "collector_overheat", 
    7: "manual", 8: "measuring", 9: "emergency" 
}

STATUS_WOOD = { 0: "off", 1: "ignition", 2: "burning", 3: "burnout", 4: "off", 5: "cooling", 6: "shutdown", 7: "pump_push" }
STATUS_PELLET = { 0: "off", 1: "standby", 2: "ignition", 3: "burning", 4: "test", 5: "runon", 6: "cleaning", 7: "error", 8: "unknown" }

# Format: (key, unit, device_class, multiplier, register_type, offset, condition, unit_id)
SENSOR_DEFINITIONS = [
    # HK1 & General
    ("outdoor_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 0, None, 1),
    ("flow_hk1", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 1, None, 1),
    ("return_hk1", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 2, None, 1),
    ("dhw_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 3, None, 1),
    ("buffer_top", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 4, None, 1),
    ("buffer_bottom", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 5, None, 1),
    ("circ_return_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 6, None, 1),
    ("room_temp_hk1", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 9, CONF_ROOM, 1),
    ("room_temp_hk2", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 10, CONF_ROOM, 1),
    
    # Read-Only Target Setpoints (Moved from number.py)
    ("target_buffer_top", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "holding", 44, None, 1),
    ("target_boiler", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "holding", 45, None, 1),

    # Heat Quantities (SystaExpresso)
    ("heat_dhw", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, 1.0, "holding_32", 23, None, 1),
    ("heat_circ", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, 1.0, "holding_32", 25, None, 1),

    # HK2
    ("flow_hk2", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 7, CONF_HK2, 1),
    ("return_hk2", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 8, CONF_HK2, 1),

    # Boiler
    ("boiler_flow", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 12, CONF_BOILER, 1),
    ("boiler_return", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 13, CONF_BOILER, 1),
    ("boiler_hours", UnitOfTime.HOURS, SensorDeviceClass.DURATION, 1.0, "holding_32", 27, None, 1),
    ("boiler_starts", None, None, 1.0, "holding_32", 29, None, 1),

    # Wood / Pellets (FIX: Pellet addresses @31 and @33)
    ("wood_flow", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 14, CONF_WOOD, 1),
    ("wood_return", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 15, CONF_WOOD, 1),
    ("wood_buffer_top", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 16, CONF_WOOD, 1),
    ("pellet_hours", UnitOfTime.HOURS, SensorDeviceClass.DURATION, 1.0, "holding_32", 31, CONF_WOOD, 1),
    ("pellet_consumption", UnitOfMass.KILOGRAMS, SensorDeviceClass.WEIGHT, 100.0, "holding", 33, CONF_WOOD, 1), # 1/10 t = 100kg
    
    # Solar
    ("collector_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 11, CONF_SOLAR, 1),
    ("solar_outdoor_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 36, CONF_SOLAR, 1),
    ("solar_power", UnitOfPower.KILO_WATT, SensorDeviceClass.POWER, 0.1, "holding", 19, CONF_SOLAR, 1), 
    ("solar_day", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, 0.1, "holding", 20, CONF_SOLAR, 1),
    ("solar_total", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, 0.1, "holding_32", 21, CONF_SOLAR, 1),

    # Pool
    ("pool_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 19, CONF_POOL, 1),
    ("pool_flow", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 20, CONF_POOL, 1),
    ("pool_return", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 21, CONF_POOL, 1),
    
    # EMS / Heat Pump (Unit ID 2)
    ("ems_hp_power", UnitOfPower.WATT, SensorDeviceClass.POWER, 1.0, "holding", 1, CONF_EMS, 2),
    ("ems_heater_power", UnitOfPower.WATT, SensorDeviceClass.POWER, 1.0, "holding", 7, CONF_EMS, 2),
    ("ems_model_id", None, None, 1.0, "holding", 4, CONF_EMS, 2),
    ("ems_sw_version", None, None, 1.0, "holding_32", 5, CONF_EMS, 2),

    # Status / Errors
    ("error_code", None, None, 1, "holding", 12, None, 1),
    ("status_ww", None, None, 1, "holding_status_ww", 34, None, 1),
    ("status_circ", None, None, 1, "holding_status_circ", 35, None, 1),
    ("status_hk1", None, None, 1, "holding_status_hk", 36, None, 1),
    ("status_hk2", None, None, 1, "holding_status_hk", 37, CONF_HK2, 1),
    ("status_solar", None, None, 1, "holding_status_solar", 39, CONF_SOLAR, 1),
    ("status_pool", None, None, 1, "holding_status_pool", 40, CONF_POOL, 1),
    ("status_boiler", None, None, 1, "holding_status_boiler", 41, CONF_BOILER, 1),
    ("status_pellet", None, None, 1, "holding_status_pellet", 42, CONF_WOOD, 1),
    ("status_wood", None, None, 1, "holding_status_wood", 43, CONF_WOOD, 1),
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
        super().__init__(hass, _LOGGER, name="ParadigmaSensors", update_interval=timedelta(seconds=config.get("scan_interval", 30)))
        self.hub = hub
        self.config = config

    async def _async_update_data(self):
        data = {}
        successful_reads = 0
        
        try:
            for s in SENSOR_DEFINITIONS:
                key, _, _, _, reg_type, offset, req_conf, unit_id = s
                if req_conf and not self.config.get(req_conf):
                    continue
                    
                if "input" in reg_type:
                    val = await self.hass.async_add_executor_job(self.hub.read_input_registers, offset, 1, unit_id)
                    if val:
                        data[f"{unit_id}_input_{offset}"] = val[0]
                        successful_reads += 1
                elif "holding_32" in reg_type:
                    val_32 = await self.hass.async_add_executor_job(self.hub.read_holding_registers, offset, 2, unit_id)
                    if val_32 and len(val_32) == 2:
                        combined = (val_32[0] << 16) | val_32[1]
                        data[f"{unit_id}_holding_32_{offset}"] = combined
                        successful_reads += 1
                else:
                    val = await self.hass.async_add_executor_job(self.hub.read_holding_registers, offset, 1, unit_id)
                    if val:
                        data[f"{unit_id}_holding_{offset}"] = val[0]
                        successful_reads += 1
                        
            if successful_reads == 0:
                raise UpdateFailed("Keine gültigen Modbus-Antworten erhalten.")
                
            return data
            
        except Exception as e:
            _LOGGER.error(f"Modbus Kommunikationsfehler: {e}")
            raise UpdateFailed(f"Verbindung fehlgeschlagen: {e}")

class ParadigmaSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry, definition):
        super().__init__(coordinator)
        self._key = definition[0]
        self._unit = definition[1]
        self._dev_class = definition[2]
        self._factor = definition[3]
        self._type = definition[4]
        self._reg_idx = definition[5]
        self._unit_id = definition[7]
        self._entry_id = entry.entry_id
        
        self._attr_has_entity_name = True
        self._attr_translation_key = self._key
        # FIX: Unique ID uses definition key
        self._attr_unique_id = f"{entry.entry_id}_{self._key}"
        
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
            key = f"{self._unit_id}_input_{self._reg_idx}"
        elif "holding_32" in self._type:
            key = f"{self._unit_id}_holding_32_{self._reg_idx}"
        else:
            key = f"{self._unit_id}_holding_{self._reg_idx}"
            
        raw = self.coordinator.data.get(key)
        
        if raw is None or raw in [0x7FFF, 0x8000, 0xFFFF, 0xFFFFFFFF]: return None

        if self._key == "error_code":
            return "no_error" if raw == 0 else str(raw)

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

        if self._unit is None and ("status" in self._type or self._key == "error_code"):
            return SensorDeviceClass.ENUM
        return None
