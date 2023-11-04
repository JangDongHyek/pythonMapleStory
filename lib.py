import time
from gtts import gTTS

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
import playsound

def createTTS(text) :
    tts = gTTS(text=text, lang='ko')
    filename = text + '.mp3'
    tts.save(filename)

def playSound(file) :
    file = "sound/" + file + ".mp3"
    playsound.playsound(file)

def getTime(bool = False) :
    if(bool) :
        return time.strftime('%Y%m%d %H%M%S')
    else :
        return time.strftime('%Y-%m-%d_%H:%M:%S')

def alert(message) :
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle("정보")
    msg.exec_()