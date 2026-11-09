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
                # Automatisches Erkennen von Komponenten über Coil 1-8 (Presence-Bits)
                # Coil 2: HK1, Coil 3: HK2, Coil 5: DHW
                hk2_detected = False
                boiler_detected = False
                
                try:
                    # Kurzer Connect für Auto-Detect
                    await self.hass.async_add_executor_job(hub.connect)
                    # Dies ist eine vereinfachte Erkennung; in komplexeren Setups ggf. feiner Granulieren
                    coils = await self.hass.async_add_executor_job(hub._client.read_coils, 1, 8, slave=user_input[CONF_SLAVE_ID])
                    if not getattr(coils, "isError", lambda: True)():
                        bits = coils.bits
                        if len(bits) >= 8:
                            hk2_detected = bits[2] # Coil 3
                            boiler_detected = True # Default / Heuristisch
                except Exception:
                    pass
                finally:
                    await self.hass.async_add_executor_job(hub.close)
                    
                user_input[CONF_HK2] = hk2_detected
                user_input[CONF_BOILER] = boiler_detected
                user_input[CONF_SOLAR] = False
                user_input[CONF_POOL] = False
                user_input[CONF_ROOM] = False
                user_input[CONF_WOOD] = False
                user_input[CONF_EMS] = False
                
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
