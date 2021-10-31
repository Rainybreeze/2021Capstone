import RPi.GPIO as gpio
import sys, os, time

os.system('chmod og+rwx /dev/gpio*')

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

forwardPin2 = 6
backwardPin2 = 5
forwardPin = 12
backwardPin = 13
gpio.setup(forwardPin, gpio.OUT, initial = gpio.LOW)
gpio.setup(backwardPin, gpio.OUT, initial = gpio.LOW)
gpio.setup(forwardPin2, gpio.OUT, initial = gpio.LOW)
gpio.setup(backwardPin2, gpio.OUT, initial = gpio.LOW)
