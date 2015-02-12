# -*- coding: utf-8 -*-


from PyQt4 import QtCore, QtGui, phonon


class Scene(QtGui.QGraphicsScene):
    """
    Class graphic scene which is able to connect to the video widget,
     show titles on it, and move them.
    """
    def __init__(self):
        """
        Correctly initializes scene
        """
        super(Scene, self).__init__()
        self.cur_item = None
        self.dpos = None
        self.video_widget = None

    def item_at(self, pos):
        """
        Returns the element on the job position in the list of elements
         At position 0 is the video
        :param pos: position
        :return: element
        """
        return self.items(QtCore.Qt.AscendingOrder)[pos + 1]

    def set_video_widget(self, widget):
        proxy = self.addWidget(widget)
        self.video_widget = proxy
        return proxy

    def mousePressEvent(self, evt):
        """
        Handler mouse click on the canvas to support the move tool with the mouse
        :param evt: Object of QGraphicsSceneEvent
        :return: None
        """
        items = self.items(evt.scenePos(), QtCore.Qt.IntersectsItemShape,
                           QtCore.Qt.DescendingOrder)
        for item in items:
            if item.isVisible() and item != self.video_widget:
                self.cur_item = item
                self.dpos = evt.scenePos() - item.scenePos()
                return

    def mouseMoveEvent(self, evt):
        """
        Handler move mouse button on the canvas to support the move tool with the mouse.
        :param evt: Object of QGraphicsSceneEvent
        :return: None
        """
        if not self.video_widget or not self.cur_item:
            return

        pos = evt.scenePos() - self.dpos
        item_rect = self.cur_item.sceneBoundingRect()
        item_rect.moveTo(pos)
        if self.cur_item.isVisible() and self.video_widget.rect().contains(item_rect):
            self.cur_item.setPos(pos)

    def mouseReleaseEvent(self, evt):
        """
        Handler release the mouse button to support the move tool with the mouse
        :param evt: Object of QGraphicsSceneEvent
        :return: None
        """
        self.cur_item = None


class VideoCanvas(QtGui.QGraphicsView):
    """
    Class canvas that displays the video and the titles on it
    """
    def __init__(self):
        """
        Correctly initializes the canvas.
         Disables this scroll.
         Creates a scene and connects to it as a widget.
        :return: None
        """
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
        """
        Specifies the video source
        :param filename: name of file with video
        :return:None
        """
        self.media.setCurrentSource(phonon.Phonon.MediaSource(filename))

    def resizeEvent(self, evt):
        """
        Handler resize the canvas.
         Correctly handles video scaling.
        :param evt: Object of QResizeEvent
        :return: None
        """
        super(VideoCanvas, self).resizeEvent(evt)
        self.fitInView(self.video_proxy, QtCore.Qt.KeepAspectRatio)

    def cleanup(self):
        """
        Function for the correct release resources
        :return: None
        """
        self.scene.clear()

class SeekSlider(phonon.Phonon.SeekSlider):
    def paintEvent(self, evt):
        super(SeekSlider, self).paintEvent(evt)
        self.mediaObject().tick.emit(self.mediaObject().currentTime())
