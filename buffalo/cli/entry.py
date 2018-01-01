"""
"""
import os
import pygame
from ._kodi import Kodi
from .util import joystick_summary
from .main import Buffalo


def main():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.display.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()
    joystick_summary(joy)
    kodi_api = Kodi.get_handle()
    buffalo = Buffalo(kodi_api)
    buffalo.main_loop()
    main(buffalo, kodi_api)
