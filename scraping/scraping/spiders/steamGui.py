import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,QLineEdit,QStatusBar, QComboBox,QPushButton,QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class steamgui(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_hight = 1600,400
        self.setMinimumSize(self.window_width, self.window_hight)
        self.setWindowTitle('Steam GUI')
        self.setObjectName('mainwidget')
        self.setStyleSheet('''
            QWidget {
                font-size: 35px;
            }
            QComboBox {
                height: 50px;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                height: 50px
            }
            QStatusBar {
                color: white;
            }
            #mainwidget {
                background-color: #1E2C3A;
            }
        ''')
        self.layout = QGridLayout()
        self.setLayout(self.layout)

    def initUI(self):
        self.label = {}
        self.combobox = {}
        self.button = {}
        self.lineedit = {}

if __name__ == '__main__':
    app = QApplication(sys.arv)

    myApp = steamgui()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing app...')