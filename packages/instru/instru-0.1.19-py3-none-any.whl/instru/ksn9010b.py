"""
Refer to Keysight X-Series Signal Analyzer: SCPI Language Compatibility Mode User's & Programmer's Reference
Page 321, 717
"""
from qcodes.instrument.ip import IPInstrument
import qcodes.utils.validators as vals


class Ksn9010b(IPInstrument):
    def __init__(self, address=None, port=5025, **kwargs):
        super().__init__('Ksn9010b', address, port, timeout=5, terminator='\n', persistent=False,
                         write_confirmation=True, **kwargs)
        self.add_parameter('marker_x',
                           get_cmd='CALCulate:MARKer:X?',
                           get_parser=float)

        self.add_parameter('marker_y',
                           get_cmd='CALCulate:MARKer:Y?',
                           get_parser=float)


if __name__ == '__main__':
    sa = Ksn9010b(address='192.168.153.100')
    print(f'Current maker frequency is {sa.marker_x.get()}')
    print(f'Current maker frequency is {sa.marker_y.get()}')

