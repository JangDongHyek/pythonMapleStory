import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedWidget, QVBoxLayout, QWidget
from gui import login,main

class Widget1(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.button = QPushButton("다음 위젯으로 전환")
        layout.addWidget(self.button)
        self.setLayout(layout)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 201)
        self.edit_id = QWidget.QLineEdit(Form)
        self.edit_id.setGeometry(QtCore.QRect(110, 60, 151, 31))
        self.edit_id.setObjectName("edit_id")
        self.edit_pw = QWidget.QLineEdit(Form)
        self.edit_pw.setGeometry(QtCore.QRect(110, 100, 151, 31))
        self.edit_pw.setObjectName("edit_pw")
        self.label_id = QtWidgets.QLabel(Form)
        self.label_id.setGeometry(QtCore.QRect(30, 60, 71, 31))
        self.label_id.setObjectName("label_id")
        self.label_pw = QtWidgets.QLabel(Form)
        self.label_pw.setGeometry(QtCore.QRect(30, 100, 71, 31))
        self.label_pw.setObjectName("label_pw")
        self.btn_login = QtWidgets.QPushButton(Form)
        self.btn_login.setGeometry(QtCore.QRect(280, 60, 75, 71))
        self.btn_login.setObjectName("btn_login")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_id.setText(_translate("Form", "ID"))
        self.label_pw.setText(_translate("Form", "PW"))
        self.btn_login.setText(_translate("Form", "Login"))

class Widget2(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.button = QPushButton("이전 위젯으로 전환")
        layout.addWidget(self.button)
        self.setLayout(layout)

class SwitchForm(QMainWindow) :
    def __init__(self):
        super().__init__()

        self.setWindowTitle("위젯 전환 예제")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.stacked_widget = QStackedWidget()

        widget1 = Widget1()
        widget2 = Widget2()

        self.stacked_widget.addWidget(widget1)
        self.stacked_widget.addWidget(widget2)

        layout.addWidget(self.stacked_widget)
        central_widget.setLayout(layout)

        widget1.button.clicked.connect(self.switch_to_widget2)
        widget2.button.clicked.connect(self.switch_to_widget1)

    def switch_to_widget1(self):
        self.stacked_widget.setCurrentIndex(0)

    def switch_to_widget2(self):
        self.stacked_widget.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget_switcher = SwitchForm()
    widget_switcher.show()
    sys.exit(app.exec_())