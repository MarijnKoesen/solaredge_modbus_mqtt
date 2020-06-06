import math
import enum

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.register_read_message import ReadHoldingRegistersResponse


RETRIES = 3
TIMEOUT = 1
UNIT = 1


class inverterDID(enum.Enum):
    SINGLE_PHASE = 101
    SPLIT_PHASE = 102
    THREE_PHASE = 103


class inverterStatus(enum.Enum):
    I_STATUS_OFF = 1
    I_STATUS_SLEEPING = 2
    I_STATUS_STARTING = 3
    I_STATUS_MPPT = 4
    I_STATUS_THROTTLED = 5
    I_STATUS_SHUTTING_DOWN = 6
    I_STATUS_FAULT = 7
    I_STATUS_STANDBY = 8


class connectionType(enum.Enum):
    RTU = 1
    TCP = 2


class registerType(enum.Enum):
    INPUT = 1
    HOLDING = 2


class registerDataType(enum.Enum):
    BITS = 1
    UINT8 = 2
    UINT16 = 3
    UINT32 = 4
    UINT64 = 5
    INT8 = 6
    INT16 = 7
    INT32 = 8
    INT64 = 9
    FLOAT16 = 10
    FLOAT32 = 11
    STRING = 12


sunspec_notimplemented = {
    "UINT16": 0xffff,
    "ACC16": 0x0000,
    "UINT32": 0xffffffff,
    "ACC32": 0x00000000,
    "UINT64": 0xffffffffffffffff,
    "ACC64": 0x0000000000000000,
    "INT16": 0x8000,
    "SCALE": 0x8000,
    "INT32": 0x80000000,
    "INT64": 0x8000000000000000,
    "FLOAT": 0x7fc00000,
    "STRING": "\x00"
}

c_sunspec_did_map = {
    "101": "Single Phase",
    "102": "Split Phase",
    "103": "Three Phase"
}

inverter_status_map = [
    "Undefined",
    "Off",
    "Sleeping",
    "Grid Monitoring",
    "Producing",
    "Producing (Throttled)",
    "Shutting Down",
    "Fault",
    "Standby"
]


