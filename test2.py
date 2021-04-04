#!/usr/bin/env python3

# Filename: test2 
__author__ = "raspython"
__date__ = '2021/04/04 08:03'


import el_display

d = el_display.SO1602A()
d.char_display("1234ABCDEabcdef##$$%%&$#ｱｲｳｴｵ")