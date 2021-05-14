#!/usr/bin/env python3

# Filename: tmp_test 
__author__ = "raspython"
__date__ = '2021/04/25 14:08'

import RPi.GPIO as GPIO
import dht11

# GPIO用意
GPIO.setmode(GPIO.BCM)

# PINナンバーを与えてライブラリーから呼び出し
instance = dht11.DHT11(pin = 21)
result = instance.read()
print(result.temperature, result.humidity)

if result.is_valid():
    print("Temperature: %-3.1f C" % result.temperature)
    print("Humidity: %-3.1f %%" % result.humidity)
else:
    print("Error: %d" % result.error_code)

GPIO.cleanup()




def main():
    pass


if __name__ == '__main__':
    main()
