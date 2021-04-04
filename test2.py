#!/usr/bin/env python3

# Filename: test2 
__author__ = "raspython"
__date__ = '2021/04/04 08:03'


import el_display

d = el_display.SO1602A()

while True:
    w = int(input())
    if w == 0:
        break
    if w == 1:
        print("ディスプレイの初期化")
        d.clear_display()
        d.return_home()
    if w == 2:
        print("文字の表示")
        d.print("ｱｶﾈﾁｬﾝｶﾜｲｲﾔｯﾀｰ      ", time=0.1)
    if w == 3:
        print("double_high ON")
        d.print_line(double_high=True)
    if w == 4:
        print("double_high OFF")
        d.print_line(double_high=False)
