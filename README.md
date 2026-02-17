# Paradigma Heating Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![version](https://img.shields.io/github/v/release/nussfuellung/paradigma-homeassistant?include_prereleases)](https://github.com/nussfuellung/paradigma-homeassistant/releases)

![Paradigma Integration Logo](logo.png)

**Now available in HACS default Repository, just search in HACS for Paradigma. No need to add a custom repository.**

This is a custom integration for **Paradigma** heating systems (SystaSmartC II / SystaComfort II) for Home Assistant. It communicates locally via **Modbus TCP**.

There is a big update coming in the first half of this year adding support for **heat pumps**, please stay calm you will get an update notification as soon as the integration is able to support it.

**IMPORTANT**
**It is necessary to remove your modbus configuration for Paradigma if you already tried to add it to HomeAssistant before you try to install this integration, as the system blocks requests from more than one device at a time!**


[🇩🇪 Zur deutschen Beschreibung springen](#german)

---

## 🇬🇧 English Description

### Compatible Devices
This integration is designed for Paradigma controllers that support the "Modbus-Schnittstelle für das Smarthome-System" protocol (Protocol Version 1.1).

* **SystaSmartC II**
* **SystaComfort II**
* **Extensions:** SystaComfort Wood, SystaComfort Pool, SystaExpresso (Fresh water station).

### Features

The integration connects to the heating controller (Unit ID 1) and provides a fully modular setup. You can enable/disable specific components during configuration.

#### 🌡️ Sensors (Read-Only)
* **Standard:** Outdoor Temp, Flow/Return (HK1), DHW Temp, Buffer (Top/Bottom), Circulation Return.
* **Status:** Text-based status messages (translated) for Heating Circuits, DHW, Circulation, and Boiler.
* **Optional Components (Selectable):**
    * **Solar:** Collector Temp, Current Power, Daily Yield, Total Yield.
    * **Heating Circuit 2 (HK2):** Flow/Return, Room Temp, Status.
    * **Boiler (Gas/Oil):** Flow/Return, Operation Hours, Starts, Status.
    * **Wood/Pellet:** Flow/Return, Buffer Top, Pellet Consumption (kg/t), Operation Hours, Detailed Status messages.
    * **Pool:** Temp, Flow/Return, Status.
    * **Room Sensors:** Room temperatures for HK1 and HK2.

#### 🎛️ Controls (Read/Write)
* **Heating Circuits:** Set target **Flow Temperature** (Vorlauf) via Number entities for HK1 and HK2.
* **Domestic Hot Water:** Set target water temperature and toggle On/Off via a **Water Heater** entity.
* **Buffer/Boiler:** Set target temperatures for Buffer Top and Boiler.

#### 🔘 Switches
* **DHW Enable:** Enable/Disable hot water preparation globally.
* **Circulation Enable:** Enable/Disable circulation pump globally.

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
4.  **Select your installed components:**
    * Check the boxes for **Solar**, **Heating Circuit 2**, **Pool**, **Room Sensors**, **Boiler**, or **Wood/Pellet** to enable the respective sensors.

> **Note:** You can change these settings later by clicking **"Configure"** on the integration entry.

---

<a name="german"></a>
## 🇩🇪 Deutsche Beschreibung

### Kompatible Geräte
Diese Integration unterstützt Paradigma Regelungen, die das Protokoll "Modbus-Schnittstelle für das Smarthome-System" (Protokoll V1.1) unterstützen.

* **SystaSmartC II**
* **SystaComfort II**
* **Erweiterungen:** SystaComfort Wood, SystaComfort Pool, SystaExpresso.

### Funktionen

Die Integration verbindet sich mit dem Heizungsregler (Unit ID 1) und bietet einen modularen Aufbau. Komponenten können bei der Einrichtung an- oder abgewählt werden.

#### 🌡️ Sensoren (Nur Lesen)
* **Standard:** Außentemperatur, Vorlauf/Rücklauf (HK1), Warmwasser, Puffer (Oben/Unten), Zirkulation Rücklauf.
* **Status:** Klartext-Statusmeldungen (übersetzt) für Heizkreise, Warmwasser, Zirkulation und Kessel (z. B. "Heizbetrieb", "Vorhaltezeit", "Ladung läuft").
* **Optionale Komponenten (Wählbar):**
    * **Solar:** Kollektor-Temp, Leistung, Tagesertrag, Gesamtertrag.
    * **Heizkreis 2 (HK2):** Vorlauf/Rücklauf, Raumtemperatur, Status.
    * **Kessel (Gas/Öl):** Vorlauf/Rücklauf, Betriebsstunden, Starts, Status.
    * **Holz/Pellets:** Vorlauf/Rücklauf, Puffer Oben, Pelletverbrauch, Betriebsstunden, Detaillierter Status (z.B. "Ausbrand", "Zünden").
    * **Pool:** Temp, Vorlauf/Rücklauf, Status.
    * **Raumfühler:** Raumtemperaturen für HK1 und HK2 (falls Fernbedienung vorhanden).

#### 🎛️ Steuerung (Lesen/Schreiben)
* **Heizkreise:** Setzen der **Soll-Vorlauftemperatur** über Nummer-Entitäten für HK1 und HK2.
* **Warmwasser:** Setzen der Warmwasser-Solltemperatur und An/Aus über eine **Water Heater** (Wassererwärmer) Entität.
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
4.  **Wählen Sie Ihre installierten Komponenten:**
    * Setzen Sie Haken bei **Solar**, **Heizkreis 2**, **Pool**, **Raumfühler**, **Kessel** oder **Holz/Pellet**, um die entsprechenden Sensoren zu aktivieren.

> **Hinweis:** Sie können diese Einstellungen jederzeit nachträglich ändern, indem Sie bei der Integration auf **"Konfigurieren"** klicken.

---

### Disclaimer / Haftungsausschluss

This is a private open-source project and **not** an official product of Ritter Energie- und Umwelttechnik GmbH & Co. KG or Paradigma. Use at your own risk.

Dies ist ein privates Open-Source-Projekt und **kein** offizielles Produkt der Ritter Energie- und Umwelttechnik GmbH & Co. KG oder Paradigma. Benutzung auf eigene Gefahr.
