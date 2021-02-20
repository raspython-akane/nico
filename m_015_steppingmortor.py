#!/usr/bin/env python3

# Filename: m_015_steppingmortor 
__author__ = "raspython"
__date__ = '2021/02/13 10:38'

import pigpio as pi
from time import sleep
from copy import copy

"""
変数の定義
"""
# PIN_NOの定義
out_a1 = 6
out_a2 = 13
out_b1 = 19
out_b2 = 26

mat_x = 23
mat_y = 24
mat_z = 25
mat_a = 12
mat_b = 16
mat_c = 20
mat_d = 21

# 7seg_ledの点灯パターン
num_char = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7c,
            0x07, 0x7f, 0x67, 0x00, 0x79]

# 1step毎の時間
# 100Hzとして0.01
sleep_time = 0.01

# step角を10倍したもの
step_angle = 18

# 位置決めステップのカウント数
step_count = 0

# モータードライバの管理変数
r_count = 0

# 入力角度の数字
inp_angle_n = [0, 0, 0, 0]

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


"""
関数定義
"""

def matrix_sw():
    """
    マトリクス入力は確認したいスイッチの
    x,y,z軸GPIO出力をLOW、そのほかをHIにした後
    a,b,c,dの入力を見てLOWになっているものが
    ボタンが押されているもの

    例 ヘッダーピンが上側の時、左上の確認したい場合
    zの出力 LOW
    yの出力 HI
    xの出力 HI

    の出力にして
    aのGPIOの入力がLOWになっていれば押下されている


    matrix入力の並び

    z_a y_a x_a
    z_b y_b x_b
    z_c y_c x_c
    z_d y_d x_d

    入力がチェックされるごとにカウントが1上がる
    入力がLOWになっているカウントをリストに入れかえす

    スイッチflag番号
    0  4  8
    1  5  9
    2  6  10
    3  7  11

    @return: 入力されたスイッチの場所の値を入れたリスト
    """
    count = 0
    inp_l = []

    y_out = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
    x = [mat_a, mat_b, mat_c, mat_d]

    # ｙ軸をzから順にLOW、そのほかをHIにする。
    for gpio_out in y_out:
        pi_g.write(mat_z, gpio_out[0])
        pi_g.write(mat_y, gpio_out[1])
        pi_g.write(mat_x, gpio_out[2])
        # x軸の入力チェック、入力されたカウントをリストに入れる
        # チェックごとにカウントが1上がる
        for x_axis in x:
            if pi_g.read(x_axis) == 0:
                inp_l.append(count)
            count += 1

    # print("入力ボタンのリスト {}".format(inp_l))

    return inp_l


def zero_padding(n):
    """
    与えられた数字を4桁で右寄せ0詰め
    0埋めしたものを桁毎にリストへ入れる
    そのリストをdisplay_charに渡す
    @param n:duty比
    @return: 0詰めしたリストを返す
    """
    # 右寄せ4桁0埋め(str)
    zero_p = str(n).zfill(4)

    # ゼロパディングした文字列を数値化しながらリストへ入れる。
    l = [int(n) for n in list(zero_p)]
    # print("ゼロパディング後: {}".format(l))

    return l



def display_char(l):
    """
    与えられた数字を7segLEDで表示する
    @param l: 表示する数字のlist
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
    r_countとstepカウントをカウントアップもしくはカウントダウンする
    @param n:変化させる値(int)
    """
    global r_count
    global step_count

    # _countの値は0～3の間でループさせる
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
    global motor_flag
    # モーター出力の為flagを1にする
    motor_flag = 1

    # 出力の値に上位1bit目から順番に1を積算して行き、各々のPINの出力を決める
    for i in range(4):
        # 出力の値を渡すのに該当桁が一桁目になるようにビットシフト
        out = (out_val[r_count] & out_pin[i]) >> (3 - i)
        pi_g.write(pin_l[i], out)
        print("GPIO_{}の出力 , {}".format(pin_l[i], out))

    # モーター出力が終わったのでflagを0に
    motor_flag = 0


