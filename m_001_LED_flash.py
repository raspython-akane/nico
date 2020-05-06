#! python3
# -*- coding: utf-8 -*-

# Filename: m_001_LED_flash 
__author__ = "raspython"
__date__ = '2020/05/06 08:25'

import RPi.GPIO as GPIO
from time import sleep



def main():
    """
    本体
    """

    """
    変数定義
    """
    # 設定時間
    flash_time = 1
    off_time = 0.5

    """
    PIN NOの定義
    """
    # LED
    led_red = 13
    led_bule = 19
    led_green = 26

    """
    GPIOの初期設定
    """
    # PIN_NOの設定
    GPIO.setmode(GPIO.BCM)
    # LEDへの出力
    GPIO.setup(led_red, GPIO.OUT)
    GPIO.setup(led_bule, GPIO.OUT)
    GPIO.setup(led_green, GPIO.OUT)

    """
    本体
    """
    try:

        # LEDを光らせる順番でGPIOのNOをリストに格納
        flash_no = [13, 19, 26, [13, 19], [13, 26], [19, 26], [13, 19, 26]]
        print(len(flash_no))

        # リストの要素の数だけループ
        for i in range(len(flash_no)):
            # LEDの点灯
            GPIO.output(flash_no[i], GPIO.HIGH)
            sleep(flash_time)
            # LEDの消灯
            GPIO.output(flash_no[i], GPIO.LOW)
            sleep(off_time)


    except KeyboardInterrupt:
        pass

    GPIO.cleanup()




if __name__ == '__main__':
    main()