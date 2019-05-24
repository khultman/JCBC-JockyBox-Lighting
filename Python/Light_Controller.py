
import logging
import math
import random
import RPi.GPIO as GPIO
import threading
from neopixel import Color
from Pixel import Pixel


class Lights(object):
    cur_mode = ""

    def __init__(self, pixel_count=30, pixel_pin=12, switch_pin=4):
        global cur_mode
        self._log = logging.getLogger(__name__)
        self._logging_variables = {}
        self._logging_variables['instance_id'] = self.__class__.__name__
        self._pixel_count = pixel_count
        self._pixel_pin = pixel_pin
        self._switch_pin = switch_pin
        self._pixel = Pixel(self._pixel_count, self._pixel_pin)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self._switch_pin, GPIO.RISING, callback=self.switch_mode, bouncetime=200)
        self._mode = "Chase"
        cur_mode = self._mode
        self._light_thread = threading.Thread(name='light_show', target=self.execute_mode)
        self._light_thread.setDaemon(True)

    def switch_mode(self, channel):
        self._log.warn("Mode Button Pushed, channel {0}".format(channel), extra=self._logging_variables)
        global cur_mode
        c_mode = self._mode
        if c_mode == "Chase" and channel != "Automatic":
            self._log.warn("Transitioning from Chase to Rainbow", extra=self._logging_variables)
            self._mode = "Rainbow"
        elif c_mode == "Rainbow" and channel != "Automatic":
            self._log.warn("Transitioning from Rainbow to Twinkle", extra=self._logging_variables)
            self._mode = "Twinkle"
        elif c_mode == "Twinkle" and channel != "Automatic":
            self._log.warn("Transitioning from Twinkle to Solid", extra=self._logging_variables)
            self._mode = "Solid"
        elif c_mode == "Solid" and channel != "Automatic":
            self._log.warn("Transitioning from Solid color to SolidWhite", extra=self._logging_variables)
            self._mode = "SolidWhite"
        elif c_mode == "SolidWhite" and channel != "Automatic":
            self._log.warn("Transitioning from SolidWhite color to SolidRed", extra=self._logging_variables)
            self._mode = "SolidRed"
        elif c_mode == "SolidRed" and channel != "Automatic":
            self._log.warn("Transitioning from SolidRed color to SolidBlue", extra=self._logging_variables)
            self._mode = "SolidBlue"
        elif c_mode == "SolidBlue" and channel != "Automatic":
            self._log.warn("Transitioning from SolidBlue color to SolidGreen", extra=self._logging_variables)
            self._mode = "SolidGreen"
        elif c_mode == "SolidGreen" and channel != "Automatic":
            self._log.warn("Transitioning from SolidGreen color to Disabled", extra=self._logging_variables)
            self._mode = "Disabled"
        elif c_mode == "Disabled" and channel != "Automatic":
            self._log.warn("Enabling Lightshow", extra=self._logging_variables)
            self._mode = "Chase"
        elif channel == "Automatic":
            self._log.warn("Automatic bump, continuing current mode", extra=self._logging_variables)
        cur_mode = self._mode

    def execute_mode(self):
        global cur_mode
        while True:
            self._log.warn("Executing mode {0}".format(cur_mode), extra=self._logging_variables)
            if cur_mode == "Chase":
                self.chase_selector()
            elif cur_mode == "Rainbow":
                self.rainbow_selector()
            elif cur_mode == "Twinkle":
                self.twinkle_selector()
            elif cur_mode == "Solid":
                self.solid_color_selector()
            elif cur_mode == "SolidWhite":
                self.solid_color_white()
            elif cur_mode == "SolidRed":
                self.solid_color_red()
            elif cur_mode == "SolidBlue":
                self.solid_color_blue()
            elif cur_mode == "SolidGreen":
                self.solid_color_green()
            elif cur_mode == "Disabled":
                self.stop()

    def light_thread(self):
        if self._light_thread.is_alive():
            return
        else:
            self._light_thread.start()

    def chase_selector(self):
        global cur_mode
        if cur_mode != "Chase":
            return
        self._pixel.color_wipe(Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self._pixel.rainbow_chase()

    def rainbow_selector(self):
        global cur_mode
        if cur_mode != "Rainbow":
            return
        self._pixel.side_wipe(Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self._pixel.rainbow_cycle(75, 1)

    def twinkle_selector(self):
        global cur_mode
        if cur_mode != "Twinkle":
            return
        self._pixel.color_wipe(Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self._pixel.twinkle(Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    def solid_color_white(self):
        global cur_mode
        if cur_mode != "SolidWhite":
            return
        self._pixel.solid_white()

    def solid_color_red(self):
        global cur_mode
        if cur_mode != "SolidRed":
            return
        self._pixel.solid_red()

    def solid_color_blue(self):
        global cur_mode
        if cur_mode != "SolidBlue":
            return
        self._pixel.solid_blue()

    def solid_color_green(self):
        global cur_mode
        if cur_mode != "SolidGreen":
            return
        self._pixel.solid_green()

    def solid_color_selector(self):
        global cur_mode
        choice = random.randint(0, 3)
        if choice == 0:
            cur_mode = "SolidWhite"
            self.solid_color_white()
        elif choice == 1:
            cur_mode = "SolidRed"
            self.solid_color_red()
        elif choice == 2:
            cur_mode = "SolidBlue"
            self.solid_color_blue()
        elif choice == 3:
            cur_mode = "SolidGreen"
            self.solid_color_green()
        else:
            self._pixel.white_wipe()

    def stop(self):
        self._pixel.clear()
