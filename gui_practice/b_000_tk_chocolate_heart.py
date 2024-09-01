#!/usr/bin/env python3

# Filename: book 
__author__ = "raspython"
__date__ = '2024/07/22 19:27'

import tkinter as tk
import tkinter.messagebox as mes

from click import command

nyn_counter = 0
icg_counter = 0

root = tk.Tk()
root.title("お菓子作りの材料屋さん")
root.geometry("300x50")


def click_handler(button):
    """
    ボタンを押したときのイベント
    @return:
    """
    global nyn_counter
    global icg_counter

    nyn =["ないです", "ないです", "ない",
          """しょうがないさ今日はバレンタインデー
             お菓子作りの材料は全部売り切れだよ"""]

    icg = ["タマゴをください。", "あ、ない。じゃあ牛乳を。", "小麦粉。", "やめたら！この仕事！！！"]

    # NYN姉貴の対応
    mes.showinfo(title="nyn姉貴",message=nyn[nyn_counter])

    # 「お菓子作りの材料は全部売り切れだよ」が表示されたらウィンドウを閉じる
    if nyn[nyn_counter] == """しょうがないさ今日はバレンタインデー
             お菓子作りの材料は全部売り切れだよ""":
        root.destroy()  # ウィンドウを閉じる
        return


    # NYNが対応するたびにセリフを変える
    nyn_counter += 1
    icg_counter += 1

    # ボタンを押されるたびにボタンのテキストを更新
    button.config(text=icg[icg_counter])


def icg_button():
    """
    windowを表示する関数
    @return:
    """

    icg = ["タマゴをください。", "あ、ない。じゃあ牛乳を。", "小麦粉。", "やめたら！この仕事！！！"]

    tk.Label(root,text="icg姉貴").pack()

    # ICG姉貴のセリフをボタンとして作成。commandにボタン自体を引数として渡す
    button = tk.Button(root, text=icg[icg_counter], command=lambda: click_handler(button))
    button.pack()


icg_button()

# メインループ
root.mainloop()

