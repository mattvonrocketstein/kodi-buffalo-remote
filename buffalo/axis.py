""" buffalo.axis
"""


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
