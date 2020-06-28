#! python3

# Filename: m_004_logic analyzer_test 
__author__ = "raspython"
__date__ = '2020/06/21 10:43'


import wiringpi as pi
import RPi.GPIO as GPIO
from time import sleep

def main():
    """
    GPIOの初期設定
    """
    # RPi.GPIO側
    # PIN_NOの設定
    GPIO.setmode(GPIO.BCM)
    # 出力
    GPIO.setup(21, GPIO.OUT,
               initial=GPIO.LOW)
    # PWM設定
    rpi = GPIO.PWM(21, 100000)
    rpi.start(0)

    # wiringpi側
    # PIN NOの設定
    pi.wiringPiSetupGpio()
    # 出力
    pi.pinMode(18, pi.GPIO.PWM_OUTPUT)
    # PWMの設定
    pi.pwmSetMode(pi.GPIO.PWM_MODE_MS)
    pi.pwmSetRange(100)
    pi.pwmSetClock(2)


    """
    本体
    """
    rpi.ChangeDutyCycle(50)
    pi.pwmWrite(18, 50)
    sleep(10)
    rpi.ChangeDutyCycle(0)
    pi.pwmWrite(18, 0)

    rpi.stop()
    GPIO.cleanup()



if __name__ == '__main__':
    main()