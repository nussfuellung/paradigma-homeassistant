"""Constants for the Paradigma integration."""
from homeassistant.const import Platform

DOMAIN = "paradigma"
DEFAULT_NAME = "SystaSmartC II"
DEFAULT_PORT = 502
CONF_SLAVE_ID = "slave_id"
DEFAULT_SLAVE_ID = 1
DEFAULT_SCAN_INTERVAL = 30

# Neue Konfigurations-Schlüssel
CONF_SOLAR = "solar_installed"
CONF_HK2 = "hk2_installed"

PLATFORMS = [Platform.SENSOR, Platform.NUMBER, Platform.SWITCH, Platform.WATER_HEATER]