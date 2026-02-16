"""Config flow for Paradigma integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME, CONF_SCAN_INTERVAL
from .const import (
    DOMAIN, DEFAULT_PORT, DEFAULT_SLAVE_ID, CONF_SLAVE_ID, DEFAULT_SCAN_INTERVAL,
    CONF_SOLAR, CONF_HK2, CONF_POOL, CONF_ROOM, CONF_BOILER, CONF_WOOD, DEFAULT_NAME
)
from .hub import ParadigmaHub

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Paradigma."""
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Verbindungstest vor dem Erstellen
            hub = ParadigmaHub(self.hass, user_input[CONF_NAME], user_input[CONF_HOST], user_input[CONF_PORT], user_input[CONF_SLAVE_ID])
            connected = await self.hass.async_add_executor_job(hub.connect)
            hub.close()

            if connected:
                return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
            else:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
                vol.Required(CONF_SLAVE_ID, default=DEFAULT_SLAVE_ID): int,
                vol.Optional(CONF_SOLAR, default=True): bool,
                vol.Optional(CONF_HK2, default=False): bool,
                vol.Optional(CONF_BOILER, default=True): bool,
                vol.Optional(CONF_WOOD, default=False): bool,
                vol.Optional(CONF_ROOM, default=False): bool,
                vol.Optional(CONF_POOL, default=False): bool,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
            }),
            errors=errors,
        )

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options."""
    def __init__(self, config_entry):
        
        pass

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            
            new_data = self.config_entry.data.copy()
            new_data.update(user_input)

            self.hass.config_entries.async_update_entry(
                self.config_entry, data=new_data
            )
            return self.async_create_entry(title="", data=new_data)

        
        data = self.config_entry.data
        
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST, default=data.get(CONF_HOST)): str,
                vol.Required(CONF_PORT, default=data.get(CONF_PORT)): int,
                vol.Required(CONF_SLAVE_ID, default=data.get(CONF_SLAVE_ID)): int,
                vol.Optional(CONF_SOLAR, default=data.get(CONF_SOLAR, True)): bool,
                vol.Optional(CONF_HK2, default=data.get(CONF_HK2, False)): bool,
                vol.Optional(CONF_BOILER, default=data.get(CONF_BOILER, True)): bool,
                vol.Optional(CONF_WOOD, default=data.get(CONF_WOOD, False)): bool,
                vol.Optional(CONF_ROOM, default=data.get(CONF_ROOM, False)): bool,
                vol.Optional(CONF_POOL, default=data.get(CONF_POOL, False)): bool,
                vol.Optional(CONF_SCAN_INTERVAL, default=data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)): int,
            }),
        )
