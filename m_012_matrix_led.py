#!/usr/bin/env python3

# Filename: m_012_matrix_led 
__author__ = "raspython"
__date__ = '2020/12/19 06:09'

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
# プルアップ設定(リストによる複数設定は不可)
pi_g.set_pull_up_down(sw_b, pi.PUD_UP)
pi_g.set_pull_up_down(sw_w, pi.PUD_UP)
# 出力設定
pi_g.set_mode(led_b, pi.OUTPUT)

# i2cの設定
# 1はbusの数拡張無しは1、0x70はスレーブアドレス
ht16k33_adr = pi_g.i2c_open(1, 0x70)
#レジスタの設定(openの戻り値でDeviceの指定、reg_address, 値）
# 内部システム発信機の有効
pi_g.i2c_write_byte_data(ht16k33_adr, 0x21, 0x01)
# LEDの表示設定の有効
pi_g.i2c_write_byte_data(ht16k33_adr, 0x81, 0x01)


# 文字のマトリクス点灯パターンの辞書
# 下位bitが文字の左端
p_word = {"0": [0b00000000,
                0b00000000,
                0b00000000,
                0b00000000,
                0b00000000,
                0b00000000,
                0b00000000,
                0b00000000],
          "あ": [0b00001000,
                 0b01111110,
                 0b00001000,
                 0b01111100,
                 0b10101010,
                 0b10011010,
                 0b01001100,
                 0b00000000],
          "い": [0b00000000,
                 0b00100010,
                 0b01000010,
                 0b10000010,
                 0b11001010,
                 0b00001100,
                 0b00001000,
                 0b00000000],
          "う": [0b00111100,
                 0b00000000,
                 0b00111100,
                 0b01000010,
                 0b01000000,
                 0b01000000,
                 0b00100000,
                 0b00011000],
          "お": [0b00001000,
                 0b01011110,
                 0b10001000,
                 0b00111100,
                 0b01001010,
                 0b01001010,
                 0b00100100,
                 0b00000000],
          "け": [0b00100010,
                 0b01111010,
                 0b00100010,
                 0b00100010,
                 0b00100010,
                 0b00100010,
                 0b00010000,
                 0b00000000],
          "ご": [0b10100000,
                 0b01111100,
                 0b00100000,
                 0b00000000,
                 0b00000100,
                 0b00000010,
                 0b11111100,
                 0b00000000],
          "ざ": [0b10100000,
                 0b11100000,
                 0b00111110,
                 0b01000000,
                 0b01111100,
                 0b00000010,
                 0b01111100,
                 0b00000000],
          "し": [0b00000100,
                 0b00000100,
                 0b00000100,
                 0b00000100,
                 0b00000100,
                 0b01000100,
                 0b00111000,
                 0b00000000],
          "す": [0b00110000,
                 0b11100000,
                 0b00111110,
                 0b00110000,
                 0b00101000,
                 0b00110000,
                 0b00100000,
                 0b00010000],
          "て": [0b11111000,
                 0b00100110,
                 0b00010000,
                 0b00001000,
                 0b00001000,
                 0b00001000,
                 0b00010000,
                 0b01100000],
          "で": [0b11111000,
                 0b00100110,
                 0b10010000,
                 0b01001000,
                 0b00001000,
                 0b00001000,
                 0b00010000,
                 0b01100000],
          "と": [0b00000100,
                 0b00001000,
                 0b01101000,
                 0b00011000,
                 0b00000100,
                 0b00000010,
                 0b11111100,
                 0b00000000],
          "ま": [0b00100000,
                 0b11111100,
                 0b00100000,
                 0b11111100,
                 0b00100000,
                 0b01111100,
                 0b10100010,
                 0b00011100],
          "め": [0b01100000,
                 0b01000010,
                 0b01111110,
                 0b10100011,
                 0b10010101,
                 0b10001001,
                 0b01010110,
                 0b00000000],
          "琴": [0b11101110,
                 0b01000100,
                 0b11101110,
                 0b00111000,
                 0b11000110,
                 0b00111000,
                 0b00100000,
                 0b00010000],
          "葉": [0b00101000,
                 0b11111110,
                 0b00110100,
                 0b00000100,
                 0b11111100,
                 0b00111000,
                 0b01010100,
                 0b10010010],
          "茜": [0b00100100,
                 0b11111111,
                 0b00100100,
                 0b11111111,
                 0b01100110,
                 0b01000010,
                 0b01111110,
                 0b00000000],
          "終": [0b00000000,
                0b00000000,
                0b00000000,
                0b00000000,
                0b00000000,
                0b00000000,
                0b00000000,
                0b00000000,
                0b00000000,
                0b00000000,
                0b00000000,
                0b00000000,
                0b00000000,
                0b00000000,
                0b00000000,
                0b00000000]}

