"""Config flow for Paradigma integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME, CONF_SCAN_INTERVAL
from .const import DOMAIN, DEFAULT_PORT, DEFAULT_SLAVE_ID, CONF_SLAVE_ID, DEFAULT_SCAN_INTERVAL
from .hub import ParadigmaHub

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default="Heizung"): str,
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Required(CONF_SLAVE_ID, default=DEFAULT_SLAVE_ID): int,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
    }
)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Paradigma."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            hub = ParadigmaHub(
                self.hass,
                user_input[CONF_NAME],
                user_input[CONF_HOST],
                user_input[CONF_PORT],
                user_input[CONF_SLAVE_ID],
            )

            connected = await self.hass.async_add_executor_job(hub.connect)
            hub.close()

            if connected:
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )
            else:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )