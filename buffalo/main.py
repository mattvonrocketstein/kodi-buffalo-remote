""" buffalo.main
"""
import time
import pygame

from .axis import BuffaloAxis
from .buttons import BuffaloButtons
JOYSTICK_POLL_DELTA = .05


class Buffalo(object):

    def __init__(self, kodi):
        self.kodi = kodi
        self.axis = BuffaloAxis(kodi)
        self.buttons = BuffaloButtons(kodi)
        self.kodi.JSONRPC.Ping()
        self.kodi.show("initializing buffalo")

    def dispatch_default(event):
        print 'NO HANDLER:', event

    def loop(self, event):
        if event.type == pygame.JOYAXISMOTION:
            return self.axis.dispatch(event)
        elif event.type in [pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN]:
            return self.buttons.dispatch(event)
        else:
            return self.dispatch_default(event)

    def main_loop(self):
        while True:
            time.sleep(JOYSTICK_POLL_DELTA)
            for event in pygame.event.get():
                self.loop(event)
