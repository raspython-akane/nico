#! python3

# Filename: m_006_01_music 
__author__ = "raspython"
__date__ = '2020/07/24 20:24'


import RPi.GPIO as GPIO
from time import sleep


def main():
    """
    本体
    """
    """
    PIN_NOの定義
    """

    buz = 21

    """
    GPIOの初期設定
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buz, GPIO.OUT)
    pwm = GPIO.PWM(buz, 50)
    pwm.start(50)

    """
    変数の設定
    """

    # 音階周波数
    lsi = 247
    do = 262
    re = 294
    mi = 330
    fa = 349
    so = 392
    ra = 440
    si = 494

    # 楽譜date
    onpu = (re, re, do, lsi, re, so, ra, si, si, si, ra,
            so, mi, mi, mi, fa, so, fa, so, mi, re, mi,
            re, lsi, re, re, re, re, do, lsi, re, so, ra,
            si, si, si, ra, so, ra, ra, ra, ra, so, so,
            fa, fa, so, so, so)
    on_time = (4, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1,
               2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2,
               1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1,
               2, 1, 2, 1, 1, 1, 1)
    off_time = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1,
                1, 1, 1, 1, 4, 4, 4)

    """
    実行部
    """

    for (m, i, j) in zip(onpu, on_time, off_time):
        pwm.ChangeDutyCycle(50)
        pwm.ChangeFrequency(m)
        sleep(i / 10)
        pwm.ChangeDutyCycle(0)
        sleep(j / 10)

    pwm.stop()
    GPIO.cleanup()


if __name__ == '__main__':
    main()