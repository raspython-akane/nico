
#!/usr/bin/env python3

# Filename: m_021_robot_arm 
__author__ = "raspython"
__date__ = '2021/10/24 13:15'


import pigpio as pi
from time import sleep
import Adafruit_PCA9685
import copy

# 変数の定義
# 入力
sw_b = 23
sw_w = 24
red_rotary_ac = 5
red_rotary_bc = 6
blue_1_rotary_ac = 13
blue_1_rotary_bc = 19
blue_2_rotary_ac = 26
blue_2_rotary_bc = 12
green_rotary_ac = 16
green_rotary_bc = 20

# 出力
led_b = 25

# 各々のサーボの移動範囲を決めるため上限値と下限値を決める。
crow_min = 285
crow_max = 455
arm_left_min = 385
arm_left_max = 505
arm_right_min = 335
arm_right_max = 525
base_min = 355
base_max = 655

# サーボパルスの初期位置の周波数を定義
crow_ini = 355
arm_left_ini = 405
arm_right_ini = 505
base_ini = 375

# 各々のサーボの初期周波数を呼び出すためのリストを作成
ini_l = [crow_ini, arm_left_ini, arm_right_ini, base_ini]

# サーボパルスの変数
# サーボパルスは初期値から始めるため初期値から値をコピーする
crow_servo = copy.copy(crow_ini)
arm_left_servo = copy.copy(arm_left_ini)
arm_right_servo = copy.copy(arm_right_ini)
base_servo = copy.copy(base_ini)
# 各々のサーボパルス変数を呼び出すためのリストを作成
servo_l = [crow_servo, arm_left_servo, arm_right_servo, base_servo]


# GPIOの初期設定
pi_g = pi.pi()

# GPIOの定義
# 入力設定
pi_g.set_mode(sw_b, pi.INPUT)
pi_g.set_mode(sw_w, pi.INPUT)
# 内部プルアップ設定
pi_g.set_pull_up_down(sw_b, pi.PUD_UP)
pi_g.set_pull_up_down(sw_w, pi.PUD_UP)

# 出力設定
pi_g.set_mode(led_b, pi.OUTPUT)


# PCA9685の設定
# PCA9685をデフォルトのアドレス(0x40)で初期化
pwm = Adafruit_PCA9685.PCA9685()

# サーボモーターの周波数
# サンプルに倣い60HZにする
pwm.set_pwm_freq(60)


def led_control(status):
    """
    青色LEDを制御する
    @param status: LEDのステータス
    """
    pi_g.write(led_b, status)


def servo_control(var, servo_channel):
    """
    指定されたサーボモーターを指定された値制御する
    @param var: サーボのPWMの変化量
    @param servo_channel: 変更するサーボのチャンネルNO
    """
    # サーボパルスを変更するためglobal変数をいじれるようにする
    global servo_l

    # servo_channelで各々のサーボパルス変数の値の変化量の倍率を呼び出せるリストを作成
    mag_l =[10, 10, 5, 10]

    # 回転方向の値にサーボによって決められた倍率をかけて
    # 一度でのサーボの変化量を決め、その値分サーボパルスの値を増減させる
    servo_l[servo_channel] += var * mag_l[servo_channel]

    # servo_channelで各々のサーボの最大値と最小値を呼び出せるようにリストを作成
    servo_limit_l = [[crow_min, crow_max], [arm_left_min, arm_left_max],
                     [arm_right_min, arm_right_max], [base_min, base_max]]

    # 各々のサーボパルスが最大値と最小値を超えないように管理
    if servo_l[servo_channel] < servo_limit_l[servo_channel][0]:
        servo_l[servo_channel] = servo_limit_l[servo_channel][0]
    elif servo_l[servo_channel] > servo_limit_l[servo_channel][1]:
        servo_l[servo_channel] = servo_limit_l[servo_channel][1]

    # debugプリントで表示させるリストを作成
    w = ["クロー用サーボのPWM制御用の値", "アーム左側サーボのPWM制御用の値",
         "アーム右側サーボのPWM制御用の値", "土台用のサーボのPWM制御用の値"]

    print("{}: {}".format(w[servo_channel], servo_l[servo_channel]))

    # サーボの制御するための値を渡す
    # 値は左から(channel, 0, pulse)
    pwm.set_pwm(servo_channel, 0, servo_l[servo_channel])

def count_control_red(pin, status, tick):
    """
    赤色ロータリーエンコーダのA-C間が
    立ち下がったときのB-C間の入力で回転方向を監視して
    値をクロー用サーボ制御関数に渡す
    @param pin:GPIOのNO
    @param status: 立ち上がり立下りの値
    @param tick:内部時計の値
    """
    # a-c間が立下り時a-cがLOWならカウントダウン
    if pi_g.read(red_rotary_bc) == 0:
        # print("赤 ccw")
        servo_control(-1, 0)
    # a-c間が立下り時a-cがHIGHならカウントアップ
    if pi_g.read(red_rotary_bc) == 1:
        # print(赤 cw)
        servo_control(1, 0)


