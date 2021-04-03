#!/usr/bin/env python3

# Filename: m_016_loadsell 
__author__ = "raspython"
__date__ = '2021/03/28 09:05'

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

# asciiの半角カナを使いたいためshift_jisにエンコードした値を渡す
l = "ABCDEabcdef##$$%%&$#ｱｲｳｴｵ".encode("shift_jis")
l = "ｱﾀﾏ\xf8\xf8".encode("shift_jis")
for i in l:
    pi_g.i2c_write_byte_data(so1602_adr, 0x40, i)


"""
EMULATE_HX711 = False

# 補正値
# referenceUnit = 1 #default
referenceUnit = 370

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711


def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()

    print("Bye!")
    sys.exit()


hx = HX711(5, 6)

# 何らかの理由で、python、numpy、hx711自体のバージョンによって、バイトの順番が常に同じではないことがわかりました。
# なぜそれが変わるのかを解明する必要があります。
# もし、超ランダムな値を経験しているなら、これらの値をMSBまたはLSBに変更すると、より安定した値を得ることができます。
# ビットとバイトの順番をデバッグして記録するコードが以下にあります。
# 最初のパラメータは、"long "の値を構築するために使用されるバイトの順序です。
# 2番目のパラメータは、各バイトに含まれるビットの順序です。
# HX711のデータシートによると、2番目のパラメータはMSBなので、変更する必要はありません。
hx.set_reading_format("MSB", "MSB")

# 基準単位を1にするには センサーなどに1kgを付けて、その重さを正確に知る。
# この場合、92は1グラムです。なぜなら、1を基準単位とした場合、重さがない状態では0に近い数字が得られるからです。
# そして2kgを加えると184000前後の数値が得られました。そこで、3分の1の法則によると
# 2000グラムが184000なら、1000グラムは184000 / 2000 = 92。
# hx.set_reference_unit(113)
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")

# 両方のチャンネルを使うには、両方を風袋引きする必要があります
# hx.tare_A()
# hx.tare_B()
"""


def main():

    """

    while True:
        try:
            # これらの3行は、読み込みフォーマットにMSBとLSBのどちらを使うかをデバッグするのに便利です。
            # hx.set_reading_format("LSB", "MSB") "の最初のパラメータのためのものです。
            # "val = hx.get_weight(5) "と "print val "の2行をコメントし、以下の3行をアンコメントして何が表示されるか確認します。

            # np_arr8_string = hx.get_np_arr8_string()
            # binary_string = hx.get_binary_string()
            # print binary_string + " " + np_arr8_string

            # 重さを表示します。MSBとLSBの問題をデバッグしている場合はコメントしてください。

            val = hx.get_weight(5)
            print(val)

            # 両方のチャンネルから重量を得るには（ロードセルをチャンネルAとBの両方に # 接続している場合）、次のようにします。
            # 両方のチャンネルから重量を得るには、次のようにします。
            # val_A = hx.get_weight_A(5)
            # val_B = hx.get_weight_B(5)
            # print "A: %s B: %s" % ( val_A, val_B )

            hx.power_down()
            hx.power_up()
            sleep(0.1)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()

    """



if __name__ == '__main__':
    main()
