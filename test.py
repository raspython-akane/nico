#! python3

# Filename: m_004_logic analyzer_test
__author__ = "raspython"
__date__ = '2020/06/21 10:43'


import RPi.GPIO as GPIO
from time import sleep

f = [261, 293, 329, 349]

buz = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(buz, GPIO.OUT)
pwm = GPIO.PWM(buz, 1000)
pwm.start(50)

for i in f:
    print(i)
    pwm.ChangeFrequency(i)
    sleep(5)


pwm.stop()
GPIO.cleanup()