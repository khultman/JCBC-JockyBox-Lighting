
import logging
import RPi.GPIO as GPIO
from neopixel import Color
from Pixel import Pixel


class Lights(object):
    def __init__(self, pixel_count = 30, pixel_pin = 12, switch_pin = 2):
        self._log = logging.getLogger(__name__)
        self._logging_variables = {}
        self._logging_variables['instance_id'] = self.__class__.__name__
        self._pixel_count = pixel_count
        self._pixel_pin = pixel_pin
        self._switch_pin = switch_pin
        self._pixel = Pixel(self._pixel_count, self._pixel_pin)
        GPIO.setup(self._switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self._switch_pin, GPIO.RISING, callback=self.switch_mode, bouncetime=300)
        self._mode = "Enabled"

    def switch_mode(self):
        self._log.warn("Mode Button Pushed, channel {0}".format(channel), extra=self._logging_variables)
        cmode = self._mode
        if cmode == "Enabled":
            self._mode = "Disabled"
        else:
            self._mode = "Enabled"

    def lightshow(self):
        while True:
            if self._mode == "Enabled":
                self._pixel.color_wipe(Color(range(255), range(255), range(255)))
                self._pixel.rainbow_chase()
                self._pixel.side_wipe(Color(range(255), range(255), range(255)))
                self._pixel.rainbow_cycle()
                self._pixel.color_wipe(Color(range(255), range(255), range(255)))
                self._pixel.twinkle(Color(range(255), range(255), range(255)))
                self._pixel.side_wipe(Color(range(255), range(255), range(255)))
            else:
                self.log.debug("Lightshow disabled")
                self._pixel.clear()

    def stop(self):
        self._pixel.clear()

