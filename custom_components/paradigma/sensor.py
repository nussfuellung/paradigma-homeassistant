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
from datetime import timedelta
import logging
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Status Mapping Texte laut PDF Seite 15/16 [cite: 217, 221, 228]
STATUS_HK = {
    0: "Aus", 1: "Heizbetrieb", 2: "Anschieben", 3: "Vorhaltezeit",
    4: "Gesperrt", 5: "Inbetriebnahme", 6: "Frostschutz", 7: "Estrich",
    8: "Kühlung/Überschuss", 9: "Manuell", 10: "Notbetrieb", 11: "Nicht installiert"
}

STATUS_WW = {
    0: "Kein Bedarf", 1: "Ladung läuft", 2: "Frostschutz", 3: "Warten (Nachheizung gesperrt)",
    4: "Nachlauf Ladepumpe", 5: "Puffer/Kessel zu warm", 13: "Sperre durch SmartHome"
}

SENSOR_TYPES = [
    # Key, Unit, Class, Factor, RegisterType, RegisterOffset (siehe PDF Seite 12/13/14)
    # 30001 entspricht Offset 0 [cite: 196]
    ("outdoor_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 0),
    ("flow_hk1", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 1),
    ("return_hk1", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 2),
    ("dhw_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 3),
    ("buffer_top", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 4),
    ("buffer_bottom", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 5),
    ("flow_hk2", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 7),
    ("return_hk2", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 8),
    ("collector_temp", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, 0.1, "input", 11),
    
    # Holding Registers (40001 Start) [cite: 210]
    ("solar_power", UnitOfPower.KILO_WATT, SensorDeviceClass.POWER, 0.1, "holding", 19), 
    ("solar_day", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, 1.0, "holding", 20),
    ("solar_total", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, 1.0, "holding", 21),
    
    # Status Registers [cite: 210]
    ("status_ww", None, None, 1, "holding_status_ww", 34),
    ("status_hk1", None, None, 1, "holding_status_hk", 36),
    ("status_hk2", None, None, 1, "holding_status_hk", 37),
]

async def async_setup_entry(hass, entry, async_add_entities):
    hub = hass.data[DOMAIN][entry.entry_id]
    coordinator = ParadigmaDataCoordinator(hass, hub)
    await coordinator.async_config_entry_first_refresh()
    
    entities = []
    for s in SENSOR_TYPES:
        entities.append(ParadigmaSensor(coordinator, entry, s))
    async_add_entities(entities)

class ParadigmaDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, hub):
        super().__init__(hass, _LOGGER, name="ParadigmaSensors", update_interval=timedelta(seconds=30))
        self.hub = hub

    async def _async_update_data(self):
        data = {}
        # Lese Input Registers (Bereich Temperaturfühler)
        inputs = await self.hass.async_add_executor_job(self.hub.read_input_registers, 0, 20)
        if inputs:
            for i, val in enumerate(inputs):
                data[f"input_{i}"] = val
        
        # Lese Holding Registers (Bereich Solar & Status)
        holdings = await self.hass.async_add_executor_job(self.hub.read_holding_registers, 0, 50)
        if holdings:
            for i, val in enumerate(holdings):
                data[f"holding_{i}"] = val
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
        
        self._attr_has_entity_name = True
        self._attr_translation_key = self._key
        self._attr_unique_id = f"{entry.entry_id}_{self._type}_{self._reg_idx}"
        self._attr_state_class = SensorStateClass.MEASUREMENT if self._unit else None

    @property
    def native_value(self):
        key = f"input_{self._reg_idx}" if "input" in self._type else f"holding_{self._reg_idx}"
        raw = self.coordinator.data.get(key)
        
        if raw is None or raw == 0x8000 or raw == 0xFFFF: # Ungültige Werte laut PDF Seite 6 [cite: 48]
            return None

        if "status_hk" in self._type:
            return STATUS_HK.get(raw, str(raw))
        if "status_ww" in self._type:
            return STATUS_WW.get(raw, str(raw))

        # Vorzeichenbehandlung (Signed Int16)
        if raw > 32767: raw -= 65536
        return raw * self._factor

    @property
    def native_unit_of_measurement(self):
        return self._unit
    
    @property
    def device_class(self):
        return self._dev_class