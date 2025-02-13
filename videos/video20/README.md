# README.md - video 20

# Using ILI9341 LCD Display

## files on the Desktop

aclock.py is the "main program" file that makes call into the API.

## API Files on the Pico
	
| Folders | File list |
|---------|-----------|
| drivers | boolpalette.py |
|         | li9341_pico.py |
|         | ili9341.py      |
|         |                  | 
| gui     | core "folder"    |
|         | fonts "folder"   |
|         | widgets "folder" |
|         |                 |
| color_setup.py |          |
|           |              |


Changes were minimized to keep Peter's files as is as uch as possible.

Notes:
- The imports were updated with the proper folder. (Becuase they were moved.)
- The color_setup.py is modified to use ili9341_pico.

CWriter is the classs