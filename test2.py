import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication,QMainWindow, QWidget

import PhiUI


class App(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui=PhiUI.Ui_MainWindow() 
        self.ui.setupUi(self)

if __name__ =="__main__":
    app = QApplication([])
    win = App()
    win.show()
    exit(app.exec())