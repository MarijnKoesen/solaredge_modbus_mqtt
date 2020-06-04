import unittest
from . import SolarData

class TestStringMethods(unittest.TestCase):
    def testParse(self):
        solarData = SolarData({
            'c_model': 'SE7K-ABCDEFGH4', 
            'c_version': '0004.0008.0028', 
            'c_serialnumber': '7F51B342', 
            'c_deviceaddress': 1, 
            'c_sunspec_did': 103, 
            'current': 301, 
            'p1_current': 99, 
            'p2_current': 102, 
            'p3_current': 100, 
            'current_scale': -2, 
            'p1_voltage': 4056, 
            'p2_voltage': 4066, 
            'p3_voltage': 4075, 
            'p1n_voltage': 2346, 
            'p2n_voltage': 2342, 
            'p3n_voltage': 2351, 
            'voltage_scale': -1, 
            'power_ac': 5970, 
            'power_ac_scale': -1, 
            'frequency': 4997, 
            'frequency_scale': -2, 
            'power_apparent': 7133, 
            'power_apparent_scale': -1, 
            'power_reactive': -3890, 
            'power_reactive_scale': -1, 
            'power_factor': -8376, 
            'power_factor_scale': -2, 
            'energy_total': 788428, 
            'energy_total_scale': 0, 
            'current_dc': 8126, 
            'current_dc_scale': -4, 
            'voltage_dc': 7471, 
            'voltage_dc_scale': -1, 
            'power_dc': 6071, 
            'power_dc_scale': -1, 
            'temperature': 4717, 
            'temperature_scale': -2, 
            'status': 4, 
            'vendor_status': 0
        })

        self.assertEqual('SE7K-ABCDEFGH4', solarData.data['model'])
        self.assertEqual('0004.0008.0028', solarData.data['version'])
        self.assertEqual('7F51B342', solarData.data['serialnumber'])
        self.assertEqual(1, solarData.data['deviceaddress'])
        self.assertEqual(103, solarData.data['sunspec_did'])

        self.assertAlmostEqual(3.01, solarData.data['current'])
        self.assertAlmostEqual(0.99, solarData.data['p1_current'])
        self.assertAlmostEqual(1.02, solarData.data['p2_current'])
        self.assertAlmostEqual(1.0, solarData.data['p3_current'])

        self.assertAlmostEqual(405.6, solarData.data['p1_voltage'])
        self.assertAlmostEqual(406.6, solarData.data['p2_voltage'])
        self.assertAlmostEqual(407.5, solarData.data['p3_voltage'])
        self.assertAlmostEqual(234.6, solarData.data['p1n_voltage'])
        self.assertAlmostEqual(234.2, solarData.data['p2n_voltage'])
        self.assertAlmostEqual(235.1, solarData.data['p3n_voltage'])

        self.assertAlmostEqual(597.0, solarData.data['power_ac'])
        self.assertAlmostEqual(49.97, solarData.data['frequency'])
        self.assertAlmostEqual(713.3, solarData.data['power_apparent'])
        self.assertAlmostEqual(-389.0, solarData.data['power_reactive'])
        self.assertAlmostEqual(-83.76, solarData.data['power_factor'])
        self.assertAlmostEqual(788428, solarData.data['energy_total'])

        self.assertAlmostEqual(0.8126, solarData.data['current_dc'])
        self.assertAlmostEqual(747.1, solarData.data['voltage_dc'])
        self.assertAlmostEqual(607.1, solarData.data['power_dc'])
        self.assertAlmostEqual(47.17, solarData.data['temperature'])
        self.assertAlmostEqual(4, solarData.data['status'])
        self.assertAlmostEqual(0, solarData.data['vendor_status'])

if __name__ == '__main__':
    unittest.main()