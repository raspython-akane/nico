#! python3

# Filename: m_006_00_buzzer
__author__ = "raspython"
__date__ = '2020/07/24 11:49'


import RPi.GPIO as GPIO
from time import sleep

def main():
    """
    本体
    """
    """
    PIN_NOの定義
    """
    # ブザー
    buz = 21

    """
    GPIOの初期設定
    """
    # PIN_NOの設定
    GPIO.setmode(GPIO.BCM)

    # 出力
    GPIO.setup(buz, GPIO.OUT)
    # PWMの設定
    pwm = GPIO.PWM(buz, 50)
    pwm.start(50)

    """
    変数の設定
    """
    # 周波数リスト
    pc98 = [2000, 1000]

    """
    実行部
    """

    for i in pc98:
        print(i)
        pwm.ChangeFrequency(i)
        sleep(0.1)

    pwm.stop()
    GPIO.cleanup()


if __name__ == '__main__':
    main()