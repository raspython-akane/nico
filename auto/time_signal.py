#!/usr/bin/env python3
# Filename: time_signal
__author__ = "raspython"
__date__ = '2020/11/07 20:17'

import datetime
from time import sleep
import subprocess


def time_rec():
    """
    現在時刻を取得し、時間と分を返す。
    """
    # 時間取得
    c_time = datetime.datetime.now()
    # print(c_time)

    h = c_time.hour
    m = c_time.minute

    return h, m


def sc_job():
    """
    スケジュール管理
    """
    flag = 0

    # 時間監視 00分になったらhをtime_signalに渡す。
    while True:
        h, m = time_rec()
        # 分の設定
        if m == 0:
            flag = time_signal(h)

        # 時報が再生されたらループを抜ける
        if flag == 1:
            print("終了処理")
            break

        sleep(0.1)



def volume_change(h):
    """
    時間によってボリュームの値を変更
    @param h: 現在時刻(hour)
    @type h: int
    """
    # 22時～5時まではボリュームを落とす
    if h < 6 or h > 21:
        subprocess.call("amixer set Master 50%", shell=True)
    else:
        subprocess.call("amixer set Master 80%", shell=True)


def time_signal(h):
    """
    時報。
    timeの値のhourをvolume_changeに渡す。
    hour.wavを実行。hourは現在時刻の時の値
    終了時に1を返す
    """
    # 時間によってボリューム調整する。
    volume_change(h)
    # 時報再生
    subprocess.call("/usr/bin/aplay /home/akane/time/{}.wav".format(h), shell=True)
    print("{}時報再生".format(h))

    return 1



def main():
    sc_job()

if __name__ == '__main__':
    main()