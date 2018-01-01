"""
"""
import os
from kodijson import Kodi as BaseKodi

KODI_HOST = os.environ.get('KODI_HOST', 'localhost:8080')
KODI_USER = os.environ.get('KODI_USER', 'guest')
KODI_PASSWORD = os.environ.get('KODI_PASSWORD', 'guest')


class Kodi(BaseKodi):

    VOLUME_DELTA = 5

    @staticmethod
    def get_handle():
        return Kodi(
            "http://{0}/jsonrpc".format(KODI_HOST),
            KODI_USER, KODI_PASSWORD)

    def volume_decrement(self):
        volume = self.volume - self.VOLUME_DELTA
        self.show('LEFT -> VolumeDown -> ' + str(volume))
        if volume > 0:
            return self.Application.SetVolume({"volume": volume})

    def volume_increment(self):
        volume = self.volume + self.VOLUME_DELTA
        self.show('RIGHT -> VolumeUp -> ' + str(volume))
        if volume < 100:
            return self.Application.SetVolume({"volume": volume})

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
