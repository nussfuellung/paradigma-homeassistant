"""Config flow for Paradigma."""
import voluptuous as vol
import logging
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME
from homeassistant.components import dhcp
from .const import DOMAIN, DEFAULT_NAME, DEFAULT_PORT, DEFAULT_SLAVE_ID, CONF_SLAVE_ID
from .const import CONF_SOLAR, CONF_HK2, CONF_POOL, CONF_ROOM, CONF_BOILER, CONF_WOOD, CONF_EMS
from .hub import ParadigmaHub

_LOGGER = logging.getLogger(__name__)

class ParadigmaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 2

    def __init__(self):
        self.discovered_host = None

    async def async_step_dhcp(self, discovery_info: dhcp.DhcpServiceInfo):
        """Handle network auto-discovery via DHCP."""
        self.discovered_host = discovery_info.ip
        
        # Verhindern, dass bereits konfigurierte Geräte via DHCP neu auftauchen (IP Check)
        for entry in self._async_current_entries():
            if entry.data.get(CONF_HOST) == self.discovered_host:
                return self.async_abort(reason="already_configured")
        
        # Unique ID based on MAC Address ensures HA doesn't discover the same device twice
        await self.async_set_unique_id(discovery_info.macaddress)
        self._abort_if_unique_id_configured(updates={CONF_HOST: self.discovered_host})
        
        _LOGGER.info(f"Paradigma Heizung im Netzwerk gefunden: {self.discovered_host}")
        
        # Setze einen Platzhalter-Titel für das Discovery-Fenster
        self.context["title_placeholders"] = {"name": "Paradigma Heizung"}
        
        # Zeige das Setup-Formular mit vorausgefüllter IP an
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            hub = ParadigmaHub(self.hass, user_input[CONF_NAME], user_input[CONF_HOST], user_input[CONF_PORT], user_input[CONF_SLAVE_ID])
            connected = await self.hass.async_add_executor_job(hub.connect)
            
            if connected:
                _LOGGER.info("Starte automatische Hardware-Erkennung (Paradigma Autodiscovery)...")
                # Default Werte
                user_input[CONF_HK2] = False
                user_input[CONF_BOILER] = True # Kessel ist meistens Standard
                user_input[CONF_SOLAR] = False
                user_input[CONF_POOL] = False
                user_input[CONF_ROOM] = False
                user_input[CONF_WOOD] = False
                user_input[CONF_EMS] = False

                try:
                    # 1. Coils für Basis-Präsenz (Heizkreis 2)
                    coils = await self.hass.async_add_executor_job(hub.read_coils, 1, 8)
                    if coils and len(coils) >= 8:
                        user_input[CONF_HK2] = bool(coils[2]) # Coil 3 = HK2

                    # 2. Probe Solar (Kollektortemperatur Input 11)
                    solar_probe = await self.hass.async_add_executor_job(hub.read_input_registers, 11, 1)
                    if solar_probe and solar_probe[0] not in [0x7FFF, 0x8000, 0xFFFF]:
                        user_input[CONF_SOLAR] = True

                    # 3. Probe Wood/Pellet (Holz Vorlauf Input 14)
                    wood_probe = await self.hass.async_add_executor_job(hub.read_input_registers, 14, 1)
                    if wood_probe and wood_probe[0] not in [0x7FFF, 0x8000, 0xFFFF]:
                        user_input[CONF_WOOD] = True

                    # 4. Probe Pool (Pool Temperatur Input 19)
                    pool_probe = await self.hass.async_add_executor_job(hub.read_input_registers, 19, 1)
                    if pool_probe and pool_probe[0] not in [0x7FFF, 0x8000, 0xFFFF]:
                        user_input[CONF_POOL] = True

                    # 5. Probe EMS / Wärmepumpe (Leistung Holding 1 auf Unit ID 2)
                    # FIX: async_add_executor_job takes strictly *args, no kwargs allowed in Home Assistant!
                    ems_probe = await self.hass.async_add_executor_job(hub.read_holding_registers, 1, 1, 2)
                    if ems_probe and ems_probe[0] not in [0x7FFF, 0x8000, 0xFFFF]:
                        user_input[CONF_EMS] = True

                    # 6. Probe Raumfühler (Raumtemp HK1 Input 9)
                    room_probe = await self.hass.async_add_executor_job(hub.read_input_registers, 9, 1)
                    if room_probe and room_probe[0] not in [0x7FFF, 0x8000, 0xFFFF]:
                        user_input[CONF_ROOM] = True

                    _LOGGER.info(f"Autodiscovery abgeschlossen: HK2={user_input[CONF_HK2]}, Solar={user_input[CONF_SOLAR]}, Wood={user_input[CONF_WOOD]}, Pool={user_input[CONF_POOL]}, EMS={user_input[CONF_EMS]}, Room={user_input[CONF_ROOM]}")
                
                except Exception as e:
                    _LOGGER.warning(f"Fehler bei der automatischen Hardware-Erkennung: {e}")
                finally:
                    await self.hass.async_add_executor_job(hub.close)

                # Set unique ID to prevent duplicate setups
                await self.async_set_unique_id(f"paradigma_{user_input[CONF_HOST]}")
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
            else:
                await self.hass.async_add_executor_job(hub.close)
                errors["base"] = "cannot_connect"

        # Pre-fill host if discovered via DHCP
        default_host = self.discovered_host if self.discovered_host else ""

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_HOST, default=default_host): str,
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
                vol.Optional(CONF_BOILER, default=data.get(CONF_BOILER, True)): bool,
                vol.Optional(CONF_WOOD, default=data.get(CONF_WOOD, False)): bool,
                vol.Optional(CONF_EMS, default=data.get(CONF_EMS, False)): bool,
            })
        )
