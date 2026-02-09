"""Paradigma Modbus Hub."""
import logging
import threading
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

_LOGGER = logging.getLogger(__name__)

class ParadigmaHub:
    def __init__(self, hass, name, host, port, slave_id):
        self._hass = hass
        self._client = ModbusTcpClient(host=host, port=port)
        self._slave_id = slave_id
        self._lock = threading.Lock()
        self.name = name

    def connect(self):
        with self._lock:
            return self._client.connect()

    def close(self):
        with self._lock:
            self._client.close()

    def _read_input_registers_safe(self, address, count):
        """Helper to try both 'slave' and 'unit' arguments."""
        try:
            return self._client.read_input_registers(address, count, slave=self._slave_id)
        except TypeError:
            return self._client.read_input_registers(address, count, unit=self._slave_id)

    def _read_holding_registers_safe(self, address, count):
        """Helper to try both 'slave' and 'unit' arguments."""
        try:
            return self._client.read_holding_registers(address, count, slave=self._slave_id)
        except TypeError:
            return self._client.read_holding_registers(address, count, unit=self._slave_id)

    def _write_register_safe(self, address, value):
        """Helper to try both 'slave' and 'unit' arguments."""
        try:
            return self._client.write_register(address, value, slave=self._slave_id)
        except TypeError:
            return self._client.write_register(address, value, unit=self._slave_id)

    def _read_coils_safe(self, address, count):
        """Helper to try both 'slave' and 'unit' arguments."""
        try:
            return self._client.read_coils(address, count, slave=self._slave_id)
        except TypeError:
            return self._client.read_coils(address, count, unit=self._slave_id)

    def _write_coil_safe(self, address, value):
        """Helper to try both 'slave' and 'unit' arguments."""
        try:
            return self._client.write_coil(address, value, slave=self._slave_id)
        except TypeError:
            return self._client.write_coil(address, value, unit=self._slave_id)

    def read_input_registers(self, address, count):
        """Read Input Registers (Function Code 0x04)."""
        with self._lock:
            try:
                result = self._read_input_registers_safe(address, count)
                if result.isError():
                    _LOGGER.error("Error reading input registers %s: %s", address, result)
                    return None
                return result.registers
            except ModbusException as exc:
                _LOGGER.error("Modbus exception reading inputs: %s", exc)
                return None
            except Exception as exc:
                _LOGGER.error("General exception reading inputs: %s", exc)
                return None

    def read_holding_registers(self, address, count):
        """Read Holding Registers (Function Code 0x03)."""
        with self._lock:
            try:
                result = self._read_holding_registers_safe(address, count)
                if result.isError():
                    _LOGGER.error("Error reading holding registers %s: %s", address, result)
                    return None
                return result.registers
            except ModbusException as exc:
                _LOGGER.error("Modbus exception reading holdings: %s", exc)
                return None
            except Exception as exc:
                _LOGGER.error("General exception reading holdings: %s", exc)
                return None

    def write_register(self, address, value):
        """Write Single Register."""
        with self._lock:
            try:
                builder = self._write_register_safe(address, value)
                return not builder.isError()
            except ModbusException as exc:
                _LOGGER.error("Modbus write register exception: %s", exc)
                return False
            except Exception as exc:
                _LOGGER.error("General exception writing register: %s", exc)
                return False

    def read_coils(self, address, count):
        """Read Coils (Function Code 0x01)."""
        with self._lock:
            try:
                result = self._read_coils_safe(address, count)
                if result.isError():
                    return None
                return result.bits
            except ModbusException:
                return None
            except Exception:
                return None

    def write_coil(self, address, value):
        """Write Single Coil (Function Code 0x05)."""
        with self._lock:
            try:
                self._write_coil_safe(address, value)
                return True
            except ModbusException:
                return False
            except Exception:
                return False