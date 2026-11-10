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

    def _read_modbus(self, func_name, address, count, slave_override=None):
        func = getattr(self._client, func_name)
        target_slave = slave_override if slave_override is not None else self._slave_id
        with self._lock:
            if not self._check_reconnect(): return None
            try:
                try:
                    res = func(address=address, count=count, device_id=target_slave)
                except TypeError:
                    try:
                        res = func(address, count, slave=target_slave)
                    except TypeError:
                        res = func(address, count, unit=target_slave)
                
                if getattr(res, "isError", lambda: True)(): return None
                return res
            except Exception as e:
                _LOGGER.error(f"Fehler beim Lesen ({func_name} {address}): {e}")
                self._client.close()
                return None

    def read_input_registers(self, address, count, slave=None):
        res = self._read_modbus("read_input_registers", address, count, slave)
        return res.registers if res else None

    def read_holding_registers(self, address, count, slave=None):
        res = self._read_modbus("read_holding_registers", address, count, slave)
        return res.registers if res else None

    def read_coils(self, address, count, slave=None):
        res = self._read_modbus("read_coils", address, count, slave)
        return res.bits if res else None

    def write_register(self, address, value, slave=None):
        target_slave = slave if slave is not None else self._slave_id
        with self._lock:
            if not self._check_reconnect(): return False
            try:
                try:
                    res = self._client.write_registers(address=address, values=[value], device_id=target_slave)
                except TypeError:
                    try:
                        res = self._client.write_registers(address, [value], slave=target_slave)
                    except TypeError:
                        res = self._client.write_registers(address, [value], unit=target_slave)
                
                if getattr(res, "isError", lambda: True)(): return False
                return True
            except Exception as e:
                _LOGGER.error(f"Fehler beim Schreiben (Register {address}): {e}")
                self._client.close()
                return False

    def write_coil(self, address, value, slave=None):
        target_slave = slave if slave is not None else self._slave_id
        with self._lock:
            if not self._check_reconnect(): return False
            try:
                try:
                    res = self._client.write_coil(address, value, device_id=target_slave)
                except TypeError:
                    try:
                        res = self._client.write_coil(address, value, slave=target_slave)
                    except TypeError:
                        res = self._client.write_coil(address, value, unit=target_slave)
                
                if getattr(res, "isError", lambda: True)(): return False
                return True
            except Exception as e:
                _LOGGER.error(f"Fehler beim Schreiben (Coil {address}): {e}")
                self._client.close()
                return False
