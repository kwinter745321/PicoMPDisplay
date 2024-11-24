# README.md - Application - Test and driver files for SSD1963 Graphics


## RP2040

The graphics require MicroPython 1.20 firmware or later.

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

| Filename          | function                              |
|-------------------| --------------------------------------|
| test


# Firmware

## RP2040-MP1.24


## RP2040-Build-LVGL

built on 14 Novemebr 2024.

Attempted to build firmware for LVGL 9.  This built MP 1.20
The MicroPython does work, but I never got the graphics to startup properly.