# CircuitPython displayio-based driver for Waveshare 2.13 V3 ePaper display for raspberry pi pico
# * https://www.waveshare.com/pico-epaper-2.13.htm
# * Waveshare SKU 19406
# * black/white 250x122 pixel display
# * code based on https://github.com/waveshare/Pico_ePaper_Code

import board, displayio


# pin mapping for the waveshare "hat" / breakout board for raspberry pi pico
CS_PIN = board.GP9
DC_PIN = board.GP8
RST_PIN = board.GP12
BUSY_PIN = board.GP13

SPI_SCK_PIN = board.GP10
SPI_MOSI_PIN = board.GP11

# See official docs for the format of the commands here:
# https://docs.circuitpython.org/en/latest/shared-bindings/displayio/#displayio.EPaperDisplay
#
# Command and data values taken from https://github.com/waveshare/Pico_ePaper_Code/blob/a99adfb508d1f0a4a182d6763282709a4eddcd47/python/Pico_ePaper-2.13_V3.py
_START_SEQUENCE = (
    b"\x12\x00\x00"                 # software reset
    b"\x01\x00\x03\xF9\x00\x00"     # driver output control
    b"\x11\x00\x01\x03"             # data entry mode
    b"\x44\x00\x02\x00\x10"         # set window xStart, xEnd
    b"\x45\x00\x04\x00\x00\xF9\x00" # set window yStart, yEnd
    b"\x4E\x00\x01\x00"             # set x cursor
    b"\x4F\x00\x02\x00\x00"         # set y cursor
    b"\x3C\x00\x01\x05"             # border waveform?
    b"\x21\x00\x02\x00\x80"         # Display update control
    b"\x18\x00\x01\x80"             # read built-in temperature sensor

    # lookup table (LUT)
    b"\x32\x00\x99" # this bit is the command to update the LUT, the below
    # large block is the LUT itself. '\x99' means 153 LUT entries
    b"\x80\x4A\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x4A\x80\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x80\x4A\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x40\x4A\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\xF0\x00\x00\x00\x00\x00\x00\xF0\x00\x00\xF0\x00"
    b"\x00\x20\xF0\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x22\x22\x22\x22\x22\x22\x00\x00\x00"

    b"\x3F\x00\x01\x22"             # ?
    b"\x03\x00\x01\x17"             # gate voltage
    b"\x04\x00\x03\x41\x00\x32"     # source voltage - VSH, VSH2, VSL
    b"\x2C\x00\x01\x36"             # VCOM
)

_STOP_SEQUENCE = b"\x10\x00\x01\x01" # enter deep sleep mode


EPD_WIDTH  = 122
EPD_HEIGHT = 250


class Waveshare213V3(displayio.EPaperDisplay):
    def __init__(self, bus: displayio.FourWire, **kwargs):
        bus.reset()

        if EPD_WIDTH % 8 == 0:
            ram_width = EPD_WIDTH
        else:
            ram_width = (EPD_WIDTH // 8) * 8 + 8

        super().__init__(
            bus,
            _START_SEQUENCE,
            _STOP_SEQUENCE,
            **kwargs,
            width=EPD_WIDTH,
            height=EPD_HEIGHT,
            ram_width=ram_width,
            ram_height=EPD_HEIGHT, # TODO: divide by eight?
            two_byte_sequence_length = True, # LUT is too big to specify its size in 7 bits
            write_black_ram_command=0x24,
            set_column_window_command=0x44,
            set_row_window_command=0x45,
            set_current_column_command=0x4E,
            set_current_row_command=0x4F,
            refresh_display_command=0x20, # "display update control" - correct?
            refresh_time=3, # TODO
        )
