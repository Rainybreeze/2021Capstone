import os
import threading

import spidev


class Infrad(threading.Thread):
    def __init__(self):
        super().__init__()
        os.system('chmod og+rwx /dev/gpio*')

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 1350000

        self.leftdata = 0
        self.middledata = 0
        self.rightdate = 0
        self.run_flag = True

    def run(self):
        while self.run_flag:
            self.leftdata = self.analog_read(0)
            self.middledata = self.analog_read(1)
            self.rightdate = self.analog_read(2)

    def stop(self):
        self.run_flag = False

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

    def analog_read(self, channel):
        r = self.spi.xfer2([1, (8 + channel) << 4, 0])
        adc_out = ((r[1] & 3) << 8) + r[2]
        return adc_out

    def data_to_voltage(self, data):
        reading = data
        voltage = reading * 3.3 / 1024
        # print("Reading = %d \t voltage = %f" % (reading, voltage))
        return voltage
