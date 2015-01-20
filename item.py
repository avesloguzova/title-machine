from video import msec_to_str, str_to_msec

__author__ = 'av'


class Item(object):
    def __init__(self, text, start_time, duration, x, y):
        self.text = text
        self._start_time = start_time
        self._duration = duration
        self.x = x
        self.y = y

    @property
    def start_time(self):
        return msec_to_str(self._start_time)

    @property
    def duration(self):
        return msec_to_str(self._duration)

    @start_time.setter
    def start_time(self, value):
        self._start_time = str_to_msec(value)

    @duration.setter
    def duration(self, value):
        self._duration = str_to_msec(value)

    @property
    def _end_time(self):
        return self._start_time + self._duration

    @staticmethod
    def properties():
        return ['text', 'start_time', 'duration', 'x', 'y']