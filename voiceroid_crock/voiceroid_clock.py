#!/usr/bin/env python3

# Filename: voiceroid_clock 
__author__ = "raspython"
__date__ = '2021/04/23 12:37'

from datetime import datetime
import locale
from tkinter import *
from PIL import Image
from PIL import ImageTk
import os
import sys
import requests
import json
import time
import threading
import RPi.GPIO as GPIO
import dht11
import subprocess


# ロケールを変更して曜日を日本語にする
locale.setlocale(locale.LC_ALL, "ja_JP.UTF-8")

# ウィンドフラグ
running = True
# 気温
temp = 0
# 湿度
humidity = 0


"""
GPIOとDHT11の準備
"""

# GPIO用意
GPIO.setmode(GPIO.BCM)
# PINナンバーを与えてライブラリーから呼び出し
instance = dht11.DHT11(pin = 21)


"""
OpenWeatherMAPの準備
"""
# OpenWeatherのAPIのkye
api_key = "piyopiyohogehoge"

"""
# URLを作成
# オプション
onecall: 詳細の気象データの呼び出しを設定
lat=hogehoge: 経度
lon=piyopiyo: 緯度
units=metric: 摂氏表示
lang=ja: 日本語表示
exclude=current,minutely,alerts&cnt: current minutely alerts&cntの情報の表示をしない
appid=hogehoge: api_key
"""
api_url = "http://api.openweathermap.org/data/2.5/onecall?lat=経度&lon=緯度&units=metric&lang=ja&exclude=current,minutely,alerts&cnt=16&appid=piyopiyohogehoge"


"""
ウィンドウの作成
"""
root = Tk()
# 解像度
root.geometry("1024x600")
# タイトル
root.title("Clock and Weather Widget")
# フレーム
canvas = Canvas(root,
                     width=1024,
                     height=600,
                     bg="black",
                     # 枠線を消す
                     highlightthickness=0)

# 配置
canvas.pack()

# linux上ではフルスクリーン化
if os.name == "nt":
    pass
elif os.name == "posix":
    root.attributes("-fullscreen", "1")


"""
画像の準備
"""

# スクリプトの絶対パス
path = os.path.dirname(os.path.abspath(sys.argv[0]))
# print(path)
# print(os.name)

# 画像を開く

akane_img = Image.open(os.path.join(path, "voiceroidicon", "akane.png"))
aoi_img = Image.open(os.path.join(path, "voiceroidicon", "aoi.png"))
akarikusa_img = Image.open(os.path.join(path, "weathericon", "001.png"))
weth_01img = Image.open(os.path.join(path, "weathericon", "01d@2x.png"))
weth_02img = Image.open(os.path.join(path, "weathericon", "02d@2x.png"))
weth_03img = Image.open(os.path.join(path, "weathericon", "03d@2x.png"))
weth_04img = Image.open(os.path.join(path, "weathericon", "04d@2x.png"))
weth_09img = Image.open(os.path.join(path, "weathericon", "09d@2x.png"))
weth_10img = Image.open(os.path.join(path, "weathericon", "10d@2x.png"))
weth_11img = Image.open(os.path.join(path, "weathericon", "11d@2x.png"))
weth_13img = Image.open(os.path.join(path, "weathericon", "13d@2x.png"))
weth_50img = Image.open(os.path.join(path, "weathericon", "50d@2x.png"))

# リサイズ
akane_resize = akane_img.resize(size=(150, 175))
aoi_resize = aoi_img.resize(size=(150, 175))
akarikusa_resize = akarikusa_img.resize(size=(105,120))
w01_resize = weth_01img.resize(size=(120, 120))
w02_resize = weth_02img.resize(size=(120, 120))
w03_resize = weth_03img.resize(size=(120, 120))
w04_resize = weth_04img.resize(size=(120, 120))
w09_resize = weth_09img.resize(size=(120, 120))
w10_resize = weth_10img.resize(size=(120, 120))
w11_resize = weth_11img.resize(size=(120, 120))
w13_resize = weth_13img.resize(size=(120, 120))
w50_resize = weth_50img.resize(size=(120, 120))

# 画像の定義
akane_icon = ImageTk.PhotoImage(akane_resize)
aoi_icon = ImageTk.PhotoImage(aoi_resize)
akari_icon = ImageTk.PhotoImage(akarikusa_resize)
w01d =ImageTk.PhotoImage(w01_resize)
w02d =ImageTk.PhotoImage(w02_resize)
w03d =ImageTk.PhotoImage(w03_resize)
w04d =ImageTk.PhotoImage(w04_resize)
w09d =ImageTk.PhotoImage(w09_resize)
w10d =ImageTk.PhotoImage(w10_resize)
w11d =ImageTk.PhotoImage(w11_resize)
w13d =ImageTk.PhotoImage(w13_resize)
w50d =ImageTk.PhotoImage(w50_resize)


