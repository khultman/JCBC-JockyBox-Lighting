
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
        GPIO.remove_event_detect(self._switch_pin)
        GPIO.add_event_detect(self._switch_pin, GPIO.RISING, callback=self.switch_mode, bouncetime=300)
        c_mode = self._mode
        if c_mode == "Initial":
            self._log.warn("Initial State", extra=self._logging_variables)
            self._mode = "Chase"
            self.execute_mode()
        elif c_mode == "Chase" and channel != "Automatic":
            self._log.warn("Transitioning from Chase to Rainbow", extra=self._logging_variables)
            self._mode = "Rainbow"
            self.execute_mode()
        elif c_mode == "Rainbow" and channel != "Automatic":
            self._log.warn("Transitioning from Rainbow to Twinkle", extra=self._logging_variables)
            self._mode = "Twinkle"
            self.execute_mode()
        elif c_mode == "Twinkle" and channel != "Automatic":
            self._log.warn("Transitioning from Twinkle to Solid", extra=self._logging_variables)
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
        if self._mode == "Chase":
            self.chase_selector()
        elif self._mode == "Rainbow":
            self.rainbow_selector()
        elif self._mode == "Twinkle":
            self.twinkle_selector()
        elif self._mode == "Solid":
            self.solid_color_selector()
        elif self._mode == "Disabled":
            self.stop()

    def chase_selector(self):
        while True:
            if self._mode != "Chase":
                break
            self._pixel.color_wipe(Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            self._pixel.rainbow_chase()

    def rainbow_selector(self):
        while True:
            if self._mode != "Rainbow":
                break
            self._pixel.side_wipe(Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            self._pixel.rainbow_cycle(75, 1)

    def twinkle_selector(self):
        while True:
            if self._mode != "Twinkle":
                break
            self._pixel.color_wipe(Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            self._pixel.twinkle(Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    def solid_color_selector(self):
        choice = random.randint(0, 3)
        if choice == 0:
            while True:
                if self._mode != "Solid":
                    break
                self._pixel.solid_white()
        elif choice == 1:
            while True:
                if self._mode != "Solid":
                    break
                self._pixel.solid_red()
        elif choice == 2:
            while True:
                if self._mode != "Solid":
                    break
                self._pixel.solid_green()
        elif choice == 3:
            while True:
                if self._mode != "Solid":
                    break
                self._pixel.solid_green()
        else:
            while True:
                if self._mode != "Solid":
                    break
                self._pixel.white_wipe()

    def stop(self):
        self._pixel.clear()

