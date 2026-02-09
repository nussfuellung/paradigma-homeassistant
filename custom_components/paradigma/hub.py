"""Paradigma Modbus Hub."""
import logging
import threading
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

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
                # WICHTIG: Dein System verlangt 'device_id' statt 'slave' oder 'unit'
                result = self._client.read_input_registers(address, count=count, device_id=self._slave_id)
                if result.isError():
                    _LOGGER.error("Fehler beim Lesen (Input %s): %s", address, result)
                    return None
                return result.registers
            except TypeError:
                # Fallback für ältere Pymodbus Versionen (falls sich was ändert)
                try:
                    result = self._client.read_input_registers(address, count, slave=self._slave_id)
                    if not result.isError(): return result.registers
                except TypeError:
                    result = self._client.read_input_registers(address, count, unit=self._slave_id)
                    if not result.isError(): return result.registers
                return None
            except ModbusException as exc:
                _LOGGER.error("Modbus Exception (Input): %s", exc)
                return None

    def read_holding_registers(self, address, count):
        """Read Holding Registers (0x03)."""
        with self._lock:
            try:
                result = self._client.read_holding_registers(address, count=count, device_id=self._slave_id)
                if result.isError():
                    _LOGGER.error("Fehler beim Lesen (Holding %s): %s", address, result)
                    return None
                return result.registers
            except TypeError:
                # Fallback
                try:
                    result = self._client.read_holding_registers(address, count, slave=self._slave_id)
                    if not result.isError(): return result.registers
                except TypeError:
                    result = self._client.read_holding_registers(address, count, unit=self._slave_id)
                    if not result.isError(): return result.registers
                return None
            except ModbusException as exc:
                _LOGGER.error("Modbus Exception (Holding): %s", exc)
                return None

    def write_register(self, address, value):
        """Write Single Register."""
        with self._lock:
            try:
                builder = self._client.write_register(address, value, device_id=self._slave_id)
                return not builder.isError()
            except TypeError:
                # Fallback
                try:
                    builder = self._client.write_register(address, value, slave=self._slave_id)
                    return not builder.isError()
                except TypeError:
                    builder = self._client.write_register(address, value, unit=self._slave_id)
                    return not builder.isError()
            except Exception as exc:
                _LOGGER.error("Fehler beim Schreiben: %s", exc)
                return False

    def read_coils(self, address, count):
        """Read Coils (0x01)."""
        with self._lock:
            try:
                result = self._client.read_coils(address, count=count, device_id=self._slave_id)
                if result.isError():
                    return None
                return result.bits
            except TypeError:
                # Fallback
                try:
                    result = self._client.read_coils(address, count, slave=self._slave_id)
                    if not result.isError(): return result.bits
                except TypeError:
                    result = self._client.read_coils(address, count, unit=self._slave_id)
                    if not result.isError(): return result.bits
                return None
            except Exception:
                return None

    def write_coil(self, address, value):
        """Write Single Coil (0x05)."""
        with self._lock:
            try:
                self._client.write_coil(address, value, device_id=self._slave_id)
                return True
            except TypeError:
                # Fallback
                try:
                    self._client.write_coil(address, value, slave=self._slave_id)
                    return True
                except TypeError:
                    self._client.write_coil(address, value, unit=self._slave_id)
                    return True
            except Exception:
                return False