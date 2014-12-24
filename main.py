#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
from multiprocessing import Process, Queue, Event
from Queue import Full
from PyQt4 import Qt, QtGui, phonon

from moviepy.editor import *

from mainwindow import Ui_MainWindow


def on_add_caption_clicked(ui):
    def handler():
        props = ["Enter text here...", "00:00:00.00", "00:00:10.00"]
        row = ui.table_captions.rowCount()
        ui.table_captions.setRowCount(row + 1)
        for i, prop in enumerate(props):
            item = QtGui.QTableWidgetItem(prop)
            item.setFlags(Qt.Qt.ItemIsEditable | Qt.Qt.ItemIsEnabled | Qt.Qt.ItemIsSelectable)
            ui.table_captions.setItem(row, i, item)

    return handler


def on_remove_caption_clicked(ui):
    def handler():
        ui.table_captions.removeRow(ui.table_captions.currentRow())

    return handler


def on_process_clicked(app, ui, orig_filename, result_filename, process, queue, done_event):
    def process_log(log):
        try:
            log_filename, logfile = log
            if not logfile:
                logfile = open(log_filename)
            log = logfile.read()
            if log:
                prev_log = ui.textbrowser_log.toPlainText()
                ui.textbrowser_log.setPlainText(prev_log + log)
                sb = ui.textbrowser_log.verticalScrollBar()
                sb.setValue(sb.maximum())
            return (log_filename, logfile)
        except IOError:
            return log

    def handler():
        titles = []
        for row in xrange(ui.table_captions.rowCount()):
            titles.append([str(ui.table_captions.item(row, col).text())
                           for col in xrange(ui.table_captions.columnCount())])

        try:
            ui.button_process.setEnabled(False)
            ui.textbrowser_log.setPlainText("")

            queue.put_nowait((orig_filename, result_filename, titles))
            done_event.clear()

            logs = [result_filename + '.wav.log', result_filename + '.log']
            logs = [(log, open(log) if os.path.exists(log) else None) for log in logs]
            while not done_event.is_set() and process.is_alive():
                done_event.wait(0.05)
                app.processEvents()
                logs = [process_log(log) for log in logs]

            ui.video_player.load(phonon.Phonon.MediaSource(result_filename))
        except Full:
            pass
        finally:
            try:
                map(lambda log: os.remove(log[0]), logs)
            except OSError:
                pass
            ui.button_process.setEnabled(True)

    return handler


def process_videoclip(queue, done_event):
    while True:
        (orig_filename, result_filename, titles) = queue.get()
        src = VideoFileClip(orig_filename)
        clips = [src]
        for t in titles:
            title, start_time, duration = t
            clip = TextClip(title, fontsize=70, color="white")
            clip = clip.set_pos("center").set_start(start_time).set_duration(duration)
            clips.append(clip)
        result = CompositeVideoClip(clips)
        result.write_videofile(result_filename, write_logfile=True, temp_audiofile=result_filename + '.wav')
        done_event.set()


def on_app_quit(process, queue):
    def handler():
        queue.close()
        process.terminate()

    return handler


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Usage: ./main.py <video file>")
    if not os.path.isfile(sys.argv[1]):
        sys.exit("Video file is not found")

    orig_filename = sys.argv[1]
    splitted = os.path.splitext(orig_filename)
    result_filename = splitted[0] + "_edited" + splitted[1]

    app = QtGui.QApplication([])
    app.setApplicationName("Title machine")

    window = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    q = Queue(1)
    e = Event()
    p = Process(target=process_videoclip, args=(q, e))
    p.start()

    ui.button_process.clicked.connect(on_process_clicked(app, ui, orig_filename, result_filename, p, q, e))
    ui.button_add_caption.clicked.connect(on_add_caption_clicked(ui))
    ui.button_remove_caption.clicked.connect(on_remove_caption_clicked(ui))
    app.lastWindowClosed.connect(on_app_quit(p, q))

    ui.video_player.load(phonon.Phonon.MediaSource(orig_filename))
    ui.textbrowser_log.setPlainText("Welcome to Title Machine!")

    window.show()
    app.exec_()

