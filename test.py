# PCA9685 PWMサーボ/LEDコントローラライブラリの簡単なデモです。
# チャンネル0を最小値から最大値まで繰り返し動かします。
# 作者 Tony DiCola
# License: パブリックドメイン
from __future__ import division
import time


# PCA9685モジュールをインポートします。
import Adafruit_PCA9685

# デバッグ出力を有効にするためにアンコメントします。
# import logging
# logging.basicConfig(level=logging.DEBUG)

# PCA9685をデフォルトのアドレス(0x40)で初期化します。
pwm = Adafruit_PCA9685.PCA9685()

# あるいは、別のアドレスやバスを指定することもできます。
# pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# 最小と最大のサーボパルス長を設定する
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096


# サーボのパルス幅の設定をより簡単にするヘルパー関数です。
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000  # 1,000,000 us per second
    pulse_length //= 60  # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096  # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)


# 周波数をサーボに適した60hzに設定する。
pwm.set_pwm_freq(60)

print('Moving servo on channel 0, press Ctrl-C to quit...')
while True:
    # Move servo on channel O between extremes.
    pwm.set_pwm(0, 0, servo_min)
    time.sleep(1)
    pwm.set_pwm(0, 0, servo_max)
    time.sleep(1)