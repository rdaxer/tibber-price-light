# 🚦 Tibber Preis-Ampel für Home Assistant

Eine Custom Integration, die deinen Tibber-Strompreis als Ampel visualisiert.

## Was macht diese Integration?

Die Tibber Preis-Ampel erstellt einen Sensor, der deinen aktuellen Strompreis bewertet:

- 🟢 **Grün**: Preis unter Tagesdurchschnitt (günstig!)
- 🟡 **Gelb**: Durchschnittlicher Preis
- 🔴 **Rot**: Preis deutlich über Durchschnitt (teuer!)

## ✅ Voraussetzungen

- Home Assistant 2024.1.0 oder neuer
- [Tibber Integration](https://www.home-assistant.io/integrations/tibber/) bereits eingerichtet
- Ein funktionierender Tibber Strompreis-Sensor

## 📦 Installation

### Via HACS (empfohlen)

1. Öffne HACS in Home Assistant
2. Klicke auf **"Integrationen"**
3. Klicke auf die **drei Punkte** oben rechts
4. Wähle **"Benutzerdefinierte Repositories"**
5. Füge diese URL hinzu: `https://github.com/rdaxer/tibber-price-light`
6. Wähle Kategorie: **"Integration"**
7. Klicke auf **"Hinzufügen"**
8. Suche nach **"Tibber Preis-Ampel"** und installiere sie
9. Starte Home Assistant neu

### Manuell

1. Kopiere den `custom_components/tibber_price_light` Ordner in dein `config/custom_components` Verzeichnis
2. Starte Home Assistant neu

## ⚙️ Konfiguration

1. Gehe zu **Einstellungen** → **Geräte & Dienste**
2. Klicke auf **+ Integration hinzufügen**
3. Suche nach **"Tibber Preis-Ampel"**
4. Wähle deinen Tibber Strompreis-Sensor aus
5. Fertig!

## 📊 Sensor Attribute

Der Sensor `sensor.tibber_preis_ampel` liefert:

- **Status**: `green`, `yellow`, oder `red`
- **current_price**: Aktueller Preis
- **min_price_today**: Minimaler Tagespreis
- **max_price_today**: Maximaler Tagespreis
- **avg_price_today**: Durchschnittlicher Tagespreis
- **threshold_yellow**: Schwellenwert für Gelb
- **threshold_red**: Schwellenwert für Rot
- **status_text**: Beschreibung (z.B. "Günstiger Preis")
- **percent_of_range**: Prozent im Tagesbereich

## 🤖 Automation Beispiel

```yaml
alias: "Benachrichtigung bei günstigem Strom"
trigger:
  - platform: state
    entity_id: sensor.tibber_preis_ampel
    to: "green"
action:
  - service: notify.mobile_app
    data:
      title: "💚 Günstiger Strom!"
      message: "Jetzt nur {{ state_attr('sensor.tibber_preis_ampel', 'current_price') }} €/kWh"
```

## 📱 Lovelace Karte

```yaml
type: entities
entities:
  - entity: sensor.tibber_preis_ampel
    name: Strompreis
    state_color: true
  - type: attribute
    entity: sensor.tibber_preis_ampel
    attribute: status_text
  - type: attribute
    entity: sensor.tibber_preis_ampel
    attribute: current_price
    suffix: " €/kWh"
```

## 🎨 Schwellenwerte anpassen

Die Standard-Schwellenwerte sind:
- **Grün**: Preis ≤ Durchschnitt
- **Gelb**: Durchschnitt < Preis ≤ Durchschnitt + 30% der Spanne
- **Rot**: Preis > Durchschnitt + 30% der Spanne

Um dies anzupassen, ändere in `sensor.py` Zeile 104:
```python
threshold_red = avg_price + (range_span * 0.3)  # Ändere 0.3 nach Belieben
```

## 🐛 Fehlersuche

**Integration erscheint nicht**  
→ Stelle sicher, dass du Home Assistant neu gestartet hast.

**Sensor zeigt "unknown"**  
→ Prüfe, ob dein Tibber-Sensor korrekt konfiguriert ist und Daten liefert.

## 📝 Lizenz

MIT License

## 💬 Support

Bei Problemen oder Fragen erstelle bitte ein Issue auf GitHub.

---

**Erstellt mit ❤️ für die Home Assistant Community**
