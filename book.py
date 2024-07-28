#!/usr/bin/env python3

# Filename: book 
__author__ = "raspython"
__date__ = '2024/07/22 19:27'

import tkinter as tk
import tkinter.messagebox as msg

def click_handler():
    """
    スイッチを押したときのイベント
    @return:
    """
    msg.showinfo(title="ｱｶﾈﾁｬﾝｶﾜｲｲﾔｯﾀｰ", message="ｱｶﾈﾁｬﾝｶﾜｲｲﾔｯﾀｰ")

def show_windows():
    """
    ウィンドウ作成
    @return:
    """
    # メインウィンドウ作成
    root =tk.Tk()
    root.wm_title("ｱｶﾈﾁｬﾝｶﾜｲｲﾔｯﾀｰbot")
    # 解像度
    root.geometry("300x200")

    # ラベルを作成
    tk.Label(root, text="あかねちゃんかわいいって言って？").pack()

    # スイッチを作成
    tk.Button(root, text="ｱｶﾈﾁｬﾝｶﾜｲｲﾔｯﾀｰ", command=click_handler).pack()

    # メインループ
    root.mainloop()


def main():
    show_windows()


if __name__ == '__main__':
    main()
