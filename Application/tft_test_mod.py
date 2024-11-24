#
# Some sample code
#
import os, gc
from struct import unpack
import time
#import urandom
import math

#  drivers on /flash 
import tft
from font7hex import font7hex
from font10 import font10
from font14 import font14
from font36sevenseg import font36sevenseg
#from sevensegnumfont import sevensegnumfont
from touch import *

DIM_BG  = 1 #  # dim background data for text
KEEP_BG = 2 #const(2)  # keep background data for text
INV_BG  = 4 #const(4)  # invert the background data for text
INV_FG  = 8 #const(8)  # use the inverted background data for text color

red = b'\xff\x00\x00'
ltgreen = b'\x00\xff\x00'
blue = b'\x00\x00\xff'
yellow = b'\xff\xff\x00'
magenta = b'\xff\x00\xff'
cyan = b'\x00\xff\xff'
brown = b'\x80\x00\x00'
green = b'\x00\x80\x00'
ltgrey = b'\xc0\xc0\xc0'
dkgrey = b'\x80\x80\x80'
white = b'\xff\xff\xff'
black = b'\x00\x00\x00'

colorlist = [ white, dkgrey, red, green, blue, yellow, magenta, cyan, brown, green, ltgrey, black ]

mytouch = TOUCH("XPT2046")

def scale_value(value, in_min, in_max, out_min, out_max):
  scaled_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  return scaled_value

#
# buttonarray for touchpad:
#
# Example
# Define touch area                   | Define display of button        | Text in Button
# Value     Type        Area            Display        fgcolor   bgcolor  text    color
# str       "c"/"r"/"s" Tuple           False/"f"/"b"  opt.      opt.      value   opt.
# "A"       "c"         (x,y,r)         "f"            (0,255,0) False    "Yes"    None
# "B"       "c"         (x1,y1,x2,y2)   "f"            (255,0,0) False    "No"     None
# "OK"      "r"         (x1,y1,x2,y2)   "b"            (0,0,255) False    "OK"     None
#
keytable = [
    [ "A", "c", ( 50, 50, 25),      "f", (0, 255, 0),     False, "Yes",  (0,0,0)],
    [ "B", "c", (120, 50, 25),      "f", (255, 0, 0),     False, "No",   False],
    [ "C", "c", (190, 50, 25),      "b", (0, 0, 255),     False, "???",  False],
    [ "Q", "s", (260, 30, 320, 70), "f", (128, 128, 128), False, "Quit", False],
]


def get_stringsize(s, font):
    hor = 0
    for c in s:
        c = ord(c)
        _, vert, cols = font.get_ch(c)
        hor += cols
    return hor, vert

