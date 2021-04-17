#!/usr/bin/env python3

# Filename: clock 
__author__ = "raspython"
__date__ = '2021/04/16 07:30'

from datetime import datetime
import locale
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


# ロケールを変更して曜日を日本語にする
locale.setlocale(locale.LC_ALL, "ja_JP.UTF-8")

"""
window作成
"""
# 作成準備
root = Tk()
style = ttk.Style()

"""
画像の準備
"""
# 茜

# 画像を開く
akane_img = Image.open("akane.png")
# リサイズ (70*80)
akane_resize = akane_img.resize(size=(140, 160))
# 画像の定義
akane_icon = ImageTk.PhotoImage(akane_resize)

"""
メインウィンドウ作成
"""
# 解像度
root.geometry("1024x600")
# タイトル
root.title("Clock and Weather Widget")


"""
メインフレームの作成
"""
flame = ttk.Frame(root)
flame.grid()




def now_time():
    """

    @return:
    """
    now = datetime.now()
    # 時間を時計の関数に渡す
    clock_label(now.hour, now. minute, now.second)
    # 年月日をカレンダー表示に渡す
    calemder_label(now.year, now.month, now.day, now.strftime("%a"))


    # 0.1秒後に再度関数の呼び出しで
    # 時間の更新
    root.after(100, now_time)



def calemder_label(y, m, d, wd):

    day = ttk.Label(
        # フレームの指定
        flame,
        # 年月日の表示
        text="{0:0>4d}年{1:0>2d}月{2:0>2d}日  （{3:}曜日）".format(y, m, d, wd),
        # フォントの種類とサイズ
        font=("IPAGothic", 50),
        background="black",
        foreground="white")
    day.place(width=880, x=0, y=0)




def clock_label(h, m, s):
    """
    時計表示のラベル
    @param flame: 表示するフレーム
    """
    clock = ttk.Label(
        # フレームの指定
        flame,
        # 時間の表示
        text="{0:0>2d}:{1:0>2d}:{2:0>2d}".format(h, m, s),
        # フォントの種類とサイズ
        font=("IPAGothic", 90),
        # 配置場所
        anchor="center",
        # 背景色
        background="black",
        # 文字の色
        foreground="white",
        # BGの余白広さ
        padding=(0, 0))
    # 配置位置
    clock.grid(row=1, column=0)


def akane_label(flame, img):
    """

    @return:
    """
    # ラベルの定義
    akane = ttk.Label(
        flame,
        image=img)


    akane.grid(row=1, column=1)







def main():

    """
    ラベルの呼び出し
    """
    # 茜
    akane_label(flame, akane_icon)
    # 時間を習得し表示
    now_time()


    root.mainloop()


    
if __name__ == '__main__':
    main()
