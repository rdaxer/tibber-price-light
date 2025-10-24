"""Sensor Plattform für Tibber Preis-Ampel."""
import logging
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

_LOGGER = logging.getLogger(__name__)

DOMAIN = "tibber_price_light"

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Richte den Sensor ein."""
    tibber_sensor = entry.data.get("tibber_sensor")
    
    if not tibber_sensor:
        _LOGGER.error("Kein Tibber Sensor konfiguriert")
        return
    
    async_add_entities([TibberPriceLightSensor(hass, tibber_sensor)], True)

class TibberPriceLightSensor(SensorEntity):
    """Repräsentation der Tibber Preis-Ampel."""
    
    def __init__(self, hass: HomeAssistant, tibber_sensor: str) -> None:
        """Initialisiere den Sensor."""
        self.hass = hass
        self._tibber_sensor = tibber_sensor
        self._state = "unknown"
        self._attributes = {}
        self._attr_name = "Tibber Preis Ampel"
        self._attr_unique_id = f"tibber_price_light_{tibber_sensor}"
        
    async def async_added_to_hass(self) -> None:
        """Wird aufgerufen, wenn der Sensor zu Home Assistant hinzugefügt wird."""
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                [self._tibber_sensor],
                self._handle_state_change,
            )
        )
        await self.async_update()
    
    @callback
    def _handle_state_change(self, event) -> None:
        """Reagiere auf Zustandsänderungen des Tibber Sensors."""
        self.hass.async_create_task(self.async_update())
    
    @property
    def state(self) -> str:
        """Gebe den aktuellen Status zurück (green, yellow, red)."""
        return self._state
    
    @property
    def icon(self) -> str:
        """Icon basierend auf dem Status."""
        if self._state == "green":
            return "mdi:traffic-light-outline"
        elif self._state == "yellow":
            return "mdi:traffic-light-outline"
        elif self._state == "red":
            return "mdi:traffic-light-outline"
        return "mdi:help-circle-outline"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Gebe zusätzliche Attribute zurück."""
        return self._attributes
    
    async def async_update(self) -> None:
        """Aktualisiere den Sensor-Status."""
        tibber_state = self.hass.states.get(self._tibber_sensor)
        
        if tibber_state is None:
            _LOGGER.warning(f"Tibber Sensor {self._tibber_sensor} nicht gefunden")
            self._state = "unknown"
            return
        
        try:
            current_price = float(tibber_state.state)
            attributes = tibber_state.attributes
            
            max_price = float(attributes.get("max_price", 0))
            min_price = float(attributes.get("min_price", 0))
            avg_price = float(attributes.get("avg_price", 0))
            
            if max_price == 0 or min_price == 0:
                _LOGGER.warning("Keine gültigen Preisdaten verfügbar")
                self._state = "unknown"
                return
            
            range_span = max_price - min_price
            threshold_red = avg_price + (range_span * 0.3)
            threshold_yellow = avg_price
            
            if current_price <= threshold_yellow:
                self._state = "green"
                status_text = "Günstiger Preis"
            elif current_price <= threshold_red:
                self._state = "yellow"
                status_text = "Durchschnittlicher Preis"
            else:
                self._state = "red"
                status_text = "Hoher Preis"
            
            percent_of_range = ((current_price - min_price) / range_span * 100) if range_span > 0 else 0
            
            self._attributes = {
                "current_price": round(current_price, 4),
                "min_price_today": round(min_price, 4),
                "max_price_today": round(max_price, 4),
                "avg_price_today": round(avg_price, 4),
                "threshold_yellow": round(threshold_yellow, 4),
                "threshold_red": round(threshold_red, 4),
                "status_text": status_text,
                "percent_of_range": round(percent_of_range, 1),
                "unit": attributes.get("unit", "EUR/kWh"),
                "tibber_sensor": self._tibber_sensor,
            }
            
            _LOGGER.debug(
                f"Preis-Ampel aktualisiert: {status_text} "
                f"(Preis: {current_price}, Schwellen: gelb<={threshold_yellow}, rot>{threshold_red})"
            )
            
        except (ValueError, TypeError) as err:
            _LOGGER.error(f"Fehler beim Verarbeiten der Preisdaten: {err}")
            self._state = "unknown"
        
        self.async_write_ha_state()