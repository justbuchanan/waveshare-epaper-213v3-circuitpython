import displayio, busio, time
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.line import Line

import waveshare213V3

displayio.release_displays()

# create the spi device and pins we will need
spi = busio.SPI(waveshare213V3.SPI_SCK_PIN, MOSI=waveshare213V3.SPI_MOSI_PIN) # no MISO used

display_bus = displayio.FourWire(
    spi,
    command=waveshare213V3.DC_PIN,
    chip_select=waveshare213V3.CS_PIN,
    reset=waveshare213V3.RST_PIN,
    baudrate=waveshare213V3.SPI_BAUD_RATE,
)

display = waveshare213V3.Waveshare213V3(
    display_bus,
    busy_pin=waveshare213V3.BUSY_PIN,
)

g = displayio.Group()

color_bitmap = displayio.Bitmap(waveshare213V3.EPD_WIDTH, waveshare213V3.EPD_HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF

# background
bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
g.append(bg_sprite)

# draw some shapes
g.append(Line(100, 50, 100, 100, 0xFF0000))
g.append(Line(50, 50, 100, 100, 0xFF0000))
g.append(Rect(20, 20, 20, 20, fill=0xFF0000))

display.show(g)
display.refresh()

time.sleep(120)
