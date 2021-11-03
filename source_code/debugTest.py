class UltrasonicTest:
    def __init__(self, gpio, ultrasonic, direction):
        self.ultrasonic = ultrasonic
        self.is_left = None
        if direction == 'left':
            self.is_left = True
        else:
            self.is_left = False

    def get_data(self):
        dir_char = None
        if self.is_left:
            dir_char = 'Ultrasonic_Left :'
        else:
            dir_char = 'Ultrasonic_right :'
        print(dir_char, self.ultrasonic.get_distance())


class InfradTest:
    def __init__(self, gpio, infrad):
        self.infrad = infrad

    def get_data(self):
        print('Infrad Left :', self.infrad.get_data(0, True))
        print('Infrad Midd :', self.infrad.get_data(1, True))
        print('Infrad Rigt :', self.infrad.get_data(2, True))
