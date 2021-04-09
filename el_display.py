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
        @param r_l:
        """
        self.val = 0x10
        if right_shift:
            self.val += 0x04

        # 設定を流す
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, self.val)


    def display_shift(self, right_shift=True):
        """
        表示を移動させる
        @param right_shift:
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


    def scroll_enable(self, hs1=True, hs2=True, hs1and2=True):
        """

        @param hs1:
        @param hs2:
        @param hs1and2:
        @return:
        """
        self.val = 0x10
        if hs1and2:
            self.val += 0x1f
        if hs1and2 == False and hs1:
            self.val += 0x04
        if hs1and2 == False and hs2:
            self.val += 0x02


        # REとISのflag ON
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x2b)

        # スクロールする、行の変更。
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, self.val)

        # REとISのflag OFF
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x28)


    def shift_enable(self, first_line=True, second_line2=True, all=True):
        """

        @param hs1:
        @param hs2:
        @param hs1and2:
        @return:
        """
        if all:
            self.val = 0x13
        if first_line:
            self.val = 0x11
        if second_line2:
            self.val = 0x12

        # RE flag ON
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x2a)

        #
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x1d)

        # REのflag OFF
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x28)


        """
        *** ISとREのフラグについて ***
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

    """
    文字の書き込み
    """

    def print(self, s, time=0):
        """
        ディスプレイに表示する
        @param s: 表示する文字列
        @param time: 文字毎の表示ディレイ単位ms  default = 0
        """
        l = s.encode("shift_jis")

        for i in l:
            self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x40, i)
            sleep(time / 1000)



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

    # 表示する文字
    p_word = "ｱｶﾈﾁｬﾝｶﾜｲｲﾔｯﾀｰ      ｱｵｲﾁｬﾝｶﾜｲｲﾔｯﾀｰ"

    # メニュー文字の決定
    m_word_lr = lambda bool: "右" if bool else "左"
    m_word_onoff = lambda bool: "ON" if bool else "OFF"

    # インスタンスを表すオブジェクトを渡すためインスタンス化
    # pythonのクラス言語使用は通常のメソッドでは、第一引数はそのクラスのインスタンス
    # を表すオブジェクトを受け取る(self)
    so1602 = So1602a()

    while True:
        # メニューの表示文字の設定
        set_w_02 = m_word_lr(flag_02)
        set_w_03 = m_word_onoff(flag_03)
        set_w_08 = m_word_onoff(flag_08)
        set_w_09 = m_word_onoff(flag_09)
        set_w_10 = m_word_onoff(flag_10)
        set_w_11 = m_word_onoff(flag_11)

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


50: ｱｶﾈﾁｬﾝｶﾜｲｲﾔｯﾀｰの表示

99: 終了
***

""".format(set_w_02, set_w_03, set_w_08, set_w_09, set_w_10, set_w_11)))

        # so1602.scroll_enable(False, False, True)
        so1602.shift_enable(False, True, False)

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
            print("スライド表示の変更")
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
            so1602.display_on_off_control(True, flag_09, flag_10)

        if n == 10:
            print("点滅の表示設定")
            flag_10 = not flag_10
            so1602.display_on_off_control(True, flag_09, flag_10)

        if n == 11:
            print("ディスプレイの表示設定")

        if n == 50:
            so1602.print(p_word, 100)


        if n == 99:
            # ディスプレイ表示をクリア
            so1602.clear_display()
            # ディスプレイ、カーソル、点滅表示を消灯
            so1602.display_on_off_control(display=False, cursor=False, blink=False)
            break



if __name__ == '__main__':
    main()
