from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic

import sys
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.setWindowTitle("AutoLibrary")

        self.ean = None
        self.ids = None

        self.chooseFileBut.clicked.connect(self.get_chosen_file)
        self.printBut.clicked.connect(self.print_labels)

    def get_chosen_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "AutoLibrary open file", "",
                                                   "All Files (*);;Python Files (*.py)",
                                                   options=QFileDialog.Options())

        try:
            if os.path.splitext(file_path)[1] == '.txt':
                filename = os.path.basename(file_path)
                self.ean, self.ids = self.parse_file(filename)

                self.fileNameLabel.setText(filename)
                self.infoLabel.setText('Файл успешно выбран')

            else:
                raise TypeError

        except TypeError:
            self.infoLabel.setText("Выберите файл конфигурации с расширением txt")

        except IndexError:
            self.infoLabel.setText("Выбран неверный файл конфигурации")

    def print_labels(self):
        pass

    @staticmethod
    def parse_file(filename):
        with open(filename) as file:
            lines = file.readlines()
            return lines[0], lines[1:]


app = QApplication(sys.argv)
app.setApplicationName("AutoLibrary")

window = MainWindow()
window.show()
sys.exit(app.exec())
