#!/usr/bin/env python3

# Filename: m_022new_raspberrypios_test 
__author__ = "raspython"
__date__ = '2024/07/28 11:35'

import pigpio
import time
import sys


# pinNoを変数に入れる
# ハードウェアPWM用
led_red = 18
led_blue = 19
# ソフトウェアPWM用
led_green = 13

# pigpioの初期設定
gpio = pigpio.pi()

# ソフトウェアPWMの周波数設定
gpio.set_PWM_frequency(led_green, 1000)
# ソフトウェアPWMのduty比のレンジを0-100にする
gpio.set_PWM_range(led_green, 100)

def led_flash(R_pin, B_pin, G_pin):
    """
    LEDをPWM制御で徐々に明るくする。
    @param R_pin: LED赤のGPIO PIN No
    @param B_pin: LED青のGPIO PIN No
    @param G_pin: LED緑のGPIO PIN No
    """
    # duty日のリストを作成。要素の若い順から、赤、青、緑
    duty_l = [0, 0, 0]

    for i in range(1, 11, 1):
        for j in range(3):
            #赤から順に0.1秒毎duty比10%づつ挙げて光らせる
            # duty比は0-MAX1,000,000なのでiに10万倍
            duty_l[j] = i * 100000

            # 赤と青はハードウェアPWM制御 緑はソフトウェアPWM制御
            # ハードウェアPWMの設定
            # hardware_PWM(gpio, PWM周波数, PWMduty(min0-max1,000,000))
            print("赤のduty比: {}".format(duty_l[0]))
            gpio.hardware_PWM(R_pin, 1000, duty_l[0])
            print("青のduty比: {}".format((duty_l[1])))
            gpio.hardware_PWM(B_pin, 1000, duty_l[1])

            # ソフトウェアPWM duty制御
            # ソフトウェアPWMのduty比は0-100のためリストの値を1万で割る
            print("緑のduty比: {}".format(int(duty_l[2] / 10000)))
            gpio.set_PWM_dutycycle(G_pin, int(duty_l[2] / 10000))

            # duty比を変更後0.1秒待つ
            time.sleep(0.5)

            # duty比のリストを初期化
            duty_l = [0, 0, 0]
            print(duty_l)

def main():

    led_flash(led_red, led_blue, led_green)

    # 各LED PINのduty比を0にする
    gpio.hardware_PWM(led_red, 1000, 0)
    gpio.hardware_PWM(led_blue, 1000, 0)
    gpio.set_PWM_dutycycle(led_green, 0)

    # pigpioの終了処理
    gpio.stop()


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        sys.exit()