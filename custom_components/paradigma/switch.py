"""Switch platform for Paradigma."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

SWITCHES = [
    ("dhw_enable", 4),   # Bit 4
    ("circ_enable", 6),  # Bit 6
]

async def async_setup_entry(hass, entry, async_add_entities):
    hub = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for s in SWITCHES:
        entities.append(ParadigmaSwitch(hub, s[0], s[1], entry))
    async_add_entities(entities)

class ParadigmaSwitch(SwitchEntity):
    def __init__(self, hub, key, address, entry):
        self._hub = hub
        self._address = address
        self._entry_id = entry.entry_id
        self._attr_has_entity_name = True
        self._attr_translation_key = key
        self._attr_unique_id = f"{entry.entry_id}_switch_{address}"
        self._is_on = False

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name="Paradigma Heizung",
            manufacturer="Paradigma",
            model="SystaSmartC II",
        )

    @property
    def is_on(self):
        return self._is_on

    def update(self):
        # Coils lesen (Bit-Adresse)
        # Die Methode read_coils erwartet die Bit-Adresse.
        # Laut PDF Seite 12 sind das Bits im Register. 
        # Modbus Function 01 (Read Coils) liest normalerweise diskrete Ausgänge.
        # Paradigma nutzt Function 01.
        res = self._hub.read_coils(self._address, 1)
        if res:
            self._is_on = res[0]

    def turn_on(self, **kwargs):
        if self._hub.write_coil(self._address, True):
            self._is_on = True

    def turn_off(self, **kwargs):
        if self._hub.write_coil(self._address, False):
            self._is_on = False