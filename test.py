#! python3

# Filename: m_004_logic analyzer_test
__author__ = "raspython"
__date__ = '2020/06/21 10:43'


import RPi.GPIO as GPIO
from time import sleep

buz = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(buz, GPIO.OUT)
pwm = GPIO.PWM(buz, 50)
pwm.start(50)

# -----音階周波数-----
lsi = 247
do = 262
re = 294
mi = 330
fa = 349
so = 392
ra = 440
si = 494
hdo = 523
morse = 815

# -----楽譜date-----
onpu = (re, re, do, lsi, re, so, ra, si, si, si, ra, so, mi, mi, mi, fa, so, fa,\
        so, mi, re, mi, re, lsi, re, re, re, re, do,lsi, re, so, ra, si, si, si,\
        ra, so, ra, ra, ra, ra, so, so, fa, fa, so, so, so)
mtime = (4, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1,\
         1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1,\
         1)
stime = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,\
         8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4,\
         4)



# -----演奏-----

for (yodo, mero, stp) in zip(onpu, mtime, stime):
    pwm.ChangeDutyCycle(50)
    pwm.ChangeFrequency(yodo)
    sleep(mero / 10)
    pwm.ChangeDutyCycle(0)
    sleep(stp / 10)

pwm.stop()
GPIO.cleanup()

