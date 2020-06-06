#! python3
# -*- coding: utf-8 -*-
__author__ = "gaa"
__date__ = '2018/11/27 10:09'
"""
計算
"""
# 内包表記で条件のTrueをカウントできる
print(sum(n <= 30 for n in [0, 14, 18, 22, 0, 2, 4]))

# 四捨五入
rou = lambda x: (x * 2 + 1) // 2
print(rou(1.5))

# 割り算の切り上げ 切り捨ての//に負を掛けてもう一度負を掛けてあげてやる
print(-(-21 // 5))


"""
表記
"""

# ”””.formatで複数行の表示を入力できる
print("""Gold {}
Silver {}
Bronze {}
""".format(a, b, c))

"""
if
"""
# 3つ以上がすべて同じ課の判定 "A" == a == b
if "A" is a is b:
    pass

"""
ランダム生成
"""
cpu = (random.randint(1,100) % 3) + 1