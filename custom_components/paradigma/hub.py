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

    def read_input_registers(self, address, count):
        """Read Input Registers (0x04)."""
        with self._lock:
            try:
                # Priorität: device_id (Neu) -> slave (Mittel) -> unit (Alt)
                try:
                    res = self._client.read_input_registers(address=address, count=count, device_id=self._slave_id)
                except TypeError:
                    try:
                        res = self._client.read_input_registers(address, count, slave=self._slave_id)
                    except TypeError:
                        res = self._client.read_input_registers(address, count, unit=self._slave_id)
                
                if res.isError():
                    _LOGGER.debug(f"Modbus Fehler Lesen Input {address}: {res}")
                    return None
                return res.registers
            except Exception as e:
                _LOGGER.error(f"Exception Lesen Input {address}: {e}")
                return None

    def read_holding_registers(self, address, count):
        """Read Holding Registers (0x03)."""
        with self._lock:
            try:
                try:
                    res = self._client.read_holding_registers(address=address, count=count, device_id=self._slave_id)
                except TypeError:
                    try:
                        res = self._client.read_holding_registers(address, count, slave=self._slave_id)
                    except TypeError:
                        res = self._client.read_holding_registers(address, count, unit=self._slave_id)

                if res.isError():
                    _LOGGER.debug(f"Modbus Fehler Lesen Holding {address}: {res}")
                    return None
                return res.registers
            except Exception as e:
                _LOGGER.error(f"Exception Lesen Holding {address}: {e}")
                return None

    def write_register(self, address, value):
        """Write Single Register."""
        with self._lock:
            try:
                try:
                    res = self._client.write_register(address, value, device_id=self._slave_id)
                except TypeError:
                    try:
                        res = self._client.write_register(address, value, slave=self._slave_id)
                    except TypeError:
                        res = self._client.write_register(address, value, unit=self._slave_id)
                return not res.isError()
            except Exception:
                return False

    def read_coils(self, address, count):
        """Read Coils (0x01)."""
        with self._lock:
            try:
                try:
                    res = self._client.read_coils(address=address, count=count, device_id=self._slave_id)
                except TypeError:
                    try:
                        res = self._client.read_coils(address, count, slave=self._slave_id)
                    except TypeError:
                        res = self._client.read_coils(address, count, unit=self._slave_id)
                
                if res.isError(): return None
                return res.bits
            except Exception:
                return None

    def write_coil(self, address, value):
        """Write Single Coil (0x05)."""
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