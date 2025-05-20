# PicoDisplay-PicoMPDisplay-Differences

20 May 2025

This document attempts to explain the differences between the PicoDisplay
and the PicoMPDisplay.  It presents a Back History and then a feature table.

# Back History
The main reason for the boards was to reduce the clutter of wires and
provide firm device connections.

## Pico Display BB
The Pico Display Base Board was designed (in 2023) to support the PicoMite
(and MMBasic.) To this end, it hard-wired pins (per PicoMite) to the female
2x20 "display" port.
Which means one can just plug-in a five (or seven inch) SSD1963 display.
There are jumpers to handle the 3v3 logic and (5v for the 7inch
backlight).

The other ports on the board also support devices built-in to the PicoMite
software. So the SD Card on SSD1963 works.  By plugging a cheap RTC into
its port, you get date/time on the board.  And so, the files on the SD Card
now have proper dates.  Also the PicoMite file system commands just work
nicely.  Additionally, the PicoMite also supports the IR Port.

## Pico MP Display BB
The PicoMPDisplay BB was designed (in 2024) to support the SSD1963 for
MicroPython using Roberthh's code.  His code made use of the Pico's PIO
features to improve the display speed.
Alas, robert's code only provided two possible pinouts which turned out to
be incompatible with the PicoMite pinout.  Hence the new board.  While I
was there I made a few improvements.

## Other Uses
You do not have to use the 2x20 Display Port.  The Pico Display BB or
PicoMP Display can then be hand-wired to be used for Other Uses since there
is a male header for each side of the Pico Board.
So, in Dec 2025/Jan 2025, I happened to follow Peter Hinge's Nano code for
small 2.4 inch ILI9341 displays and simply hand-wired the display to the
Base Board.  The Base Board holds the Pico board steady and provides LEDs
and PushButtons, etc. Since January, I have been using LVGL-MicroPython
with 2-to-4 inch displays which is a good alternative to the PicoMite.

# Feature Table

The boards hold the standard Pico USB board.  Pico* is the same size for Pico, PicoW and Pico2.

|   Feature                      | PicoDisplay BB | PicoMPDisplay BB | Comments |
|--------------------------------|----------------|------------------|----------|
|  100mmx85mm Base Board         |       x        |        x         |          |
| two sets of mount holes        |       x        |        x         |          |
| Display Port (DP) for SSD1963  |       x        |        x         |          |
| DP hard-wired per PicoMite(TM) |       x        |        -         |          |
| DP hard-wired per roberthh     |       -        |        x         |          |
| Female port for standard Pico* |       x        |        x         |          |
| Male headers for Pico*         |       x        |        x         |          |
| USB-C Power Port (for 5 volt)  |       x        |        x         |          |
| RTC Port hard-wired to I2C     |       x        |        x         | Note 5   |
| OLED Port hard-wired to I2C    |       x        |        x         | Note 1   |
| Potentiometer (10K)            |       x        |        x         |          |
| Pushbuttons (two)              |       x        |        x         | Note 2   |
| LEDs (two)                     |       x        |        x         | Note 3   |
| IR Port                        |       x        |        x         | Note 4   |
| UART-0 Port                    |       -        |        x         |          |

- Note 1 - Cannot be used at same time with SSD1963 for PicoMite
- Note 2 - Pulled-up with 10 resistors
- Note 3 - LEDs (Green/Red) connected to 220 Ohm [221] resistor to Ground
- Note 4 - Signal connected to GP22
- Note 5 - Extra female right-angle port (could be used to add pullups or connection to external devices)

