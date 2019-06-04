#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QMainWindow, QLabel, QApplication)
from PyQt5.QtCore import *
from PyQt5 import uic
import sys


# Main menu
class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 350)
        self.setWindowTitle('AutoLibrary')
        self.init_UI()

    def init_UI(self):
        # LOAD IMAGE
        set_background(self)

        # Загрузка GUI
        uic.loadUi('GUI/Main_menu.ui', self)

        self.create_barcodes_menu.clicked.connect(lambda: show_window(self, creatingWin))

        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


# Creating bar codes menu
class Creating(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 350)
        self.setWindowTitle('AutoLibrary')
        self.init_UI()

    def init_UI(self):
        # LOAD IMAGE
        set_background(self)

        # Загрузка GUI
        uic.loadUi('GUI/Add_menu.ui', self)

        self.error.hide()

        # self.pushStart.clicked.connect(lambda: show_window(self, startWin))

        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            show_window(self, mainWin)


# LOAD IMAGE
def set_background(self):
    self.setWindowIcon(QIcon(QPixmap('GUI/images_for_GUI/icon.png')))

    self.bg = QLabel(self)
    self.bg.resize(350, 350)
    # self.bg.setPixmap(QPixmap("GUI/images_for_GUI/background.jpg").scaled(700, 370))


def show_window(old, new):
    if not (new is None):
        new.show()
    if not (old is None):
        old.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainMenu()
    creatingWin = Creating()
    creatingWin.hide()
    sys.exit(app.exec_())
