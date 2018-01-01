"""
"""
import os
import pygame
from buffalo._kodi import Kodi
from buffalo.util import joystick_summary
from buffalo.main import Buffalo

SDL_VIDEODRIVER = os.environ.get(
    "SDL_VIDEODRIVER", "dummy")
JOYSTICK_DEV = int(os.environ.get(
    "JOYSTICK_DEV", "0"))


def main():
    os.environ["SDL_VIDEODRIVER"] = SDL_VIDEODRIVER
    pygame.init()
    pygame.display.init()
    joy = pygame.joystick.Joystick(JOYSTICK_DEV)
    joy.init()
    joystick_summary(joy)
    kodi_api = Kodi.get_handle()
    buffalo = Buffalo(kodi_api)
    buffalo.main_loop()
    main(buffalo, kodi_api)
