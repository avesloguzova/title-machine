#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
from multiprocessing import Pool
from PyQt4 import Qt, QtCore, QtGui, phonon

import moviepy.editor as editor

from item import Item
from video import VideoCanvas
from mainwindow import Ui_MainWindow
from moviepy.video.io.ffmpeg_reader import ffmpeg_parse_infos


items = []


def on_add_caption_clicked(ui):
    """

    :param ui:
    :return:
    """
    def handler():
        cur_time = ui.video_canvas.media.currentTime()
        row = len(items)
        ui.table_captions.setRowCount(row + 1)
        new_item = Item("Enter text here...", cur_time, 1000, 0, 0)
        items.append(new_item)

        f = QtGui.QFont()
        f.setPointSize(20)
        scene_item = ui.video_canvas.scene.addText(new_item.text, f)
        scene_item.setPos(new_item.x, new_item.y)
        scene_item.setDefaultTextColor(QtGui.QColor(255, 255, 255))

        def handle_size_change():
            new_item.x = scene_item.x()
            new_item.y = scene_item.y()
            on_tablewidget_cell_changed(ui)(row, 3)
            on_tablewidget_cell_changed(ui)(row, 4)

        scene_item.xChanged.connect(handle_size_change)
        scene_item.yChanged.connect(handle_size_change)

        for i, prop in enumerate(Item.properties()):
            tw_item = QtGui.QTableWidgetItem(getattr(new_item, prop))
            tw_item.setFlags(Qt.Qt.ItemIsEditable | Qt.Qt.ItemIsEnabled | Qt.Qt.ItemIsSelectable)
            ui.table_captions.setItem(row, i, tw_item)

    return handler


def on_remove_caption_clicked(ui):
    """

    :param ui:
    :return:
    """
    def handler():
        row = ui.table_captions.currentRow()
        ui.table_captions.removeRow(row)
        item = ui.video_canvas.scene.item_at(row)
        ui.video_canvas.scene.removeItem(item)
        del items[row]

    return handler


def on_tablewidget_cell_changed(ui):
    """

    :param ui:
    :return:
    """
    def handler(row, col):
        prop = Item.properties()[col]
        item = items[row]
        tw_item = ui.table_captions.item(row, col)
        scene_item = ui.video_canvas.scene.item_at(row)
        if prop == "x" or prop == "y":
            tw_item.setText(str(getattr(item, prop)))
        elif prop == "text":
            setattr(item, prop, tw_item.text())
            scene_item.setPlainText(item.text)
        else:
            try:
                setattr(item, prop, tw_item.text())
                on_video_tick(ui)(ui.video_canvas.media.currentTime())
            except Exception:
                tw_item.setText(str(getattr(item, prop)))

    return handler


def get_log_filenames(result_filename):
    """

    :param result_filename:
    :return:
    """
    return [result_filename + '.wav.log', result_filename + '.log']


def on_process_clicked(ui, orig_filename, result_filename, pool):
    """

    :param ui:
    :param orig_filename:
    :param result_filename:
    :param pool:
    :return:
    """
    def handler():
        if not items:
            return

        ui.button_process.setEnabled(False)
        ui.textbrowser_log.setPlainText("")

        titles = []
        for item in items:
            titles.append((str(item.text), item.start_time,
                           item.duration, item.x, item.y))

        def on_finish(result):
            ui.button_process.setEnabled(True)
            try:
                [os.remove(l) for l in get_log_filenames(result_filename)]
            except OSError:
                pass

        pool.apply_async(process_videoclip, (orig_filename, result_filename, titles), callback=on_finish)

    return handler


def process_videoclip(orig_filename, result_filename, titles):
    """

    :param orig_filename:
    :param result_filename:
    :param titles:
    :return:
    """
    try:
        src = editor.VideoFileClip(orig_filename)
        clips = [src]
        for elem in titles:
            title, start_time, duration, x, y = elem
            clip = editor.TextClip(title, fontsize=50, color="white")
            clip = clip.set_position((x, y)).set_start(start_time).set_duration(duration)
            clips.append(clip)
        result = editor.CompositeVideoClip(clips)
        result.write_videofile(result_filename, write_logfile=True, temp_audiofile=result_filename + '.wav')
        return True
    except Exception:
        return False


