#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
from multiprocessing import Process, Queue, Event, Pool
from Queue import Full, Empty
from PyQt4 import Qt, QtCore, QtGui, phonon

import moviepy.editor as editor

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


def get_log_filenames(result_filename):
    return [result_filename + '.wav.log', result_filename + '.log']


def on_process_clicked(app, ui, orig_filename, result_filename, pool):
    def handler():
        ui.button_process.setEnabled(False)
        ui.textbrowser_log.setPlainText("")

        titles = []
        for row in xrange(ui.table_captions.rowCount()):
            titles.append([str(ui.table_captions.item(row, col).text())
                           for col in xrange(ui.table_captions.columnCount())])

        def on_finish(result):
            ui.button_process.setEnabled(True)
            if result:
                ui.video_player.load(phonon.Phonon.MediaSource(result_filename))
            try:
                [os.remove(l) for l in get_log_filenames(result_filename)]
            except OSError:
                pass

        pool.apply_async(process_videoclip, (orig_filename, result_filename, titles), callback=on_finish)

    return handler


def process_videoclip(orig_filename, result_filename, titles):
    try:
        src = editor.VideoFileClip(orig_filename)
        clips = [src]
        for elem in titles:
            title, start_time, duration = elem
            clip = editor.TextClip(title, fontsize=70, color="white")
            clip = clip.set_pos("center").set_start(start_time).set_duration(duration)
            clips.append(clip)
        result = editor.CompositeVideoClip(clips)
        result.write_videofile(result_filename, write_logfile=True, temp_audiofile=result_filename + '.wav')
        return True
    except:
        return False


def on_log_dir_changed(watcher, result_filename):
    def handler(path):
        for log in get_log_filenames(result_filename):
            if os.path.exists(log):
                watcher.addPath(log)
            else:
                watcher.removePath(log)

    return handler


def on_log_file_changed(ui, watcher):
    def handler(path):
        try:
            with open(path) as logfile:
                ui.textbrowser_log.setPlainText(logfile.read())
                sb = ui.textbrowser_log.verticalScrollBar()
                sb.setValue(sb.maximum())
        except IOError:
            pass

    return handler


def on_app_quit(pool):
    def handler():
        pool.terminate()
        pool.join()
    return handler


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: ./main.py <video file>")
    if not os.path.isfile(sys.argv[1]):
        sys.exit("Video file is not found")

    orig_filename = os.path.abspath(sys.argv[1])
    splitted = os.path.splitext(orig_filename)
    result_filename = splitted[0] + "_edited" + splitted[1]

    app = QtGui.QApplication([])
    app.setApplicationName("Title machine")
    window = QtGui.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(window)

    pool = Pool(1)
    log_watcher = QtCore.QFileSystemWatcher([os.path.dirname(result_filename)])

    ui.button_process.clicked.connect(
        on_process_clicked(app, ui, orig_filename, result_filename, pool))
    ui.button_add_caption.clicked.connect(on_add_caption_clicked(ui))
    ui.button_remove_caption.clicked.connect(on_remove_caption_clicked(ui))
    log_watcher.directoryChanged.connect(on_log_dir_changed(log_watcher, result_filename))
    log_watcher.fileChanged.connect(on_log_file_changed(ui, log_watcher))
    app.lastWindowClosed.connect(on_app_quit(pool))

    ui.video_player.load(phonon.Phonon.MediaSource(orig_filename))
    ui.textbrowser_log.setPlainText("Welcome to Title Machine!")

    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

