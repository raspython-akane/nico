#!/usr/bin/env python3

# Filename: m_015_steppingmortor 
__author__ = "raspython"
__date__ = '2021/02/13 10:38'

import pigpio as pi
from time import sleep

# 7seg_ledの点灯パターン
num_char = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7c,
            0x07, 0x7f, 0x67, 0x00]

# GPIOの初期設定
pi_g = pi.pi()

# I2Cの設定
# 1はbus番号、0ｘ70はスレーブアドレス。
ht16k33_adr = pi_g.i2c_open(1, 0x70)
# レジスタの設定(openの戻り値でDeviceの指定、reg_address, 値）
# 内部システム発信機の有効
pi_g.i2c_write_byte_data(ht16k33_adr, 0x21, 0x01)
# LEDの表示設定の有効
pi_g.i2c_write_byte_data(ht16k33_adr, 0x81, 0x01)
# INT/LOWの出力はLOW
pi_g.i2c_write_byte_data(ht16k33_adr, 0xa1, 0x00)


def key_val():
    """
    キーマトリクスの入力の値をリストに入れて返す。
    すべての読み込みが終わると値は初期化される(16k33の仕様)
    @return: キーマトリクスの入力の値
    """
    # キーマトリクスの入力のレジスタアドレスのリスト
    adr_l = [0x40, 0x41, 0x42, 0x43, 0x44, 0x45]

    val_l =[]
    for i in adr_l:
        val_l.append(pi_g.i2c_read_byte_data(ht16k33_adr, i))

    print(val_l)


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
    print("ゼロパディング後: {}".format(l))

    # 7segLEDに表示
    display_char(l)



def display_char(l):
    """
    与えられた数字を7segLEDで表示する
    @param l: 表示する数字のlist
    @type l: l
    """
    # リストの値を逆順化
    l.reverse()
    print(l)

    for i, n in enumerate(l):
        pi_g.i2c_write_byte_data(ht16k33_adr, i * 2, num_char[n])


def main():
    print_n = 0
    try:
        while True:
            # キーマトリクスの読み込み
            key_l = key_val()
            print(key_l)

            # 黒のスイッチが押されたらスタート
            if key_l[[0]] == 1:
                print("スタート")
                zero_padding(print_n)

            # 白のスイッチが押されたら終了処理
            if key_l[0] == 2:
                break

            sleep(0.1)

    except KeyboardInterrupt:
        pass

    pi_g.stop()


if __name__ == '__main__':
    main()
