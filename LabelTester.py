from PyQt5 import QtCore, QtWidgets, QtGui, uic

import pandas as pd

import sys
import os


class LabelTester(QtWidgets.QMainWindow, uic.loadUiType("LabelTester.ui")[0]):

    def __init__(self, app: QtWidgets.QApplication = None):
        def excepthook(*args):
            sys.__excepthook__(*args)

        sys.excepthook = excepthook
        if app is None:
            app = QtWidgets.QApplication(sys.argv)
            app.setApplicationName("Label Tester")
        self.app_ = app
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Label Tester')

        self.db = None
        self.db_path = None
        self.db_changed = False
        self.clear_on_find = False
        self.mark_scan = False
        self.mark_label = False

        self.save_button.triggered.connect(self.save_db)
        self.choose_button.clicked.connect(self.file_dialog)
        self.load_button.clicked.connect(self.load_db)

        self.line_end_checkbox.stateChanged.connect(self.track_line_end)
        self.line_end_checkbox.stateChanged.emit(self.line_end_checkbox.checkState())
        self.find_clear_checkbox.stateChanged.connect(lambda state: setattr(self, 'clear_on_find', state))
        self.find_clear_checkbox.stateChanged.emit(self.find_clear_checkbox.checkState())

        self.find_button.clicked.connect(self.find_book)
        self.id_input.setValidator(QtGui.QIntValidator())

        self.mark_scan_checkbox.stateChanged.connect(lambda state: setattr(self, 'mark_scan', state))
        self.mark_scan_checkbox.stateChanged.emit(self.mark_scan_checkbox.checkState())
        self.mark_label_checkbox.stateChanged.connect(lambda state: setattr(self, 'mark_label', state))
        self.mark_label_checkbox.stateChanged.emit(self.mark_label_checkbox.checkState())

    def file_dialog(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(dlg.ExistingFile)
        dlg.setNameFilter('Excel table (*.xls *.xlsx)')
        if dlg.exec():
            self.file_path_input.setText(dlg.selectedFiles()[0])
            self.load_db()

    @staticmethod
    def missing_db_dialog():
        m_box = QtWidgets.QMessageBox()
        m_box.setIcon(m_box.Warning)
        m_box.setWindowTitle("Database error")
        m_box.setText("Database not loaded")
        m_box.exec()

    def db_save_dialog(self):
        m_box = QtWidgets.QMessageBox()
        m_box.setIcon(m_box.Question)
        m_box.setWindowTitle("Save database")
        m_box.setText("Do you want to save changes?")
        m_box.setStandardButtons(m_box.Yes | m_box.Cancel | m_box.No)
        ans = m_box.exec()
        if ans == m_box.Yes:
            self.save_db()
            return True
        elif ans == m_box.Cancel:
            return False
        else:
            return True

    def track_line_end(self, state):
        if state:
            self.id_input.returnPressed.connect(self.find_book)
        else:
            self.id_input.returnPressed.disconnect()

    def find_book(self):
        if self.db is None:
            self.missing_db_dialog()
        else:
            bid = int(self.id_input.text() if self.id_input.text() else 0)
            if self.clear_on_find:
                self.id_input.setText('')
            data = self.db[self.db.iloc[:, 0] == bid]
            if not data.empty:
                self.name_value.setText(data.iloc[0, 1])
                self.author_value.setText(data.iloc[0, 3])
                self.code_value.setText(str(data.iloc[0, 0]))
                if len(data) > 1:
                    self.error_label.setText('DUPLICATE DETECTED')
                else:
                    self.error_label.setText('')
                    if self.mark_scan and 'scanned' in self.db.columns:
                        self.db_changed = True
                        self.db.loc[self.db.iloc[:, 0] == bid, 'scanned'] += 1
                    if self.mark_label and 'labeled' in self.db.columns:
                        self.db_changed = True
                        self.db.loc[self.db.iloc[:, 0] == bid, 'labeled'] += 1
            else:
                self.error_label.setText('Not found')
                self.name_value.setText('#')
                self.author_value.setText('#')
                self.code_value.setText(str(bid))

    def load_db(self):
        self.status_label.setText('#')
        timer = QtCore.QTimer(self)
        timer.setSingleShot(True)
        status = 'OK'
        timer.timeout.connect(lambda: self.status_label.setText(status))
        try:
            path = self.file_path_input.text()
            if not os.path.isfile(path):
                raise FileNotFoundError(path)
            elif self.db is not None and self.db_changed:
                if not self.db_save_dialog():
                    timer.start(2000)
                    return
            try:
                self.db = pd.read_excel(path)
                self.db_path = path
                self.db_changed = False
                self.status_label.setText('Database loaded!')
            except Exception as error:
                m_box = QtWidgets.QMessageBox()
                m_box.setIcon(m_box.Critical)
                m_box.setWindowTitle("Loading error")
                m_box.setText("Could not load database")
                m_box.setDetailedText(str(error))
                m_box.setStandardButtons(m_box.Abort)
                m_box.exec()
        except (FileNotFoundError, PermissionError) as error:
            m_box = QtWidgets.QMessageBox()
            m_box.setIcon(m_box.Critical)
            m_box.setWindowTitle("Database error")
            m_box.setText('File not found' if isinstance(error, FileNotFoundError) else 'Error')
            m_box.setInformativeText(str(error))
            m_box.setStandardButtons(m_box.Abort)
            m_box.exec()
        timer.start(2000)

    def save_db(self):
        if self.db is None:
            self.missing_db_dialog()
        else:
            try:
                self.db.to_excel(self.db_path, index=False)
                self.db_changed = False
            except PermissionError as error:
                m_box = QtWidgets.QMessageBox()
                m_box.setIcon(m_box.Critical)
                m_box.setWindowTitle("Save error")
                m_box.setText("Can't write to database, file is busy")
                m_box.setInformativeText("Please close any programs that could use database file")
                m_box.setDetailedText(str(error))
                m_box.setStandardButtons(m_box.Retry | m_box.Abort)
                if m_box.exec() == m_box.Retry:
                    self.save_db()
                    self.db_changed = False

    def start(self):
        self.show()

    def exit(self):
        sys.exit(self.app_.exec())


if __name__ == '__main__':
    main = LabelTester()
    main.start()
    main.exit()
