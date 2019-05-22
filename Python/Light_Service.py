
import argparse
import logging
from Light_Controller import Lights

class Light_Service(object):
    def __init__(self):
        self._args = self.get_cli_args(sys.argv[1:])
        self.lights = Lights( self._args.Pixel_Count, self._args.Pixel_Pin, self._args.Switch_Pin )

    def get_cli_args(self, args=None):
        parser = argparse.ArgumentParser(description='Run the Light Controller Service')

    def main(self):
        try:
            self._log.debug("Entering main loop", extra=self._logging_variables)
            while True:
                self.lights.switch_mode()
                time.sleep(self._args.cycle)
        except KeyboardInterrupt:
            self.lights.stop()
            pass

if __name__ == '__main__':
    service = Light_Service()
    service.main()
