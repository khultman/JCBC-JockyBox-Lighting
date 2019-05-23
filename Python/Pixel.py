import math
from neopixel import *
import time


# LED strip configuration:
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (12 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering


class Pixel(object):
    def __init__(self, count=LED_COUNT, pin=LED_PIN, frequency=LED_FREQ_HZ,
                 dma=LED_DMA, brightness=LED_BRIGHTNESS, invert=LED_INVERT,
                 channel=LED_CHANNEL, strip=LED_STRIP):
        self._led_count = count
        self._led_pin = pin
        self._led_frequency = frequency
        self._led_dma = dma
        self._led_brightness = brightness
        self._led_invert = invert
        self._led_channel = channel
        self._led_strip = strip
        self._strip = Adafruit_NeoPixel(self._led_count, self._led_pin, self._led_frequency,
                                        self._led_dma, self._led_invert, self._led_brightness,
                                        self._led_channel, self._led_strip)
        self._strip.begin()

    @staticmethod
    def _is_number(item):
        return type(item) in (int, float)

    def clear(self):
        for i in range(self._strip.numPixels()):
            self._strip.setPixelColor(i, Color(0, 0, 0))
        self._strip.show()

    def color_wipe(self, color, wait_ms=75):
        # Wipe color across display a pixel at a time.
        for i in range(self._strip.numPixels()):
            self._strip.setPixelColor(i, color)
            self._strip.show()
            time.sleep(wait_ms/1000.0)

    def red_wipe(self):
        self.color_wipe(Color(255, 0, 0))

    def blue_wipe(self):
        self.color_wipe(Color(0, 255, 0))

    def green_wipe(self):
        self.color_wipe(Color(0, 0, 255))

    def white_wipe(self):
        self.color_wipe(Color(127, 127, 127))

    def side_wipe(self, color, wait_ms=75):
        # Wipe color from outside in
        for i in range(math.ceil(self._strip.numPixels()/2)):
            self._strip.setPixelColor(i, color)
            self._strip.setPixelColor(self._strip.numPixels()-i, color)
            self._strip.show()
            time.sleep(wait_ms/1000.0)

    def chase(self, color, wait_ms=75, iterations=10):
        # Movie theater light style chaser animation.
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self._strip.numPixels(), 3):
                    self._strip.setPixelColor(i+q, color)
                self._strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self._strip.numPixels(), 3):
                    self._strip.setPixelColor(i+q, 0)

    def red_chase(self):
        self.chase(Color(255, 0, 0))

    def blue_chase(self):
        self.chase(Color(0, 255, 0))

    def green_chase(self):
        self.chase(Color(0, 0, 255))

    def white_chase(self):
        self.chase(Color(127, 127, 127))

    def rainbow_chase(self, wait_ms=75):
        # Rainbow movie theater light style chaser animation.
        for j in range(256):
            for q in range(3):
                for i in range(0, self._strip.numPixels(), 3):
                    self._strip.setPixelColor(i+q, self.wheel((i+j) % 255))
                self._strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self._strip.numPixels(), 3):
                    self._strip.setPixelColor(i+q, 0)

    @staticmethod
    def wheel(pos):
        # Generate rainbow colors across 0-255 positions.
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow(self, wait_ms=50, iterations=1):
        # Draw rainbow that fades across all pixels at once.
        for j in range(256*iterations):
            for i in range(self._strip.numPixels()):
                self._strip.setPixelColor(i, self.wheel((i+j) & 255))
            self._strip.show()
            time.sleep(wait_ms/1000.0)

    def rainbow_cycle(self, wait_ms=50, iterations=5):
        # Draw rainbow that uniformly distributes itself across all pixels.
        for j in range(256*iterations):
            for i in range(self._strip.numPixels()):
                self._strip.setPixelColor(i, self.wheel((int(i * 256 / self._strip.numPixels()) + j) & 255))
            self._strip.show()
            time.sleep(wait_ms/1000.0)

    def twinkle(self, color, wait_ms=75, duration=10):
        nsteps = 10
        self._strip.fill((0, 0, 0))
        leds = {}
        for i in range(0, self._strip.numPixels()):
            j = random.randint(0, self._led_count-1)
            k = random.randint(0, 1)
            while j in leds:
                j = random.randint(0, self._strip.numPixels()-1)
            leds[j] = [k, int(i*nsteps/self._strip.numPixels())]
            start = time.monotonic()
            while time.monotonic()-start < duration:
                for k, v in leds.items():
                    if v[1] == nsteps:
                        leds.pop(k, None)
                        self._strip.setPixelColor(i, color)
                        j = random.randint(0, self._led_count-1)
                        i = random.randint(0, 1)
                        while j in leds:
                            j = random.randint(0, self._led_count-1)
                        leds[j] = [i, 0]
                    else:
                        factor = (2.0*v[1]/nsteps)
                        if v[1] > nsteps/2:
                            factor = 2-factor
                        if self._is_number(v[0]):
                            self._strip.setPixelColor(k, color)
        self._strip.show()
        time.sleep(wait_ms/1000.0)
