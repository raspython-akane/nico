#! python3

# Filename: m_003_timing_color 
__author__ = "raspython"
__date__ = '2020/06/06 18:38'


import RPi.GPIO as GPIO
from time import sleep
from random import randint


def main():
    """
    本体
    """
    """
    PIN_NOの定義
    """
    # LED
    upper_r = 13
    upper_g = 19
    upper_b = 26
    lower_r = 17
    lower_g = 27
    lower_b = 22
    led_l =[upper_r,upper_g, upper_b,
            lower_r,lower_g, lower_b]

    # スイッチ
    sw_w = 12
    sw_r = 16
    sw_g = 20
    sw_b = 21

    """
    GPIOの初期設定
    """
    # PIN_NOの設定
    GPIO.setmode(GPIO.BCM)
    # 入力
    GPIO.setup([sw_w, sw_r, sw_g, sw_b], GPIO.IN,
               pull_up_down=GPIO.PUD_UP)
    # 出力
    GPIO.setup(led_l, GPIO.OUT,
               initial=GPIO.LOW)

    """
    実行部
    """
    try:
        # スイッチ白を押されるまでループ
        while GPIO.input(sw_w) == GPIO.HIGH:
            for i in range(10):
                # LED点灯前に1秒待つ
                sleep(1)

                # 色を決める乱数の生成
                color_num = (randint(1, 100) % 3)
                # print(color_num)

                # 乱数が0なら赤、1なら緑、2なら青を点灯
                # 上下のLED点灯間隔とスイッチの入力リミットは
                # 1ループするごとに0.1秒毎短くなる
                GPIO.output(led_l[color_num], GPIO.HIGH)
                sleep(1 - (i * 0.1))
                GPIO.output(led_l[color_num], GPIO.LOW)
                GPIO.output(led_l[color_num + 3], GPIO.HIGH)
                sleep(1 - (i * 0.1))
                GPIO.output(led_l[color_num + 3], GPIO.LOW)





    except KeyboardInterrupt:
        pass

    GPIO.cleanup()


if __name__ == '__main__':
    main()