def count_control_blue1(pin, status, tick):
    """
    青色ロータリーエンコーダの左側のA-C間が
    立ち下がったときのB-C間の入力で回転方向を監視して
    値をアーム用左側サーボ制御関数に渡す
    @param pin:GPIOのNO
    @param status: 立ち上がり立下りの値
    @param tick:内部時計の値
    """
    # a-c間が立下り時a-cがLOWならカウントダウン
    if pi_g.read(blue_1_rotary_bc) == 0:
        # print("青左 ccw")
        servo_control(-1, 1)
    # a-c間が立下り時a-cがHIGHならカウントアップ
    if pi_g.read(blue_1_rotary_bc) == 1:
        # print("青左 cw")
        servo_control(1, 1)


def count_control_blue2(pin, status, tick):
    """
    青色ロータリーエンコーダの右側のA-C間が
    立ち下がったときのB-C間の入力で回転方向を監視して
    値をアーム用右側サーボ制御関数に渡す
    @param pin:GPIOのNO
    @param status: 立ち上がり立下りの値
    @param tick:内部時計の値
    """
    # a-c間が立下り時a-cがLOWならカウントダウン
    if pi_g.read(blue_2_rotary_bc) == 0:
        # print("青右 ccw")
        servo_control(-1, 2)
    # a-c間が立下り時a-cがHIGHならカウントアップ
    if pi_g.read(blue_2_rotary_bc) == 1:
        # print("青右 cw")
        servo_control(1, 2)


def count_control_green(pin, status, tick):
    """
    緑色ロータリーエンコーダのA-C間が
    立ち下がったときのB-C間の入力で回転方向を監視して
    値を台座用サーボ制御関数に渡す
    @param pin:GPIOのNO
    @param status: 立ち上がり立下りの値
    @param tick:内部時計の値
    """
    # a-c間が立下り時a-cがLOWならカウントダウン
    if pi_g.read(green_rotary_bc) == 0:
        # print("緑 ccw")
        servo_control(-1, 3)
    if pi_g.read(green_rotary_bc) == 1:
        # print("緑 cw")
        servo_control(1, 3)


def rotary_monitoring():
    """
    ロータリーエンコーダーの出力波形を監視する
    各々のロータリーエンコーダが渡されたら割り込み開始
    各々の回転方向監視の関数を呼ぶ
    白のスイッチが押されたらループを抜ける
    """
    # ロータリーエンコーダが回された時の割り込みの定義
    red = pi_g.callback(red_rotary_ac, pi.FALLING_EDGE, count_control_red)
    blue1 = pi_g.callback(blue_1_rotary_ac, pi.FALLING_EDGE, count_control_blue1)
    blue2 = pi_g.callback(blue_2_rotary_ac, pi.FALLING_EDGE, count_control_blue2)
    green = pi_g.callback(green_rotary_ac, pi.FALLING_EDGE, count_control_green)

    while True:

        # 白のスイッチが押されたら終了
        if pi_g.read(sw_w) == 0:
            # コールバックの終了処理
            red.cancel()
            blue1.cancel()
            blue2.cancel()
            green.cancel()
            break

        sleep(0.1)

def initial_position():
    """
    サーボの周波数が初期位置の周波数と同じかをチェック
    違うならば0.05秒ごとに1づつ増加減して合わせる
    """
    global servo_l
    # print(servo_l)
    # print(ini_l)

    print("初期位置へ移動中。少々お待ちください...")
    for i in range(4):
        # 初期周波数にサーボを移動する際、急激に動かすと危険なため
        # 0.1秒ごと1づつ増減させ合わせる
        if servo_l[i] > ini_l[i]:
            # print("大きい")
            while servo_l[i] > ini_l[i]:
                servo_l[i] -= 1
                sleep(0.05)
                # print(servo_l[i])

                pwm.set_pwm(i, 0, servo_l[i])

        elif servo_l[i] < ini_l[i]:
            # print("小さい")
            while servo_l[i] < ini_l[i]:
                servo_l[i] += 1
                sleep(0.05)
                # print(servo_l[i])

                pwm.set_pwm(i, 0, servo_l[i])

        else:
            # print("おなじ")
            pwm.set_pwm(i, 0, servo_l[i])

    print("初期位置に移動しました")



def main_control():
    """
    黒のスイッチが押されたらロータリーエンコーダの
    モニタリングを開始する。
    その時青色LEDを点灯させる。
    白スイッチを押されると終了。
    """

    # 初期位置へ移動
    initial_position()

    try:
        while True:
            # 黒のスイッチを押されると開始
            if pi_g.read(sw_b) == 0:
                print("開始")
                # LED青の点灯
                led_control(1)
                # ロータリーエンコーダの監視へ
                rotary_monitoring()

            # 白のスイッチが押されると終了
            elif pi_g.read(sw_w) == 0:
                print("終了")
                # LED青の消灯
                led_control(0)
                break


            sleep(0.1)

    except KeyboardInterrupt:
        pass

    # LED青の消灯
    led_control(0)
    # GPIOの終了処理
    pi_g.stop()
    # 初期位置に移動中
    initial_position()


def main():
    # メイン処理
    main_control()


if __name__ == '__main__':
    main()