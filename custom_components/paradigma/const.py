"""Constants for the Paradigma integration."""
from homeassistant.const import Platform

DOMAIN = "paradigma"
DEFAULT_NAME = "Paradigma"
DEFAULT_PORT = 502
CONF_SLAVE_ID = "slave_id"
DEFAULT_SLAVE_ID = 1  # Unit ID 1 laut PDF Seite 9 [cite: 122]
DEFAULT_SCAN_INTERVAL = 30

PLATFORMS = [Platform.SENSOR, Platform.NUMBER, Platform.SWITCH, Platform.WATER_HEATER]