def input_angle():
    """
    入力角度の変更
    入力モード中は入力桁以外の7segLEDを点滅させる
    入力角度は入力桁の値を8と9のスイッチでカウントアップダウン
    入力桁の移動は10、11のスイッチで左右に変える
    7番スイッチを押されたら入力終了
    """
    print("入力開始")
    # 入力角度の変数
    global inp_angle_n
    # 点滅フラグ
    flash_flag = 0
    # 入力桁の変数
    digits_num = 0

    while True:
        # キー入力の確認
        inp_l = matrix_sw()

        # 入力角度のリストを表示するときに逆順に変更するため
        # リストをコピーする
        char_l = copy(inp_angle_n)

        # 入力時は0.1秒ごと入力角度の入力桁数以外の桁を点滅させる
        # 入力パターン
        if flash_flag == 0:
            # print("入力角度は {}".format(char_l))
            display_char(char_l)
            flash_flag = 1
        # 消灯パターン
        else:
            for i in range(4):
                # 入力桁は点滅させない
                if i == digits_num:
                    # print(l)
                    pi_g.i2c_write_byte_data(ht16k33_adr, i * 2, num_char[char_l[3 - digits_num]])
                    # 下一桁目にはデシマルポイントを付ける
                    if i == 1:
                        pi_g.i2c_write_byte_data(ht16k33_adr, i * 2,
                                                 (num_char[char_l[3 - digits_num]] | 0x80))
                # 入力桁以外は消灯
                else:
                    # 下一桁目はデシマルポイントのみを表示
                    if i == 1:
                        pi_g.i2c_write_byte_data(ht16k33_adr, i * 2, 0x80)
                    else:
                        pi_g.i2c_write_byte_data(ht16k33_adr, i * 2, num_char[10])
            flash_flag = 0
        

        # 8番スイッチが押されたら入力角度の入力桁のカウントアップ
        if 8 in inp_l:
            inp_angle_n [3 - digits_num] += 1
            # 9を超えたら0に戻す
            if inp_angle_n[3 - digits_num] > 9:
                inp_angle_n[3 - digits_num] = 0
            print("入力変更後の入力角のリスト{}".format(inp_angle_n))
        # 9番スイッチが押されたら入力角度の入力桁のカウントダウン
        elif 9 in inp_l:
            inp_angle_n[3 - digits_num] -= 1
            # 0より小さくなったら9にする
            if inp_angle_n[3 - digits_num] < 0:
                inp_angle_n[3 - digits_num] = 9
            print("入力変更後の入力角のリスト{}".format(inp_angle_n))
        # 10番スイッチが押されたら入力桁を左へずらす
        elif 10 in inp_l:
            digits_num += 1
            # 入力桁が3より大きくなったら0へ戻す
            if digits_num > 3:
                digits_num = 0
            print("入力桁変更後の値 {}".format(digits_num))
        # 11番スイッチが押されたら入力桁を右へずらす
        elif 11 in inp_l:
            digits_num -= 1
            # 入力桁が0より小さくなったら3にする
            if digits_num < 0:
                digits_num = 3
            print("入力桁変更後の値 {}".format(digits_num))

        # 7番スイッチが押されたら入力終了
        if 7 in inp_l:
                # 角度の値のチェック
                if num_check(inp_angle_n) == 0:
                    inp_angle_n = [0, 0, 0, 0]

                print("入力終了")
                break

        sleep(0.3)


def num_check(l):
    """
    入力角度のチェック720より大きい場合はエラーを返す
    @param l:
    @return: 正常時はTrue,異常時はFaleを返す
    """
    print("入力角度のチェック")
    # 入力角度のチェック。720度より大きい場合はEを1秒間表示して入力角度に0を代入
    check = 0
    for i, j in enumerate(l):
        # リストのインデックス0から順に1000,100,10,1倍したものを加算
        # print(1000 / (10 ** i))
        check += j * (1000 / (10 ** i))
    if check > 7200:
        print("入力エラー")
        # EEEEの表示
        display_char([11, 11, 11, 11])
        sleep(3)

        return False

    else:
        return True


def step_cal(l=None):
    """
    入力角度からstep数を計算する。
    step数は四捨五入して整数にする。
    """
    angle = 0

    # 関数に値を渡されていないときはlにはinp_angle_nが入る
    if l is None:
        l = inp_angle_n

    # print("入力角度のリストの値 {}".format(inp_angle_n))
    # リストの値を数値に直して入力角を整数にする
    for i, j in enumerate(l):
        # リストのインデックス0から順に1000,100,10,1倍したものを加算
        # print(1000 / (10 ** i))
        angle += j * (1000 / (10 ** i))
    # print("入力角度の整数 {}".format(angle))
    # 四捨五入(roundは氏ね)
    step =  int((((angle * 10) / step_angle) + 5) / 10)
    # print("入力角度への移動step数 {}".format(step))

    move_to_angle(step)


