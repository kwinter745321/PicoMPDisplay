#
# Some sample code
#
import os, gc
from struct import unpack
import time
import urandom

from machine import Pin

import tft
from font14 import font14
from font10 import font10
#from sevensegnumfont import sevensegnumfont
from font7hex import font7hex

DIM_BG  = const(1)  # dim background data for text
KEEP_BG = const(2)  # keep background data for text
INV_BG  = const(4)  # invert the background data for text
INV_FG  = const(8)  # use the inverted background data for text color

def displayfile(mytft, name, width, height):
    with open(name, "rb") as f:
        gc.collect()
        row = 0
        parts = name.split(".") # get extension
        if len(parts) > 1:
            mode = parts[-1].lower()
        if mode == "raw": # raw 16 bit 565 format with swapped bytes
            b = bytearray(width * 2)
            imgheight = os.stat(name)[6] // (width * 2)
            skip = (height - imgheight) // 2
            if skip > 0:
                mytft.fillRectangle(0, 0, width - 1, skip, (0, 0, 0))
            else:
                skip = 0
            for row in range(skip, height):
                n = f.readinto(b)
                if not n:
                    break
                tft.tft_io.swapbytes(b, width * 2)
                mytft.drawBitmap(0, row, width, 1, b, 16)
            mytft.fillRectangle(0, row, width - 1, height - 1, (0, 0, 0))
        elif mode == "bmp":  # Windows bmp file
            BM, filesize, res0, offset = unpack("<hiii", f.read(14))
            (hdrsize, imgwidth, imgheight, planes, colors, compress, imgsize,
             h_res, v_res, ct_size, cti_size) = unpack("<iiihhiiiiii", f.read(40))
            if imgwidth <= width: ##
                skip = ((height - imgheight) // 2)
                if skip > 0:
                    mytft.fillRectangle(0, height - skip, width - 1, height - 1, (0, 0, 0))
                else:
                    skip = 0
                if colors in (1,4,8):  # must have a color table
                    if ct_size == 0: # if 0, size is 2**colors
                        ct_size = 1 << colors
                    colortable = bytearray(ct_size * 4)
                    f.seek(hdrsize + 14) # go to colortable
                    n = f.readinto(colortable) # read colortable
                    if colors == 1:
                        bsize = imgwidth // 8
                    elif colors == 2:
                        bsize = imgwidth // 4
                    elif colors == 4:
                        bsize = imgwidth // 2
                    elif colors == 8:
                        bsize = imgwidth
                    # for i in range(0, ct_size * 4, 4):
                        # colortable[i], colortable[i + 2] = colortable[i + 2], colortable[i]
                    bsize = (bsize + 3) & 0xfffc # must read a multiple of 4 bytes
                    b = bytearray(bsize)
                    f.seek(offset)
                    for row in range(height - skip - 1, -1, -1):
                        n = f.readinto(b)
                        if n != bsize:
                            break
                        mytft.drawBitmap(0, row, imgwidth, 1, b, colors, colortable)
                else:
                    f.seek(offset)
                    if colors == 16:
                        bsize = (imgwidth*2 + 3) & 0xfffc # must read a multiple of 4 bytes
                        b = bytearray(bsize)
                        for row in range(height - skip - 1, -1, -1):
                            n = f.readinto(b)
                            if n != bsize:
                                break
                            mytft.drawBitmap(0, row, imgwidth, 1, b, colors)
                    elif colors == 24:
                        bsize = (imgwidth*3 + 3) & 0xfffc # must read a multiple of 4 bytes
                        b = bytearray(bsize)
                        for row in range(height - skip - 1, -1, -1):
                            n = f.readinto(b)
                            if n != bsize:
                                break
                            mytft.drawBitmap(0, row, imgwidth, 1, b, colors)
                mytft.fillRectangle(0, 0, width - 1, row, (0, 0, 0))
        elif mode == "data": # raw 24 bit format with rgb data (gimp export type data)
            b = bytearray(width * 3)
            imgheight = os.stat(name)[6] // (width * 3)
            skip = (height - imgheight) // 2
            if skip > 0:
                mytft.fillRectangle(0, 0, width - 1, skip, (0, 0, 0))
            else:
                skip = 0
            for row in range(skip, height):
                n = f.readinto(b)
                if not n:
                    break
                tft.tft_io.swapcolors(b, width * 3)
                mytft.drawBitmap(0, row, width, 1, b, 24)
            mytft.fillRectangle(0, row, width - 1, height - 1, (0, 0, 0))
    mytft.backlight(100)

def main(v_flip = False, h_flip = False):
    print("main")
    #mytft = tft.TFT("SSD1963", "LB04301", tft.LANDSCAPE, v_flip, h_flip)
    #mytft = tft.TFT("SSD1963", "AT050TN92", tft.LANDSCAPE, v_flip, h_flip)
    #print("AT050TN92")
    mytft = tft.TFT("SSD1963", "AT070TN92", tft.LANDSCAPE, v_flip, False)
    width, height = mytft.getScreensize()
    print(width, height)
    mytft.setXY(0, 0, 479, 815) # manual clear of the pyhsical frame buffer
    mytft.tft_io.fillSCR(mytft.BGcolorvect, 480 * 816)

    mytft.backlight(100)

    if True:
        drawpixel = mytft.drawPixel
        color = bytearray((0, 255, 0))
        start = time.ticks_ms()
        for i in range (0, 480):  # filling pixel-by-pixel
            mytft.drawVLine(i, 0, 272, color)
            # for j in range (0, 271):
                # drawpixel(i, j, color)
        time0 = time.ticks_ms() - start
        print('DrawPixels: {} ms'.format(time0))
        time.sleep_ms(2000)

        mytft.fillRectangle(0, 0, 479, 799, bytes(b'\x00\x00\x00')) # burst fill
        start = time.ticks_ms()
        for _ in range(2):
            mytft.clrSCR(b'\xff\xff\xff')
            # mytft.fillRectangle(0, 0, 479, 799, bytes(b'\xff\xff\xff')) # burst fill
            time.sleep_ms(500)
            mytft.clrSCR(b'\x00\x00\x00')
            # mytft.fillRectangle(0, 0, 479, 799, bytes(b'\x00\x00\x00')) # burst fill
            time.sleep_ms(500)
        time0 = time.ticks_ms() - start
        print('FillRectangle: {} ms'.format((time0 - 2000)/4))
        time.sleep_ms(1000)

    if True:
        mytft.clrSCR()
        font = font10
        mytft.setTextStyle((240, 240, 240), None, 0, font, 0)
        mytft.setTextPos(0, 0, 200, False)
        print(mytft.printString("This text will be cut after some characters"))
        mytft.drawHLine(0, 20, 200)
        time.sleep_ms(4000)



    if False:
        mytft.clrSCR()
        mytft.setTextPos(0, height * 0)
        mytft.setTextStyle((255, 0, 0), None, 0, font7hex)
        mytft.printString("This is text on Page 1")

        mytft.setTextPos(0, height * 1)
        mytft.setTextStyle((0, 255, 0), None, 0, font7hex)
        mytft.printString("This is text on Page 2")

        mytft.setTextPos(0, height * 2)
        mytft.setTextStyle((0, 0, 255), None, 0, font7hex)
        mytft.printString("This is text on Page 3")

        for i in range(3):
            mytft.setScrollStart(height * 0)
            time.sleep_ms(1000)
            mytft.setScrollStart(height * 1)
            time.sleep_ms(1000)
            mytft.setScrollStart(height * 2)
            time.sleep_ms(1000)
        mytft.setScrollStart(height * 0)

    if True:
        mytft.clrSCR()
        s = "0123456789"
        font = font10
        mytft.setTextStyle((240, 240, 240), None, 0, font, 1)
        bfa = height % font.bits_vert + font.bits_vert
        vsa = height - bfa
        mytft.setScrollArea(0, vsa, bfa)
        mytft.setTextPos(0, height - font.bits_vert)
        mytft.printString("           This is the non-scrolling area")
        mytft.setTextPos(0, 0)
        for j in range(70):
            mytft.printString("Line {:4} ".format(j))
            for i in range(3):
                mytft.printString(s)
            mytft.printCR()      # No, then CR
            mytft.printNewline() # NL: advance to the next line
            x,y = mytft.getTextPos()
            mytft.setTextPos(0, height - font.bits_vert)
            mytft.printString("Line {:4} ".format(j))
            mytft.setTextPos(x,y)
        mytft.printString(">")
        time.sleep_ms(2000)

    if True:
        mytft.clrSCR()
        mytft.setTextPos(0, 0)
        mytft.setTextStyle((255, 255, 255), None, 0, font7hex)
        mytft.printString("0123456789" * 5)
        mytft.setTextPos(0, 20)
        mytft.printString("abcdefghijklmnopqrstuvwxyz" * 2)
        time.sleep_ms(2000)

        mytft.setTextPos(0, 0)
        mytft.setTextStyle((0, 255, 0), None, KEEP_BG, font14)
        mytft.printString("ABCDE        NOPQRSTUVWXYZ")
        mytft.setTextPos(0, 40)
        mytft.setTextStyle((0, 255, 0), None, 0, font14)
        mytft.printString("abcdefghijklmnopqrstuvwxyz")
        mytft.setTextPos(0, 80)
        mytft.printString("0123456789!\"$%&/()=?")
        time.sleep_ms(2000)

        mytft.setColor((255,255,255))
        mytft.fillClippedRectangle(200, 150, 300, 250, (255, 0, 0))
        mytft.drawClippedRectangle(0, 150, 100, 250, (0, 255, 0))
        time.sleep_ms(2000)

    if seven:
        mytft.clrSCR()
        cnt = 3
        mytft.setTextStyle((255,255,255), None, 0, sevensegnumfont)
        while cnt >= 0:
            mytft.setTextPos((width // 2) - 32, (height // 2) - 30)
            mytft.printString("{:2}".format(cnt))
            cnt -= 1
            time.sleep_ms(1000)

        gc.collect()
        mytft.clrSCR()
        buf = bytearray(5000)
        with open ("logo50.raw", "rb") as f:
            n = f.readinto(buf)
        mytft.tft_io.swapbytes(buf, 5000)
        for i in range(3):
            mytft.clrSCR()
            for cnt in range(50):
                x = urandom.randint(0, width - 51)
                y = urandom.randint(0, height - 51)
                mytft.drawBitmap(x, y, 50, 50, buf, 16)
            time.sleep_ms(1000)

#    files = "F0012.bmp", "F0010.raw", "F0013.data","F0020_1.bmp", "F0020_2.bmp", "F0020_4.bmp", "F0020_8.bmp", "F0020.bmp", "F0013.bmp"
    files = "F0020_1.bmp", "F0020_2.bmp", "F0020_4.bmp", "F0020_8.bmp", "F0020.bmp"

    mytft.setTextStyle((255, 255, 255), None, DIM_BG, font14)
    while seven:
        for name in files:
           # ## name = files[pyb.rng() % len(files)]
            start = time.ticks_ms()
            displayfile(mytft, name, width, height)
            time0 = time.ticks_ms() - start
            print("Display {}: {} ms".format(name, time0))
            mytft.setTextPos(180, 230)
            mytft.printString(name)
            time.sleep_ms(6000)


gp17 = Pin("GP17",Pin.OUT)
gp17.on()
time.sleep_ms(10)
gp17.off()
time.sleep_ms(20)
gp17.on()
seven = False
main(False, False)
print("done")

