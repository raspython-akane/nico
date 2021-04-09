#!/usr/bin/env python3

# Filename: el_display
__author__ = "raspython"
__date__ = '2021/04/04 06:43'

import pigpio as pi
from time import sleep


class So1602a:

    def __init__(self):
        """
        コンストラクタ
        """
        # pigpioの用意
        self.pi_g = pi.pi()

        # I2Cの設定
        # 1はbus番号、0x3cはスレーブアドレス。
        self.so1602_adr = self.pi_g.i2c_open(1, 0x3c)

        # ディスプレイをON
        self.display_on_off_control()
        # ディスプレイ表示をクリア
        self.clear_display()
        # カーソルを左上へ
        self.return_home()
        # 表示後のカーソル移動の方向とスライド表示設定
        self.entry_mode()
        # 表示ライン数と拡大表示の設定
        self.print_line()
        # コントラストの設定
        self.contrast_control(0xff)


    """
    コマンド
    """

    def clear_display(self):
        """
        ディスプレイ表示をクリアする
        """
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x01)
        # print("ディスプレイの表示をクリア")


    def return_home(self):
        """
        カーソルを左上に戻す
        """
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x02)
        # print("カーソルを初期値へ")


    def entry_mode(self, right_shift=True, slide=False):
        """
        文字を表示してからのカーソル位置の移動方向の設定と
        スライド表示表示する設定
        スライド方向は右側から固定
        スライド設定をした場合はカーソルの移動方向は右側の設定になる

        @param right_shift: カーソルの移動方向。Trueなら右
        @param right_shift: スライド設定
        """
        self.val = 0x04
        if right_shift:
            self.val = 0x06
        elif right_shift == False and self.val == 0x06:
            self.val = 0x04

        if slide:
            self.val = 0x07
        elif slide == False and right_shift:
            self.val = 0x06

        # 設定を流す
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, self.val)


    def display_on_off_control(self, display=True, cursor=True,  blink=True):
        """
        ディスプレイの表示設定
        @param display: ディスプレイの表示設定
        @param cursor: カーソルの表示の設定
        @param blink:  カーソル位置の点滅表示の設定
        """

        self.val= 0x08

        # カーソル位置の点滅表示
        if blink:
            self.val += 0x01
        # カーソルの表示
        if cursor:
            self.val += 0x02
        # ディスプレイの表示
        if display:
            self.val += 0x04

        # 設定を流す
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, self.val)


    def cursor_shift(self, right_shift=True):
        """
        カーソルの移動
        @param r_l: 移動flag
        """
        self.val = 0x10
        if right_shift:
            self.val += 0x04

        # 設定を流す
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, self.val)


    def display_shift(self, right_shift=True):
        """
        表示を移動させる
        @param right_shift: 表示flag
        """
        self.val = 0x18
        if right_shift:
            self.val += 0x04

        # 設定を流す
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, self.val)


    def print_line(self, tow_line=True, double_high=False):
        """
        表示ラインと表示の高さ設定
        double_highにする場合は表示は2LINEにする
        @param towline: 文字を表示するライン default = 2LINE
        @param double_high: 文字のフォントの高さ default = 1LINE
        """
        self.val = 0x20
        # 表示ラインの設定
        if tow_line:
            self.val += 0x08
        if double_high:
            self.val += 0x04

        # 設定を流す
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, self.val)


    def shift_enable(self, first_line=True, second_line2=True, all=True):
        """
        スクロールをする行を決定する
        @param first_line: 1行目
        @param second_line2: 2行目
        @param all: どっちもO
        @return:
        """
        if all:
            self.val = 0x13
        elif first_line:
            self.val = 0x11
        elif second_line2:
            self.val = 0x12

        # display shift enableをONする準備
        # REのflag ON
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x2a)

        # display shift enableをON
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x1d)

        # REのflag OFF
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x28)


        """
        *** ISフラグについて ***
        0x29でREとISを同時にONはできない
        REの変更の値が1の時点でextended fanction setになるので
        RE変更フラグが0の0x29でISのフラグを立ててからREのフラグを変更する
        フラグを戻す時もREに0の変更を与えて拡張設定をOFFしてからISのフラグを切る
        """
        # ISのflagをON
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x29)

        # REのflag ON
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x2a)

        # スクロールする、行の変更。
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, self.val)

        # REのflag OFF
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x28)

        # ISのFlagをOFF
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x28)


        # display shift enableをFFする準備
        # REのflag ON
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x2a)

        # display shift enableをOFF
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x1c)

        # REのflag OFF
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x28)


    def contrast_control(self, n=0x7f):
        """
        コントラストの設定
        @contrastの値にコントラストを変更する
        @param n: コントラストの値
        """
        contrast = n
        # RE flag ON
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x2a)
        # SD flag ON
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x79)

        # contrastの値の変更
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x81)
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, contrast)

        # SD flag OFF
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x78)
        # RE flag OFF
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x28)


    def fade_out_blinking(self, fade=False, blink=False, frames=0b0001):
        """
        文字をフェードアウトまたは点滅させる
        フェードアウトと点滅は両立できない
        タイミングの時間はコマンドで与える下位4bitで決定
        ----------------
        0000b 8Frames
        0001b 16Frames
        :     :
        1110b 120Frames
        1111b 126Frames
        ----------------

        @param fade:  フェードflag
        @param blink:  点滅flag
        @param frames: フェードする時間設定
        """
        # RE flag ON
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x2a)
        # SD flag ON
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x79)

        # 点滅の設定
        if blink:
            self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x23)
            self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, (0b00110000 | frames))

        # フェードの設定
        elif fade:
            self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x23)
            self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, (0b00100000 | frames))

        else:
            self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x23)
            self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, (0b00000000))


        # SD flag OFF
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x78)
        # RE flag OFF
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x28)




    """
    文字の書き込み
    """

    def print(self, s, time=0, slide_flag=False):
        """
        ディスプレイに表示する
        @param s: 表示する文字列
        @param time: 文字毎の表示ディレイ単位ms  default = 0
        """
        l = s.encode("shift_jis")

        for i, s in enumerate(l):
            if i < 20 and slide_flag:
                self.shift_enable(True, False, False)
            # 2行目以降の表示の時は1行目はスライドさせない
            if i > 19 and slide_flag:
                self.shift_enable(False, True, False)

            self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x40, s)
            sleep(time / 1000)
        self.shift_enable(False, False, True)



