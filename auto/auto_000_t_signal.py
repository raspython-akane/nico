#!/usr/bin/env python3
# coding:utf-8
# Filename: auto_000_t_signal
__author__ = "raspython"
__date__ = '2020/11/06 10:36'

import datetime
from time import sleep
import subprocess
import schedule



def time_rec():
    """
    現在時刻を取得し、時間と分を返す。
    """
    # 時間取得
    c_time = datetime.datetime.now()
    # print(c_time)

    h = c_time.hour
    m = c_time.minute
    s = c_time.second

    return h, m, s


def sc_job():
    """
    スケジュール管理
    """
    # 毎時0分にtime_signalを呼び出す。
    schedule.every().hour.at(":00").do(time_signal)

    while True:
        schedule.run_pending()
        sleep(0.1)


def volume_change(h):
    """
    時間によってボリュームの値を変更
    @param h: 現在時刻(hour)
    @type h: int
    """
    if h < 6 or h > 21:
        subprocess.call("amixer set Master 50%", shell=True)
    else:
        subprocess.call("amixer set Master 80%", shell=True)


def time_signal():
    """
    時報。
    timeの値のhourをvolume_changeに渡す。
    hour.wavを実行。hourは現在時刻の時の値
    """
    # 時刻を変数に入れる(tuple)
    time = time_rec()
    volume_change(time[0])
    subprocess.call("aplay /home/akane/time/{}.wav".format(time[0]), shell=True)
    print("{}時{}分{}秒報再生".format(time[0], time[1], time[2]))


def main():
    sc_job()

if __name__ == '__main__':
    main()