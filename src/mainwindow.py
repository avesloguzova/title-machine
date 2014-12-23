# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sat Dec 20 20:07:49 2014
# by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(746, 362)
        self.main_widget = QtGui.QWidget(MainWindow)
        self.main_widget.setObjectName(_fromUtf8("main_widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.main_widget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitter_2 = QtGui.QSplitter(self.main_widget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.video_player = phonon.Phonon.VideoPlayer(self.widget)
        self.video_player.setObjectName(_fromUtf8("video_player"))
        self.verticalLayout.addWidget(self.video_player)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.button_play = QtGui.QPushButton(self.widget)
        self.button_play.setObjectName(_fromUtf8("button_play"))
        self.horizontalLayout_2.addWidget(self.button_play)
        self.button_pause = QtGui.QPushButton(self.widget)
        self.button_pause.setObjectName(_fromUtf8("button_pause"))
        self.horizontalLayout_2.addWidget(self.button_pause)
        self.button_stop = QtGui.QPushButton(self.widget)
        self.button_stop.setObjectName(_fromUtf8("button_stop"))
        self.horizontalLayout_2.addWidget(self.button_stop)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.textbrowser_log = QtGui.QTextBrowser(self.splitter)
        self.textbrowser_log.setMaximumSize(QtCore.QSize(16777215, 200))
        self.textbrowser_log.setObjectName(_fromUtf8("textbrowser_log"))
        self.widget1 = QtGui.QWidget(self.splitter_2)
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.v_layout_2 = QtGui.QVBoxLayout(self.widget1)
        self.v_layout_2.setMargin(0)
        self.v_layout_2.setObjectName(_fromUtf8("v_layout_2"))
        self.h_layout_1 = QtGui.QHBoxLayout()
        self.h_layout_1.setObjectName(_fromUtf8("h_layout_1"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.h_layout_1.addItem(spacerItem2)
        self.button_add_caption = QtGui.QPushButton(self.widget1)
        self.button_add_caption.setObjectName(_fromUtf8("button_add_caption"))
        self.h_layout_1.addWidget(self.button_add_caption)
        self.button_remove_caption = QtGui.QPushButton(self.widget1)
        self.button_remove_caption.setObjectName(_fromUtf8("button_remove_caption"))
        self.h_layout_1.addWidget(self.button_remove_caption)
        self.v_layout_2.addLayout(self.h_layout_1)
        self.table_captions = QtGui.QTableWidget(self.widget1)
        self.table_captions.setObjectName(_fromUtf8("table_captions"))
        self.table_captions.setColumnCount(3)
        self.table_captions.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.table_captions.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table_captions.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.table_captions.setHorizontalHeaderItem(2, item)
        self.v_layout_2.addWidget(self.table_captions)
        self.button_process = QtGui.QPushButton(self.widget1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.button_process.setFont(font)
        self.button_process.setObjectName(_fromUtf8("button_process"))
        self.v_layout_2.addWidget(self.button_process)
        self.horizontalLayout.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.main_widget)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.button_play, QtCore.SIGNAL(_fromUtf8("clicked()")), self.video_player.play)
        QtCore.QObject.connect(self.button_pause, QtCore.SIGNAL(_fromUtf8("clicked()")), self.video_player.pause)
        QtCore.QObject.connect(self.button_stop, QtCore.SIGNAL(_fromUtf8("clicked()")), self.video_player.stop)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Title Machine", None))
        self.button_play.setText(_translate("MainWindow", "Play", None))
        self.button_pause.setText(_translate("MainWindow", "Pause", None))
        self.button_stop.setText(_translate("MainWindow", "Stop", None))
        self.button_add_caption.setText(_translate("MainWindow", "Add", None))
        self.button_remove_caption.setText(_translate("MainWindow", "Remove", None))
        item = self.table_captions.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Text", None))
        item = self.table_captions.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Start time", None))
        item = self.table_captions.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Duration", None))
        self.button_process.setText(_translate("MainWindow", "PROCESS", None))


from PyQt4 import phonon
