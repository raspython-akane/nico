#!/usr/bin/env python3

# Filename: m_20_rotation_servo_test 
__author__ = "raspython"
__date__ = '2021/09/09 20:08'

import pigpio as pi
from time import sleep

# サーボ制御用のPINNO
pin = 4

#piGPIOの定義
pi_g = pi.pi()

"""
pwmのパルス幅中央値が1500。
中央値から値が増えると左回転、減ると右回転。
値が中央値から離れるほどスピードが上がる。
maxは2400、minは500
"""
l = [1500, 1800, 2400, 1500, 1300, 500]

# ローテーションサーボの制御
for i in l:
    pi_g.set_servo_pulsewidth(pin, i)
    print(i)

    sleep(5)

# OFF指令
pi_g.set_servo_pulsewidth(pin, 0)

#終了処理
pi_g.stop()


def main():
    pass


if __name__ == '__main__':
    main()
