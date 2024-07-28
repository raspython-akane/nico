#!/usr/bin/env python3

# Filename: m_022new_raspberrypios_test 
__author__ = "raspython"
__date__ = '2024/07/28 11:35'

import pigpio
import time
import sys


# pinNoを変数に入れる
led_red = 26
led_blue = 19
led_green = 13

# pigpioの初期設定
gpio = pigpio.pi()


def led_flash(R_pin, B_pin, G_pin):
    """
    LEDをPWM制御で徐々に明るくする。
    @param R_pin: LED赤のGPIO PIN No
    @param B_pin: LED青のGPIO PIN No
    @param G_pin: LED緑のGPIO PIN No
    """
    # pin noをリストに入れる
    pin_l = [R_pin, B_pin, G_pin]
    # duty日のリストを作成。要素の若い順から、赤、青、緑
    duty_l = [0, 0, 0]

    for i in range(11):
        for j in range(3):
            #赤から順に0.1秒毎duty比10%づつ挙げて光らせる
            # duty比は0-MAX1,000,000なのでiに10万倍
            duty_l[i] = i * 100000

            #ハードウェアPWMの設定
            # hardware_PWM(gpio, PWM周波数, PWMduty(min0-max1,000,000))
            gpio.hardware_PWM(pin_l[j], 1000, duty_l[j])

            # duty比を変更後0.1秒待つ
            time.sleep(0.1)

            # ruty比のリストを初期化
            duty_l = [0, 0, 0]

def main():

    led_flash(led_red, led_blue, led_green)

    # pigpioの終了処理
    gpio.stop()


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        sys.exit()