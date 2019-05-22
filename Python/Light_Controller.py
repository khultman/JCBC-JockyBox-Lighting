
import logging
import RPi.GPIO as GPIO
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
        self._mode = "Default"

    def switch_mode(self):
        switch_mode()

    def stop(self):
        self._pixel.clear()
