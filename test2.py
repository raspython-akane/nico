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
        d.clear_display()
        d.return_home()
    if w == 2:
        d.print("1234ABCDEabcdef##$$%%&$#ｱｲｳｴｵ", time=0.1)
    if w == 3:
        d.print_line(double_high=True)
    if w == 4:
        d.print_line(double_high=False)
    if w == 5:
        d.display_method(reverse=False)
    if w == 6:
        d.display_method(reverse=True)
    if w == 7:
        d.display_method(one_character=True)
    if w == 8:
        d.display_method(one_character=False)
    if w == 9:
        d.cursor_display_shift()
    if w == 10:
        d.cursor_display_shift(right_shift=False)
    if w == 11:
        d.cursor_display_shift(display_shift=True)