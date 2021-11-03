import threading
import time


class Ultrasonic(threading.Thread):
    def __init__(self, pin_trig, pin_echo, gpio):
        super().__init__()
        self.trigPin = pin_trig
        self.echoPin = pin_echo
        self.gpio = gpio
        self.distance = 0
        self.run_flag = True
        self.gpio.setmode(gpio.BCM)
        gpio.setup(self.trigPin, gpio.OUT, initial=gpio.LOW)
        gpio.setup(self.echoPin, gpio.IN)
        print('초음파 센서 설정됨, 트리거 : ', self.trigPin, ', 에코 : ', self.echoPin)

    def get_distance(self):
        return self.distance

    def read_start(self):
        stop = 0
        start = 0
        while self.run_flag:
            self.gpio.output(self.trigPin, False)
            time.sleep(0.5)

            self.gpio.output(self.trigPin, True)
            time.sleep(0.0001)
            self.gpio.output(self.trigPin, False)

            while self.gpio.input(self.echoPin) == 0:
                start = time.time()

            while self.gpio.input(self.echoPin) == 1:
                stop = time.time()

            time_interval = stop - start
            distance = time_interval * 17000
            distance = round(distance, 2)
            self.distance = distance
            # print("값 : ", self.distance)

    def run(self):
        print("초음파 센서 스레드 실행됨")
        self.read_start()

    def stop(self):
        self.run_flag = False

