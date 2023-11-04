import time

import init
from gui import login,main
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

app = QtWidgets.QApplication(sys.argv)
#
Form2 = QtWidgets.QWidget()
main = main.Form()
main.setupUi(Form2)

Form1 = QtWidgets.QWidget()
login = login.Form()
login.setupUi(Form1,Form2,main)
Form1.show()

# Form2 = QtWidgets.QWidget()
# ui = main.Form()
# ui.setupUi(Form2)
# Form2.show()

app.exec_()  # exec_()가 종료되면 다음 코드가 실행됩니다.