def on_log_dir_changed(watcher, result_filename):
    """

    :param watcher:
    :param result_filename:
    :return:
    """
    def handler(path):
        for log in get_log_filenames(result_filename):
            if os.path.exists(log):
                watcher.addPath(log)
            else:
                watcher.removePath(log)

    return handler


def on_log_file_changed(ui, watcher):
    """

    :param ui:
    :param watcher:
    :return:
    """
    def handler(path):
        try:
            with open(path) as logfile:
                ui.textbrowser_log.setPlainText(logfile.read())
                sb = ui.textbrowser_log.verticalScrollBar()
                sb.setValue(sb.maximum())
        except IOError:
            pass

    return handler


def on_app_quit(ui, pool):
    """

    :param ui:
    :param pool:
    :return:
    """
    def handler():
        pool.terminate()
        pool.join()
        ui.video_canvas.cleanup()

    return handler


def on_video_state_changed(ui):
    """

    :param ui:
    :return:
    """
    def handler(new, old):
        is_enabled = new == phonon.Phonon.PausedState
        ui.button_add_caption.setEnabled(is_enabled)
        ui.button_remove_caption.setEnabled(is_enabled)
        ui.table_captions.setEnabled(is_enabled)
        # NOTE: disable because it doesn't notify about position changes
        ui.video_seek.setEnabled(not is_enabled)

    return handler


def on_video_tick(ui):
    """

    :param ui:
    :return:
    """
    def handler(pos):
        for i, item in enumerate(items):
            scene_item = ui.video_canvas.scene.item_at(i)
            scene_item.setVisible(item.is_visible(pos))

    return handler


def main():
    """

    :return:
    """
    if len(sys.argv) != 2:
        sys.exit("Usage: ./main.py <video file>")
    if not os.path.isfile(sys.argv[1]):
        sys.exit("Video file is not found")

    orig_filename = os.path.abspath(sys.argv[1])
    splitted = os.path.splitext(orig_filename)
    result_filename = splitted[0] + "_edited" + splitted[1]

    try:
        ffmpeg_parse_infos(orig_filename)
    except IOError:
        sys.exit("Can't detect valid video in specified file")

    app = QtGui.QApplication([])
    app.setApplicationName("Title machine")
    window = QtGui.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(window)

    ui.video_canvas = VideoCanvas()
    ui.video_canvas.set_source(orig_filename)
    ui.video_seek.setMediaObject(ui.video_canvas.media)
    ui.v_layout_1.insertWidget(0, ui.video_canvas)

    pool = Pool(1)
    log_watcher = QtCore.QFileSystemWatcher([os.path.dirname(result_filename)])

    ui.button_process.clicked.connect(
        on_process_clicked(ui, orig_filename, result_filename, pool))
    ui.button_add_caption.clicked.connect(on_add_caption_clicked(ui))
    ui.button_remove_caption.clicked.connect(on_remove_caption_clicked(ui))
    ui.table_captions.cellChanged.connect(on_tablewidget_cell_changed(ui))

    ui.button_play.clicked.connect(ui.video_canvas.media.play)
    ui.button_pause.clicked.connect(ui.video_canvas.media.pause)
    ui.video_canvas.media.stateChanged.connect(on_video_state_changed(ui))
    ui.video_canvas.media.tick.connect(on_video_tick(ui))

    log_watcher.directoryChanged.connect(on_log_dir_changed(log_watcher, result_filename))
    log_watcher.fileChanged.connect(on_log_file_changed(ui, log_watcher))
    app.lastWindowClosed.connect(on_app_quit(ui, pool))

    ui.textbrowser_log.setPlainText("Welcome to Title Machine!")

    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

