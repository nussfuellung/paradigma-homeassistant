"""Switch platform for Paradigma."""
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

# Key, BitAddress
# Quelle: PDF Seite 12, Tabelle B1 [cite: 192]
SWITCHES = [
    ("dhw_enable", 4),   # Bit 4
    ("circ_enable", 6),  # Bit 6
]

async def async_setup_entry(hass, entry, async_add_entities):
    hub = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for s in SWITCHES:
        entities.append(ParadigmaSwitch(hub, s[0], s[1], entry.entry_id))
    async_add_entities(entities)

class ParadigmaSwitch(SwitchEntity):
    def __init__(self, hub, key, address, uid):
        self._hub = hub
        self._address = address
        self._attr_has_entity_name = True
        self._attr_translation_key = key
        self._attr_unique_id = f"{uid}_switch_{address}"
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    def update(self):
        res = self._hub.read_coils(self._address, 1)
        if res:
            self._is_on = res[0]

    def turn_on(self, **kwargs):
        if self._hub.write_coil(self._address, True):
            self._is_on = True

    def turn_off(self, **kwargs):
        if self._hub.write_coil(self._address, False):
            self._is_on = False