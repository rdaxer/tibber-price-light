"""Config Flow für Tibber Preis-Ampel."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

_LOGGER = logging.getLogger(__name__)

DOMAIN = "tibber_price_light"

class TibberPriceLightConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config Flow für die Tibber Preis-Ampel."""
    
    VERSION = 1
    
    async def async_step_user(self, user_input=None):
        """Erster Schritt - Tibber Sensor auswählen."""
        errors = {}
        
        if user_input is not None:
            tibber_sensor = user_input.get("tibber_sensor")
            
            if tibber_sensor:
                state = self.hass.states.get(tibber_sensor)
                if state is None:
                    errors["tibber_sensor"] = "sensor_not_found"
                else:
                    await self.async_set_unique_id(f"tibber_price_light_{tibber_sensor}")
                    self._abort_if_unique_id_configured()
                    
                    return self.async_create_entry(
                        title=f"Preis-Ampel ({tibber_sensor.split('.')[-1]})",
                        data=user_input,
                    )
            else:
                errors["tibber_sensor"] = "no_sensor_selected"
        
        tibber_sensors = []
        for state in self.hass.states.async_all():
            if state.entity_id.startswith("sensor.") and "tibber" in state.entity_id.lower():
                if "electricity_price" in state.entity_id or "price" in state.entity_id:
                    tibber_sensors.append(state.entity_id)
        
        data_schema = vol.Schema({
            vol.Required("tibber_sensor"): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain="sensor",
                    multiple=False
                )
            ),
        })
        
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "info": "Wähle deinen Tibber Strompreis-Sensor aus."
            }
        )