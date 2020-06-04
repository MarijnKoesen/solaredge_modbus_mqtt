import math

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
            value = data[config['field']] if 'field' in config else data[fieldName]

            if 'scaleField' in config:
                value = value * math.pow(10, data[config['scaleField']])

            result[fieldName] = value

        return result

    def getModel(self):
        return self.data['model']