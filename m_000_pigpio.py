#!/usr/bin/env python3

# Filename: m_000_pigpio 
__author__ = "raspython"
__date__ = '2020/12/19 20:27'

import pigpio as pi
from time import sleep

# pin_noの定義
sw_b = 16
sw_w = 21
led_b = 18

# GPIOの初期設定
pi_g = pi.pi()
# 入力設定
pi_g.set_mode(sw_b, pi.INPUT)
pi_g.set_mode(sw_w, pi.INPUT)
# プルアップ設定 ピンの定義をまとめてリストでは使えない
pi_g.set_pull_up_down(sw_b, pi.PUD_UP)
pi_g.set_pull_up_down(sw_w, pi.PUD_UP)
# 出力設定
pi_g.set_mode(led_b, pi.OUTPUT)


# i2cの設定
# 1はbusの数拡張無しは1、0x70はスレーブアドレス
ht16k33_adr = pi_g.i2c_open(1, 0x70)
#レジスタの設定(openの戻り値でDeviceの指定、reg_adress, 値）
# 内部システム発信機の有効
pi_g.i2c_write_byte_data(ht16k33_adr, 0x21, 0x01)
# LEDの表示設定の有効
pi_g.i2c_write_byte_data(ht16k33_adr, 0x81, 0x01)


def sw_test():
    """
    黒のスイッチを押したらLED点灯
    白のスイッチを押したらLED消灯
    プルアップなのでボタン押しで0
    """
    while True:
        if pi_g.read(sw_b) == 0:
            pi_g.write(led_b, 1)
        if pi_g.read(sw_w) == 0:
            pi_g.write(led_b, 0)
            break
        sleep(0.1)


def matrix_test():
    """
    マトリクスLEDの点灯と消灯のテスト
    """
    # マトリクスLEDの横軸の数
    matrix_row = 16

    while True:

        # 黒のスイッチを押すとマトリクスLEDを全点灯
        if pi_g.read(sw_b) == 0:

            # 青のLEDを点灯
            pi_g.write(led_b, 1)

            # マトリクスLEDの点灯パターン
            out = [0b11111111, 0b11111111,
                   0b11111111, 0b11111111,
                   0b11111111, 0b11111111,
                   0b11111111, 0b11111111,
                   0b11111111, 0b11111111,
                   0b11111111, 0b11111111,
                   0b11111111, 0b11111111,
                   0b11111111, 0b11111111]

            for i in range(matrix_row):
                pi_g.i2c_write_byte_data(ht16k33_adr, i, out[i])

        # 白のスイッチを押すとマトリクスLEDを全消灯
        if pi_g.read(sw_w) == 0:

            # 青のLEDを消灯
            pi_g.write(led_b, 0)

            # マトリクスLEDの消灯
            out = [0, 0,
                   0, 0,
                   0, 0,
                   0, 0,
                   0, 0,
                   0, 0,
                   0, 0,
                   0, 0]

            for i in range(matrix_row):
                pi_g.i2c_write_byte_data(ht16k33_adr, i, out[1])

            break

        sleep(0.1)

def main():
    # スイッチを使ってLEDの点灯
    sw_test()

    # pi.gpioの終了処理
    pi_g.stop()


if __name__ == '__main__':
    main()