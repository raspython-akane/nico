# TKinterでウィンドウを生成。茨城の天気情報を取得して、ウィンドウに表示。

from tkinter import *

root = Tk()

weather_info = get_weather_info('Ibaraki')

lbl = Label(root, text=weather_info)
lbl.pack()

root.mainloop()