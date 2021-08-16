import smbus
from time import sleep
import datetime
import pigpio as pi

# pinの定義
int_pin = 26

# GPIOの初期設定
pi_g = pi.pi()
# 入力設定
pi_g.set_mode(int_pin, pi.INPUT)


REG_INTR_STATUS_1 = 0x00
REG_INTR_STATUS_2 = 0x01
REG_INTR_ENABLE_1 = 0x02
REG_INTR_ENABLE_2 = 0x03
REG_FIFO_WR_PTR = 0x04
REG_OVF_COUNTER = 0x05
REG_FIFO_RD_PTR = 0x06
REG_FIFO_DATA = 0x07
REG_FIFO_CONFIG = 0x08
REG_MODE_CONFIG = 0x09
REG_SPO2_CONFIG = 0x0A
REG_LED1_PA = 0x0C
REG_LED2_PA = 0x0D
REG_PILOT_PA = 0x10
REG_MULTI_LED_CTRL1 = 0x11
REG_MULTI_LED_CTRL2 = 0x12
REG_TEMP_INTR = 0x1F
REG_TEMP_FRAC = 0x20
REG_TEMP_CONFIG = 0x21
REG_PROX_INT_THRESH = 0x30
REG_REV_ID = 0xFE
REG_PART_ID = 0xFF

class MAX30102():
    # setup()相当の部分
    def __init__(self, channel=1, address=0x57, gpio_pin=7):
        # Raspberry Piでi2cを行う各種設定
        self.address = address
        self.channel = channel
        # i2cのセットアップ
        self.bus = smbus.SMBus(self.channel)

        self.reset()

        sleep(1) # wait 1 sec

        # 割り込みレジスタを読み捨て(この心拍センサは割り込みレジスタを読むと割り込み状態をクリアする)
        reg_data = self.bus.read_i2c_block_data(self.address, REG_INTR_STATUS_1, 1)

        self.setup()

    def reset(self):
        self.bus.write_i2c_block_data(self.address, REG_MODE_CONFIG, [0x40])

    def setup(self, led_mode=0x03):
        # INTR setting
        self.bus.write_i2c_block_data(self.address, REG_INTR_ENABLE_1, [0xc0])
        self.bus.write_i2c_block_data(self.address, REG_INTR_ENABLE_2, [0x00])

        # FIFO_WR_PTR[4:0]
        self.bus.write_i2c_block_data(self.address, REG_FIFO_WR_PTR, [0x00])
        # OVF_COUNTER[4:0]
        self.bus.write_i2c_block_data(self.address, REG_OVF_COUNTER, [0x00])
        # FIFO_RD_PTR[4:0]
        self.bus.write_i2c_block_data(self.address, REG_FIFO_RD_PTR, [0x00])

        # sample avg = 4, fifo rollover = false, fifo almost full = 17
        self.bus.write_i2c_block_data(self.address, REG_FIFO_CONFIG, [0x4f])

        # 0x02 for read-only, 0x03 for SpO2 mode, 0x07 multimode LED
        self.bus.write_i2c_block_data(self.address, REG_MODE_CONFIG, [led_mode])
        # SPO2_ADC range = 4096nA, SPO2 sample rate = 100Hz, LED pulse-width = 411uS
        self.bus.write_i2c_block_data(self.address, REG_SPO2_CONFIG, [0x27])

        # choose value for ~7mA for LED1
        self.bus.write_i2c_block_data(self.address, REG_LED1_PA, [0x24])
        # choose value for ~7mA for LED2
        self.bus.write_i2c_block_data(self.address, REG_LED2_PA, [0x24])
        # choose value fro ~25mA for Pilot LED
        self.bus.write_i2c_block_data(self.address, REG_PILOT_PA, [0x7f])

    # 赤色/IRのLEDのデータを読むのはこれ
    def read_fifo(self):
        red_led = None
        ir_led = None

        # read 1 byte from registers (values are discarded)
        reg_INTR1 = self.bus.read_i2c_block_data(self.address, REG_INTR_STATUS_1, 1)
        reg_INTR2 = self.bus.read_i2c_block_data(self.address, REG_INTR_STATUS_2, 1)

        # read 6-byte data from the device
        d = self.bus.read_i2c_block_data(self.address, REG_FIFO_DATA, 6)

        # mask MSB [23:18]
        red_led = (d[0]<<16 | d[1] << 8 | d[2]) & 0x03FFFF
        ir_led = (d[3]<<16 | d[4] << 8 | d[5]) & 0x03FFFF

        return red_led, ir_led

def main():
    m = MAX30102()
    try:
        m.setup()

        for i in range(100):
            while pi_g.read(int_pin) == 1:
                pass
            red, ir = m.read_fifo()
            time = datetime.datetime.now()
            print(time, red, ir)



    except KeyboardInterrupt:

        pass


if __name__ == '__main__':
    main()