#! python3

# Filename: m_009_infrared 
__author__ = "raspython"
__date__ = '2020/09/06 08:43'

import RPi.GPIO as GPIO
from time import sleep


def main():
    """
    本体
    """
    """
    PIN_NOの定義
    """
    # スイッチ
    sw_i = 5
    led_r = 6
    led_b = 13

    """
    GPIOの初期設定
    """
    # PIN_NOの設定
    GPIO.setmode(GPIO.BCM)
    # 入力
    GPIO.setup(sw_i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # 出力
    GPIO.setup([led_r, led_b], GPIO.OUT, initial=GPIO.LOW)

    """
    変数
    """
    flag = True
    count = 0

    """
    実行部
    """
    try:
        while True:
            # 赤外線が遮られた時の処理
            if GPIO.input(sw_i) == GPIO.HIGH and flag:
                # flagの値を反転
                flag = not flag
                # print("flagが反転 {}".format(flag))
                # LED青点灯
                GPIO.output(led_b, GPIO.HIGH)

            # 通ったものがなくなったときの処理
            if GPIO.input(sw_i) != GPIO.HIGH and flag == False:
                # カウントアップ
                count += 1
                print("カウンター 【{}】".format(count))
                # flagの値を反転
                flag = not flag
                # print("flagが反転 {}".format(flag))
                # LED消灯
                GPIO.output(led_b, GPIO.LOW)

            if count == 10:
                print("カウントが10になったので終了")
                # LED赤を1秒点灯させてから消灯して
                # ループを抜ける
                GPIO.output(led_r, GPIO.HIGH)
                sleep(1)
                GPIO.output(led_r, GPIO.LOW)
                break

    except KeyboardInterrupt:
        pass
    GPIO.cleanup()

if __name__ == '__main__':
    main()