#!/usr/bin/env python3

# Filename: m_015_steppingmortor 
__author__ = "raspython"
__date__ = '2021/02/13 10:38'

import pigpio as pi
from time import sleep

"""
変数の定義
"""
# PIN_NOの定義
out_a1 = 6
out_a2 = 13
out_b1 = 19
out_b2 = 26

# 7seg_ledの点灯パターン
num_char = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7c,
            0x07, 0x7f, 0x67, 0x00]

# 1step毎の時間
# 100Hzとして0.01
sleep_time = 0.01

# step角を10倍したもの
step_angle = 18

# 位置決めステップのカウント数
step_count = 0

# モータードライバの管理変数
r_count = 0

# 出力GPIOのリスト
pin_l = [out_a1, out_a2, out_b1, out_b2]

# 出力の値のリスト
# 2相励磁の出力の値を順にリスト化(17PM-K044データーシートより)
# データーシートの表の並びはa b a^ b^の順なので注意
out_val = [0b1010, 0b0110, 0b0101, 0b1001]
# 出力の場所のリスト
out_pin = [0b1000, 0b0100, 0b0010, 0b0001]


"""
初期設定
"""
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

    print("キー入力のバイナリの値: {}".format(val_l))

    return val_l


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
    # print("ゼロパディング後: {}".format(l))

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

    for i, n in enumerate(l):
        if i == 1:
            # 7segLEDの下二桁目にデシマルポイントを付けるため
            # 表示の値に0x80を加算
            pi_g.i2c_write_byte_data(ht16k33_adr, i * 2, (num_char[n] | 0x80))
            # print(bin(num_char[n] | 0x80))
        else:
            pi_g.i2c_write_byte_data(ht16k33_adr, i * 2, num_char[n])
            # print(bin(num_char[n]))


def count_control(n):
    """
    r_countとstepカウントをインクリメントもしくはデクリメントする
    @param n:変化させる値(int)
    """
    global r_count
    global step_count

    # _countの値は0～7の間でループさせる
    r_count += n
    if r_count > 3:
        r_count = 0
    elif r_count < 0:
        r_count = 3

    step_count += n

    print("r_count: {}, step_count: {}".format(r_count, step_count))


def rotation():
    """
    回転制御2相励磁のローテーションの場所の出力値をGPIOで出力する
    """

    # 出力の値に上位1bit目から順番に1を積算して行き、各々のPINの出力を決める
    for i in range(4):
        # 出力の値を渡すのに該当桁が一桁目になるようにビットシフト
        out = (out_val[r_count] & out_pin[i]) >> (3 - i)
        pi_g.write(pin_l[i], out)
        print(bin(out_val[r_count] & out_pin[i]))
        print("GPIO_{}の出力 , {}".format(pin_l[i], out))


def jog(flag):
    """
    ステップ数が0から400の間ならインクリメントとデクリメント制御
    黄色、もしくは橙のスイッチが押された場合count_control()を呼ぶ
    黄色: 1づつインクリメント
    橙  : 1づつデクリメント
    その後モーターの回転制御関数を呼ぶ。
    @param flag: 回転方向の値(int)
    @return:
    """
    if step_count < 400 and flag == 1:
        count_control(flag)
    elif step_count > 0 and flag == -1:
        count_control(flag)

    rotation()


def control():
    """
    制御部分
    押されたスイッチによって制御する関数を呼び出す。
    制御間隔は変数で決めた値
    """
    while True:
        # ステップ数にステップ角の10倍の18
        zero_padding(step_count * step_angle)

        key_l = key_val()
        if key_l[2] == 0b010:
            jog(1)
        elif key_l[2] == 0b100:
            jog(-1)

        if key_l[0] == 2:
            break

        sleep(sleep_time)




def main():
    # モーターの初期位置をa1のみが出力の場所からスタート
    rotation()

    # キーマトリクスの読み込み初期化
    key_l = key_val()


    try:
        while True:
            # 黒のスイッチが押されたらスタート
            if key_l[0] == 0b001:
                print("スタート")
                control()

            # 白のスイッチが押されたら終了処理
            if key_l[0] == 2:
                print("終了処理")
                break
            # キーマトリクスの読み込み
            key_l = key_val()

            sleep(0.1)

    except KeyboardInterrupt:
        pass

    # 終了処理
    pi_g.write(out_a1, 0)
    pi_g.write(out_a2, 0)
    pi_g.write(out_b1, 0)
    pi_g.write(out_b2, 0)
    for i in range(4):
        pi_g.i2c_write_byte_data(ht16k33_adr, i * 2, num_char[10])
    pi_g.stop()


if __name__ == '__main__':
    main()
