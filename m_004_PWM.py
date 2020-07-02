#! python3

# Filename: m_004_PWM 
__author__ = "raspython"
__date__ = '2020/07/01 19:42'


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
    flash_red = 20
    pwm_red = 21


    """
    GPIOの初期設定
    """
    # PIN_NOの設定
    GPIO.setmode(GPIO.BCM)

    # 出力
    GPIO.setup(flash_red, GPIO.OUT,
               initial=GPIO.LOW)
    # PWM設定
    GPIO.setup(pwm_red, GPIO.OUT)
    # PWM周波数は50Hz
    pwm = GPIO.PWM(pwm_red, 50)
    # dutyの初期化
    pwm.start(0)

    try:
        # 通常出力
        GPIO.output(flash_red, GPIO.HIGH)
        # PWM出力
        # 100%から1秒ごとにduty比が10%づつ下がる
        # 0でループ終了
        for i in range(11):
            pwm.ChangeDutyCycle(100 - (i * 10))
            print(100 - (i * 10))
            sleep(1)

        GPIO.output(flash_red, GPIO.LOW)
        pwm.ChangeDutyCycle(0)

    except KeyboardInterrupt:
        pass

    pwm.stop()
    GPIO.cleanup()


if __name__ == '__main__':
    main()