# 表示する文字のlist
word_l = ["あ", "け", "ま", "し", "て", "お", "め", "で",
          "と", "う", "ご", "ざ", "い", "ま", "す", "0",
          "琴", "葉", "0", "茜"]


def b_storing(length):
    """
    与えられた値の文字分リストから抜き出し、点灯パターンの
    バイナリをbitシフトしながら表示用のバイナリに加算していく。
    最後にそのリストを返す。
    @param length: 格納する文字数
    @type length: int
    @return:表示用のバイナリのリスト
    @rtype: list
    """
    global word_l
    # 表示用のbinリスト
    p_w_l = [0, 0, 0, 0, 0, 0, 0, 0]

    # 格納したい文字を逆から順にして処理していく
    for i in range(length, 0, -1):
        # rage(, , -1)のループ変数の最後を0にしたいので
        # ループ変数を-1する
        i -= 1
        w_l = p_word[word_l[i]]
        print("リストに格納する文字: {}".format(word_l[i]))

        # 8行分の処理
        for j in range(8):
            # print(bin(w_l[j]))
            # 何文字目かによりその分8bit左へシフト
            tmp_bin = w_l[j] << ((i) * 8)
            # 表示用のバイナリとと加算
            p_w_l[j] = p_w_l[j] | tmp_bin
            print("【{}】を格納した後の{}行目のバイナリデータ: {}"
                  .format(word_l[i], j + 1, bin(p_w_l[j]),))

    for i in range(length):
        del word_l[0]
    print("格納した文字を削除後のリスト: {}".format(word_l))

    return p_w_l


def eight_bit_divide(p_b_l):
    """
    与えられたリストの中の32bitのバイナリデータの
    下位16bitを8bit2つに分けてリストに入れて、それを返す。
    @param p_b_l:
    @type p_b_l:
    @return:
    @rtype:
    """
    l = []
    h_8b = 0b1111111100000000
    l_8b = 0b11111111
    for i in range(len(p_b_l)):
        # 下位8bitをリストに入れる
        # 下位16～9bitを右へ8bitシフトしてリストに入れる
        l.append(p_b_l[i] & l_8b)
        l.append(((p_b_l[i]) & h_8b) >> 8)

    # print(l)
    return l


def b_shift(l, c):
    """
    与えられたリストを8it分割関数に渡し
    そのリストを点灯用の関数に渡す
    その後、与えられた値分リストの中の全バイナリを
    1bitシフトさせながら点灯関数に渡す
    @param l: 点灯パターンのリスト
    @type l: list
    @param c: bitシフトさせる回数
    @type c: int
    """
    for i in range(c):
         bin_list = eight_bit_divide(l)
         matrix_led(bin_list)
         for j in range(len(l)):
            l[j] = l[j] >> 1
            print(bin(l[j]))

            sleep(0.1)

def matrix_led(l):
    """
    与えられた点灯パターンでマトリクスLEDを点灯させる
    @param l: マトリクスLEDの点灯パターンのリスト
    @type l: list
    """
    # マトリクスLED2つで16行
    matrix_row = 16
    for i in range(matrix_row):
        pi_g.i2c_write_byte_data(ht16k33_adr, i, l[i])

def main():
    try:
        while True:
            # 黒のスイッチを押されたら処理開始。
            if pi_g.read(sw_b) == 0:
                # 青のLED点灯
                pi_g.write(led_b, 1)

                # 表示の準備
                # 最初のに文字を格納
                b_l = b_storing(2)
                # 初期表示は両方のドットマトリクスも全消灯から開始するため
                # リストの中身全部を16bit左へシフト
                for i in range(len(b_l)):
                    b_l[i] = b_l[i] << 16
                    print(bin(b_l[i]))

                b_shift(b_l, 32)

                break

                """
                for i in range(32):
                    print_list = eight_bit_divide(b_l)
                    for j in range(len(b_l)):
                        b_l[j] = b_l[j] >> 1
                        print(bin(b_l[j]))
                """

            # 白のスイッチを押されたらLEDを消灯してループを抜ける
            if pi_g.read(sw_w) == 0:
                break
    except KeyboardInterrupt:
        pass

    # 青のLED消灯
    pi_g.write(led_b, 0)
    # マトリクスLEDの消灯
    matrix_led(p_word["終"])
    # pi.gpioの終了処理
    pi_g.stop()

if __name__ == '__main__':
    main()