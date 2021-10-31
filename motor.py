import RPi.GPIO as gpio
import time


class Motor:
    def __init__(self, forward_pin, backward_pin, gpio):
        self.forwardPin = forward_pin
        self.backwardPin = backward_pin
        self.gpio = gpio
        self.gpio.setup(self.forwardPin, self.gpio.OUT, initial=self.gpio.LOW)
        self.gpio.setup(self.backwardPin, self.gpio.OUT, initial=self.gpio.LOW)
        print('모터 설정됨 : ', forward_pin, '번, ', backward_pin, '번.')

    def go_forward(self):
        self.gpio.output(self.forwardPin, self.gpio.LOW)
        self.gpio.output(self.backwardPin, self.gpio.HIGH)

    def go_backward(self):
        self.gpio.output(self.backwardPin, self.gpio.LOW)
        self.gpio.output(self.forwardPin, self.gpio.HIGH)

    def stop(self):
        self.gpio.output(self.forwardPin, self.gpio.LOW)
        self.gpio.output(self.backwardPin, self.gpio.LOW)


class MotorControl:
    def __init__(self, left_pins, right_pins, vacc_pins, gpio):
        self.leftMotor = Motor(left_pins[0], left_pins[1], gpio)
        self.rightMotor = Motor(right_pins[0], right_pins[1], gpio)
        self.vaccMotor = Motor(vacc_pins[0], vacc_pins[1], gpio)
        self.gpio = gpio
        print('좌측모터, 우측모터, 흡입모터 설정됨')

    def go_ahead(self):
        self.leftMotor.go_forward()
        self.rightMotor.go_forward()

    def go_back(self):
        self.leftMotor.go_backward()
        self.rightMotor.go_backward()

    def turn_left(self):
        self.rightMotor.go_backward()
        self.leftMotor.go_forward()
        time.sleep(0.5)
        self.rightMotor.stop()
        self.leftMotor.stop()
        time.sleep(0.2)

    def turn_right(self):
        self.rightMotor.go_forward()
        self.leftMotor.go_backward()
        time.sleep(0.5)
        self.rightMotor.stop()
        self.leftMotor.stop()
        time.sleep(0.2)

    def move_right(self):
        self.leftMotor.go_backward()
        self.rightMotor.go_forward()
        time.sleep(0.225)

        self.leftMotor.go_backward()
        self.rightMotor.go_backward()
        time.sleep(0.6)

        self.leftMotor.go_forward()
        self.rightMotor.go_backward()
        time.sleep(0.225)

        self.leftMotor.stop()
        self.rightMotor.stop()

    def move_left(self):
        self.rightMotor.go_backward()
        self.leftMotor.go_forward()
        time.sleep(0.225)

        self.leftMotor.go_backward()
        self.rightMotor.go_backward()
        time.sleep(0.6)

        self.rightMotor.go_forward()
        self.leftMotor.go_backward()
        time.sleep(0.225)

        self.leftMotor.stop()
        self.rightMotor.stop()

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()

    def start_vacc(self):
        self.vaccMotor.go_forward()

    def stop_vacc(self):
        self.vacc_motor_stop()

    def vacc_motor_run(self):
        self.vaccMotor.go_backward()

    def vacc_motor_stop(self):
        self.vaccMotor.stop()
