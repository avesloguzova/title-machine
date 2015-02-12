# -*- coding: utf-8 -*-
__author__ = 'avesloguzova'

from datetime import time, datetime



class Item(object):
    """
    Class represent title added to video

    """
    def __init__(self, text, start_time, duration, x, y):
        self.text = text
        self._start_time = start_time
        self._duration = duration
        self.x = x
        self.y = y

    def is_visible(self, pos):
        """
        Check is title visible in position
        :param pos: position
        :return: True or False
        """
        return self._start_time <= pos and self._start_time + self._duration >= pos

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

    @staticmethod
    def properties():
        return ['text', 'start_time', 'duration', 'x', 'y']


def msec_to_str(msec):
    """
    convert time from number representation to string
    :param msec: time in millisecond
    :return:
    """
    hour = int(msec / (60 * 60 * 1000))
    minute = int(msec / (60 * 1000)) % 60
    second = int(msec / 1000) % 60
    return time(hour, minute, second).strftime("%H:%M:%S.") + str(msec % 1000)


def str_to_msec(s):
    """
    Convert string representation of time to number
    :param s: string
    :return: time in millisecond
    """
    ts, msec = s.split(".")
    msec = int(msec)
    t = datetime.strptime(str(ts), "%H:%M:%S")
    return t.hour * 60 * 60 * 1000 + \
           t.minute * 60 * 1000 + \
           t.second * 1000 + msec