class MyInverter:

    model = "SolarEdge"
    stopbits = 1
    parity = "N"
    baud = 115200

    registers = (
        ("c_model", 40020, 16, registerType.HOLDING, registerDataType.STRING, str, "Model", ""),
        ("c_version", 40044, 8, registerType.HOLDING, registerDataType.STRING, str, "Version", ""),
        ("c_serialnumber", 40052, 16, registerType.HOLDING, registerDataType.STRING, str, "Serial", ""),
        ("c_deviceaddress", 40068, 1, registerType.HOLDING, registerDataType.UINT16, int, "Modbus ID", ""),
        ("c_sunspec_did", 40069, 1, registerType.HOLDING, registerDataType.UINT16, int, "SunSpec DID", c_sunspec_did_map),
        ("current", 40071, 1, registerType.HOLDING, registerDataType.UINT16, int, "Current", "A"),
        ("p1_current", 40072, 1, registerType.HOLDING, registerDataType.UINT16, int, "P1 Current", "A"),
        ("p2_current", 40073, 1, registerType.HOLDING, registerDataType.UINT16, int, "P2 Current", "A"),
        ("p3_current", 40074, 1, registerType.HOLDING, registerDataType.UINT16, int, "P3 Current", "A"),
        ("current_scale", 40075, 1, registerType.HOLDING, registerDataType.INT16, int, "Current Scale Factor", ""),
        ("p1_voltage", 40076, 1, registerType.HOLDING, registerDataType.UINT16, int, "P1 Voltage", "V"),
        ("p2_voltage", 40077, 1, registerType.HOLDING, registerDataType.UINT16, int, "P2 Voltage", "V"),
        ("p3_voltage", 40078, 1, registerType.HOLDING, registerDataType.UINT16, int, "P3 Voltage", "V"),
        ("p1n_voltage", 40079, 1, registerType.HOLDING, registerDataType.UINT16, int, "P1-N Voltage", "V"),
        ("p2n_voltage", 40080, 1, registerType.HOLDING, registerDataType.UINT16, int, "P2-N Voltage", "V"),
        ("p3n_voltage", 40081, 1, registerType.HOLDING, registerDataType.UINT16, int, "P3-N Voltage", "V"),
        ("voltage_scale", 40082, 1, registerType.HOLDING, registerDataType.INT16, int, "Voltage Scale Factor", ""),
        ("power_ac", 40083, 1, registerType.HOLDING, registerDataType.INT16, int, "Power", "W"),
        ("power_ac_scale", 40084, 1, registerType.HOLDING, registerDataType.INT16, int, "Power Scale Factor", ""),
        ("frequency", 40085, 1, registerType.HOLDING, registerDataType.UINT16, int, "Frequency", "Hz"),
        ("frequency_scale", 40086, 1, registerType.HOLDING, registerDataType.INT16, int, "Frequency Scale Factor", ""),
        ("power_apparent", 40087, 1, registerType.HOLDING, registerDataType.INT16, int, "Power (Apparent)", "VA"),
        ("power_apparent_scale", 40088, 1, registerType.HOLDING, registerDataType.INT16, int, "Power (Apparent) Scale Factor", ""),
        ("power_reactive", 40089, 1, registerType.HOLDING, registerDataType.INT16, int, "Power (Reactive)", "VA"),
        ("power_reactive_scale", 40090, 1, registerType.HOLDING, registerDataType.INT16, int, "Power (Reactive) Scale Factor", ""),
        ("power_factor", 40091, 1, registerType.HOLDING, registerDataType.INT16, int, "Power Factor", "%"),
        ("power_factor_scale", 40092, 1, registerType.HOLDING, registerDataType.INT16, int, "Power Factor Scale Factor", ""),
        ("energy_total", 40093, 2, registerType.HOLDING, registerDataType.UINT32, int, "Total Energy", "Wh"),
        ("energy_total_scale", 40095, 1, registerType.HOLDING, registerDataType.UINT16, int, "Total Energy Scale Factor", ""),
        ("current_dc", 40096, 1, registerType.HOLDING, registerDataType.UINT16, int, "DC Current", "A"),
        ("current_dc_scale", 40097, 1, registerType.HOLDING, registerDataType.INT16, int, "DC Current Scale Factor", ""),
        ("voltage_dc", 40098, 1, registerType.HOLDING, registerDataType.UINT16, int, "DC Voltage", "V"),
        ("voltage_dc_scale", 40099, 1, registerType.HOLDING, registerDataType.INT16, int, "DC Voltage Scale Factor", ""),
        ("power_dc", 40100, 1, registerType.HOLDING, registerDataType.INT16, int, "DC Power", "W"),
        ("power_dc_scale", 40101, 1, registerType.HOLDING, registerDataType.INT16, int, "DC Power Scale Factor", ""),
        ("temperature", 40103, 1, registerType.HOLDING, registerDataType.INT16, int, "Temperature", "°C"),
        ("temperature_scale", 40106, 1, registerType.HOLDING, registerDataType.INT16, int, "Temperature Scale Factor", ""),
        ("status", 40107, 1, registerType.HOLDING, registerDataType.UINT16, int, "Status", inverter_status_map),
        ("vendor_status", 40108, 1, registerType.HOLDING, registerDataType.UINT16, int, "Vendor Status", ""),
    )

    def __init__(
        self, host=False, port=False,
        device=False, stopbits=False, parity=False, baud=False,
        timeout=TIMEOUT, retries=RETRIES, unit=UNIT
    ):
        self.host = host
        self.port = port
        self.device = device

        self.firstRegister = self.registers[0][1]
        self.registerLength = (self.registers[-1][1]+self.registers[-1][2]) - self.registers[0][1]

        if stopbits:
            self.stopbits = stopbits

        if parity:
            self.parity = parity

        if baud:
            self.baud = baud

        self.timeout = timeout
        self.retries = retries
        self.unit = unit

        if device:
            self.mode = connectionType.RTU
            self.client = ModbusSerialClient(
                method="rtu",
                port=self.device,
                stopbits=self.stopbits,
                parity=self.parity,
                baudrate=self.baud,
                timeout=self.timeout)
        else:
            self.mode = connectionType.TCP
            self.client = ModbusTcpClient(
                host=self.host,
                port=self.port,
                timeout=self.timeout
            )

    def __repr__(self):
        if self.mode == connectionType.RTU:
            return f"{self.model}({self.device}, {self.mode}: stopbits={self.stopbits}, parity={self.parity}, baud={self.baud}, timeout={self.timeout}, unit={hex(self.unit)})"
        elif self.mode == connectionType.TCP:
            return f"{self.model}({self.host}:{self.port}, {self.mode}: timeout={self.timeout}, unit={hex(self.unit)})"
        else:
            return f"<{self.__class__.__module__}.{self.__class__.__name__} object at {hex(id(self))}>"

    def _read_holding_registers(self, address, length):
        for i in range(self.retries):
            result = self.client.read_holding_registers(address=address, count=length, unit=self.unit)

            if isinstance(result, ReadHoldingRegistersResponse):
                return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)

        return None

    def _decode_value(self, data, length, dtype, vtype):
        try:
            if dtype == registerDataType.UINT16:
                decoded = data.decode_16bit_uint()
            elif dtype == registerDataType.UINT32:
                decoded = data.decode_32bit_uint()
            elif dtype == registerDataType.INT16:
                decoded = data.decode_16bit_int()
            elif dtype == registerDataType.STRING:
                decoded = data.decode_string(length * 2).decode("utf-8").replace("\x00", "")
            else:
                raise NotImplementedError(dtype)

            if decoded == sunspec_notimplemented[dtype.name]:
                return False
            else:
                return vtype(decoded)
        except NotImplementedError:
            raise

    def connected(self):
        return bool(self.client.connect())

    def read(self):
        rawData = self._read_holding_registers(self.firstRegister, self.registerLength)
        data = {}

        offset = self.firstRegister
        for register in self.registers:
            name, address, length, rtype, dtype, vtype, label, fmt = register

            if (address > offset):
                bytesToSkip = address - offset
                offset += bytesToSkip
                rawData.skip_bytes(bytesToSkip*2)

            data[name] = self._decode_value(rawData, length, dtype, vtype)
            offset += length

        return data


