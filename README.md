# Paradigma Heating Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![version](https://img.shields.io/github/v/release/nussfuellung/paradigma-homeassistant?include_prereleases)](https://github.com/nussfuellung/paradigma-homeassistant/releases)

![Paradigma Integration Logo](logo.png)

This is a custom integration for **Paradigma** heating systems (SystaSmartC II / SystaComfort II) for Home Assistant. It communicates locally via **Modbus TCP**.

[🇩🇪 Zur deutschen Beschreibung springen](#german)

---

## 🇬🇧 English Description

### Compatible Devices
This integration is designed for Paradigma controllers that support the "Modbus-Schnittstelle für das Smarthome-System" protocol (Protocol Version 1.1).

* **SystaSmartC II**
* **SystaComfort II**
* Compatible extensions (Sensors only): SystaComfort Wood, SystaComfort Pool.

### Features

The integration connects to the heating controller (Unit ID 1) and provides the following entities:

#### 🌡️ Sensors (Read-Only)
* **Temperatures:** Outdoor, Flow/Return (Heating Circuits 1 & 2), Domestic Hot Water (DHW), Buffer (Top/Bottom), Collector.
* **Solar:** Current Solar Power, Daily Yield, Total Yield.
* **Status:** Text-based status messages for Heating Circuits, DHW, and Boiler (e.g., "Heating Mode", "Frost Protection", "Standby").

#### 🎛️ Controls (Read/Write)
* **Heating Circuits:** Set target **Flow Temperature** (Vorlauf) via Number entities.
    * *Note: This controls the flow temperature setpoint sent to the controller, not the room temperature directly.*
* **Domestic Hot Water:** Set target water temperature via a **Water Heater** entity.
* **Buffer/Boiler:** Set target temperatures for Buffer Top and Boiler.

#### 🔘 Switches
* **DHW Enable:** Enable/Disable hot water preparation.
* **Circulation Enable:** Enable/Disable circulation pump.

### Installation via HACS

1.  Open **HACS** in Home Assistant.
2.  Go to **Integrations** > Top right menu `...` > **Custom repositories**.
3.  Enter the URL of your repository (e.g., `https://github.com/nussfuellung/paradigma-homeassistant`).
4.  Select Category: **Integration**.
5.  Click **Add** and then install "Paradigma".
6.  Restart Home Assistant.

### Configuration

1.  Go to **Settings** > **Devices & Services**.
2.  Click **Add Integration** and search for **Paradigma**.
3.  Enter the connection details:
    * **Host:** IP address of your SystaSmartC/Comfort.
    * **Port:** Default is `502`.
    * **Unit ID:** Default is `1`.
    * **Scan Interval:** How often to update data (default 30s).

---

<a name="german"></a>
## 🇩🇪 Deutsche Beschreibung

### Kompatible Geräte
Diese Integration unterstützt Paradigma Regelungen, die das Protokoll "Modbus-Schnittstelle für das Smarthome-System" (Protokoll V1.1) unterstützen.

* **SystaSmartC II**
* **SystaComfort II**
* Kompatible Erweiterungen (nur Sensoren): SystaComfort Wood, SystaComfort Pool.

### Funktionen

Die Integration verbindet sich mit dem Heizungsregler (Unit ID 1) und stellt folgende Entitäten bereit:

#### 🌡️ Sensoren (Nur Lesen)
* **Temperaturen:** Außentemperatur, Vorlauf/Rücklauf (HK1 & HK2), Warmwasser, Puffer (Oben/Unten), Kollektor.
* **Solar:** Aktuelle Solarleistung, Tagesertrag, Gesamtertrag.
* **Status:** Klartext-Statusmeldungen für Heizkreise, Warmwasser und Kessel (z. B. "Heizbetrieb", "Frostschutz", "Ladung läuft").

#### 🎛️ Steuerung (Lesen/Schreiben)
* **Heizkreise:** Setzen der **Soll-Vorlauftemperatur** über Nummer-Entitäten.
    * *Hinweis: Dies steuert die Vorlauftemperatur, die an den Regler gesendet wird, nicht direkt die Raumtemperatur.*
* **Warmwasser:** Setzen der Warmwasser-Solltemperatur über eine **Water Heater** (Wassererwärmer) Entität.
* **Puffer/Kessel:** Setzen der Solltemperaturen für Puffer Oben und den Kessel.

#### 🔘 Schalter
* **Warmwasser Freigabe:** Ein-/Ausschalten der Warmwasserbereitung (DHW Enable).
* **Zirkulation Freigabe:** Ein-/Ausschalten der Zirkulationspumpe (Circ Enable).

### Installation über HACS

1.  Öffnen Sie **HACS** in Home Assistant.
2.  Gehen Sie zu **Integrationen** > Menü oben rechts `...` > **Benutzerdefinierte Repositories**.
3.  Geben Sie die URL Ihres Repositories ein (z.B. `https://github.com/nussfuellung/paradigma-homeassistant`).
4.  Kategorie: **Integration**.
5.  Klicken Sie auf **Hinzufügen** und installieren Sie "Paradigma".
6.  Starten Sie Home Assistant neu.

### Konfiguration

1.  Gehen Sie zu **Einstellungen** > **Geräte & Dienste**.
2.  Klicken Sie auf **Integration hinzufügen** und suchen Sie nach **Paradigma**.
3.  Geben Sie die Verbindungsdaten ein:
    * **IP-Adresse:** Die IP Ihrer SystaSmartC/Comfort im Netzwerk.
    * **Port:** Standard ist `502`.
    * **Unit ID:** Standard ist `1`.
    * **Aktualisierungsintervall:** Wie oft Daten abgerufen werden (Standard 30s).

---

### Disclaimer / Haftungsausschluss

This is a private open-source project and **not** an official product of Ritter Energie- und Umwelttechnik GmbH & Co. KG or Paradigma. Use at your own risk.

Dies ist ein privates Open-Source-Projekt und **kein** offizielles Produkt der Ritter Energie- und Umwelttechnik GmbH & Co. KG oder Paradigma. Benutzung auf eigene Gefahr.
