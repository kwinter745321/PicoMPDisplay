# PicoMPDisplay
 SSD1963 Display Board for MicroPython Pico

The Pico MP Display Base Board v1.0.1 is a printed circuit board (PCB) designed for a Raspberry Pi Pico “RP2040” board (“Pico”) and a SSD1963 LCD display board.  

- Note: This board expects RP2040 MicroPython 1.20 or later firmware. 

- For the current demonstration software see the [README.md](https://github.com/kwinter745321/PicoMPDisplay/tree/main/Application) in the Application directory.

The 24-bit graphics are fast because the display uses eight data lines.  The pictures demonstrate the Pico MP Display Base Board hosting a five (5) inch 800x480 pixel display and a seven (7) inch 800x480 pixel display.  Affordable displays simply insert into the Display Port.  A separate power connector provides power to the seven inch display and optionally it can power the whole system.

|   Description                 | Pictures|
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------- |
|   Five-inch SSD1963 Display  |  <img src="Images\FiveInch-ColorDemo.jpg" width="400">                                                                                                                   |
|   Seven-inch SSD1963 Display  | <img src="Images\SevenInch-ColorDemo.jpg" width="400">                                                                                                                |


The Pico MP Display Base Board is especially suitable for projects requiring a large LCD Display with a touchscreen and integrated SD card.  The graphics are based on roberthh’s MicroPython TFT class library.  

The PCB includes various onboard components and ports for external devices. The male headers provide a flexible means to wire connections to the components. The ports have PCB connections to Pico pins and permit an easy way to simply insert the external devices. There should be no need to solder any wires nor drill holes for any parts.

## Component Details
The matching Pico male headers provide an easy means to wire to onboard devices or to test the with a Logic Analyzer. The male headers can also be used to add connections to sensors and devices on an external breadboard.

The PCB supports several external devices via ports:

- The SSD1963 LCD Display with integrated Touch and SD Card.
- DS3231/AT24Cxx module with a 3-volt CR2032 coin battery adapter.
- Bluetooth/UART module.
- 0.96 inch OLED display board.
- Infrared Receiver board.

The 40-pin Display Port is wired to specific GPIO pins to provide an 8-data line interface for the 24-bit color 800*480 LCD display and SPI pins for the Thin Film Transistor (TFT) Touchscreen and SD Card. The PCB includes jumpers for LCD display power and for the display board’s optional flash chip. 

## TFT Support
The recommended software is roberthh’s TFT class library at his GitHub site.  He developed the software for a 4.3 inch and a 7 inch display using the RP2040 PIO for the interface.  All of his software runs in MicroPython 1.20 or later. 

The author has five inch and seven inch SSD1963 integrated LCD displays (with Touch and SD Card).  He modified roberthh’s TFT file slightly to support these displays.  And he modified roberthh’s test program to demonstrate more of the primitive graphics and touch. The driver and test files are at the author’s GitHub.  The resulting software can be incorporated into your projects now. Note: this is the files found in the Application folder of this repo. [README.md](Application\README.md)

Over time the author hopes to update the GitHub site with additional MicroPython code to provide a higher level of graphics.