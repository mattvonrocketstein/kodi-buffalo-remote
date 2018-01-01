""" buffalo.buttons
"""
import pygame

KEYMAP = dict(
    select=6, start=7,
    left=4, right=5,
    a=0, red=0,
    b=1, yellow=1,
    x=2, blue=2,
    y=3, green=3, )

REVERSE_KEYMAP = dict(zip(KEYMAP.values(), KEYMAP.keys()))


class BuffaloButtons(object):

    def __init__(self, kodi):
        self.kodi = kodi

    def dispatch(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            for k in KEYMAP:
                if KEYMAP[k] == event.button:
                    try:
                        fxn = getattr(self, '{0}'.format(k))
                    except NameError:
                        pass
                    else:
                        return fxn(event)
            return self.default(event)

    def select(self, event):
        self.kodi.show('select -> Back')
        return self.kodi.Input.Back()

    def start(self, event):
        self.kodi.show('start -> ContextMenu')
        return self.kodi.Input.ContextMenu()

    def blue(self, event):
        self.kodi.show('blue-X -> Home')
        return self.kodi.GUI.ActivateWindow({"window": "home"})

    def red(self, event):
        self.kodi.show('red-A -> Player.PlayPause')
        return self.kodi.Player.PlayPause()

    def yellow(self, event):
        self.kodi.show('yellow-B -> PlayPause')
        return self.kodi.Player.PlayPause()

    def left(self, event):
        self.kodi.volume_decrement()

    def right(self, event):
        self.kodi.volume_increment()

    def default(self, event):
        self.kodi.show('{0} -> Select'.format(
            REVERSE_KEYMAP[event.button].upper()))
        return self.kodi.Input.Select()

    x = blue
    a = red
    b = yellow
    y = green = default
