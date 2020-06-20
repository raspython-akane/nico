#! python3

# Filename: m_003_timing_color 
__author__ = "raspython"
__date__ = '2020/06/06 18:38'


import RPi.GPIO as GPIO
from time import sleep
from random import randint



def main():
    """
    本体
    """
    """
    PIN_NOの定義
    """
    # LED
    upper_r = 13
    upper_g = 19
    upper_b = 26
    lower_r = 17
    lower_g = 27
    lower_b = 22
    led_l =[upper_r,upper_g, upper_b,
            lower_r,lower_g, lower_b]

    # スイッチ
    sw_w = 12
    sw_r = 16
    sw_g = 20
    sw_b = 21
    sw_l = [sw_r, sw_g, sw_b, sw_w]

    """
    GPIOの初期設定
    """
    # PIN_NOの設定
    GPIO.setmode(GPIO.BCM)
    # 入力
    GPIO.setup(sw_l, GPIO.IN,
               pull_up_down=GPIO.PUD_UP)
    # 出力
    GPIO.setup(led_l, GPIO.OUT,
               initial=GPIO.LOW)

    """
    変数の定義
    """
    binary_l = [0b001, 0b010, 0b100]

    """
    実行部
    """
    try:
        while True:
            # スイッチ白を押されるとスタート
            if GPIO.input(sw_w) != GPIO.HIGH:
                break
            else:
                sleep(0.1)

        print("start")

        for i in range(10):
            # 入力flag
            flag = 0b000
            # LED点灯前に1秒待つ
            sleep(1)

            # 色を決める乱数の生成
            color_num = (randint(1, 99) % 3)
            print("乱数{}".format(color_num))

            # 1ループ毎LEDの点灯消灯を0.1秒短くする
            wait = 1 - (i * 0.1)

            # 乱数が0なら赤、1なら緑、2なら青を点灯
            # 上下のLEDの点灯までに待ち時間が入る
            GPIO.output(led_l[color_num], GPIO.HIGH)
            sleep(wait)
            GPIO.output(led_l[color_num], GPIO.LOW)
            GPIO.output(led_l[color_num + 3], GPIO.HIGH)
            sleep(wait)
            GPIO.output(led_l[color_num + 3], GPIO.LOW)

            # 入力待機
            # ループごとに入力判定と0.1秒wait
            # ループ回数は正解することによって減っていく
            for j in range(10 - i):
                sleep(0.1)

                #入力判定
                # 各ボタンの入力をビットマスクで管理
                if GPIO.input(sw_l[0]) != GPIO.HIGH:
                    flag = flag | binary_l[0]
                if GPIO.input(sw_l[1]) != GPIO.HIGH:
                    flag = flag | binary_l[1]
                if GPIO.input(sw_l[2]) != GPIO.HIGH:
                    flag = flag | binary_l[2]
                print("入力{} 正解{}"
                      .format(flag, binary_l[color_num]))

                if flag == binary_l[color_num]:
                    print("正解")
                    break

            else:
                print("失敗")
                GPIO.output([led_l[0], led_l[3]],
                            GPIO.HIGH)
                sleep(1)
                GPIO.output([led_l[0], led_l[3]],
                            GPIO.LOW)
                break

        else:
            print("完走おめでとう")
            GPIO.output(led_l[2], led_l[5],
                        GPIO.HIGH)
            sleep(1)
            GPIO.output(led_l[2], led_l[5],
                        GPIO.LOW)

    except KeyboardInterrupt:
        pass

    GPIO.cleanup()
    print("終了")


if __name__ == '__main__':
    main()