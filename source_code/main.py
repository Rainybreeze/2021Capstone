import os
import sys
import time

import RPi.GPIO as GPIO

import lidar
import motor
import ultrasonic
import infrad


# functions
def show_ultrasonic_data():
    if ultrasonic_left.get_distance() != 0:
        print("left : ", ultrasonic_left.get_distance())
    if ultrasonic_right.get_distance() != 0:
        print("right : ", ultrasonic_right.get_distance())


def show_adc_data():
    print('left : %.3f' % infrad_sensor.get_data(0, True), end=', ')
    print('mid : %.3f' % infrad_sensor.get_data(1, True), end=', ')
    print('right : %.3f' % infrad_sensor.get_data(2, True))


def detect_falling():
    if ultrasonic_left.get_distance() >= 10 or ultrasonic_right.get_distance() >= 10:
        print("fallen")
        motor_ctl.stop()
        motor_ctl.go_block_back()


def detect_wall(is_left):
    if infrad_sensor.get_data(1, True) > 1.5:
        motor_ctl.stop()
        time.sleep(0.5)
        left = infrad_sensor.get_data(0, True)
        right = infrad_sensor.get_data(2, True)
        print('front wall available', left, right)
        if left > 1.7:
            is_left = False
        if right > 1.7:
            if not is_left:
                motor_ctl.go_block_back()
        if is_left:
            print('turn left')
            motor_ctl.turn_left()
            motor_ctl.go_block()
            motor_ctl.go_block()
            motor_ctl.turn_left()
            return False
        else:
            print('turn right')
            motor_ctl.turn_right()
            motor_ctl.go_block()
            motor_ctl.go_block()
            motor_ctl.turn_right()
            return True


def sys_exit():
    motor_ctl.stop()
    motor_ctl.vacc_motor_stop()
    ultrasonic_right.stop()
    ultrasonic_left.stop()
    infrad_sensor.stop()
    print("종료합니다")
    sys.exit()


# main code
running_flag = True
isDebug = False
for arg in sys.argv:
    if arg == '-debug':
        isDebug = True
        print('debug mode')

if os.geteuid() != 0:
    exit("no root permission! plz run with 'sudo'.")

os.system('chmod og+rwx /dev/gpio*')

roscore = lidar.roscore()
lidar_rviz = lidar.roslidar()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

leftMotor_pin = [6, 5]
rightMotor_pin = [12, 13]
vaccMotor_pin = [19, 16]

motor_ctl = motor.MotorControl(leftMotor_pin, rightMotor_pin, vaccMotor_pin, GPIO)

leftSonic_pin = [17, 18]
rightSonic_pin = [27, 22]

ultrasonic_left = ultrasonic.Ultrasonic(leftSonic_pin[0], leftSonic_pin[1], GPIO)
ultrasonic_left.start()
ultrasonic_right = ultrasonic.Ultrasonic(rightSonic_pin[0], rightSonic_pin[1], GPIO)
ultrasonic_right.start()

infrad_sensor = infrad.Infrad()
infrad_sensor.start()

try:
    is_left = False
    # motor_ctl.vacc_motor_run()
    # motor_ctl.turn_left()
    while running_flag:
        motor_ctl.go_block()
        # detect_falling()
        is_left = detect_wall(is_left)
        show_adc_data()
        show_ultrasonic_data()

    sys_exit()
except KeyboardInterrupt:
    sys_exit()
