"""
    * jstest /dev/input/js0
"""
import os
import time
import pygame
from kodijson import Kodi as BaseKodi

JOYSTICK_POLL_DELTA = .05

KODI_HOST = os.environ.get('KODI_HOST', 'localhost:8080')
USER = os.environ.get('KODI_USER', 'guest')
PASSWORD = os.environ.get('KODI_PASSWORD', 'guest')


class BuffaloAxis(object):
    def __init__(self, kodi):
        self.kodi = kodi

    def dispatch(self, event):
        if event.value == 0:
            return
        elif event.axis == 1 and event.value == 1:
            return self.down(event)
        elif event.axis == 1 and event.value < 0:
            return self.up(event)
        elif event.axis == 0 and event.value == 1:
            return self.right(event)
        elif event.axis == 0 and event.value < 0:
            return self.left(event)

    def down(self, event):
        self.kodi.show('down')
        return self.kodi.Input.Down()

    def up(self, event):
        self.kodi.show('up')
        return self.kodi.Input.Up()

    def right(self, event):
        self.kodi.show('right')
        return self.kodi.Input.Right()

    def left(self, event):
        self.kodi.show('left')
        return self.kodi.Input.Left()


class Buffalo(object):

    def __init__(self, kodi):
        self.kodi = kodi
        self.axis = BuffaloAxis(kodi)
        self.buttons = BuffaloButtons(kodi)
        self.kodi.JSONRPC.Ping()
        self.kodi.show("initializing buffalo")

    def dispatch_default(event):
        print event

    def loop(self, event):
        if event.type == pygame.JOYAXISMOTION:
            return self.axis.dispatch(event)
        elif event.type in [pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN]:
            return self.buttons.dispatch(event)
        else:
            return self.dispatch_default(event)


class BuffaloButtons(object):

    KEYMAP = dict(
        select=6, start=7,
        left=4, right=5,
        a=0, red=0,
        b=1, yellow=1,
        x=2, blue=2,
        y=3, green=3, )

    REVERSE_KEYMAP = dict(zip(KEYMAP.values(), KEYMAP.keys()))

    def __init__(self, kodi):
        self.kodi = kodi

    def dispatch(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            for k in self.KEYMAP:
                if self.KEYMAP[k] == event.button:
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
        volume = self.kodi.volume - self.kodi.VOLUME_DELTA
        self.kodi.show('LEFT -> VolumeDown -> ' + str(volume))
        if volume > 0:
            return self.kodi.Application.SetVolume({"volume": volume})

    def right(self, event):
        volume = self.kodi.volume + self.kodi.VOLUME_DELTA
        self.kodi.show('RIGHT -> VolumeUp -> ' + str(volume))
        if volume < 100:
            return self.kodi.Application.SetVolume({"volume": volume})

    def default(self, event):
        self.kodi.show('{0} -> Select'.format(
            self.REVERSE_KEYMAP[event.button].upper()))
        return self.kodi.Input.Select()

    x = blue
    a = red
    b = yellow
    y = green = default


def summary(joy):
    print
    print "Name of the joystick:", joy.get_name()
    print "Number of hats:", joy.get_numhats()
    print "Number of track balls:", joy.get_numballs()
    print "Number of axis:", joy.get_numaxes()
    print "Number of buttons:", joy.get_numbuttons()
    print


class Kodi(BaseKodi):

    VOLUME_DELTA = 5

    @property
    def volume(self):
        obj = self.Application.GetProperties({"properties": ["volume"]})
        result = int(obj['result']['volume'])
        print 'kodi.volume', result
        return result

    def show(self, msg):
        print msg
        self.GUI.ShowNotification(
            {"title": "joystick", "message": str(msg)})


def main(buffalo, kodi):
    while True:
        time.sleep(JOYSTICK_POLL_DELTA)
        for event in pygame.event.get():
            buffalo.loop(event)


if __name__ == '__main__':
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.display.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()
    summary(joy)
    kodi = Kodi("http://{0}/jsonrpc".format(KODI_HOST), USER, PASSWORD)
    buffalo = Buffalo(kodi)
    main(buffalo, kodi)
