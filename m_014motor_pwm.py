#!/usr/bin/env python3

# Filename: m_14motor
__author__ = "raspython"
__date__ = '2021/01/04 10:19'

import pigpio as pi
from time import sleep

# pin_noの定義
sw_black = 23
sw_white = 24
sw_red = 25
sw_orange =12
sw_yellow = 16
sw_green = 20
sw_blue = 21
motor_out_1 = 19
motor_out_2 = 26

# PWMの周波数
freq = 1000
# duty比の分解能
pwm_range = 100
# 初期duty比
duty = 50

# 7segledの点灯パターン
num_char = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7c,
            0x07, 0x7f, 0x67, 0x00]

# GPIOの初期設定
pi_g = pi.pi()

# 入力設定
pi_g.set_mode(sw_black, pi.INPUT)
pi_g.set_mode(sw_white, pi.INPUT)
pi_g.set_mode(sw_red, pi.INPUT)
pi_g.set_mode(sw_orange, pi.INPUT)
pi_g.set_mode(sw_yellow, pi.INPUT)
pi_g.set_mode(sw_green, pi.INPUT)
pi_g.set_mode(sw_blue, pi.INPUT)

# プルアップ設定
pi_g.set_pull_up_down(sw_black, pi.PUD_UP)
pi_g.set_pull_up_down(sw_white, pi.PUD_UP)
pi_g.set_pull_up_down(sw_red, pi.PUD_UP)
pi_g.set_pull_up_down(sw_orange, pi.PUD_UP)
pi_g.set_pull_up_down(sw_yellow, pi.PUD_UP)
# pi_g.set_pull_up_down(sw_green, pi.PUD_UP)
# pi_g.set_pull_up_down(sw_blue, pi.PUD_UP)

# 出力設定
pi_g.set_mode(motor_out_1, pi.OUTPUT)
pi_g.set_mode(motor_out_2, pi.OUTPUT)

# I2Cの設定
# 1はbus番号、0x70はスレーブアドレス。
ht16k33_adr = pi_g.i2c_open(1, 0x70)
# レジスタの設定(openの戻り値でDeviceの指定、reg_address, 値）
# 内部システム発信機の有効
pi_g.i2c_write_byte_data(ht16k33_adr, 0x21, 0x01)
# LEDの表示設定の有効
pi_g.i2c_write_byte_data(ht16k33_adr,0x81, 0x01)

# ソフトウェアPWMの設定

# PWMの周波数の設定
# セットアップでGPIOのサンプリングの設定を
# 8マイクロ秒に設定してあるので選べる周波数は
# 5000  2500  1250 1000  625  500  313  250  200
pi_g.set_PWM_frequency(motor_out_1, freq)
pi_g.set_PWM_frequency(motor_out_2, freq)

# duty比の分解能の設定
pi_g.set_PWM_range(motor_out_1, pwm_range)
pi_g.set_PWM_range(motor_out_2, pwm_range)



def cw():
    """
    前転制御
    """
    pi_g.set_PWM_dutycycle(motor_out_1, duty)
    pi_g.set_PWM_dutycycle(motor_out_2, 0)



def ccw():
    """
    逆転制御

    """
    pi_g.set_PWM_dutycycle(motor_out_1, 0)
    pi_g.set_PWM_dutycycle(motor_out_2, duty)


def brake():
    """
    ブレーキ制御
    """
    pi_g.set_PWM_dutycycle(motor_out_1, 100)
    pi_g.set_PWM_dutycycle(motor_out_2, 100)


def duty_up(pin, level, tick):
    """
    duty比をMAX100まで1カウントアップする

    @param pin: コールバックの呼び出しのGPIO_NO
    @type pin: int
    @param level: edgeの種類
    @type level:int
    @param tick: 処理間隔
    @type tick:int
    """
    # print(pin, level, tick)
    global duty

    if duty < 100:
        duty += 1
    print("カウントアップして {}".format(duty))


def duty_down(pin, level, tick):
    """
    duty比をmin0まで1カウントダウンする

    @param pin: コールバックの呼び出しのGPIO_NO
    @type pin: int
    @param level: edgeの種類
    @type level:int
    @param tick: 処理間隔
    @type tick:int
    """
    global duty

    if duty > 0:
        duty -= 1
    print("カウントダウンして {}".format(duty))


def display_char(l):
    """
    与えられた数字を7segLEDで表示する
    @param l: 表示する数字のlist
    @type l: l
    """
    # リストを逆順化する
    l.reverse()
    print(l)
    for i, n in enumerate(l):
        # print(i, n)
        pi_g.i2c_write_byte_data(ht16k33_adr, i * 2, num_char[n])
        # print(ht16k33_adr, i * 2, num_char[n])



def zero_padding(n):
    """
    与えられた数字を4桁で右寄せ0詰め
    0埋めしたものを桁毎にリストへ入れる
    そのリストをdisplay_charに渡す
    @param n:duty比
    @type n:int
    """
    # 右寄せ4桁0埋め(str)
    zero_p = str(n).zfill(4)

    # ゼロパディングした文字列を数値化しながらリストへ入れる。
    l = [int(n) for n in list(zero_p)]
    # print("duty比を桁ごとにリスト化 {}".format(l))

    # ディスプレイ表示
    display_char(l)


def motor_control():
    """
    モーターの制御部
    """
    # モーターの状態
    # 0が停止、1が前転、2が逆転
    motor_flag = 0

    # 緑か青のスイッチが押されたらduty比の変更
    # callback関数に渡す関数は関数名で関数を呼び出すのではない
    # コールバックされた関数にはpin番号、状態、tickの3つの値が渡される
    # 最後に必ずコールバックのキャンセルをかける
    cb0 = pi_g.callback(sw_green, pi.FALLING_EDGE, duty_up)
    cb1 = pi_g.callback(sw_blue, pi.FALLING_EDGE, duty_down)

    while True:
        # PWMの数字を右寄せ0埋めして7segLEDで表示する
        zero_padding(duty)

        # 赤のスイッチを押されたら前転開始
        if pi_g.read(sw_red) == 0 or motor_flag == 1:
            # 前転以外からなら以下の処理
            if motor_flag != 1:
                print("前転開始")
                motor_flag = 1
            # 前転関数を呼ぶ
            cw()

        # 橙のスイッチが押されたら逆転開始
        if pi_g.read(sw_orange) == 0 or motor_flag == 2:
            # 逆転以外からなら以下の処理
            if motor_flag != 2:
                print("逆転開始")
                motor_flag = 2
            ccw()

        # 黄色のスイッチが押されたらブレーキ開始
        if pi_g.read(sw_yellow) == 0 or motor_flag == 0:
            # 停止以外からなら以下の処理
            if motor_flag != 0:
                print("ブレーキ開始")
                motor_flag = 0
            brake()

        # 白のスイッチが押されたらループを抜けて終了
        if pi_g.read(sw_white) == 0:
            break

        sleep(0.1)

    # コールバックのキャンセル
    cb0.cancel()
    cb1.cancel()

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

    # 7segLEDを消灯
    l = [10, 10, 10, 10]
    display_char(l)

    # GPIOの終了処理
    pi_g.write(motor_out_1, 0)
    pi_g.write(motor_out_2, 0)
    pi_g.stop()


if __name__ == '__main__':
    main()
