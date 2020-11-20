#!/usr/bin/env python3
# Filename: m_010_7seg_counter
__author__ = "raspython"
__date__ = '2020/11/09 09:12'

import wiringpi as pi
from time import sleep


"""
I2Cの設定(wiringpi)
"""
pi.wiringPiSetupGpio()
i2c = pi.I2C()
# スレーブアドレスを代入
ht16k33_adr = i2c.setup(0x70)
# レジスタの設定
# efの値は20Hだが、書き込みの先頭アドレスはD8
# からなので0ｘ21
# 内部システム発信機の有効
i2c.writeReg8(ht16k33_adr, 0x21, 0x01)
# LEDの表示設定の有効
i2c.writeReg8(ht16k33_adr, 0x81, 0x01)
# INT/LOWの出力はLOW
i2c.writeReg8(ht16k33_adr, 0xa1, 0x00)



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
    # n_list.reverse()
    # 7segLEDに表示
    for i, num in enumerate(n_list):
        i2c.writeReg8(ht16k33_adr, i * 2, p_char[num])
        # print("{}桁目の表示 【{}】".format(i + 1, n_list[i]))


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
    # print("ゼロパディング後 {}".format(zero_p))

    # ゼロパディングされた値をint型にしてlistに格納
    n_list = [int(n) for n in list(zero_p)]
    # print("リスト入れた後 {}".format(n_list))

    # 表示用にリストを逆順にする
    n_list.reverse()

    # 7segLED表示
    led_flash()


def key_inp_val():
    """
    キーマトリクスの入力の値をリストに入れて返す
    アドレスをすべて読みこむとHTK16K33の値は初期化される
    @return:レジスタの値のリスト
    @rtype: list
    """
    # キーマトリクス入力データーのアドレスリスト
    # 黒白赤は0x40、青黄橙は0x42
    adr_l = [0x40, 0x41, 0x42, 0x43, 0x44, 0x45]

    v_l = []
    for i in adr_l:
        v_l.append(i2c.readReg8(ht16k33_adr, i))

    # print(v_l)
    return v_l


def matlix_key():
    """
    実行部、
    ボタン黒を押されたら入力開始
    ボタン白を押されたら終了処理
    赤、青、黄、橙を押されたら対応の数字を加算して表示
    """
    try:

        # ボタンの色の入力の値
        black = 0b00000001
        white = 0b00000010
        red = 0b00000100
        blue = 0b00000001
        yellow = 0b0000010
        orange = 0b0000100
        """
        print("黒{} 白{} 赤{} 青{} 黄{} 橙{}"
              .format(bin(black), bin(white), bin(red),
                      bin(blue), bin(yellow), bin(orange)))
        """

        # ボタンを押して表示する値
        orange_num = 0b00000001
        yellow_num = 0b00000010
        blue_num = 0b00000100
        red_num = 0b00001000

        # キーマトリクスの入力の値の初期化
        # 一度読みこんでレジスタの値をリセットする
        key_inp_val()

        # 表示flag
        p_flag = False

        # 表示する数字
        p_num = 0

        # ボタン白を押されるまでループ
        while True:

            # すべてのキーアドレスを読みこんだときに
            # INTの値がアクティブなら255を代入する
            act_f = i2c.readReg8(ht16k33_adr, 0x60)
            # print(act_f)

            # キーマトリクスの入力の値の読み込み
            # 0x40と0x42の値をそれぞれ変数に入れる
            val_l = key_inp_val()
            key_adr_40 = val_l[0]
            key_adr_42 = val_l[2]
            # print(key_adr_40, key_adr_42)

            # 黒スイッチを押されたらLED表示開始
            if key_adr_40 & black or p_flag:
                zero_p_list(p_num)
                p_flag = True

            # 黒ボタンを押され且つキーが押されている場合
            # 以下の処理をする

            if p_flag & (key_adr_40 > 0 or key_adr_42 > 0):

                # 赤、青、黄、橙のボタンのアクティブに
                # 対応した数字を加算して表示する
                if key_adr_42 & orange == orange:
                    p_num |= orange_num
                if key_adr_42 & yellow == yellow:
                    p_num |= yellow_num
                if key_adr_42 & blue == blue:
                    p_num |= blue_num
                if key_adr_40 & red == red:
                    p_num |= red_num
                print(p_num)

                # 白ボタンを押されたらループを抜ける
                if key_adr_40 & white == white:
                    p_num = 0
                    print("終了処理開始")
                    break

            # キーが押されてないなら0を表示
            else:
                p_num = 0

            # 白ボタンを押されたらループを抜ける
            if key_adr_40 & white == white:
                print("終了処理開始")
                break

            sleep(0.05)


    except KeyboardInterrupt:
        pass



def led_check():
    """
    7segLEDの表示チェック用
    数字4つを入力して表示させる
    0～10で入力
    10の入力で表示するのは"-"
    5秒表示して終了
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

    sleep(5)


"""
ほんへ
"""

def main():
    global n_list

    # 7segLED表示チェック。
    #通常時はコメントアウト
    # led_check()

    # マトリクス入力読み込み
    matlix_key()

    # LEDを消灯して終了処理
    n_list = [11, 11, 11, 11]
    led_flash()



if __name__ == '__main__':
    main()