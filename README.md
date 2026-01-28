# Paradigma Heating Integration for Home Assistant

![Paradigma Integration Logo](logo.png)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![version](https://img.shields.io/github/v/release/nussfuellung/paradigma-homeassistant?include_prereleases)](https://github.com/nussfuellung/paradigma-homeassistant/releases)

This is a custom integration for **Paradigma** heating systems (SystaSmartC II / SystaComfort II) for Home Assistant. It communicates locally via **Modbus TCP**.

[🇩🇪 Zur deutschen Beschreibung springen](#paradigma-heizung-integration-f%C3%BCr-home-assistant)

---

## 🇬🇧 English Description

### Compatible Devices
This integration is designed for Paradigma controllers that support the "Modbus-Schnittstelle für das Smarthome-System" protocol (Protocol Version 1.1).

* [cite_start]**SystaSmartC II** [cite: 2]
* **SystaComfort II**
* [cite_start]Compatible extensions (Sensors only): SystaComfort Wood, SystaComfort Pool[cite: 196, 201].

### Features

[cite_start]The integration connects to the heating controller (Unit ID 1) [cite: 122] and provides the following entities:

#### 🌡️ Sensors (Read-Only)
* [cite_start]**Temperatures:** Outdoor, Flow/Return (HK1 & HK2), Domestic Hot Water (DHW), Buffer (Top/Bottom), Collector[cite: 196].
* [cite_start]**Solar:** Current Solar Power, Daily Yield, Total Yield[cite: 205].
* [cite_start]**Status:** Text-based status messages for Heating Circuits, DHW, and Boiler (e.g., "Heating Mode", "Frost Protection", "Standby")[cite: 217, 228].

#### 🎛️ Controls (Read/Write)
* [cite_start]**Heating Circuits:** Set target **Flow Temperature** (Vorlauf) via Number entities[cite: 205].
    * *Note: This controls the flow temperature setpoint, not the room temperature directly.*
* [cite_start]**Domestic Hot Water:** Set target water temperature via a **Water Heater** entity[cite: 205].
* [cite_start]**Buffer/Boiler:** Set target temperatures for Buffer Top and Boiler[cite: 214].

#### 🔘 Switches
* [cite_start]**DHW Enable:** Enable/Disable hot water preparation[cite: 192].
* [cite_start]**Circulation Enable:** Enable/Disable circulation pump[cite: 192].

### Installation via HACS

1.  Open **HACS** in Home Assistant.
2.  Go to "Integrations" > Top right menu `...` > **Custom repositories**.
3.  Enter the URL of this repository: `https://github.com/DEIN_GITHUB_USER/paradigma-homeassistant`.
4.  Select Category: **Integration**.
5.  Click **Add** and then install "Paradigma".
6.  Restart Home Assistant.

### Configuration

1.  Go to **Settings** > **Devices & Services**.
2.  Click **Add Integration** and search for **Paradigma**.
3.  Enter the connection details:
    * **Host:** IP address of your SystaSmartC/Comfort.
    * [cite_start]**Port:** Default is `502`[cite: 88].
    * [cite_start]**Unit ID:** Default is `1`[cite: 122].
    * **Scan Interval:** How often to update data (default 30s).

---

## 🇩🇪 Deutsche Beschreibung

### Kompatible Geräte
Diese Integration unterstützt Paradigma Regelungen, die das Protokoll "Modbus-Schnittstelle für das Smarthome-System" (Protokoll V1.1) unterstützen.

* [cite_start]**SystaSmartC II** [cite: 2]
* **SystaComfort II**
* [cite_start]Kompatible Erweiterungen (nur Sensoren): SystaComfort Wood, SystaComfort Pool[cite: 196, 201].

### Funktionen

[cite_start]Die Integration verbindet sich mit dem Heizungsregler (Unit ID 1) [cite: 122] und stellt folgende Entitäten bereit:

#### 🌡️ Sensoren (Nur Lesen)
* [cite_start]**Temperaturen:** Außentemperatur, Vorlauf/Rücklauf (HK1 & HK2), Warmwasser, Puffer (Oben/Unten), Kollektor[cite: 196].
* [cite_start]**Solar:** Aktuelle Solarleistung, Tagesertrag, Gesamtertrag[cite: 205].
* [cite_start]**Status:** Klartext-Statusmeldungen für Heizkreise, Warmwasser und Kessel (z. B. "Heizbetrieb", "Frostschutz", "Ladung läuft")[cite: 217, 228].

#### 🎛️ Steuerung (Lesen/Schreiben)
* [cite_start]**Heizkreise:** Setzen der **Soll-Vorlauftemperatur** über Nummer-Entitäten[cite: 205].
    * *Hinweis: Dies steuert die Vorlauftemperatur, nicht direkt die Raumtemperatur.*
* [cite_start]**Warmwasser:** Setzen der Warmwasser-Solltemperatur über eine **Water Heater** (Wassererwärmer) Entität[cite: 205].
* [cite_start]**Puffer/Kessel:** Setzen der Solltemperaturen für Puffer Oben und den Kessel[cite: 214].

#### 🔘 Schalter
* [cite_start]**Warmwasser Freigabe:** Ein-/Ausschalten der Warmwasserbereitung[cite: 192].
* [cite_start]**Zirkulation Freigabe:** Ein-/Ausschalten der Zirkulationspumpe[cite: 192].

### Installation über HACS

1.  Öffnen Sie **HACS** in Home Assistant.
2.  Gehen Sie zu "Integrationen" > Menü oben rechts `...` > **Benutzerdefinierte Repositories**.
3.  Geben Sie die URL dieses Repositories ein: `https://github.com/DEIN_GITHUB_USER/paradigma-homeassistant`.
4.  Kategorie: **Integration**.
5.  Klicken Sie auf **Hinzufügen** und installieren Sie "Paradigma".
6.  Starten Sie Home Assistant neu.

### Konfiguration

1.  Gehen Sie zu **Einstellungen** > **Geräte & Dienste**.
2.  Klicken Sie auf **Integration hinzufügen** und suchen Sie nach **Paradigma**.
3.  Geben Sie die Verbindungsdaten ein:
    * **IP-Adresse:** Die IP Ihrer SystaSmartC/Comfort im Netzwerk.
    * [cite_start]**Port:** Standard ist `502`[cite: 88].
    * [cite_start]**Unit ID:** Standard ist `1`[cite: 122].
    * **Aktualisierungsintervall:** Wie oft Daten abgerufen werden (Standard 30s).

---

### Disclaimer / Haftungsausschluss

This is a private open-source project and **not** an official product of Ritter Energie- und Umwelttechnik GmbH & Co. KG or Paradigma. Use at your own risk.

Dies ist ein privates Open-Source-Projekt und **kein** offizielles Produkt der Ritter Energie- und Umwelttechnik GmbH & Co. KG oder Paradigma. Benutzung auf eigene Gefahr.
