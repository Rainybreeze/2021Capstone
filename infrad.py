import os
import threading

import spidev


class Infrad(threading.Thread):
    def __init__(self):
        super().__init__()
        os.system('chmod og+rwx /dev/gpio*')

        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 1350000

        self.leftdata = 0
        self.middledata = 0
        self.rightdate = 0

    def run(self):
        while True:
            self.leftdata = self.analog_read(0)
            self.middledata = self.analog_read(1)
            self.rightdate = self.analog_read(2)

    def get_data(self, channel, returnvolts):
        if returnvolts:
            if channel == 0:
                return self.data_to_voltage(self.leftdata)
            elif channel == 1:
                return self.data_to_voltage(self.middledata)
            elif channel == 2:
                return self.data_to_voltage(self.rightdate)
            else:
                return 0
        else:
            if channel == 0:
                return self.leftdata
            elif channel == 1:
                return self.middledata
            elif channel == 2:
                return self.rightdate
            else:
                return 0

    def analog_read(channel):
        r = spi.xfer2([1, (8 + channel) << 4, 0])
        adc_out = ((r[1] & 3) << 8) + r[2]
        return adc_out

    def data_to_voltage(self, data):
        reading = data
        voltage = reading * 3.3 / 1024
        # print("Reading = %d \t voltage = %f" % (reading, voltage))
        return voltage


