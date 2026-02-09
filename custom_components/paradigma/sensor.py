"""Sensors for Paradigma."""
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfTemperature, UnitOfEnergy, UnitOfPower, UnitOfTime
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from homeassistant.helpers.entity import DeviceInfo
from datetime import timedelta
import logging
from .const import DOMAIN, CONF_SOLAR, CONF_HK2, CONF_POOL, CONF_ROOM, CONF_BOILER, CONF_WOOD

_LOGGER = logging.getLogger(__name__)

# --- DEUTSCHE ÜBERSETZUNGEN FÜR STATUS-CODES (Vervollständigt) ---

# Heizkreis Status [cite: 228]
STATUS_HK = { 
    0: "Aus", 1: "Heizbetrieb", 2: "Anschieben", 3: "Vorhaltezeit", 
    4: "Gesperrt", 5: "Inbetriebnahme", 6: "Frostschutz", 7: "Estrich", 
    8: "Kühlung/Überschuss", 9: "Manuell", 10: "Notbetrieb", 
    11: "Nicht installiert", 12: "Kühlkreis aktiv" 
}

# Warmwasser Status 
STATUS_WW = { 
    0: "Kein Bedarf", 1: "Ladung läuft", 2: "Frostschutz", 3: "Warten", 
    4: "Nachlauf Ladepumpe", 5: "Puffer/Kessel zu warm", 
    6: "Warten auf Wasserentnahme", 7: "Wasserentnahme", 8: "Inbetriebnahme", 
    9: "Manuell", 10: "Betrieb Zirkulation", 11: "Nachlauf Zirkulation", 
    12: "Zirkulation Sperrzeit", 13: "Sperre durch SmartHome" 
}

# Pool Status [cite: 229]
STATUS_POOL = { 
    0: "Keine Erweiterung", 1: "Aus", 2: "Gesperrt", 3: "Warm genug", 
    4: "Frostschutz", 5: "Aufheizen Normal", 6: "Aufheizen Komfort", 
    7: "Solarer Überschuss", 8: "Gesperrt (Puffer kalt)", 
    9: "Gesperrt (WW Vorrang)", 10: "Kühlen" 
}

# Zirkulation Status [cite: 221, 227]
STATUS_CIRC = { 
    0: "Nicht verwendet", 1: "Nachlauf", 2: "Gesperrt", 3: "Aus", 
    4: "Gesperrt (Fühler)", 5: "An", 6: "Frostschutz", 7: "Sperre SmartHome" 
}

# Kessel Status [cite: 232-246]
STATUS_BOILER = { 
    0: "Aus", 1: "An", 2: "An für Heizkreis", 3: "Lädt Puffer", 
    4: "Gesperrt", 5: "Kühlung WP", 6: "WW Bereitung" 
}

# Solar Status [cite: 254]
STATUS_SOLAR = { 
    0: "Wartet", 1: "Frostschutz", 2: "Anschieben", 3: "Einschaltverzögerung", 
    4: "Ladung läuft", 5: "Speicher voll", 6: "Kollektor überhitzt", 
    7: "Manuell", 8: "Messung", 9: "Notbetrieb" 
}

# Holz/Pellet Status [cite: 251, 252]
STATUS_WOOD = { 0: "Kein Kessel", 1: "Aus", 2: "Anheizen", 3: "Leistungsbrand", 4: "Ausbrand", 5: "Nachkühlen", 6: "Schaltet ab", 7: "Pumpe schiebt an" }
STATUS_PELLET = { 0: "Aus", 1: "Standby", 2: "Anheizen", 3: "Leistungsbrand", 4: "Test Abgasklappe", 5: "Nachlauf", 6: "Reinigung", 7: "Störung", 8: "Unbekannt" }

SENSOR_DEFINITIONS = [
    # Key, Unit, Class, Factor, RegisterType, RegisterOffset, RequiresConfig
    
    # --- Standard Temperaturen ---
    ("outdoor_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 0, None),
    ("flow_hk1", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 1, None),
    ("return_hk1", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 2, None),
    ("dhw_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 3, None),
    ("buffer_top", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 4, None),
    ("buffer_bottom", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 5, None),
    ("circ_return_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 6, None),

    # --- Raumfühler (Optional) ---
    ("room_temp_hk1", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 9, CONF_ROOM),
    ("room_temp_hk2", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 10, CONF_ROOM),

    # --- Heizkreis 2 (Optional) ---
    ("flow_hk2", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 7, CONF_HK2),
    ("return_hk2", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 8, CONF_HK2),

    # --- Kessel (Gas/Öl) ---
    ("boiler_flow", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 12, CONF_BOILER),
    ("boiler_return", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 13, CONF_BOILER),
    ("boiler_hours", UnitOfTime.HOURS, SensorDeviceClass.DURATION, 1.0, "holding", 27, CONF_BOILER),
    ("boiler_starts", None, None, 1.0, "holding", 29, CONF_BOILER),

    # --- Holz / Pellets (Optional) ---
    ("wood_flow", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 14, CONF_WOOD),
    ("wood_return", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 15, CONF_WOOD),
    ("wood_buffer_top", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 16, CONF_WOOD),
    ("pellet_hours", UnitOfTime.HOURS, SensorDeviceClass.DURATION, 1.0, "holding", 31, CONF_WOOD),
    
    # --- Solar (Optional) ---
    ("collector_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 11, CONF_SOLAR),
    ("solar_power", UnitOfPower.KILO_WATT, SensorDeviceClass.POWER, 0.1, "holding", 19, CONF_SOLAR), 
    ("solar_day", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, 1.0, "holding", 20, CONF_SOLAR),
    ("solar_total", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, 1.0, "holding", 21, CONF_SOLAR),

    # --- Pool (Optional) ---
    ("pool_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 19, CONF_POOL),
    ("pool_flow", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 20, CONF_POOL),
    ("pool_return", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 21, CONF_POOL),
    
    # --- STATUS MELDUNGEN ---
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
        
        # 1. Input Registers
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

        # 2. Holding Registers
        offsets_holding = [34, 35, 36]
        if self.config.get(CONF_HK2): offsets_holding.append(37)
        if self.config.get(CONF_SOLAR): offsets_holding.extend([19, 20, 21, 39])
        if self.config.get(CONF_BOILER): offsets_holding.extend([27, 29, 41])
        if self.config.get(CONF_WOOD): offsets_holding.extend([31, 42, 43])
        if self.config.get(CONF_POOL): offsets_holding.append(40)

        for off in offsets_holding:
            val = await self.hass.async_add_executor_job(self.hub.read_holding_registers, off, 1)
            if val: data[f"holding_{off}"] = val[0]
            
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
        key = f"input_{self._reg_idx}" if "input" in self._type else f"holding_{self._reg_idx}"
        raw = self.coordinator.data.get(key)
        
        if raw is None or raw in [0x8000, 0xFFFF]: return None

        # --- Status Text-Übersetzung ---
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
        return self._dev_class