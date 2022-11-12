# CircuitPython driver for Waveshare 2.13" V3 Pico ePaper display

This project is a driver for a small (122px X 250px) eInk/ePaper display for the Raspberry Pi Pico. See the [product page](https://www.waveshare.com/pico-epaper-2.13.htm) for more details and pictures.

This driver implementation is based on code from https://github.com/waveshare/Pico_ePaper_Code, but ported to CircuitPython, using the [displayio library](https://docs.circuitpython.org/en/latest/shared-bindings/displayio/#displayio.EPaperDisplay).

There are multiple ways to interface with this display using a raspberry pi. The manufacturer provides code samples in C and python (based on micropython). I am currently using CircuitPython for a project, so I ported the supplied micropython code to CircuitPython.

## Running the example

- Install CircuitPython (I'm using the [8.0.0 beta](https://github.com/adafruit/circuitpython/releases/tag/8.0.0-beta.4))

- Copy the driver and example to the pi:

  - copy `waveshare213v3.py` as-is
  - copy `example.py`, but rename to `main.py`

- Install required dependencies
  - [Adafruit_CircuitPython_Display_Shapes](https://github.com/adafruit/Adafruit_CircuitPython_Display_Shapes)
    - From https://github.com/adafruit/Adafruit_CircuitPython_Display_Shapes/releases/tag/2.5.6, download adafruit-circuitpython-display-shapes-8.x-mpy-2.5.6.zip
    - Unzip it
    - From the unzipped folder, copy `lib/adafruit_display_shapes/` into the `/lib` folder of the raspberry pi device

## Limitations

- Doesn't support rotation of the display. The defaults work, but setting the display's rotation to something other than `0` causes problems.
- The display blinks on and off twice on startup. I understand some blinking is a necessary thing with ePaper, but this feels excessive...
