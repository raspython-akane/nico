#! python3

# Filename: m_004_logic analyzer_test
__author__ = "raspython"
__date__ = '2020/06/21 10:43'


import wiringpi as pi
from time import sleep

def main():
    """
    GPIOの初期設定
    """

    # wiringpi側
    # PIN NOの設定
    pi.wiringPiSetupGpio()
    # 出力
    pi.pinMode(18, pi.GPIO.PWM_OUTPUT)
    # PWMの設定
    pi.pwmSetRange(192)
    pi.pwmSetClock(4)

    """
    本体
    """
    pi.pwmWrite(18, 96)
    sleep(10)
    pi.pwmWrite(18, 0)


if __name__ == '__main__':
    main()