class MainFrame():
    def __init__(self):

        global running

        # 更新のいらない文字の表記
        self.dislpal_text()
        # 茜と葵の配置
        self.voiceroid_img(akane_icon, aoi_icon)
        # 年月日の初期表示
        self.now = datetime.now()
        # 天気情報の初期表示
        self.weather(self.now)
        self.calender(self.now)
        # 温度と湿度の初期表示
        self.temp_display()
        # 日時情報の更新
        self.update_display()
        # あかり草の配置
        self.akarisou()

        # イベント処理のループ
        root.mainloop()

        running = False


    def dislpal_text(self):
        """
        更新なし文字の表記
        """

        # 気温と降水確率
        word_l = ["最高", "最低", "降水確率", " 0時", " 6時", "12時", "18時"]
        x_l = [60, 60, 275, 246, 246, 246, 246]
        y_l = [525, 565, 390, 435, 475, 515, 555]
        font_size_l = [25, 25, 20, 19, 19, 19, 19]
        fill_l = ["red", "deep sky blue", "gray", "white", "white", "white", "white"]

        for i in range(14):
            # 翌日(6より大きい分)はx座標に+350
            if i > 6:
                x_l[i - 7] += 350
            # 当日と翌日でX座標以外は同じなのでテーブルを繰り返す
            i %= 7
            # print("word_l: {} x: {} y: {} fontsize: {} fill {}".format(word_l[i], x_l[i], y_l[i], font_size_l[i], fill_l))
            canvas.create_text(
                x_l[i],
                y_l[i],
                # 最高気温
                text=(word_l[i]),
                # fontの種類とサイズ
                font=("IPAGothic", font_size_l[i]),
                # fontの色
                fill=fill_l[i])


        # 温度と湿度
        tword_l = ["室内条件", "室温", "湿度", "℃", "％"]
        tx_l = [820, 760, 760, 885, 885]
        ty_l = [485, 525, 565, 525, 565]
        tcolor_l = ["gray", "tomato", "khaki", "white", "white"]
        tfont_size = [18, 25, 25, 25, 25]

        for i in range(5):
            # --- 温度と湿度の表示---
            canvas.create_text(
                tx_l[i],
                ty_l[i],
                # 日付の表示
                text="{}".format(tword_l[i]),
                # fontの種類とサイズ
                font=("IPAGothic", tfont_size[i]),
                # fontの色
                fill=tcolor_l[i])


    def calender(self, now):
        """
        日時の描画
        @param now: datetimeの値
        """
        # 前の表示のクリア
        canvas.delete("calender")

        canvas.create_text(
            # 開始のxy座標
            550,
            60,
            # 年月日の表示
            text="{0:0>4d}年{1:0>2d}月{2:0>2d}日（{3:}曜日）".format(
                now.year, now.month, now.day, now.strftime("%a")),
            # fontの種類とサイズ
            font=("IPAGothic", 60),
            # fontの色
            fill="white",
            # 画面更新毎にテキストを消すためtag付け
            tag="calender")


    def clock(self, now):
        """
        時間の表示
        @param now: datetimeの値
        """

        # 時間の表示
        canvas.create_text(
            # 開始のxy座標
            510,
            210,
            # 時間の表示
            text="{0:0>2d}:{1:0>2d}:{2:0>2d}".format(now.hour, now.minute, now.second),
            # fontの種類とサイズ
            font=("IPAGothic", 108),
            # fontの色
            fill="white",
            # 画面更新毎にテキストを消すためtag付け
            tag="clock")


    def voiceroid_img(self, akane, aoi):
        """
        ボイロのイメージの表示
        """
        icon_l = [akane, aoi]
        x_l = [130, 890]
        y_l = [200, 200]
        for i in range(2):
            canvas.create_image(
                x_l[i],
                y_l[i],
                image=icon_l[i])


    def weather(self, now):
        """
        気象情報の表示
        @param now: datetimeの値
        """
        # 呼び出されるごとにタグわけした描画をクリアする
        canvas.delete("thr_hour")

        # 天気アイコンの呼び出し用の辞書
        w_icon_dic = {
            "01d": w01d,
            "02d": w02d,
            "03d": w03d,
            "04d": w04d,
            "09d": w09d,
            "10d": w10d,
            "11d": w11d,
            "13d": w13d,
            "50d": w50d}

        # 四捨五入用一行関数
        rou = lambda x: (x * 2 + 1) // 2

        # 気象情報を入れるリストを定義
        max_t_list = []
        min_t_list = []
        description = []
        icon_keys = []
        rainy_percent_list = ["---", "---", "---", "---", "---", "---", "---", "---"]

        # OpenWeatherMapからjsonのデータを取得
        response = requests.get(api_url)
        json_date = json.loads(response.text)
        # print(json_date)

        # 日毎のデーターの処理
        for i, day_date in enumerate(json_date["daily"]):
            # print(item)
            # 2日分のデータの取得
            if i < 2:

                # 最高気温と最低気温の取得
                # 返り値はfloart
                # 小数点以下は四捨五入
                max_t = int(rou(day_date["temp"]["max"]))
                min_t = int(rou(day_date["temp"]["min"]))
                # print("{}日後の 最高気温: {} 最低気温: {}".format(i, max_t, min_t))
                str_max = str(max_t) + "℃"
                str_min = str(min_t) + "℃"
                # 各々のリストへ追加
                max_t_list.append(str_max)
                min_t_list.append(str_min)
                # print(max_t_list, min_t_list)

                # 天気テキストの取得
                description.append(day_date["weather"][0]["description"])
                # print(description)
                # 天気アイコンのkey取得
                icon_keys.append(day_date["weather"][0]["icon"])
                # print(icon_keys)

        # 現在時刻から降水確率のリストのインデックスを指定
        list_index = now.hour // 6
        print(list_index)

        # 時間ごとのデーター処理
        # 最大8回分のデータが必要なので8回ループ
        for i in range(8):
            # 現在のインデックス開始番号とループカウンタを加算
            counter = (list_index + i)
            # print(counter)
            # 加算値が8より少ないときはデータを取得してリストへ入れる
            if counter < 8:
                hour_weather_date = json_date["hourly"][i * 6]
                # print("{}時間後の気象データ {}".format(i, hour_weather_date["pop"]))
                # 10倍して四捨五入の用意
                f = hour_weather_date["pop"] * 10
                # 四捨五入
                r = rou(f)
                # 10倍して%表記の単位へ(int)
                rainy_percent = int(r * 10)
                # 文字列化して%を付ける
                str_rainy = str(rainy_percent) + "%"

                # リストに入れるインデックスの計算の変数
                index_n = list_index + i
                # リストへ格納
                rainy_percent_list[index_n] = (str_rainy)
                # print(rainy_percent_list)

        # 日時と天気アイコンの変数
        cal_x = 200
        cal_y = 343
        w_icon_x = 100
        w_icon_y = 420
        day = ["今日", "明日"]
        # 気象情報表記用の変数
        w_text_list_x = [95, 140, 140]
        w_text_list_y = [485, 525, 565]
        val_text_l = [description, max_t_list, min_t_list]
        font_size_l = [15, 25, 25]
        # 降水確率用の変数
        rainy_x = 315
        rainy_y_l = [435, 475, 515, 555]



        # 表示
        # 1ループ目は当日、2ループ目は翌日
        for i in range(2):

            # 翌日は350X座標が移動
            x_move = i * 350

            # --- 天気の日付の表示---
            canvas.create_text(
                cal_x + x_move,
                cal_y,
                # 日付の表示
                text="{} {}月{}日".format(day[i], now.month, now.day + i),
                # fontの種類とサイズ
                font=("IPAGothic", 20),
                # fontの色
                fill="white",
                # 画面更新毎にテキストを消すためtag付け
                tag="thr_hour")

            # --- 天気のアイコンの表示---
            # キーに対応するアイコンがないときは表示しない
            try:
                canvas.create_image(
                    w_icon_x + x_move,
                    w_icon_y,
                    # 天気の文字をキーにアイコンを呼び出す
                    image=w_icon_dic[icon_keys[i]],
                    # 画面更新毎にテキストを消すためtag付け
                    tag="thr_hour")
            except KeyError:
                pass

            # --- 天気のテキスト、最高気温、最低気温の表示 ---
            for j in range(3):
                # --- 天気テキストの表示 ---
                canvas.create_text(
                    w_text_list_x[j] + x_move,
                    w_text_list_y[j],
                    # 天気のテキストの表示
                    text=(val_text_l[j][i]),
                    # fontの種類とサイズ
                    font=("IPAGothic", font_size_l[j]),
                    # fontの色
                    fill="white",
                    # 画面更新毎にテキストを消すためtag付け
                    tag="thr_hour")

            # --- 降水確率の表示 ---
            for k in range(4):
                canvas.create_text(
                    # x軸は当日と翌日で変化
                    rainy_x + x_move,
                    # y軸は表示毎に変化
                    rainy_y_l[k],
                    # 降水確率の表示
                    text=(rainy_percent_list[k + (i * 4)]),
                    # fontの種類とサイズ
                    font=("IPAGothic", 19),
                    # fontの色
                    fill="white",
                    # 画面更新毎にテキストを消すためtag付け
                    tag="thr_hour")


    def temp_display(self):
        """
        温度湿度の表示
        """
        tmp_hum_l = [temp, humidity]
        y_l = [525, 565]
        for i in range(2):
            # --- 温度と湿度の表示---
            canvas.create_text(
                835,
                y_l[i],
                # 日付の表示
                text=tmp_hum_l[i],
                # fontの種類とサイズ
                font=("IPAGothic", 23),
                # fontの色
                fill="white",
                # 画面更新毎にテキストを消すためtag付け
                tag="clock")


    def update_display(self):
        """
        表示の更新
        日付変更時間で日付を変更
        時間は500ms毎に変更
        """

        # 現在時刻の情報を変数に入れる
        now = datetime.now()

        # 時間画面を更新するため元のテキストを削除
        canvas.delete("clock")

        # 日時データを時計の関数に渡す
        self.clock(now)

        # 0時0分0秒に日付を更新
        if now.hour == 0 and now.minute == 0 and now.second == 0:
            # canvasdateと日時データをcalender関数に渡す
            self.calender(now)

        # 0:30から3時間ごとに気象情報を更新
        l = [0, 3, 6, 9, 12, 15, 18, 21]
        if (now.hour in l) and now.minute == 30 and now.second == 0:
            self.weather(now)

        # 温度と湿度を更新
        self.temp_display()

        # 0.5秒ごとに画面を更新
        root.after(500, self.update_display)



    def akarisou(self):
        """
        わぁ
        クリックするとバルス
        """
        akari_butt = Button(
            # イメージ
            image=akari_icon,
            # 背景色
            background="black",
            # ボタンを押したときの背景色
            activebackground="black",
            # 動作
            command=self.window_close)
        akari_butt.place(x=912, y=465)


    def window_close(self):
        """
        windowを閉じる
        """
        root.destroy()