class SolarData:

    fields = {
            'model': {'field': 'c_model'},
            'version': {'field': 'c_version'},
            'serialnumber': {'field': 'c_serialnumber'},
            'deviceaddress': {'field': 'c_deviceaddress'},
            'sunspec_did': {'field': 'c_sunspec_did'},

            'status': {},
            'vendor_status': {},

            'current': {'scaleField': 'current_scale', 'unit': 'A'},
            'p1_current': {'scaleField': 'current_scale', 'unit': 'A'},
            'p2_current': {'scaleField': 'current_scale', 'unit': 'A'},
            'p3_current': {'scaleField': 'current_scale', 'unit': 'A'},

            'p1_voltage': {'scaleField': 'voltage_scale', 'unit': 'V'},
            'p2_voltage': {'scaleField': 'voltage_scale', 'unit': 'V'},
            'p3_voltage': {'scaleField': 'voltage_scale', 'unit': 'V'},
            'p1n_voltage': {'scaleField': 'voltage_scale', 'unit': 'V'},
            'p2n_voltage': {'scaleField': 'voltage_scale', 'unit': 'V'},
            'p3n_voltage': {'scaleField': 'voltage_scale', 'unit': 'V'},

            'power_ac': {'scaleField': 'power_ac_scale', 'unit': 'W'},
            'frequency': {'scaleField': 'frequency_scale', 'unit': 'Hz'},
            'power_apparent': {'scaleField': 'power_apparent_scale', 'unit': 'W'},
            'power_reactive': {'scaleField': 'power_reactive_scale', 'unit': 'W'},
            'power_factor': {'scaleField': 'power_factor_scale', 'unit': '%'},
            'energy_total': {'scaleField': 'energy_total_scale', 'unit': 'Wh'},
            'current_dc': {'scaleField': 'current_dc_scale', 'unit': 'A'},
            'voltage_dc': {'scaleField': 'voltage_dc_scale', 'unit': 'V'},
            'power_dc': {'scaleField': 'power_dc_scale', 'unit': 'W'},
            'temperature': {'scaleField': 'temperature_scale', 'unit': '°C'},
    } 

    def __init__(self, data):
        self.rawData = data
        self.data = self._parseData(data)

    def _parseData(self, data):
        result = {}

        for fieldName, config in self.fields.items():
            dataField = config['field'] if 'field' in config else fieldName
            if dataField not in data:
                continue

            value = data[config['field']] if 'field' in config else data[fieldName]

            if 'scaleField' in config:
                value = value * math.pow(10, data[config['scaleField']])

            result[fieldName] = value

        return result

    def getModel(self):
        return self.data['model']