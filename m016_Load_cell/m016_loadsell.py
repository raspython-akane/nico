#!/usr/bin/env python3

# Filename: m016_loadsell 
__author__ = "raspython"
__date__ = '2021/06/29 19:11'

import el_display
import time
import sys

EMULATE_HX711 = False

referenceUnit = 368

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711


def cleanAndExit():
    print("終了処理中...")

    if not EMULATE_HX711:
        GPIO.cleanup()

    print("終了します。")
    sys.exit()


hx = HX711(5, 6)

# 基準となる単位の算出方法
# 基準単位を1にするには センサーなどに1kgを付けて、その重さを正確に知る。
# この場合、92は1グラムです。なぜなら、1を基準単位とした場合、重さがない状態では0に近い数字が得られるからです。
# そして2kgを加えると184000前後の数値が得られました。そこで、3分の1の法則によると
# 2000グラムが184000であれば、1000グラムは184000 / 2000 = 92です。
# hx.set_reference_unit(113)
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()

print("風袋引き完了。今すぐ重量を追加してください...")

def main():

    # 有機EL用のクラスをインスタンス化
    so1602a = el_display.So1602a()
    # アンダーカーソルとブロックカーソルを消す。
    so1602a.display_on_off_control(True, False, False)

    # 1行目に表示する文字のリスト
    first_line_word = ["ｹﾞﾝｻﾞｲﾉｼﾞｭｳﾘｮｳ      " ,]

    while True:
        try:
            # 四捨五入
            rou = lambda x: (x * 2 + 1) // 2

            # 重さを取得し四捨五入した後、文字列化
            val = hx.get_weight(5)
            weight = str(int(rou(val)))

            # 重量の値
            # print(weight)

            # 単位を追加
            s = weight + " (g)"

            # 1段目には表示している重量のステータスを入れる
            pri_w = first_line_word[0]

            # 2段目には現在重量の文字列を入れる
            pri_w += s

            # ディスプレイの表示をクリア
            so1602a.clear_display()

            # 重量の表記を右寄せにするため、2列目のみシフトさせる。
            so1602a.shift_enable(False, True, False)
            shift_n = 16 - len(s)
            # print("シフトさせる文字数は {}文字".format(shift_n))
            for i in range(shift_n):
                so1602a.display_shift()

            # ディスプレイの表示
            so1602a.print(pri_w)


            hx.power_down()
            hx.power_up()
            time.sleep(0.1)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


if __name__ == '__main__':
    main()
