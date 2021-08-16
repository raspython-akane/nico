#!/usr/bin/env python3

# Filename: m_018_pulse_oximeter 
__author__ = "raspython"
__date__ = '2021/08/15 20:09'

import pigpio as pi
from time import sleep
import el_display


# pinの定義
int_pin = 26

# データの取得回数
sampling = 1000

# カウンタ変数
count_var = 0

# GPIOの初期設定
pi_g = pi.pi()
# 入力設定
pi_g.set_mode(int_pin, pi.INPUT)

# max30102のi2C設定
# 1はbus番号、0x57はスレーブアドレス
max30102_adr = pi_g.i2c_open(1, 0x57)

def reset():
    """
    データの各レジスタをパワーオン状態にリセットする
    レジスタアドレス0x09に0x40を与える
    """
    pi_g.i2c_write_byte_data(max30102_adr, 0x09, 0x40)

def read_date(pin, status, tick):
    """
    FIFOデータレジスタを読みこむ。
    """
    global count_var

    red = None
    ir = None

    # New FIFO Data Readyを読み込んで割り込みをクリアする
    reg_date1 = pi_g.i2c_read_byte_data(max30102_adr, 0x00)
    # Internal Temperature Ready Flagを読み込んでクリアする
    reg_date2 = pi_g.i2c_read_byte_data(max30102_adr, 0x01)


    read_d = pi_g.i2c_read_i2c_block_data(max30102_adr, 0x07, 6)
    # print("FIFI date regの値: {}".format(read_d))
    # 1byteデータをシフトし、3byte(24bit)のデータにして下位18bitでマスクする
    # 18bitなのはpulse widthが411μs samples per second が100の値の為
    red = (read_d[1][0] << 16 | read_d[1][1] << 8 | read_d[1][2]) & 0b0011_1111_1111_1111_1111
    ir = (read_d[1][3] << 16 | read_d[1][4] << 8 | read_d[1][5]) & 0b0011_1111_1111_1111_1111

    print(red, ir)
    count_var += 1

    return read_d

def shutdown():
    """
    シャットダウンコントロール処理
    """
    pi_g.i2c_write_byte_data(max30102_adr, 0x09, 0x80)

def main():
    # データレジスタの初期化
    reset()
    sleep(1)

    # レジスタの設定
    # 割り込み制御の設定
    pi_g.i2c_write_byte_data(max30102_adr, 0x02, 0xc0)
    pi_g.i2c_write_byte_data(max30102_adr, 0x03, 0x00)

    # FIFOセッティング
    # FIFO Write Pointer
    pi_g.i2c_write_byte_data(max30102_adr, 0x04, 0x00)
    # FIFO Overflow Counter
    pi_g.i2c_write_byte_data(max30102_adr, 0x05, 0x00)
    # FIFO Read Pointer
    pi_g.i2c_write_byte_data(max30102_adr, 0x06, 0x00)
    # FIFO Configuration
    pi_g.i2c_write_byte_data(max30102_adr, 0x08, 0x4f)
    # mode control
    pi_g.i2c_write_byte_data(max30102_adr, 0x09, 0x03)
    # SpO2 Configuration
    pi_g.i2c_write_byte_data(max30102_adr, 0x0a, 0x27)
    # LED1の電流設定
    pi_g.i2c_write_byte_data(max30102_adr, 0x0c, 0x24)
    # LED2の電流設定
    pi_g.i2c_write_byte_data(max30102_adr, 0x0d, 0x24)
    # pilotLEDの電流設定
    pi_g.i2c_write_byte_data(max30102_adr, 0x10, 0x7f)
    # Power Ready Flagを読みこんで初期化
    reg_date1 = pi_g.i2c_read_byte_data(max30102_adr, 0x00)

    try:
        """
        while count_var < sampling:
            # 割り込み信号が立下り時に読み込み関数を呼ぶ
            cb = pi_g.callback(int_pin, pi.FALLING_EDGE, read_date)
        """
        for i in range(1000):
            while pi_g.read(int_pin) == 1:
                pass
            read_date(0,0,0)



    except KeyboardInterrupt:
        pass

    # cb.cancel()
    shutdown()
    pi_g.stop()

if __name__ == '__main__':
    main()
