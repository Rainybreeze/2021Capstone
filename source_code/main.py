import os
import sys
import time

import RPi.GPIO as GPIO

import lidar
import motor
import ultrasonic
import infrad
import debugTest


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
        motor_ctl.go_block_back()
        falling_block_turn()


def falling_block_turn():
    if infrad_sensor.get_data(0, True) > 1.4:
        print('turn right')
        motor_ctl.turn_right()
        motor_ctl.go_block()
        motor_ctl.go_block()
        motor_ctl.turn_right()
    elif infrad_sensor.get_data(0, True) > 1.4:
        motor_ctl.turn_left()
        motor_ctl.go_block()
        motor_ctl.go_block()
        motor_ctl.turn_left()
    else:
        motor_ctl.stop()
        motor_ctl.go_block_back()
        motor_ctl.go_block_back()
        falling_block_turn()


def detect_wall(is_left):
    if infrad_sensor.get_data(1, True) > 1.4:
        motor_ctl.stop()
        time.sleep(0.5)
        left = infrad_sensor.get_data(0, True)
        right = infrad_sensor.get_data(2, True)
        print('front wall available', left, right)

        if left > 1.4 and right > 1.4:
            falling_block_turn()
        elif left > 1.4:
            is_left = False
        elif right > 1.4:
            is_left = True

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
    GPIO.cleanup()
    print("종료합니다")
    sys.exit()


# main code
running_flag = True
isDebug = False
idle_time = 0
DEFAULT_IDLE_TIME = 43200

len(sys.argv)
for i in range(0, len(sys.argv)):
    if sys.argv[i] == '-debug':
        isDebug = True
        print('debug mode')
    if sys.argv[i] == '-setup-idle-time':
        if sys.argv[i+1] == 'minutes':
            idle_time = (int(sys.argv[i + 2]) * 60)
        elif sys.argv[i+1] == 'hours':
            idle_time = (int(sys.argv[i + 2]) * 60 * 60)


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

leftSonic_pin = [18, 17]
rightSonic_pin = [27, 22]

ultrasonic_left = ultrasonic.Ultrasonic(leftSonic_pin[0], leftSonic_pin[1], GPIO)
ultrasonic_left.start()
ultrasonic_right = ultrasonic.Ultrasonic(rightSonic_pin[0], rightSonic_pin[1], GPIO)
ultrasonic_right.start()

infrad_sensor = infrad.Infrad()
infrad_sensor.start()

if isDebug:
    leftUltrasonic_test = debugTest.UltrasonicTest(GPIO, ultrasonic_left, direction='left')
    rightUltrasonic_test = debugTest.UltrasonicTest(GPIO, ultrasonic_right, direction='right')
    infrad_test = debugTest.InfradTest(GPIO, infrad_sensor)

try:
    print(idle_time)
    if isDebug:
        while True:
            leftUltrasonic_test.get_data()
            rightUltrasonic_test.get_data()
            infrad_test.get_data()
            time.sleep(1)

    is_left = False
    print('none debug mode')
    motor_ctl.vacc_motor_run()
    time.sleep(0.5)
    motor_ctl.vacc_motor_stop()
    # motor_ctl.turn_left()
    motor_ctl.go_block()
    time.sleep(0.5)
    motor_ctl.go_block_back()
    time.sleep(0.5)
    while True:
        while running_flag:
            show_adc_data()
            time.sleep(1)
            '''
            motor_ctl.go_block()
            # detect_falling()
            is_left = detect_wall(is_left)
            show_adc_data()
            show_ultrasonic_data()
            '''
        while not running_flag:
            time.sleep(500)
except KeyboardInterrupt:
    sys_exit()
