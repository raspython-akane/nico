

print("ABC123#$%ｱｲｳ".encode("shift_jis"))
print(b"ABCDEF123#$%")

print(hex(ord("A")))

# インポート
import el_display

val = 0
val |= 0b000_00100
print(bin(val))