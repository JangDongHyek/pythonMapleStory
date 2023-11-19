import time

import init
from gui import login,main
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import lib
import db
import globals

app = QtWidgets.QApplication(sys.argv)
#
Form2 = QtWidgets.QWidget()
main = main.Form()
main.setupUi(Form2)

Form1 = QtWidgets.QWidget()
login = login.Form()
login.setupUi(Form1,Form2,main)

ip = lib.getIp()
dbu = db.DB()

dict = {"ip" : ip}
data = dbu.dictSelect("user_ips", dict)
if(data) :
    dict = {"_id": data['users_id']}

    user = dbu.dictSelect("users", dict)

    globals.user = user
    dick = {
        "u_id": str(globals.user['_id'])
    }
    characters = dbu.dictSelect("characters", dick, "", True)
    globals.characters = characters

    main.setupData()
    main.selectCharacter(user['main_character'])
    main.radioButton.setChecked(True)
    Form2.show()

else :
    Form1.show()


app.exec_()  # exec_()가 종료되면 다음 코드가 실행됩니다.