def print_centered(tft, x, y, s, color, font):
    length, height = get_stringsize(s, font)
    tft.setTextStyle(b'\xff\xff\xff', None, 2, font14)
    tft.setTextPos(x - length // 2, y - height // 2)
    tft.printString(s)

def get_from_keybd(tft, touchpad, keytable, font):
#
# first, check, if buttons are to be displayed
#
    # if not keytable:
    #     return None
    fgcolor = tft.getColor()  # save old colors
    bgcolor = tft.getBGColor()
    for key in keytable:
        dtype = key[3]
        if dtype:   # display the button?
            if key[4]:  # change color?
                tft.setColor(key[4])
            if key[5]:  # change BG color?
                tft.setBGColor(key[5])
            if key[7]:  # Font color?
                fontcolor = key[7]
            else:
                fontcolor = fgcolor
            if key[1] == "c":  # circle
                if dtype == "b":
                    tft.drawCircle(key[2][0], key[2][1], key[2][2])
                elif dtype == "f":
                    tft.fillCircle(key[2][0], key[2][1], key[2][2])
                if key[6]:
                    print_centered(tft, key[2][0], key[2][1], key[6], fontcolor, font)
            elif key[1] == "r": # rectangle
                if dtype == "b":
                    tft.drawRectangle(key[2][0], key[2][1], key[2][2], key[2][3])
                elif dtype == "f":
                    tft.fillRectangle(key[2][0], key[2][1], key[2][2], key[2][3])
                if key[6]:
                    tft.setColor(fontcolor)
                    print_centered(tft, (key[2][0] + key[2][2]) // 2, (key[2][1] + key[2][3]) // 2, key[6], fontcolor, font)
            elif key[1] == "s": # clipped rectangle
                if dtype == "b":
                    tft.drawClippedRectangle(key[2][0], key[2][1], key[2][2], key[2][3])
                elif dtype == "f":
                    tft.fillClippedRectangle(key[2][0], key[2][1], key[2][2], key[2][3])
                if key[6]:
                    tft.setColor(fontcolor)
                    print_centered(tft, (key[2][0] + key[2][2]) // 2, (key[2][1] + key[2][3]) // 2, key[6], fontcolor, font)
    tft.setColor(fgcolor) # restore them
    tft.setBGColor(bgcolor)
# get a touch value
    value = touchpad.get_touch()  # get a touch
    print("touch:",value)
    vx, vy = value
    newx = scale_value(vx, 480, 0, 0, 800)
    newy = scale_value(vy, 0, 272, 0, 480)
    value = (int(newx), int(newy))
    print("touch:",value)
# 
# check whether it is in one of the button areas
#
    if value:  # did not get a None
        for key in keytable:
            dx = value[0] - key[2][0]
            dy = value[1] - key[2][1]
            #print("key:",key[0],key[1],"d:",(dx * dx + dy * dy),"k:",(key[2][2] * key[2][2]))
            if key[1] == "c":  # circler
                dx = value[0] - key[2][0]
                dy = value[1] - key[2][1]
                if (dx * dx + dy * dy) < (key[2][2] * key[2][2]):  # Pythagoras is alive
                    print("returning",key[0])
                    return key[0]
            elif key[1] in ("r", "s"):  # rectangle
                if key[2][0] <= value[0] <= key[2][2] and key[2][1] <= value[1] <= key[2][3]:
                    return key[0]
    return None


#     value = mytouch.get_touch()  # get a touch (blocking)
# 
#     if value:
#         print(value,"x:",int(scale_value(value[0],10,480,800,0)),"y:",int(scale_value(value[1],10,272,0,480)))



def main(v_flip = False, h_flip = False):
    print("TFT Start")
    #mytft = tft.TFT("SSD1963", "LB04301", tft.LANDSCAPE, v_flip, h_flip)
    #mytft = tft.TFT("SSD1963", "AT070TN92", tft.PORTRAIT, v_flip, h_flip)
    #mytft = tft.TFT("SSD1963", "AT070TN92", tft.LANDSCAPE, True, h_flip)
    mytft = tft.TFT("SSD1963", "AT050TN92", tft.LANDSCAPE, v_flip, h_flip)
    width, height = mytft.getScreensize()
    #print(width, height)
    mytft.setXY(0, 0, 479, 815) # manual clear of the physical frame buffer
    mytft.tft_io.fillSCR(mytft.BGcolorvect, 480 * 816)

    mytft.backlight(100)

    
    if test1 == True:
        print("test 1")
        #drawpixel = mytft.drawPixel
        #GBR
        color = bytearray((255, 0, 0))
        start = time.ticks_ms()
        for i in range (0, 255):
            mytft.drawVLine(i, 0, 272, color)
        time0 = time.ticks_ms() - start
        print('  a. Draw 480 Vertical Lines: color:(255,0,0) [0-272] {} ms'.format(time0))
        time.sleep_ms(2000)
        
        start = time.ticks_ms()
        mytft.fillRectangle(0, 0, 479, 799, bytes(b'\x00\x00\x00')) # burst fill
        time0 = time.ticks_ms() - start
        print('  b. FillRectangle:           color:(0,0,0) (480x800) {} ms'.format(time0))
        time.sleep_ms(2000)
        
        start = time.ticks_ms()
        mytft.fillRectangle(0, 0, 479, 799, bytes(b'\x80\x80\x80')) # burst fill
        time0 = time.ticks_ms() - start
        print('  c. FillRectangle:     color:(128,128,128) (480x800) {} ms'.format(time0))
        time.sleep_ms(4000)
        
        start = time.ticks_ms()
        mytft.clrSCR(b'\xff\xff\xff')
        time0 = time.ticks_ms() - start
        print('  d. clrSCR:            color:(255,255,255) (480x800) {} ms'.format(time0))
        time.sleep_ms(2000)
        
        start = time.ticks_ms()
        mytft.clrSCR(b'\x00\x00\x00')
        time0 = time.ticks_ms() - start
        print('  e. clrSCR:                  color:(0,0,0) (480x800) {} ms'.format(time0))
        time.sleep_ms(2000)
                
        start = time.ticks_ms()
        mytft.clrSCR()
        time0 = time.ticks_ms() - start
        print('  f. clrSCR:                       color:() (480x800) {} ms'.format(time0))
        time.sleep_ms(2000)
        
    
    if test2 == True:
        print("test 2")
        mytft.clrSCR()
        #font = font10
        mytft.setTextStyle((240, 240, 240), None, 0, font7hex, 0)
        mytft.setTextPos(0, 0, 800, False)
        print(mytft.printString("This is font7hex text: 1234567890 abcd ABCD !@#$%"))
        mytft.drawHLine(0, 20, 400)
        
        mytft.setTextStyle((240, 240, 240), None, 0, font10, 0)
        mytft.setTextPos(0, 40, 800, False)
        print(mytft.printString("This is font10 text: 1234567890 abcd ABCD !@#$%"))
        mytft.drawHLine(0, 60, 400)
        
        mytft.setTextStyle((240, 240, 240), None, 0, font14, 0)
        mytft.setTextPos(0, 80, 800, False)
        print(mytft.printString("This is font14 text: 1234567890 abcd ABCD !@#$%"))
        mytft.drawHLine(0, 100, 600)
        
        #mytft.setTextStyle((240, 240, 240), None, 0, font36sevenseg, 0)
        mytft.setTextStyle((240, 240, 240), None, 0, font36sevenseg, 0)
        mytft.setTextPos(0, 120, 800, False)
        print(mytft.printString("1234567890"))  #only these
        mytft.drawHLine(0, 170, 300)

        time.sleep_ms(4000)

   
    if test3 == True:
        print("test 3")
        mytft.clrSCR()
       
#         for c in colorlist:
#             mytft.setColor(c)
#             for i in range(0,255):
#                 mytft.drawVLine(i, 100, 200)
#             mytft.setTextPos(300, 200)
#             mytft.setTextStyle(fgcolor=c, bgcolor=black, transparency=None, font=font14)
#             mytft.printString("text "+ str(c) + "     ")
#             time.sleep_ms(500)
            
        mytft.setColor(cyan)
        x0 = 100
        y0 = 100
        for x in range(100, 600, 5):
            y = int(50*math.sin(x)  + 100)
            mytft.drawLine(x0, y0, x,y, cyan)
            mytft.drawLine(100,100,600,100,red)
            x0 = x
            y0 = y
        time.sleep_ms(2000)
   
    if test4 == True:
        print("test 4")
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

    
    if test5 == True:
        print("test 5")
        mytft.clrSCR()
        mytft.setTextPos(0, 0)
        mytft.setTextStyle((255, 255, 255), None, 0, font7hex)
        mytft.printString("0123456789" * 5)
        mytft.setTextPos(0, 20)
        mytft.printString("abcdefghijklmnopqrstuvwxyz" * 2)
        time.sleep_ms(4000)
        
        mytft.clrSCR()
        mytft.setTextPos(0, 0)
        mytft.setTextStyle((0, 255, 0), None, KEEP_BG, font14)
        mytft.printString("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        mytft.setTextPos(0, 40)
        mytft.setTextStyle((0, 255, 0), None, 0, font14)
        mytft.printString("abcdefghijklmnopqrstuvwxyz")
        mytft.setTextPos(0, 80)
        mytft.printString("0123456789!\"$%&/()=?")
        time.sleep_ms(4000)

        mytft.setColor((255,255,255))
        mytft.fillClippedRectangle(200, 150, 300, 250, (255, 0, 0))
        mytft.drawClippedRectangle(0, 150, 100, 250, (0, 255, 0))
        time.sleep_ms(2000)

#    files = "F0012.bmp", "F0010.raw", "F0013.data","F0020_1.bmp", "F0020_2.bmp", "F0020_4.bmp", "F0020_8.bmp", "F0020.bmp", "F0013.bmp"
    files = "F0020_1.bmp", "F0020_2.bmp", "F0020_4.bmp", "F0020_8.bmp", "F0020.bmp"

    
    #mytft.setTextStyle((255, 255, 255), None, DIM_BG, font14)
    if test6 == True:
        print("test 6")
        mytft.setTextStyle((255, 255, 255), None, DIM_BG, font14)
        for name in files:
           # ## name = files[pyb.rng() % len(files)]
            start = time.ticks_ms()
            #displayfile(mytft, name, width, height)
            time0 = time.ticks_ms() - start
            print("Display {}: {} ms".format(name, time0))
            mytft.setTextPos(180, 230)
            mytft.printString(name)
            time.sleep_ms(2000)
            
    if test7 == True:
        print("test 7")
        mytft.clrSCR()
        start = time.ticks_ms()
        for color in [ white, dkgrey, red, green, blue, yellow, magenta, cyan, brown, green, ltgrey, black]:
            mytft.clrSCR(color)
            time.sleep_ms(1000)
        #mytft.drawPixel(i,j, color)
        time0 = time.ticks_ms() - start
        print('  a. Draw 480 Vertical Lines: color:(255,0,0) [0-272] {} ms'.format(time0))
        time.sleep_ms(2000)

    if test8 == True:
        print("test 8")
        mytft.clrSCR()
        rtn = ""
        while rtn != "Q":
            rtn = get_from_keybd(mytft, mytouch, keytable, font14) 
            print("rtn:",rtn) 

    if test9 == True:
        print("test 9")
        mytft.clrSCR()  
        c = 0
        for i in range(50,750, 50):
            mytft.drawCircle(i, 50, 20, colorlist[c])
            mytft.fillCircle(i, 100, 20, colorlist[c])
            mytft.drawRectangle(i-20, 150, i+20, 150+40, colorlist[c])
            mytft.fillRectangle(i-20, 200, i+20, 200+40, colorlist[c])
            for j in range(0, 40, 5):
                mytft.drawHLine(i-20, 250+j, 40, colorlist[c])
            for j in range(0, 40, 4):
                mytft.drawVLine(i+j-20, 300, 40, colorlist[c])
            c = c + 1
            if c > len(colorlist)-2:
                c = 0
        time.sleep_ms(4000)
        mytft.clrSCR()
        


##################################################################################



test1 = True  #clear screen
test2 = True  # four font size test
test3 = True   #not sure
test4 = True  #scroll text
test5 = True  #five time font7 two time font13 and two rect
test6 = False  #displayFile
test7 = True  #clear creen by colorlist
test8 = False   #test keyboard with touch
test9 = True


main(True, False)


print("done")

