#!/usr/bin/env python3
# Filename: m_010_7seg_counter
__author__ = "raspython"
__date__ = '2020/11/09 09:12'

import wiringpi as pi
import RPi.GPIO as GPIO
from time import sleep


"""
PIN_NOの代入
"""
#LED
#赤外線LED
led_inf = 5
led_r = 6
led_b = 13


"""
RPi.GPIOの初期設定
"""
# BCMのGPIO_NOで呼び出し
GPIO.setmode(GPIO.BCM)
# 入力
GPIO.setup(led_inf, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# 出力
GPIO.setup([led_r, led_b], GPIO.OUT, initial=GPIO.LOW)


"""
I2Cの設定(wiringpi)
"""
pi.wiringPiSetupGpio()
i2c = pi.I2C()
# スレーブアドレスを代入
ht16k33_adr = i2c.setup(0x70)
# レジスタの設定
# 内部システム発信機の有効
i2c.writeReg8(ht16k33_adr, 0x21, 0x01)
# LEDの表示設定の有効
i2c.writeReg8(ht16k33_adr, 0x81, 0x01)



"""
変数の定義
"""

# 表示用の4桁数字のリスト
# 初期値は0000
n_list = [0, 0, 0, 0]

# 7segLEDの点灯パターン
# indexと同じ整数を表示 index10は"-" index11は消灯
p_char = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7c,
          0x07, 0x7f, 0x67, 0x40, 0x00]


"""
関数の定義
"""


def led_flash():
    """
    n_listの数値をLEDに表示
    """
    # リストを逆順に並び替え
    n_list.reverse()
    # 7segLEDに表示
    for i, num in enumerate(n_list):
        i2c.writeReg8(ht16k33_adr, i * 2, p_char[num])
        print("{}桁目の表示 【{}】".format(i + 1, n_list[i]))


def zero_p_list(c):
    """
    与えられた値を4桁でゼロパディング
    その後数値化してn_listに入れてled_flash()を呼ぶ。
    @param c:カウント数
    @type c: int
    """
    global n_list

    # 与えられた値を4桁で右寄せ0埋め(str)
    zero_p = str(c).zfill(4)
    print("ゼロパディング後 {}".format(zero_p))

    # ゼロパディングされた値をint型にしてlistに格納
    n_list = [int(n) for n in list(zero_p)]
    print("リスト入れた後 {}".format(n_list))


    # 7segLED表示
    led_flash()


def proximity_counter():
    """
    赤外線LEDと赤外線フォトトランジスタ間を遮られた
    物がなくなるとカウントアップ
    その値をzero_p_listに渡す。
    """
    # 変数定義
    flag = True
    count = 0

    try:
        while True:
            # 赤外線が遮られた時の処理
            if GPIO.input(led_inf) == GPIO.HIGH and flag:
                # flagの値を反転
                flag = not flag
                print("flagが反転して {} に".format(flag))
                # LED 青点灯
                GPIO.output(led_b, GPIO.HIGH)

            # 遮られたものがなくなったときの処理
            if GPIO.input(led_inf) != GPIO.HIGH and flag == False:
                count += 1
                print("現在のカウント 【{}】".format(count))
                # flagの値を反転
                flag = not flag
                print("flagが反転して {} に".format(flag))
                # LED 青消灯
                GPIO.output(led_b, GPIO.LOW)
                # zero_p_list()にカウントの数値を渡す
                zero_p_list(count)
                sleep(0.1)

            # カウントが10まで行ったら3秒赤LEDを点灯
            if count > 9:
                print("カウントが10になったので終了")
                # LED赤を1秒点灯させてから消灯して
                # ループを抜ける
                GPIO.output(led_r, GPIO.HIGH)
                sleep(3)
                GPIO.output(led_r, GPIO.LOW)
                break

    except KeyboardInterrupt:
        pass


def led_check():
    """
    7segLEDの表示チェック用
    数字4つを入力して表示させる
    0～10で入力
    10の入力で表示するのは"-"
    """
    global n_list

    # 半角数字の0~10の入力チェック
    mess = "半角数字の0～10を入れてください"
    i = 0
    while i < 4:
        try:
            n = int(input("{} {}桁目".format(mess, 4 - i)))
            if n < 0 or n > 10:
                print("*error* {}".format(mess))
            else:
                n_list[3 - i] = n
                i += 1

        except ValueError:
            print("*error* {}".format(mess))

    # 7segLED表示
    led_flash()


"""
ほんへ
"""

def main():
    global n_list
    # 7segLED表示チェック。
    #通常時はコメントアウト
    # led_check()

    # 最初に0000を表示させる
    led_flash()

    # カウント開始
    proximity_counter()

    # LEDを消灯して終了処理
    n_list = [11, 11, 11, 11]
    led_flash()
    GPIO.cleanup()



if __name__ == '__main__':
    main()