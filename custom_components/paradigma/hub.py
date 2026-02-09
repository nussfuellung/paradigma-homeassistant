"""Paradigma Modbus Hub."""
import logging
import threading
from pymodbus.client import ModbusTcpClient

_LOGGER = logging.getLogger(__name__)

class ParadigmaHub:
    def __init__(self, hass, name, host, port, slave_id):
        self._hass = hass
        self._slave_id = int(slave_id)
        self._client = ModbusTcpClient(host=host, port=port)
        self._lock = threading.Lock()
        self.name = name

    def connect(self):
        with self._lock:
            return self._client.connect()

    def close(self):
        with self._lock:
            self._client.close()

    def _read_modbus(self, func_name, address, count):
        """Helper to try device_id, slave, and unit."""
        func = getattr(self._client, func_name)
        with self._lock:
            try:
                try:
                    res = func(address=address, count=count, device_id=self._slave_id)
                except TypeError:
                    try:
                        res = func(address, count, slave=self._slave_id)
                    except TypeError:
                        res = func(address, count, unit=self._slave_id)
                
                if res.isError(): return None
                return res
            except Exception:
                return None

    def read_input_registers(self, address, count):
        res = self._read_modbus("read_input_registers", address, count)
        return res.registers if res else None

    def read_holding_registers(self, address, count):
        res = self._read_modbus("read_holding_registers", address, count)
        return res.registers if res else None

    def read_coils(self, address, count):
        res = self._read_modbus("read_coils", address, count)
        return res.bits if res else None

    def write_register(self, address, value):
        with self._lock:
            try:
                try:
                    self._client.write_register(address, value, device_id=self._slave_id)
                except TypeError:
                    try:
                        self._client.write_register(address, value, slave=self._slave_id)
                    except TypeError:
                        self._client.write_register(address, value, unit=self._slave_id)
                return True
            except Exception:
                return False

    def write_coil(self, address, value):
        with self._lock:
            try:
                try:
                    self._client.write_coil(address, value, device_id=self._slave_id)
                except TypeError:
                    try:
                        self._client.write_coil(address, value, slave=self._slave_id)
                    except TypeError:
                        self._client.write_coil(address, value, unit=self._slave_id)
                return True
            except Exception:
                return False