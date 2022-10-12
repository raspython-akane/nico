#!/usr/bin/env python3

# Filename: m_30AI_flash 
__author__ = "raspython"
__date__ = '2022/10/12 19:30'


# GPIO13番PINを1秒ごとにONとOFFを10回繰り返す。
# 最後にGPIOのクリーンアップをする。

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)

for i in range(10):
    GPIO.output(13, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(13, GPIO.LOW)
    time.sleep(1)

GPIO.cleanup()