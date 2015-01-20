# -*- coding: utf-8 -*-

from datetime import time, datetime
from PyQt4 import QtCore, QtGui, phonon


def msec_to_str(msec):
    hour = (msec / (60 * 60 * 1000))
    minute = (msec / (60 * 1000)) % 60
    second = (msec / 1000) % 60
    return time(hour, minute, second).strftime("%H:%M:%S.") + str(msec % 1000)


def str_to_msec(s):
    ts, msec = s.split(".")
    msec = int(msec)
    t = datetime.strptime(str(ts), "%H:%M:%S")
    return t.hour * 60 * 60 * 1000 + \
           t.minute * 60 * 1000 + \
           t.second * 1000 + msec


class Scene(QtGui.QGraphicsScene):
    def __init__(self):
        super(Scene, self).__init__()
        self.cur_item = None
        self.video_widget = None

    def item_at(self, pos):
        return self.items(QtCore.Qt.AscendingOrder)[pos + 1]

    def set_video_widget(self, widget):
        proxy = self.addWidget(widget)
        self.video_widget = proxy
        return proxy

    def mousePressEvent(self, evt):
        items = self.items(evt.scenePos(), QtCore.Qt.IntersectsItemShape,
                           QtCore.Qt.DescendingOrder)
        for item in items:
            if item.isVisible() and item != self.video_widget:
                self.cur_item = item
                return

    def mouseMoveEvent(self, evt):
        if not self.video_widget or not self.cur_item:
            return

        pos = evt.scenePos()
        if self.cur_item.isVisible() and self.video_widget.rect().contains(pos):
            self.cur_item.setPos(pos)

    def mouseReleaseEvent(self, evt):
        self.cur_item = None


class VideoCanvas(QtGui.QGraphicsView):
    def __init__(self):
        super(VideoCanvas, self).__init__()
        self.setFrameShape(QtGui.QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scene = Scene()
        self.setScene(self.scene)
        self.video_widget = phonon.Phonon.VideoWidget()
        self.media = phonon.Phonon.MediaObject()
        self.media.setTickInterval(50)
        phonon.Phonon.createPath(self.media, self.video_widget)
        self.video_proxy = self.scene.set_video_widget(self.video_widget)
        self.setSceneRect(self.video_proxy.rect())

    def set_source(self, filename):
        self.media.setCurrentSource(phonon.Phonon.MediaSource(filename))

    def resizeEvent(self, evt):
        super(VideoCanvas, self).resizeEvent(evt)
        self.fitInView(self.video_proxy, QtCore.Qt.KeepAspectRatio)

    def cleanup(self):
        self.scene.clear()
