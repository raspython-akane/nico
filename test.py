import pigpio as pi
from time import sleep
import sys

"""
初期設定
"""
pi_g = pi.pi()

# I2Cの設定
# 1はbus番号、0x3cはスレーブアドレス。
so1602_adr = pi_g.i2c_open(1, 0x3c)


# ディスプレイの初期化(秋月の説明書より)
"""
このモジュールはリセット後に内部で初期設定を行っており
通常は「Display ON」コマンドのみで使用できますが、リセット後に
「Clear Display」「Return Home」コマンドを実行する事をお勧めいたします。
"""

# 関数の値は(スレーブアドレス, コマンド送信の値0x00, コマンドの値)

# Clear Display
pi_g.i2c_write_byte_data(so1602_adr, 0x00, 0x01)
# Return Home
pi_g.i2c_write_byte_data(so1602_adr, 0x00, 0x02)
# Display On
pi_g.i2c_write_byte_data(so1602_adr, 0x00, 0x0f)

print("ｱ".encode("shift_jis"))
print(b"ABCDEF")