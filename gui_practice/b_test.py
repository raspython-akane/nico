#!/usr/bin/env python3

# Filename: b_test 
__author__ = "raspython"
__date__ = '2024/09/01 16:52'

import TkEasyGUI as te  #以下import文は省略

s = te.popup_no_wait(message="", title="", {"ICG": "RU"})
print(s)