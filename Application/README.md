# README.md - Application - Test and driver files for SSD1963 Graphics

The inspiration for this collection is the TFT driver from "roberthh"
[LINK to roberthh's GitHub site with TFT driver ](https://github.com/robert-hh/SSD1963-TFT-Library-for-PyBoard-and-RP2040)

November 24, 2024

I collected the files that worked with my five and seven inch SSD1963 display and made minor modifications.
It is a very basic collection of graphics.  roberthh created tft.py using the RP2040 PIO (tft_pio.py) in 2017.
So, only the RP2040 chip works with the tft driver.

Meanwhile....

Seems Robert colloborated with Peter Hinch.  And Peter developed several GUI libraries (Nano-GUI and Micro-GUI).  The Micro GUI uses asyncio.  
Alas they are designed for the smaller "SPI" style LCD displays.  The next step is to migrate Peter's micro-GUI program and use roberthh's TFT SSD1963 library.

# Testing

Below is the current working set of files that I tested with a five (5) inch display. 
Disable test 6 as I have not integrate the sdcard yet.

If you plug in a seven inch Display then make sure to edit the test file slightly.
Make sure to disable test 6 and test 8 (as the touch needs to be calibrated)
Then change the last line as follows: main(True, False)


## FILES THAT WORK ON RP2040

The graphics requires MicroPython 1.20 firmware or later.

### DRIVER FILES (must reside on Pico)

| Filename          | function                              |
|-------------------| --------------------------------------|
| font7hex.py       | small font                            |
| font10.py         | font                                  |
| font14.py         | font (often default)                  |
| font36sevenseg.py | looks like 7 segments                 |
| sdcard.py         | SD Card driver                        |
| tft_pio.py        | tft "pio" driver required by tft      |
| tft.py            | main driver for graphics              |
| TFTfont.py        | font driver required by any font file |
| touch.py          | XPT2046 touch driver                  |

### TEST FILES

| Filename          | function                                   |
|-------------------| -------------------------------------------|
| test_sdcard       | Brief stand-alone test of SD Card          |
| tft_test.py       | Roberthh's slightly modified LCD test file |
| tft_test_mod.py   | I modified above to add more tests         |

| Test 6 in the tft_test_mod.py file does an integrated Touch/LCD test.  I modified this slightly to work in landscape mode.

Roberthh's site discusses how to generate Font files.
