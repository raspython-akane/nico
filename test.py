import pigpio as pi
from time import sleep


# GPIOの初期設定
pi_g = pi.pi()


# 入力設定
pi_g.set_mode(21, pi.INPUT)
pi_g.set_pull_up_down(21, pi.PUD_DOWN)

pi_g.set_mode(4, pi.OUTPUT)

while True:
    print(pi_g.read(21))
    pi_g.write(4, 1)
    sleep(1)
    pi_g.write(4, 0)
    sleep(1)

