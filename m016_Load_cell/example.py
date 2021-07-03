#! /usr/bin/python2

import el_display
import time
import sys

EMULATE_HX711=False

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

# 何らかの理由で、python、numpy、hx711自体のバージョンによって、バイトの順番が常に同じではないことがわかりました。
# なぜそれが変わるのかを解明する必要があります。
# もし、超ランダムな値を経験しているなら、これらの値をMSBまたはLSBに変更すると、より安定した値を得ることができます。
# ビットとバイトの順番をデバッグして記録するコードが以下にあります。
# 最初のパラメータは、"long "の値を構築するために使用されるバイトの順序です。
# 2番目のパラメータは、各バイトに含まれるビットの順序です。
# HX711のデータシートによると、2番目のパラメータはMSBなので、変更する必要はありません。
hx.set_reading_format("MSB", "MSB")

# 基準となる単位の算出方法
# 基準単位を1にするには センサーなどに1kgを付けて、その重さを正確に知る。
# この場合、92は1グラムです。なぜなら、1を基準単位とした場合、重さがない状態では0に近い数字が得られるからです。
# そして2kgを加えると184000前後の数値が得られました。そこで、3分の1の法則によると
# 2000グラムが184000であれば、1000グラムは184000 / 2000 = 92です。
#hx.set_reference_unit(113)
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("風袋引き完了。今すぐ重量を追加してください...")

# 両方のチャンネルを使うには、両方の風袋引きが必要です
#hx.tare_A()
#hx.tare_B()



while True:
    try:
        # これらの3行は、読み込みフォーマットにMSBとLSBのどちらを使うかをデバッグするのに便利です。
        # hx.set_reading_format("LSB", "MSB") "の最初のパラメータのためのものです。
        # "val = hx.get_weight(5) "と "print val "の2行をコメントし、以下の3行をアンコメントして何が表示されるか確認します。

        # np_arr8_string = hx.get_np_arr8_string()
        # binary_string = hx.get_binary_string()
        # print binary_string + " " + np_arr8_string


        # 四捨五入
        rou = lambda x: (x * 2 + 1) // 2

        # 重さを表示します。MSBとLSBの問題をデバッグしている場合はコメントしてください。
        val = hx.get_weight(5)
        weight = int(rou(val))
        print(weight)

        # 両方のチャンネルから重量を得るには（ロードセルをチャンネルAとBの両方に # 接続している場合）、次のようにします。
        # 両方のチャンネルから重量を得るには、次のようにします。
        #値_A = hx.get_weight_A(5)
        #val_B = hx.get_weight_B(5)
        #print "A: %s B: %s" % ( val_A, val_B )

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
