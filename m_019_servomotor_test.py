#!/usr/bin/env python3

# Filename: m_019_servomotor_test 
__author__ = "raspython"
__date__ = '2021/08/31 18:55'


import pigpio as pi
from time import sleep

# サーボ制御のPINNO
pin = 4

# pigpioの定義
pi_g = pi.pi()

# pwmのパルス幅1460で0度、2410で90度、550で-90度
# 単位はμs pulse
l = [1460, 2410, 550]
s = [1, 0.5]

# サーボモーターの制御
for i in s:
    for j in l:
        pi_g.set_servo_pulsewidth(pin, j)

        sleep(i)

# 0度に戻す
pi_g.set_servo_pulsewidth(pin, l[0])
sleep(0.5)
# OFF指令
pi_g.set_servo_pulsewidth(pin, 0)

# 終了処理
pi_g.stop()

def main():
    pass


if __name__ == '__main__':
    main()
