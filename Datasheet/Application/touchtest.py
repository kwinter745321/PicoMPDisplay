#
# Some sample code
#
import os, gc
from uctypes import addressof
#from tft import *
import tft
from touch import *
from TFTfont import *
import font14

DIM_BG  = const(1)  # dim background data for text
KEEP_BG = const(2)  # keep background data for text
INV_BG  = const(4)  # invert the background data for text
INV_FG  = const(8)  # use the inverted background data for text color



#
# Get string dimensions in pixels
# 
def get_stringsize(s, font):
    hor = 0
    for c in s:
        c = ord(c)
        _, vert, cols = font.get_ch(c)
        hor += cols
    return hor, vert

def print_centered(tft, x, y, s, color, font):
    length, height = get_stringsize(s, font)
    print("L,H:",length,height)
    tft.setTextStyle(b'\xff\xff\xff', None, 2, font14)
    tft.setTextPos(x - length // 2, y - height // 2)
    tft.printString(s)

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

def get_from_keybd(tft, touchpad, keytable, font):
#
# first, check, if buttons are to be displayed
#
    if not keytable:
        return None
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
# 
# check whether it is in one of the button areas
#
    if value:  # did not get a None
        for key in keytable:
            if key[1] == "c":  # circler
                dx = value[0] - key[2][0]
                dy = value[1] - key[2][1]
                if (dx * dx + dy * dy) < (key[2][2] * key[2][2]):  # Pythagoras is alive!
                    return key[0]
            elif key[1] in ("r", "s"):  # rectangle
                if key[2][0] <= value[0] <= key[2][2] and key[2][1] <= value[1] <= key[2][3]:
                    return key[0]
    return None

def scale_value(value, in_min, in_max, out_min, out_max):
  scaled_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  return scaled_value


def main():

    #mytft = TFT("SSD1963", "LB04301", LANDSCAPE)
    mytft = tft.TFT("SSD1963", "AT050TN92", tft.LANDSCAPE, False, False)
    width, height = mytft.getScreensize()
    print(width, height)
    mytft.setXY(0, 0, 479, 815) # manual clear of the physical frame buffer
    mytft.tft_io.fillSCR(mytft.BGcolorvect, 480 * 816)
    

    
    
    mytouch = TOUCH("XPT2046")
    mytft.backlight(100) # light on

    #mytft.setTextStyle((255, 255, 255), None, 0, font14)
    print("main loop: before while")
    cnt = 0
    rtn = ""
    while rtn != "Q":
        #rtn = get_from_keybd(mytft, mytouch, keytable, font14)
        value = mytouch.get_touch()  # get a touch
        print(value,"x:",int(scale_value(value[0],10,480,800,0)),"y:",int(scale_value(value[1],10,272,0,480)))
        if cnt >= 5:
            rtn = 'Q'
            print("Returned: ", rtn)
        #mytft.setTextPos(0, 150)
        #mytft.setTextStyle(None, None, 0, font14)
        #mytft.setTextStyle((255, 255, 255), None, 0, font14)
        #mytft.printString("Button Value: " + repr(rtn) + " ")
        cnt = cnt + 1
        time.sleep(2)

main()
