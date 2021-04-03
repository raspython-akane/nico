#!/usr/bin/env python3

# Filename: SO1602A
__author__ = "raspython"
__date__ = '2021/04/04 06:43'

import pigpio as pi


class SO1602A():

    def __init__(self):
        """
        初期化
        """
        # pigpioの用意
        self.pi_g = pi.pi()

        # I2Cの設定
        # 1はbus番号、0x3cはスレーブアドレス。
        self.so1602_adr = self.pi_g.i2c_open(1, 0x3c)

        self.clear_display()
        self.return_home()
        self.display_on()


    def clear_display(self):
        """
        Clear Display
        """
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x01)


    def return_home(self):
        """
        Return Home
        """
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x02)


    def display_on(self):
        """
        表示設定
        パラメータ 0000 01DCB

        D = 1 ディスプレイON
        D = 0 ディスプレイOFF

        C = 1 カーソルON
        C = 0 カーソルOFF

        B = 1 カーソル位置を点滅させる
        B = 0 カーソル位置を点滅させない

        """
        self.pi_g.i2c_write_byte_data(self.so1602_adr, 0x00, 0x0f)





def main():
    pass


if __name__ == '__main__':
    main()
