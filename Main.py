#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QMainWindow, QLabel, QApplication)
from PyQt5.QtCore import *
from PyQt5 import uic
import sys
from BAR import BarcodeGenerator
import random


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

        self.pushCreate_barcodes_menu.clicked.connect(lambda: show_window(self, creatingWin))

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

        self.pushCreate_barcodes.clicked.connect(self.generateBarCodes)

        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            show_window(self, mainWin)

    # this function activates after clicking "Создать штрих коды" and generates bar codes
    def generateBarCodes(self):
        number_of_books = int(self.number_of_books.text())

        bar = BarcodeGenerator('ean13')
        for i in range(number_of_books):
            # !!! need to compare with the database
            id_of_book = str(random.randint(1000000000000, 9999999999999))
            bar.generate_barcode(id_of_book, id_of_book)

        show_window(self, confirmationWin)


class Confirmation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 130)
        self.setWindowTitle('AutoLibrary')
        self.init_UI()

    def init_UI(self):
        # LOAD IMAGE
        set_background(self)

        # Загрузка GUI
        uic.loadUi('GUI/confirmation_win.ui', self)

        self.pushYes.clicked.connect(lambda: show_window(self, mainWin))
        # self.pushNo.clicked.connect(lambda: show_window(self, mainWin))

        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Y:
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
    confirmationWin = Confirmation()
    confirmationWin.hide()
    sys.exit(app.exec_())
