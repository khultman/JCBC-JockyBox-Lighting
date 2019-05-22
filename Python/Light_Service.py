#!/usr/bin/env python3

import argparse
import logging
from Light_Controller import Lights
from logger import MLOGGER


class LightService(object):
    def __init__(self):
        self._args = self.get_cli_args(sys.argv[1:])
        self.mlogger = MLOGGER(None, level=self._args.loglevel, logtype=self._args.logtype, filename=self._args.logfile)
        self._logging_variables = {}
        self._logging_variables['instance_id'] = self.__class__.__name__
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.debug("_args passed in", extra=self._logging_variables)
        self._log.debug(vars(self._args), extra=self._logging_variables)
        self.lights = Lights( self._args.Pixel_Count, self._args.Pixel_Pin, self._args.Switch_Pin)

    @staticmethod
    def get_cli_args(args=None):
        parser = argparse.ArgumentParser(description='Run the Light Controller Service')
        basic_cfg = parser.add_argument_group('JockyBox Configuration')
        basic_cfg.add_argument("-cy", "--cycle",
                               help="Time in seconds between each loop cycle, defaults to 600",
                               type=int,
                               action="store",
                               dest="cycle",
                               default=600)
        basic_gpio = parser.add_argument_group("GPIO Configuration")
        basic_gpio.add_argument("-sp", "--switchpin",
                                help="GPIO of Switch Pin, default 2",
                                type=int,
                                action="store",
                                dest="DoorPin",
                                default=2)
        basic_pix = parser.add_argument_group('Neopixel Configuration')
        basic_pix.add_argument("-pp", "--pixelpin",
                               help="GPIO of NeoPixel Controller",
                               type=int,
                               action="store",
                               dest="PixelPin",
                               default="12")
        basic_pix.add_argument("--pixels",
                               help="The number of pixels connected to the strip",
                               type=int,
                               action="store",
                               dest="PixelPixels",
                               default=30)
        basic_pix.add_argument("--pixelchannel",
                               help="PWM Channel of NeoPixel",
                               type=int,
                               choices=[0, 1],
                               action="store",
                               dest="pixel_channel",
                               default=0)
        results = parser.parse_args(args)
        return results

    def main(self):
        try:
            self._log.debug("Entering main loop", extra=self._logging_variables)
            while True:
                self.lights.lightshow()
                time.sleep(self._args.cycle)
        except KeyboardInterrupt:
            self.lights.stop()
            pass


if __name__ == '__main__':
    service = LightService()
    service.main()
