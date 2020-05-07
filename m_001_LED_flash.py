#! python3

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
    led_blue = 19
    led_green = 26

    """
    GPIOの初期設定
    """
    # PIN_NOの設定
    GPIO.setmode(GPIO.BCM)
    # LEDへの出力
    GPIO.setup(led_red, GPIO.OUT)
    GPIO.setup(led_blue, GPIO.OUT)
    GPIO.setup(led_green, GPIO.OUT)

    """
    実行部
    """
    try:

        # LEDを光らせる順番でGPIOのNOをリストに格納
        flash_no = [led_red, led_blue, led_green,
                    [led_red, led_blue], [led_red, led_green],
                    [led_blue, led_green], [led_red, led_blue, led_green]]

        print(len(flash_no))

        # リストの要素を渡してループ
        for n in flash_no:
            # LEDの点灯
            GPIO.output(n, GPIO.HIGH)
            sleep(flash_time)
            # LEDの消灯
            GPIO.output(n, GPIO.LOW)
            sleep(off_time)

    except KeyboardInterrupt:
        pass

    GPIO.cleanup()




if __name__ == '__main__':
    main()