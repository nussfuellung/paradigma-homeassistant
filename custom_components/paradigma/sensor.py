"""Sensors for Paradigma."""
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature, UnitOfEnergy, UnitOfPower
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.helpers.entity import DeviceInfo
from datetime import timedelta
import logging
from .const import DOMAIN, CONF_SOLAR, CONF_HK2

_LOGGER = logging.getLogger(__name__)

STATUS_HK = {
    0: "Aus", 1: "Heizbetrieb", 2: "Anschieben", 3: "Vorhaltezeit",
    4: "Gesperrt", 5: "Inbetriebnahme", 6: "Frostschutz", 7: "Estrich",
    8: "Kühlung/Überschuss", 9: "Manuell", 10: "Notbetrieb", 11: "Nicht installiert"
}

STATUS_WW = {
    0: "Kein Bedarf", 1: "Ladung läuft", 2: "Frostschutz", 3: "Warten",
    4: "Nachlauf Ladepumpe", 5: "Puffer/Kessel zu warm", 13: "Sperre durch SmartHome"
}

SENSOR_DEFINITIONS = [
    # Key, Unit, Class, Factor, RegisterType, RegisterOffset, RequiresConfig
    # Temperaturen (Input 30xxx) [cite: 196]
    ("outdoor_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 0, None),
    ("flow_hk1", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 1, None),
    ("return_hk1", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 2, None),
    ("dhw_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 3, None),
    ("buffer_top", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 4, None),
    ("buffer_bottom", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 5, None),
    
    # Optional HK2 [cite: 196]
    ("flow_hk2", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 7, CONF_HK2),
    ("return_hk2", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 8, CONF_HK2),
    
    # Solar Temperaturen (Input) & Leistung (Holding) [cite: 196, 210]
    ("collector_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 11, CONF_SOLAR),
    ("solar_power", UnitOfPower.KILO_WATT, SensorDeviceClass.POWER, 0.1, "holding", 19, CONF_SOLAR), 
    ("solar_day", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, 1.0, "holding", 20, CONF_SOLAR),
    ("solar_total", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, 1.0, "holding", 21, CONF_SOLAR),
    
    # Status (Holding) [cite: 210]
    ("status_ww", None, None, 1, "holding_status_ww", 34, None),
    ("status_hk1", None, None, 1, "holding_status_hk", 36, None),
    ("status_hk2", None, None, 1, "holding_status_hk", 37, CONF_HK2),
]

async def async_setup_entry(hass, entry, async_add_entities):
    hub = hass.data[DOMAIN][entry.entry_id]
    coordinator = ParadigmaDataCoordinator(hass, hub, entry.data)
    await coordinator.async_config_entry_first_refresh()
    
    entities = []
    for s in SENSOR_DEFINITIONS:
        # Prüfen, ob Sensor aktiviert ist (Solar / HK2)
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
        # Gezielte Einzelabfragen statt Block-Lesen, um Fehler 131/2 zu vermeiden
        
        # 1. Input Registers (Temperaturen)
        offsets_input = [0, 1, 2, 3, 4, 5] # Standard
        if self.config.get(CONF_HK2): offsets_input.extend([7, 8])
        if self.config.get(CONF_SOLAR): offsets_input.append(11)
        
        for off in offsets_input:
            val = await self.hass.async_add_executor_job(self.hub.read_input_registers, off, 1)
            if val: data[f"input_{off}"] = val[0]

        # 2. Holding Registers
        offsets_holding = [34, 36] # Status WW, HK1
        if self.config.get(CONF_HK2): offsets_holding.append(37)
        
        # Solar Holding Registers
        if self.config.get(CONF_SOLAR):
            # Leistung, Tag, Gesamt
            offsets_holding.extend([19, 20, 21])

        for off in offsets_holding:
            count = 1
            # Solar Gesamtenergie ist oft 2 Register lang (Long), hier lesen wir erst mal 1 Register (Word)
            # Laut PDF ist es 2 Register (40022/40023). Das Hub liest 16bit.
            # Wenn dein Wert komisch aussieht, müssen wir hier 2 lesen.
            val = await self.hass.async_add_executor_job(self.hub.read_holding_registers, off, count)
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
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name="Paradigma Heizung", # Fallback Name
            manufacturer="Paradigma",
            model="SystaSmartC II",
        )

    @property
    def native_value(self):
        key = f"input_{self._reg_idx}" if "input" in self._type else f"holding_{self._reg_idx}"
        raw = self.coordinator.data.get(key)
        
        if raw is None or raw == 0x8000 or raw == 0xFFFF: # [cite: 48]
            return None

        if "status_hk" in self._type:
            return STATUS_HK.get(raw, str(raw))
        if "status_ww" in self._type:
            return STATUS_WW.get(raw, str(raw))

        # Signed Int16 Behandlung für Temperaturen
        if self._unit == UnitOfTemperature.CELSIUS:
             if raw > 32767: raw -= 65536
        
        return raw * self._factor

    @property
    def native_unit_of_measurement(self):
        return self._unit
    
    @property
    def device_class(self):
        return self._dev_class