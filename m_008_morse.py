#! python3

# Filename: m_008_morse
__author__ = "raspython"
__date__ = '2020/08/14 08:00'

import wiringpi as pi
from time import sleep
import unicodedata


def main():
    """
    本体
    """
    """
    PIN NOの定義
    """
    buz = 21

    """
    GPIOの初期設定
    """
    pi.wiringPiSetupGpio()
    pi.softToneCreate(buz)

    """
    モールス符号用辞書
    """
    # キーは文字で値は長さ
    # 英数ひらがなに対応
    # 拗音 促音は通常の文字とする
    dic = {
        '0': [3, 3, 3, 3, 3],
        '1': [1, 3, 3, 3, 3],
        '2': [1, 1, 3, 3, 3],
        '3': [1, 1, 1, 3, 3],
        '4': [1, 1, 1, 1, 3],
        '5': [1, 1, 1, 1, 1],
        '6': [3, 1, 1, 1, 1],
        '7': [3, 3, 1, 1, 1],
        '8': [3, 3, 3, 1, 1],
        '9': [3, 3, 3, 3, 1],

        'a': [1, 3],
        'b': [3, 1, 1, 1],
        'c': [3, 1, 3, 1],
        'd': [3, 1, 1],
        'e': [1],
        'f': [1, 1, 3, 1],
        'g': [3, 3, 1],
        'h': [1, 1, 1, 1, ],
        'i': [1, 1],
        'j': [1, 3, 3, 3],
        'k': [3, 1, 3],
        'l': [1, 3, 1, 1],
        'm': [3, 3],
        'n': [3, 1],
        'o': [3, 3, 3],
        'p': [1, 3, 3, 1],
        'q': [3, 3, 1, 3],
        'r': [1, 3, 1],
        's': [1, 1, 1],
        't': [3],
        'u': [1, 1, 3],
        'v': [1, 1, 1, 3],
        'w': [1, 3, 3],
        'x': [3, 1, 1, 3],
        'y': [3, 1, 3, 3],
        'z': [3, 3, 1, 1],

        'あ': [3, 3, 1, 3, 3],
        'い': [1, 3],
        'う': [1, 1, 3],
        'え': [3, 1, 3, 3, 3],
        'お': [1, 3, 1, 1, 1],
        'か': [1, 3, 1, 1],
        'き': [3, 1, 3, 1, 1],
        'く': [1, 1, 1, 3],
        'け': [3, 1, 3, 3],
        'こ': [3, 3, 3, 3],
        'さ': [3, 1, 3, 1, 3],
        'し': [3, 3, 1, 3, 1],
        'す': [3, 3, 3, 1, 3],
        'せ': [1, 3, 3, 3, 1],
        'そ': [3, 3, 3, 1],
        'た': [3, 1],
        'ち': [1, 1, 3, 1],
        'つ': [1, 3, 3, 1],
        'て': [1, 3, 1, 3, 3],
        'と': [1, 1, 3, 1, 1],
        'な': [1, 3, 1],
        'に': [3, 1, 3, 1],
        'ぬ': [1, 1, 1, 1],
        'ね': [3, 3, 1, 3, ],
        'の': [1, 1, 3, 3],
        'は': [3, 1, 1, 1],
        'ひ': [3, 3, 1, 1, 3],
        'ふ': [3, 3, 1, 1],
        'へ': [1],
        'ほ': [3, 1, 1],
        'ま': [3, 1, 1, 3],
        'み': [1, 1, 3, 1, 3],
        'む': [3],
        'め': [3, 1, 1, 1, 3],
        'も': [3, 1, 1, 3, 1],
        'や': [1, 3, 3],
        'ゆ': [3, 1, 1, 3, 3],
        'よ': [3, 3],
        'ら': [1, 1, 1],
        'り': [3, 3, 1],
        'る': [3, 1, 3, 3, 1],
        'れ': [3, 3, 3],
        'ろ': [1, 3, 1, 3],
        'わ': [3, 1, 3],
        'を': [1, 3, 3, 3],
        'ん': [1, 3, 1, 3, 1],
        '゙': [1, 1],
        '゚': [1, 1, 3, 3, 1],
        'ー': [1, 3, 3, 1, 3]}


    """
    実行部
    """

    # 拗音 促音を変換するためのlistの用意
    pal_word = ["っ", "ゃ", "ゅ", "ょ",
                "ぁ", "ぃ", "ぅ", "ぇ", "ぉ"]
    con_word = ["つ", "や", "ゆ", "よ",
                "あ", "い", "う", "え", "お"]

    while True:

        """
        入力チェックと置き換え
        """
        # 英字の大文字は小文字に変換
        inp_w = input('発信したい文字を'
                      '半角英数、ひらがなで入れて'
                      'ください >> ').lower()
        print("入力された文字は 【{}】".format(inp_w))

        # 濁音と半濁音の処理
        # 合成文字の濁点と半濁点を結合文字へ変更
        inp_w = unicodedata.normalize("NFD", inp_w)
        print("結合文字に変換後【{}】".format(inp_w))


        # 入力された文字の拗音 促音を置き換え
        # 一文字毎リスト化
        for p, c in zip(pal_word, con_word):
            # print(p, c)
            inp_w = inp_w.replace(p, c)
            #  inp_w = [l.replace(p, c) for l in inp_w]
            # print(inp_w)
        # print("置き換え後の文字リスト 【{}】".format(inp_w))

        # 文字のチェック
        for w in inp_w:
            if "あ" <= w <= "ん" \
                    or "a" <= w <= "z" \
                    or "1" <= w <= "9" \
                    or w == "ー" \
                    or w == "゙" \
                    or w == "゚":
                pass

            else:
                print("半角英数、ひらがな以外が入っています")
                break
        else:
            print("入力チェックOK")
            break


    """
    制御
    """
    for word in inp_w:
        # 辞書のキーを指定して音を鳴らす
        # 長音は単音の3倍
        for long in dic[word]:
            print("発音してる文字 【{}】".format(word))
            print("発音の長さ 【{}】".format(long))
            pi.softToneWrite(buz, 1000)
            sleep(long / 15)
            pi.softToneWrite(buz, 0)
            # 符号間の間は短音と同じ間隔
            sleep(1 / 15)

        # 文字間は長音と同じ
        sleep(2 / 15)


if __name__ == '__main__':
    main()