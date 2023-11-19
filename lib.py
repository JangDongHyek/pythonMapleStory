import time
from gtts import gTTS
import requests

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
import playsound

def getIp():
    try:
        # 외부 웹사이트에 GET 요청을 보내서 공인 IP 주소를 가져옵니다.
        response = requests.get("https://api64.ipify.org?format=json")

        if response.status_code == 200:
            public_ip = response.json()["ip"]
            return public_ip
        else:
            print(f"HTTP 요청 실패: 상태 코드 {response.status_code}")
            return None
    except Exception as e:
        print(f"에러 발생: {e}")
        return None


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