def temp_and_humidity():
    """
    気温と湿度を取得
    ウィンドウが終了したらループを抜ける
    """
    global temp
    global humidity

    # ウィンドウフラグがTrueの時はループ
    while running:

        # 温度と湿度を読みこみ
        result = instance.read()
        # print(result.temperature, result.humidity)

        temp = result.temperature
        humidity = result.humidity

        # DHT11の読み込みがおかしいときは更新をしない
        if temp == 0 and humidity == 0:
            pass
        else:
            time.sleep(10)

    print("温度監視終了")


def time_tone():
    """
    毎時0分に時報を鳴らす
    23時から翌朝5時まではボリュームを下げる
    wavファイルを再生したら10秒間スリープ
    """

    # ウィンドウフラグがTrueの時はループ
    while running:

        # 現在時刻を取得
        now = datetime.now()

        hour = now.hour
        min = now.minute
        sec = now.second

        # 毎時0分0秒でwavを再生。
        if min == 0 and sec == 0:

            # 時間によってボリュームを調整
            # 23時から翌朝5時まではボリュームを落とす
            if hour < 6 or hour > 22:
                subprocess.call("amixer set Master 50%", shell=True)
            else:
                subprocess.call("amixer set Master 100%", shell=True)

            # 時報の再生
            subprocess.call("/usr/bin/aplay {}/timetone/{}.wav".format(path, hour), shell=True)

            # 再生したら10秒スリープ
            time.sleep(10)

        time.sleep(0.1)

    print("時間監視終了")


def main():

    global running

    try:
        # マルチスレッドスタート
        thread_temp = threading.Thread(target=temp_and_humidity)
        thread_tone = threading.Thread(target=time_tone)

        thread_temp.start()
        thread_tone.start()

        # インスタンス化
        MainFrame()

        # 終了処理
        thread_tone.join()
        thread_temp.join()

    except:
        pass

    #終了処理
    GPIO.cleanup()
    running = False


if __name__ == '__main__':
    main()
