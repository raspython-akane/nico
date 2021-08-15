#!/usr/bin/env python3

# Filename: m_016_rotary_encoder 
__author__ = "raspython"
__date__ = '2021/07/27 09:54'

import pigpio as pi
from time import sleep


"""
GPIO周りの設定
"""

# PIN_NOの定義
# 入力
r_sw = 21
rotary_ac = 19
rotary_bc = 26
# 出力
led_r = 4

# カウンタ変数
counter = 0

# LEDarrayの点灯パターン
output_l=[0, 0x01, 0x03, 0x07, 0x0f, 0x1f, 0x3f, 0x7f, 0xff]


# GPIOの初期設定
pi_g = pi.pi()
# 入力設定
pi_g.set_mode(r_sw, pi.INPUT)
# プルダウン設定
pi_g.set_pull_up_down(r_sw, pi.PUD_DOWN)
# 出力設定
pi_g.set_mode(led_r, pi.OUTPUT)


# i2cの設定
# 1はbus番号、0x70はスレーブアドレス
ht16k33_adr = pi_g.i2c_open(1, 0x70)
# レジスタの設定(デバイスの指定, レジスタのアドレス, 値)
# 内部システム発信機の有効
pi_g.i2c_write_byte_data(ht16k33_adr, 0x21, 0x01)
# LEDの表示設定の有効
pi_g.i2c_write_byte_data(ht16k33_adr, 0x81, 0x01)


def led_red_control(par):
    """
    赤色LEDを制御する
    @param par: LEDの状態の値
    """
    pi_g.write(led_r,par)


def led_array_control(n):
    """
    LEDarrayを制御する
    入力の値までのLEDを光らせる
    @param n:どこまで光らせるかの値
    """
    # 初期化のためLEDを全消灯
    pi_g.i2c_write_byte_data(ht16k33_adr, 0, 0)
    pi_g.i2c_write_byte_data(ht16k33_adr, 1, 0)
    if n < 9:
        pi_g.i2c_write_byte_data(ht16k33_adr, 0, output_l[n])
    elif n > 8:
        pi_g.i2c_write_byte_data(ht16k33_adr, 0, output_l[8])
        pi_g.i2c_write_byte_data(ht16k33_adr, 1, output_l[n - 8])


def count_control(pin, status, tick):
    """
    A-C間が立ち下がったときのB-C間の入力で回転歩行とカウントを管理
    カウンターは0から100までの値で管理
    @param pin:GPIOのNO
    @param status: 立ち上がり立下りの値
    @param tick:内部時計の値
    """
    global counter
    # print("A-C on")
    # a-c間が立下り時a-cがLOWならカウントダウン
    if pi_g.read(rotary_bc) == 0:
        # print("ccw")
        counter -= 1
        if counter < 0:
            counter = 0
        p_word = str(counter)
        print("カウンタの値は {}".format(p_word))

    # a-c間が立下り時a-cがHIGHならカウントアップ
    if pi_g.read(rotary_bc) == 1:
        # print("cw")
        counter += 1
        if counter > 100:
            counter = 100
        p_word = str(counter)
        print("カウンタの値は {}".format(p_word))


def rotary_monitorring():
    """
    ロータリーエンコーダーの出力波形を監視してカウント数の値で
    LEDアレイを制御する
    LEDアレイは10のカウント毎に1段づつLEDが点灯
    """

    # ロータリーエンコーダが回された時の割り込みの定義
    r_a = pi_g.callback(rotary_ac, pi.FALLING_EDGE, count_control)

    while True:
        # 何行目までLEDを点灯させるか計算して制御関数に渡す
        row = int(counter / 10)
        print("LEDを点灯させる行数 {}".format(row))
        led_array_control(row)


        # ロータリーエンコーダのスイッチが押されたら終了
        if pi_g.read(r_sw) == 1:
            # コールバックの終了処理
            r_a.cancel()
            break

        sleep(0.1)



def main_control():
    """
    ロータリーエンコーダのスイッチを監視し、押されたらロータリーエンコーダの
    モニタリングを開始する。
    その時赤色LEDを点灯させる。
    もう一度スイッチを押されると終了。
    """

    # 起動時は赤LEDを消灯させる
    led_red_control(0)

    # 1つのスイッチで開始終了させるたflagで管理させる
    # 初期値は0
    sw_flag = 0

    try:
        while True:
            # ロータリースイッチを一度押すと開始処理
            if (sw_flag == 0) & (pi_g.read(r_sw) == 1):
                # チャタリング防止のため押されたら05秒スリープ
                for i in range(0, 11, 2):
                    led_array_control(i)
                    sleep(0.1)
                led_array_control(0)

                # 赤色LED点灯
                led_red_control(1)

                print("開始")
                sw_flag = 1
                # ロータリーエンコーダの監視へ
                rotary_monitorring()



            # ロータリーエンコーダのスイッチを2度目の押下で終了する
            elif (sw_flag == 1) & (pi_g.read(r_sw) == 1):
                print("終了")
                break


            sleep(0.1)

    except KeyboardInterrupt:
        pass

    # GPIOの終了処理
    # 終了時はLEDを全消灯
    led_red_control(0)
    led_array_control(0)

    pi_g.stop()


def main():
    # メイン処理
    main_control()


if __name__ == '__main__':
    main()
