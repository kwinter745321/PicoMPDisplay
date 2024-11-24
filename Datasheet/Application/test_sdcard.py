# test_sdcard.py for PICO 2040
#
import sdcard, os
from machine import Pin, SPI

#CD pullup to VCC with 10K e.g. btn3
WP = None
SPISCK = 'GP14'
SPIMOSI = 'GP15'
SPIMISO = 'GP12'
CS = Pin('GP13')

sd = sdcard.SDCard(SPI(1), CS)
os.mount(sd, '/sd')
#print(os.listdir('/'))
os.chdir('/sd')
#os.mkdir('test')
print(os.listdir())



                     
                     