def main():

    """
    変数設定
    """
    flag_02 = True
    flag_03 = False
    flag_08 = False
    flag_09 = True
    flag_10 = True
    flag_11 = True
    flag_12 = 2
    flag_13 = False
    flag_14 = False

    # 表示する文字
    p_word = "ｱｶﾈﾁｬﾝｶﾜｲｲﾔｯﾀｰ      "
    p_aka_ao = "ｱｶﾈﾁｬﾝｶﾜｲｲﾔｯﾀｰ      ｱｵｲﾁｬﾝｶﾜｲｲﾔｯﾀｰ      "

    # メニュー文字の設定
    m_word_lr = lambda bool: "右" if bool else "左"
    m_word_onoff = lambda bool: "ON" if bool else "OFF"

    # インスタンスを表すオブジェクトを渡すためインスタンス化
    # pythonのクラス言語使用は通常のメソッドでは、第一引数はそのクラスのインスタンス
    # を表すオブジェクトを受け取る(self)
    so1602 = So1602a()

    while True:

        # メニュー文字の決定
        set_w_02 = m_word_lr(flag_02)
        set_w_03 = m_word_onoff(flag_03)
        set_w_08 = m_word_onoff(flag_08)
        set_w_09 = m_word_onoff(flag_09)
        set_w_10 = m_word_onoff(flag_10)
        set_w_11 = m_word_onoff(flag_11)
        if flag_12 == 2 and flag_03 == True:
            set_w_12 = "両方ON"
        elif flag_12 == 0:
            set_w_12 = "1行目ON"
        elif flag_12 == 1:
            set_w_12 = "2行目ON"
        else:
            set_w_12 = "両方OFF"
        set_w_13 = m_word_onoff(flag_13)
        set_w_14 = m_word_onoff(flag_14)

        # メニューの表示
        n = int(input(
"""

***
0 : ディスプレイの初期化
1 : カーソルを初期位置に移動
2 : 文字の表示方向の変更       【カーソルの{}側に表示】
3 : スライドして表示の設定     【{}】
4 : カーソルを右へ移動
5 : カーソルを左へ移動
6 : ディスプレイ表示を右へシフト
7 : ディスプレイ表示を左へシフト
8 : double_high                【{}】
9 : アンダーカーソルの表示     【{}】
10: ブロックカーソルの表示     【{}】
11: ディスプレイの表示を消す   【{}】
12: シフトさせる行の設定       【{}】
13: 文字のフェードアウト       【{}】
14: 文字の点滅                 【{}】


50: ｱｶﾈﾁｬﾝｶﾜｲｲﾔｯﾀｰの表示

99: 終了
***

""".format(set_w_02, set_w_03, set_w_08, set_w_09, set_w_10, set_w_11,
           set_w_12, set_w_13, set_w_14)))


        # 設定
        if n == 0:
            print("ディスプレイの初期化")
            so1602.clear_display()

        if n == 1:
            print("カーソルを初期位置に移動")
            so1602.return_home()

        if n == 2:
            print("表示方向の変更")
            flag_02 = not flag_02
            if flag_02:
                so1602.entry_mode(flag_02)

            else:
                so1602.entry_mode(flag_02)

        if n == 3:
            print("スライドイン表示の変更")
            flag_03 = not flag_03
            if flag_03:
                # 左からスライド固定の為表示方向flagはTrueにする
                flag_02 = True
                so1602.entry_mode(flag_02, True)

            else:
                so1602.entry_mode(flag_02, False)

        if n == 4:
            print("カーソルをを右へシフト")
            so1602.cursor_shift()

        if n == 5:
            print("カーソルを左へシフト")
            so1602.cursor_shift(False)

        if n == 6:
            print("ディスプレイ表示を右へシフト")
            so1602.display_shift()

        if n == 7:
            print("ディスプレイ表示を左へシフト")
            so1602.display_shift(False)

        if n == 8:
            print("double_high変更")
            flag_08 = not flag_08
            so1602.print_line(double_high=flag_08)

        if n == 9:
            print("カーソルの表示設定")
            flag_09 = not flag_09
            so1602.display_on_off_control(flag_11, flag_09, flag_10)

        if n == 10:
            print("点滅の表示設定")
            flag_10 = not flag_10
            so1602.display_on_off_control(flag_11, flag_09, flag_10)

        if n == 11:
            print("ディスプレイの表示設定")
            flag_11 = not flag_11
            so1602.display_on_off_control(flag_11, flag_09, flag_10)

        if n == 12:
            print("スライドさせる行の変更")
            flag_12 = (flag_12 + 1)% 3

            # print(flag_12)
            if flag_12 == 2:
                so1602.shift_enable(False, False, True)
            elif flag_12 == 1:
                so1602.shift_enable(False, True, False)
            elif flag_12 == 0:
                so1602.shift_enable(True, False, False)

        if n == 13:
            print("フェードの設定")
            flag_13 = not flag_13
            # 点滅がONならOFFにする
            if flag_14:
                flag_14 = not flag_14
            so1602.fade_out_blinking(flag_13, flag_14)

        if n == 14:
            print("点滅設定")
            flag_14 = not flag_14
            # フェードがONならOFFにする
            if flag_13:
                flag_13= not flag_13
            so1602.fade_out_blinking(flag_13, flag_14)

        if n == 50:
            flag_12 = 2
            so1602.print(p_word, 100)

        if n == 51:
            flag_12 = 2
            so1602.print(p_aka_ao, 100, flag_03)


        if n == 99:
            # ディスプレイ表示をクリア
            so1602.clear_display()
            # ディスプレイ、カーソル、点滅表示を消灯
            so1602.display_on_off_control(display=False, cursor=False, blink=False)
            break



if __name__ == '__main__':
    main()
