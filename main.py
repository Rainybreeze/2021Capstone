import os
import sys
import time

import RPi.GPIO as GPIO

import lidar
import motor
import ultrasonic
import infrad

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

leftSonic_pin = [3, 2]
rightSonic_pin = [14, 4]

ultrasonic_left = ultrasonic.Ultrasonic(leftSonic_pin[0], leftSonic_pin[1], GPIO)
ultrasonic_right = ultrasonic.Ultrasonic(rightSonic_pin[1], rightSonic_pin[1], GPIO)

infrad_sensor = infrad.Infrad()
try:
    motor_ctl.vacc_motor_run()
    while True:
        # print(ultrasonic_right.get_distance())
        print("동작중")
        time.sleep(1)
except KeyboardInterrupt:
    motor_ctl.stop()
    motor_ctl.vacc_motor_stop()
    print("종료합니다")
    sys.exit()
