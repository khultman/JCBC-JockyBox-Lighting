
import logging
import math
import random
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
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self._switch_pin, GPIO.RISING, callback=self.switch_mode, bouncetime=300)
        self._mode = "Initial"

    def switch_mode(self, channel):
        self._log.warn("Mode Button Pushed, channel {0}".format(channel), extra=self._logging_variables)
        c_mode = self._mode
        if c_mode == "Initial":
            self._log.warn("Initial State", extra=self._logging_variables)
            self._mode = "Lightshow"
            self.execute_mode()
        elif c_mode == "Lightshow" and channel != "Automatic":
            self._log.warn("Transitioning from Lightshow to solid color", extra=self._logging_variables)
            self._mode = "Solid"
            self.execute_mode()
        elif c_mode == "Solid" and channel != "Automatic":
            self._log.warn("Transitioning from Solid color to disabled", extra=self._logging_variables)
            self._mode = "Disabled"
            self.execute_mode()
        elif c_mode == "Disabled" and channel != "Automatic":
            self._log.warn("Enabling Lightshow", extra=self._logging_variables)
            self._mode = "Lightshow"
            self.execute_mode()
        elif channel == "Automatic":
            self._log.warn("Automatic bump, continuing current mode", extra=self._logging_variables)
            self.execute_mode()

    def execute_mode(self):
        self._log.warn("Executing mode {0}".format(self._mode), extra=self._logging_variables)
        if self._mode == "Lightshow":
            self.light_show()
        elif self._mode == "Solid":
            self.solid_color_selector()
        elif self._mode == "Disabled":
            self.stop()

    def light_show(self):
        while True:
            if self._mode == "Lightshow":
                self._pixel.color_wipe(Color(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
                self._pixel.rainbow_chase()
            else:
                self._log.debug("Lightshow disabled")
                self.stop()
            if self._mode == "Enabled":
                self._pixel.side_wipe(Color(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
                self._pixel.rainbow_cycle()
            else:
                self._log.debug("Lightshow disabled")
                self.stop()
            if self._mode == "Enabled":
                self._pixel.color_wipe(Color(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
                self._pixel.twinkle(Color(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            else:
                self._log.debug("Lightshow disabled")
                self.stop()
            if self._mode == "Enabled":
                self._pixel.side_wipe(Color(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            else:
                self._log.debug("Lightshow disabled")
                self.stop()

    def solid_color_selector(self):
        choice = random.randint(0, 3)
        if choice == 0:
            while True:
                self._pixel.white_wipe()
        elif choice == 1:
            while True:
                self._pixel.red_wipe()
        elif choice == 2:
            while True:
                self._pixel.green_wipe()
        elif choice == 3:
            while True:
                self._pixel.blue_wipe()
        else:
            while True:
                self._pixel.white_wipe()

    def stop(self):
        self._pixel.clear()

