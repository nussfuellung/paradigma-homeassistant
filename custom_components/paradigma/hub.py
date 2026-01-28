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

    def read_input_registers(self, address, count):
        """Read Input Registers (Function Code 0x04)."""
        with self._lock:
            try:
                # PDF Seite 10: Input Registers 30xxx. Pymodbus nutzt 0-basierten Index.
                # Adresse im Code ist der Offset zu 30001[cite: 196].
                result = self._client.read_input_registers(address, count, slave=self._slave_id)
                if result.isError():
                    return None
                return result.registers
            except ModbusException:
                return None

    def read_holding_registers(self, address, count):
        """Read Holding Registers (Function Code 0x03)."""
        with self._lock:
            try:
                # PDF Seite 10: Holding Registers 40xxx.
                # Adresse im Code ist der Offset zu 40001[cite: 205].
                result = self._client.read_holding_registers(address, count, slave=self._slave_id)
                if result.isError():
                    return None
                return result.registers
            except ModbusException:
                return None

    def write_register(self, address, value):
        """Write Single Register."""
        with self._lock:
            try:
                builder = self._client.write_register(address, value, slave=self._slave_id)
                return not builder.isError()
            except ModbusException:
                return False

    def read_coils(self, address, count):
        """Read Coils (Function Code 0x01)."""
        with self._lock:
            try:
                result = self._client.read_coils(address, count, slave=self._slave_id)
                if result.isError():
                    return None
                return result.bits
            except ModbusException:
                return None

    def write_coil(self, address, value):
        """Write Single Coil (Function Code 0x05)."""
        with self._lock:
            try:
                self._client.write_coil(address, value, slave=self._slave_id)
                return True
            except ModbusException:
                return False