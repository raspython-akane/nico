#! python3

# Filename: m_002_sw_color 
__author__ = "raspython"
__date__ = '2020/05/16 09:27'

import RPi.GPIO as GPIO
from time import sleep


def main():
    """
    本体
    """
    """
    PIN_NOの定義
    """
    # LED

    led_r = 13
    led_g = 19
    led_b = 26
    # スイッチ
    sw_w = 12
    sw_r = 16
    sw_b = 20
    sw_g = 21

    """
    GPIOの初期設定
    """
    # PIN_NOの設定
    GPIO.setmode(GPIO.BCM)
    # 入力
    GPIO.setup(sw_w, GPIO.IN)
    GPIO.setup(sw_r, GPIO.IN)
    GPIO.setup(sw_g, GPIO.IN)
    GPIO.setup(sw_b, GPIO.IN)
    # 出力
    GPIO.setup(led_r, GPIO.OUT)
    GPIO.setup(led_g, GPIO.OUT)
    GPIO.setup(led_b, GPIO.OUT)

    """
    実行部
    """
    try:
        while True:
            # スイッチの色とLEDの色は赤、青、緑は色と対応
            # LEDが消灯中スイッチを押されると点灯する
            # LEDが点灯中は消灯
            if GPIO.input(sw_r) != GPIO.HIGH:
                print("スイッチ赤ON")
                GPIO.output(led_r, GPIO.HIGH)
                GPIO.output([led_g, led_b], GPIO.LOW)
            elif GPIO.input(sw_b) != GPIO.HIGH:
                print("スイッチ青ON")
                GPIO.output(led_b, GPIO.HIGH)
                GPIO.output([led_r, led_g], GPIO.LOW)
            elif GPIO.input(sw_g) != GPIO.HIGH:
                print("スイッチ緑ON")
                GPIO.output(led_g, GPIO.HIGH)
                GPIO.output([led_r, led_b], GPIO.LOW)
            # スイッチ白を押すと終了
            if GPIO.input(sw_w) != GPIO.HIGH:
                break
            sleep(0.1)

    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
    print("終了")

if __name__ == '__main__':
    main()