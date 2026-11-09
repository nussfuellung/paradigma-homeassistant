# Paradigma Heating Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
[![version](https://img.shields.io/github/v/release/nussfuellung/paradigma-homeassistant?include_prereleases)](https://github.com/nussfuellung/paradigma-homeassistant/releases)
[![Downloads](https://img.shields.io/github/downloads/nussfuellung/paradigma-homeassistant/total.svg?style=flat)](https://github.com/nussfuellung/paradigma-homeassistant/releases)
[![Stars](https://img.shields.io/github/stars/nussfuellung/paradigma-homeassistant.svg?style=flat)](https://github.com/nussfuellung/paradigma-homeassistant/stargazers)
[![Issues](https://img.shields.io/github/issues/nussfuellung/paradigma-homeassistant.svg?style=flat)](https://github.com/nussfuellung/paradigma-homeassistant/issues)
[![Last Commit](https://img.shields.io/github/last-commit/nussfuellung/paradigma-homeassistant.svg?style=flat)](https://github.com/nussfuellung/paradigma-homeassistant/commits/main)

![Paradigma Integration Logo](logo.png)

> [!TIP]
> **Now available in the Marketplace! Just search for "Paradigma" in HACS. No need to add a custom repository anymore.**

This is a custom integration for **Paradigma** heating systems for Home Assistant. It communicates locally via **Modbus TCP**.

A major update adding support for **heat pumps** is planned for the first half of this year. You will receive an update notification via Marketplace as soon as this feature becomes available. (There are already experimental features included)
=======
> **Now available in the Home Assistant Marketplace! Just search for "Paradigma" in the Marketplace. No need to add a custom repository anymore.**

This is a custom integration for **Paradigma** heating systems for Home Assistant. It communicates locally via **Modbus TCP**.
>>>>>>> 852c050 (change readme)

> [!IMPORTANT]
> **If you previously added your heating system manually via YAML, make sure to remove all old Modbus files/entries from your `configuration.yaml`. Otherwise, the system may block the Modbus communication.**

[🇩🇪 Zur deutschen Beschreibung springen](#german)

---

## 🇬🇧 English Description

### Compatible Devices
This integration is designed for Paradigma controllers that support the "Modbus-Schnittstelle für das Smarthome-System" protocol (Protocol Version 1.1).

- **SystaSmartC II**
- **SystaComfort II**
- **Extensions:** SystaComfort Wood, SystaComfort Pool, SystaExpresso (Fresh water station), EzeeMaster / EMS (Heat Pumps).

### Features

The integration connects to the heating controller (Unit ID 1 & Unit ID 2) and provides a fully modular setup. Hardware detection is mostly automatic, but you can manually enable or disable specific components during configuration.

#### 🌡️ Sensors (Read-Only)
- **Standard:** Outdoor Temp, Flow/Return (HK1), DHW Temp, Buffer (Top/Bottom), Circulation Return.
- **Status & Errors:** Clear-text status messages (fully translated) for Heating Circuits, DHW, Circulation, and Boiler. Dedicated sensor for Controller Error Codes.
- **Optional Components (Selectable):**
    * **Solar:** Collector Temp, Outdoor Temp (Collector), Current Power, Daily Yield, Total Yield.
    * **Heating Circuit 2 (HK2):** Flow/Return, Room Temp, Status.
    * **Boiler (Gas/Oil):** Flow/Return, Operation Hours, Starts, Status.
    * **Wood/Pellet (e.g. PELEO):** Flow/Return, Buffer Top, Pellet Consumption, Operation Hours, Detailed Status messages (e.g., "Burnout", "Ignition").
    * **Heat Pump / EMS:** Current Heat Pump Power, Heater Rod Power, PV Surplus (Write), Grid Limit (Write), Tariff Control (Select), Model ID, Software Version.
    * **Pool:** Temp, Flow/Return, Status.
    * **Room Sensors:** Room temperatures for HK1 and HK2.
    * **SystaExpresso (Fresh water):** Heat quantity for DHW and Circulation.

#### 🎛️ Controls (Read/Write)
- **Heating Circuits:** Set target **Flow Temperature** (Vorlauf) via Number entities for HK1 and HK2. (Max limits are dynamically fetched from the controller).
- **Domestic Hot Water:** Set target water temperature and toggle On/Off via a **Water Heater** entity.
- **Heat Pump Tariffs:** Select the current Heat Pump Tariff (Normal, High/Block, Low/Release) via a Select entity.

#### 🔘 Switches
- **DHW Enable:** Enable/Disable hot water preparation globally.
- **Circulation Enable:** Enable/Disable circulation pump globally.

### Installation via Marketplace

1.  Open **Marketplace** in Home Assistant (formerly known as HACS).
2.  Search for **Paradigma**.
3.  Click **Download** / **Install**.
4.  Restart Home Assistant.

### Configuration

1.  Go to **Settings** > **Devices & Services**.
2.  Click **Add Integration** and search for **Paradigma**.
3.  Enter the connection details:
    * **Host:** IP address of your SystaSmartC/Comfort.
    * **Port:** Default is `502`.
    * **Unit ID:** Default is `1`.
4.  **Select your installed components:**
    * The integration will try to auto-detect your setup (e.g., HK2, Boiler).
    * Check or uncheck the boxes for **Solar**, **Heating Circuit 2**, **Pool**, **Room Sensors**, **Boiler**, **Wood/Pellet**, or **Heat Pump / EMS** to enable the respective sensors.

> **Note:** You can change these settings at any time by clicking **"Configure"** on the integration entry.

---

<a name="german"></a>
## 🇩🇪 Deutsche Beschreibung

### Kompatible Geräte
Diese Integration unterstützt Paradigma Regelungen, die das Protokoll "Modbus-Schnittstelle für das Smarthome-System" (Protokoll V1.1) unterstützen.

- **SystaSmartC II**
- **SystaComfort II**
- **Erweiterungen:** SystaComfort Wood, SystaComfort Pool, SystaExpresso (Frischwasserstation), EzeeMaster / EMS (Wärmepumpen).

### Funktionen

Die Integration verbindet sich mit dem Heizungsregler (Unit ID 1 & Unit ID 2) und bietet einen modularen Aufbau. Viele Baugruppen werden automatisch erkannt, können aber manuell an- oder abgewählt werden.

#### 🌡️ Sensoren (Nur Lesen)
- **Standard:** Außentemperatur, Vorlauf/Rücklauf (HK1), Warmwasser, Puffer (Oben/Unten), Zirkulation Rücklauf.
- **Status & Störungen:** Klartext-Statusmeldungen (mehrsprachig) für Heizkreise, Warmwasser, Zirkulation und Kessel (z. B. "Heizbetrieb", "Ladung läuft"). Eigener Sensor für Regler-Störcodes.
- **Optionale Komponenten (Wählbar):**
    * **Solar:** Kollektor-Temp, Außentemp (Kollektor), Leistung, Tagesertrag, Gesamtertrag.
    * **Heizkreis 2 (HK2):** Vorlauf/Rücklauf, Raumtemperatur, Status.
    * **Kessel (Gas/Öl):** Vorlauf/Rücklauf, Betriebsstunden, Starts, Status.
    * **Holz/Pellets (z.B. PELEO):** Vorlauf/Rücklauf, Puffer Oben, Pelletverbrauch (kg), Betriebsstunden, Detaillierter Status (z.B. "Ausbrand", "Anheizen").
    * **Wärmepumpe / EMS:** Aktuelle Wärmepumpen-Leistung, Heizstab-Leistung, PV-Überschuss (Schreiben), Netzlimit (Schreiben), Tarif-Steuerung (Auswahl), Model-ID, Software-Version.
    * **Pool:** Temp, Vorlauf/Rücklauf, Status.
    * **Raumfühler:** Raumtemperaturen für HK1 und HK2 (falls Fernbedienung vorhanden).
    * **SystaExpresso (Frischwasser):** Wärmemengen-Zähler für Trinkwasser und Zirkulation.

#### 🎛️ Steuerung (Lesen/Schreiben)
- **Heizkreise:** Einstellen der **Soll-Vorlauftemperatur** über Zahlen-Entitäten (Number) für HK1 und HK2. (Die maximal erlaubten Werte werden dynamisch aus dem Regler ausgelesen).
- **Warmwasser:** Einstellen der Warmwasser-Solltemperatur und An/Aus über eine **Wassererwärmer** (Water Heater) Entität.
- **Wärmepumpen-Tarife:** Auswahl des aktuellen Wärmepumpen-Tarifs (Normal, Hochtarif/Sperre, Niedertarif/Freigabe) über eine Select-Entität.

#### 🔘 Schalter
- **Warmwasser Freigabe:** Ein-/Ausschalten der Warmwasserbereitung (DHW Enable).
- **Zirkulation Freigabe:** Ein-/Ausschalten der Zirkulationspumpe (Circ Enable).

### Installation über Marketplace

1.  Öffnen Sie **Marketplace** in Home Assistant (früher bekannt als HACS).
2.  Suchen Sie nach **Paradigma**.
3.  Klicken Sie auf **Herunterladen**.
4.  Starten Sie Home Assistant neu.

### Konfiguration

1.  Gehen Sie zu **Einstellungen** > **Geräte & Dienste**.
2.  Klicken Sie auf **Integration hinzufügen** und suchen Sie nach **Paradigma**.
3.  Geben Sie die Verbindungsdaten ein:
    * **IP-Adresse:** Die IP Ihrer SystaSmartC/Comfort im Netzwerk.
    * **Port:** Standard ist `502`.
    * **Unit ID:** Standard ist `1`.
4.  **Wählen Sie Ihre installierten Komponenten:**
    * Die Integration versucht, Ihre Hardware (z.B. HK2, Kessel) automatisch zu erkennen.
    * Setzen oder entfernen Sie Haken bei **Solar**, **Heizkreis 2**, **Pool**, **Raumfühler**, **Kessel**, **Holz/Pellet** oder **Wärmepumpe / EMS**, um die entsprechenden Sensoren zu steuern.

> **Hinweis:** Sie können diese Einstellungen jederzeit nachträglich ändern, indem Sie bei der Integration auf **"Konfigurieren"** klicken.

---

### Disclaimer / Haftungsausschluss

This is a private open-source project and **not** an official product of Ritter Energie- und Umwelttechnik GmbH & Co. KG or Paradigma. Use at your own risk.

Dies ist ein privates Open-Source-Projekt und **kein** offizielles Produkt der Ritter Energie- und Umwelttechnik GmbH & Co. KG oder Paradigma. Benutzung auf eigene Gefahr.
