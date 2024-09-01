#!/usr/bin/env python3

# Filename: b_test 
__author__ = "raspython"
__date__ = '2024/09/01 16:52'

import TkEasyGUI as te #以下import文は省略
import math

# ポップアップを表示
QUIZ = [
    {"問題": "TCP/IPはインターネット通信の基本的なプロトコルである。", "答え": "Yes"},
    {"問題": "Javaはオブジェクト指向言語であるが、他重軽傷をサポートしている。", "答え": "No"}
]

ok = 0

# 出題
for i, qdate in enumerate(QUIZ):
    # リストから問題と答えを取り出す
    q = qdate["問題"]
    a = qdate["答え"]

    # ポップアップで問題を表示
    user = te.popup_yes_no(q, title=f"クイズ第{i+1}問目")
    # 答え合わせ
    if user == a:
        te.popup("正解")
        ok += 1
    else:
        te.popup("残念")

# 成績発表
rate = math.floor(ok / len(QUIZ) * 100)
te.popup(f"{ok}問正解。正解率:{rate}%", title="成績")