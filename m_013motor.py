#!/usr/bin/env python3

# Filename: m_14motor
__author__ = "raspython"
__date__ = '2021/01/03 17:38'

import pigpio as pi
from time import sleep

# pin_noの定義
sw_black = 23
sw_white = 24
sw_red = 25
sw_orange =12
sw_yellow = 16
h_bridge_top_left = 6
h_bridge_top_right = 13
h_bridge_bottom_left = 19
h_bridge_bottom_right = 26

# GPIOの初期設定
pi_g = pi.pi()

# 入力設定
pi_g.set_mode(sw_black, pi.INPUT)
pi_g.set_mode(sw_white, pi.INPUT)
pi_g.set_mode(sw_red, pi.INPUT)
pi_g.set_mode(sw_orange, pi.INPUT)
pi_g.set_mode(sw_yellow, pi.INPUT)

# プルアップ設定
pi_g.set_pull_up_down(sw_black, pi.PUD_UP)
pi_g.set_pull_up_down(sw_white, pi.PUD_UP)
pi_g.set_pull_up_down(sw_red, pi.PUD_UP)
pi_g.set_pull_up_down(sw_orange, pi.PUD_UP)
pi_g.set_pull_up_down(sw_yellow, pi.PUD_UP)

# 出力設定
pi_g.set_mode(h_bridge_top_left, pi.OUTPUT)
pi_g.set_mode(h_bridge_top_right, pi.OUTPUT)
pi_g.set_mode(h_bridge_bottom_left, pi.OUTPUT)
pi_g.set_mode(h_bridge_bottom_right, pi.OUTPUT)

"""
***** 注意 *****

h_bridge_top_left と h_bridge_bottom_left
h_bridge_top_right と h_bridge_bottom_right
は同時にONしないこと

***** 注意 *****
"""



def cw():
    """
    前転制御
    """
    pi_g.write(h_bridge_top_left, 1)
    pi_g.write(h_bridge_top_right, 0)
    pi_g.write(h_bridge_bottom_right, 1)
    pi_g.write(h_bridge_bottom_left, 0)


def ccw():
    """
    逆転制御
    """
    pi_g.write(h_bridge_top_left, 0)
    pi_g.write(h_bridge_top_right, 1)
    pi_g.write(h_bridge_bottom_right, 0)
    pi_g.write(h_bridge_bottom_left, 1)


def brake():
    """
    ブレーキ制御
    """
    pi_g.write(h_bridge_top_left, 1)
    pi_g.write(h_bridge_top_right, 1)
    pi_g.write(h_bridge_bottom_right, 0)
    pi_g.write(h_bridge_bottom_left, 0)

def motor_control():
    """
    モーターの制御部
    """
    # モーターの状態
    # 0が停止、1が前転、2が逆転
    motor_flag = 0
    while True:
        # 赤のスイッチが押されたら前転
        if pi_g.read(sw_red) == 0 or motor_flag == 1:
            # 前転以外からなら以下の処理
            if motor_flag != 1:
                print("前転開始")
                motor_flag = 1
            # 前転関数を呼ぶ
            cw()

        # 橙のスイッチが押されたら逆転
        if pi_g.read(sw_orange) == 0 or motor_flag == 2:
            # 逆転以外からなら以下の処理
            if motor_flag != 2:
                print("逆転開始")
                motor_flag = 2
            ccw()

        # 黄色のスイッチが押されたらブレーキ
        if pi_g.read(sw_yellow) == 0 or motor_flag == 0:
            # 停止以外からなら以下の処理
            if motor_flag != 0:
                print("ブレーキ開始")
                motor_flag = 0
            brake()

        # 白のスイッチが押されたらループを抜けて終了
        if pi_g.read(sw_white) == 0:
            break

        sleep(0.01)

def main():
    try:
        while True:
            # 黒のスイッチを押されたら制御開始
            if pi_g.read(sw_black) == 0:
                print("制御開始")
                motor_control()

            # 白のスイッチが押されたらループを抜けて終了
            if pi_g.read(sw_white) == 0:
                print("終了")
                break

            sleep(0.1)
    except KeyboardInterrupt:
        pass

    # GPIOの終了処理
    pi_g.write(h_bridge_top_left, 0)
    pi_g.write(h_bridge_bottom_right, 0)
    pi_g.write(h_bridge_top_right, 0)
    pi_g.write(h_bridge_bottom_left, 0)
    pi_g.stop()


if __name__ == '__main__':
    main()
