import pigpio as pi

pi_g = pi.pi()
pi_g.set_mode(21, pi.INPUT)
pi_g.set_pull_up_down(21, pi.PUD_UP)

out_a1 = 6
out_a2 = 13
out_b1 = 19
out_b2 = 26

# 位置決めステップのカウント数
step_count = 0

# モータードライバの管理変数
r_count = 0

# 出力GPIOのリスト
pin_l = [out_a1, out_a2, out_b1, out_b2]

# 出力の値のリスト
# 2相励磁の出力の値を順にリスト化(17PM-K044データーシートより)
# データーシートの表の並びはa b a^ b^の順なので注意
out_val = [0b1010, 0b0110, 0b0101, 0b1001]
# 出力の場所のリスト
out_pin = [0b1000, 0b0100, 0b0010, 0b0001]



while True:
    print("loop")
    if pi_g.read(21) == 0:
        break

    # _countの値は0～3の間でループさせる
    r_count += r_count
    if r_count > 3:
        r_count = 0
    elif r_count < 0:
        r_count = 3

    step_count += r_count

    print("r_count: {}, step_count: {}".format(r_count, step_count))


    # 出力の値に上位1bit目から順番に1を積算して行き、各々のPINの出力を決める
    for i in range(4):
        # 出力の値を渡すのに該当桁が一桁目になるようにビットシフト
        out = (out_val[r_count] & out_pin[i]) >> (3 - i)
        pi_g.write(pin_l[i], out)
        print(bin(out_val[r_count] & out_pin[i]))
        print("GPIO_{}の出力 , {}".format(pin_l[i], out))

pi_g.write(out_a1, 0)
pi_g.write(out_a2, 0)
pi_g.write(out_b1, 0)
pi_g.write(out_b2, 0)
pi_g.stop()