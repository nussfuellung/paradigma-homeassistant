"""Paradigma Modbus Hub with Auto-Reconnect."""
import logging
import threading
from time import monotonic
from pymodbus.client import ModbusTcpClient

_LOGGER = logging.getLogger(__name__)

class ParadigmaHub:
    def __init__(self, hass, name, host, port, slave_id):
        self._hass = hass
        self._slave_id = int(slave_id)
        self._client = ModbusTcpClient(host=host, port=port, timeout=5.0)
        self._lock = threading.Lock()
        self.name = name
        self._closed = False
        self._retry_after = 0.0

    def _check_reconnect(self):
        if self._closed:
            return False
        if monotonic() < self._retry_after:
            return False
            
        if not self._client.connected:
            try:
                if not self._client.connect():
                    _LOGGER.warning("Modbus-Verbindung zu %s fehlgeschlagen, nächster Versuch in 5s", self.name)
                    self._retry_after = monotonic() + 5.0
                    return False
                _LOGGER.info("Modbus-Verbindung zu %s erfolgreich hergestellt", self.name)
            except Exception as e:
                _LOGGER.warning("Modbus-Verbindungsfehler: %s", e)
                self._retry_after = monotonic() + 5.0
                return False
        return True

    def connect(self):
        with self._lock:
            return self._check_reconnect()

    def close(self):
        with self._lock:
            self._closed = True
            self._client.close()

    def read_input_registers(self, address, count, slave=None):
        with self._lock:
            if not self._check_reconnect(): return None
            try:
                unit = slave if slave is not None else self._slave_id
                res = self._client.read_input_registers(address, count, slave=unit)
                if getattr(res, "isError", lambda: True)(): return None
                return res.registers
            except Exception as e:
                _LOGGER.error("Fehler beim Lesen (Input %s): %s", address, e)
                self._client.close()
                return None

    def read_holding_registers(self, address, count, slave=None):
        with self._lock:
            if not self._check_reconnect(): return None
            try:
                unit = slave if slave is not None else self._slave_id
                res = self._client.read_holding_registers(address, count, slave=unit)
                if getattr(res, "isError", lambda: True)(): return None
                return res.registers
            except Exception as e:
                _LOGGER.error("Fehler beim Lesen (Holding %s): %s", address, e)
                self._client.close()
                return None

    def write_register(self, address, value, slave=None):
        with self._lock:
            if not self._check_reconnect(): return False
            try:
                unit = slave if slave is not None else self._slave_id
                res = self._client.write_register(address, value, slave=unit)
                if getattr(res, "isError", lambda: True)(): return False
                return True
            except Exception as e:
                _LOGGER.error("Fehler beim Schreiben (Register %s): %s", address, e)
                self._client.close()
                return False
