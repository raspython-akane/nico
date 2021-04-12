

print("ABC123#$%ｱｲｳ".encode("shift_jis"))
print(b"ABCDEF123#$%")

print(hex(ord("A")))

# インポート
import el_display

# インスタンス化
so1602 = el_display.So1602a()

# コマンド関数の呼び出し
so1602.clear_display()
so1602.return_home()