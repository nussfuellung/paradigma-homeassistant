"""Config flow for Paradigma."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME
from .const import DOMAIN, DEFAULT_NAME, DEFAULT_PORT, DEFAULT_SLAVE_ID, CONF_SLAVE_ID
from .const import CONF_SOLAR, CONF_HK2, CONF_POOL, CONF_ROOM, CONF_BOILER, CONF_WOOD, CONF_EMS
from .hub import ParadigmaHub

class ParadigmaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 2

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            hub = ParadigmaHub(self.hass, user_input[CONF_NAME], user_input[CONF_HOST], user_input[CONF_PORT], user_input[CONF_SLAVE_ID])
            connected = await self.hass.async_add_executor_job(hub.connect)
            await self.hass.async_add_executor_job(hub.close)
            
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
                vol.Optional(CONF_EMS, default=False): bool,
            }),
            errors=errors
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return ParadigmaOptionsFlowHandler(config_entry)

class ParadigmaOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            new_data = {**self.config_entry.data, **user_input}
            self.hass.config_entries.async_update_entry(self.config_entry, data=new_data)
            return self.async_create_entry(title="", data={})

        data = self.config_entry.data
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(CONF_SOLAR, default=data.get(CONF_SOLAR, False)): bool,
                vol.Optional(CONF_HK2, default=data.get(CONF_HK2, False)): bool,
                vol.Optional(CONF_POOL, default=data.get(CONF_POOL, False)): bool,
                vol.Optional(CONF_ROOM, default=data.get(CONF_ROOM, False)): bool,
                vol.Optional(CONF_BOILER, default=data.get(CONF_BOILER, False)): bool,
                vol.Optional(CONF_WOOD, default=data.get(CONF_WOOD, False)): bool,
                vol.Optional(CONF_EMS, default=data.get(CONF_EMS, False)): bool,
            })
        )
