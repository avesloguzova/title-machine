from video import msec_to_str, str_to_msec

__author__ = 'av'


class Item(object):
    def __init__(self, text, start_time, duration, x, y):
        self.text = text
        self.start_time_as_number = start_time
        self.durationtion_as_number = duration
        self.x = x
        self.y = y

    @property
    def start_time(self):
        return msec_to_str(self.start_time_as_number)

    @property
    def duration(self):
        return msec_to_str(self._duration)

    @start_time.setter
    def start_time(self, value):
        self.start_time_as_number = str_to_msec(value)

    @duration.setter
    def duration(self, value):
        self._duration = str_to_msec(value)

    @property
    def end_time(self):
        return self.start_time_as_number + self._duration

    @staticmethod
    def properties():
        return ['text', 'start_time', 'duration', 'x', 'y']