def move_to_angle(step):
    """
    現在のstep数から入力角度のstep数への移動指示
    @param step: 入力角度のステップ数
    @return:
    """
    while True:
        # 現在角度の表示
        l = zero_padding(step_count * step_angle)
        display_char(l)

        # 移動先step数と現在のstep数が同じなら何もしないで抜ける
        if step == step_count:
            break
        # CW方向
        elif step > step_count:
            print("CWへ移動残り {}step".format(step - step_count))
            count_control(1)
        # CCW方向
        elif step < step_count:
            print("CCWへ移動残り {}step".format(step_count - step))
            count_control(-1)

        # 回転指示
        rotation()

        sleep(sleep_time)


def read_txt():
    """
    step.txtの中の角度を数値化してstep数計算関数に渡す
    """
    angle_list = []
    try:
        # テキストファイルから読み込み
        with open("step.txt", "r", encoding="UTF-8") as inp_txt:
            # 行ごとに数値に変換
            for txt in inp_txt:
                    # 数字の場合は数値化してリストへ格納
                    try:
                        # print("数値化する値 {}".format(txt))
                        # 入力は小数点第一位まであるので
                        # 10倍して整数にする
                        angle = [int(float(i) * 10) for i in txt.split()]
                        angle_list.append(angle[0])

                        # print("テキストから読みこんだ値のリスト {}".format(angle_list))
                    # 数字じゃないときはエラー表示して抜ける
                    # 入力されたリストは空にする
                    except ValueError:
                        print("step.txtエラー")
                        display_char([11, 11, 11, 11])
                        sleep(3)
                        angle_list = []
                        break

            # 数値化したリストの中身を順に0埋め関数に渡してリスト化
            for i in angle_list:
                l = zero_padding(i)
                print("step.txtの{}を桁ごとにリスト化 {}".format(i, l))

                # リスト化したものをstep計算関数へ渡す。
                step_cal(l)
                sleep(1)

    except FileNotFoundError:
        print("設定ファイルが見つかりません")


def jog(flag):
    """
    ステップ数が0から400の間ならインクリメントとデクリメント制御
    黄色、もしくは橙のスイッチが押された場合count_control()を呼ぶ
    黄色: 1づつカウントアップ
    橙  : 1づつカウントダウン
    その後モーターの回転制御関数を呼ぶ。
    @param flag: 回転方向の値(int)
    """
    # CW方向
    if step_count < 400 and flag == 1:
        count_control(flag)
    # CCW方向
    elif step_count > 0 and flag == -1:
        count_control(flag)

    # 回転指示
    rotation()


def control():
    """
    制御部分
    押されたスイッチによって制御する関数を呼び出す。
    制御間隔は変数で決めた値
    """

    while True:
        # 現在角度の表示
        l = zero_padding(step_count * step_angle)
        display_char(l)

        # キーマトリクスのチェック
        inp_l = matrix_sw()

        # スイッチ3が押されたら角度入力
        if 3 in inp_l:
            input_angle()
        # スイッチ1が押されたら入力角からstep数を計算し移動
        elif 1 in inp_l:
            step_cal()
        # スイッチ5が押されたらテキストの入力角へ順次移動
        elif 5 in inp_l:
            read_txt()
        # スイッチ2が押されたらCW方向にjog運転
        elif 2 in inp_l:
            jog(1)
        # スイッチ6が押されたらCCW方向にjog運転
        elif 6 in inp_l:
            jog(-1)

        if 4 in inp_l:
            break

        sleep(sleep_time)


def main():
    # モーターの初期位置をa1のみが出力の場所からスタート
    rotation()

    try:
        while True:
            
            # 黒のスイッチが押されたらスタート
            inp_l = matrix_sw()
            if 0 in inp_l:
                print("スタート")
                control()

            # 白のスイッチが押されたら終了処理
            inp_l = matrix_sw()
            if 4 in inp_l:
                print("終了処理")
                break

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
