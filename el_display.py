#!/usr/bin/env python3

# Filename: SO1602A
__author__ = "raspython"
__date__ = '2021/04/04 06:43'

import pigpio as pi
from time import sleep


class SO1602A:

    def __init__(self):

        # pigpioの用意
        self.pi_g = pi.pi()

        # I2Cの設定
        # 1はbus番号、0x3cはスレーブアドレス。
        self.so1602_adr = self.pi_g.i2c_open(1, 0x3c)

        self.clear_display()
        self.return_home()
        self.display_method()
        self.display_set()
        self.print_line()


    """
    setting
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


    def display_method(self, reverse=False, one_character=False):
        """
        カーソルの移動方向を設定 Trueならカーソルから逆方向へ表示
        one_charcterはなんやこれ？
        @param reverse: カーソルの移動方向 Trueで右 Falseで左へシフト
        @param one_character:よくわからん！さわるな！
        """
        self.val = 0x06
        if reverse:
            self.val -= 0x02
        if one_character:
            self.val += 0x01

        # 設定を流す
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, self.val)


    def display_set(self, display=True, cursor=True,  blink=True):
        """
        ディスプレイの表示設定
        @param display: ディスプレイの表示設定 default = True
        @param cursor: カーソルの表示 default = True
        @param blink:  カーソル位置の点滅 default = True
        """

        self.val= 0x08
        # ディスプレイの表示
        if display:
            self.val += 0x01
        # カーソルの表示
        if cursor:
            self.val += 0x02
        # カーソル位置の点滅表示
        if blink:
            self.val += 0x04

        # 設定を流す
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, self.val)


    def cursor_display_shift(self, right_shift=True, display_shift=False):
        """
        カーソルの移動
        @param r_l:
        @return:
        """
        self.val = 0x10
        if right_shift:
            self.val += 0x04
        if display_shift:
            self.val += 0x08

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


    """
    文字の書き込み
    """


    def print(self, s, time=0):
        """
        ディスプレイに表示する
        @param s: 表示する文字列
        @param time: 文字毎の表示ディレイ default = 0
        """
        l = s.encode("shift_jis")

        for i in l:
            self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x40, i)
            sleep(time)




def main():
    pass


if __name__ == '__main__':
    main()
