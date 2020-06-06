#! python3

# Filename: m_002_01_event_toggle 
__author__ = "raspython"
__date__ = '2020/05/31 06:08'


import RPi.GPIO as GPIO
from time import sleep


def main():
    """
    本体
    """
    """
    PIN_NOの定義
    """
    # LED
    led_r = 13
    led_g = 19
    led_b = 26
    # スイッチ
    sw_w = 12
    sw_r = 16
    sw_b = 20
    sw_g = 21

    """
    GPIOの初期設定
    """
    # PIN_NOの設定
    GPIO.setmode(GPIO.BCM)
    # 入力 内部プルアップを使用
    GPIO.setup([sw_w, sw_r,sw_b, sw_g], GPIO.IN,
               pull_up_down=GPIO.PUD_UP)
    # 出力
    GPIO.setup([led_r, led_b, led_g], GPIO.OUT,
               initial=GPIO.LOW)
    # イベント取得の設定
    GPIO.add_event_detect(sw_r, GPIO.FALLING, bouncetime=300)
    GPIO.add_event_detect(sw_b, GPIO.FALLING, bouncetime=300)
    GPIO.add_event_detect(sw_g, GPIO.FALLING, bouncetime=300)

    """
    実行部
    """
    try:
        while True:
            #スイッチが押されると対応のLEDが点灯、消灯を繰り返す。
            if GPIO.event_detected(sw_r):
                print("スイッチ赤ON")
                if GPIO.input(led_r) == GPIO.LOW:
                    GPIO.output(led_r, GPIO.HIGH)
                else:
                    GPIO.output(led_r, GPIO.LOW)
            elif GPIO.event_detected(sw_b):
                print("スイッチ青ON")
                if GPIO.input(led_b) == GPIO.LOW:
                    GPIO.output(led_b, GPIO.HIGH)
                else:
                    GPIO.output(led_b, GPIO.LOW)
            elif GPIO.event_detected(sw_g):
                print("スイッチ緑ON")
                if GPIO.input(led_g) == GPIO.LOW:
                    GPIO.output(led_g, GPIO.HIGH)
                else:
                    GPIO.output(led_g, GPIO.LOW)

            # スイッチ白を押すと終了
            if GPIO.input(sw_w) != GPIO.HIGH:
                break
            sleep(0.1)

    except KeyboardInterrupt:
        pass

    # イベント取得の終了
    GPIO.remove_event_detect(sw_r)
    GPIO.remove_event_detect(sw_b)
    GPIO.remove_event_detect(sw_g)

    GPIO.cleanup()
    print("終了")

if __name__ == '__main__':
    main()