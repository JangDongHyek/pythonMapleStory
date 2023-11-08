from PyQt5.QtCore import QThread, pyqtSignal
import time
import globals
import win32api
import gsl
import gml
import random
import lib
import os

class CCTV(QThread) :
    update_signal = pyqtSignal(bool,str)
    def run(self):
        lie_count = 0
        logCount = 0

        while globals.main:
            try :
                if win32api.GetKeyState(globals.mainKey):
                    # 로그
                    gsl.screenshot("res/log/{}".format(logCount))
                    logCount += 1
                    if (logCount > 100):
                        logCount = 0

                    # 거탐
                    if (gsl.imageYolo("lie")):
                        lie_count += 1
                        if (lie_count > 1):
                            lib.playSound("real_detection")
                            # 서취된 파일 저장
                            gsl.screenshot("res/detection/{}".format(lib.getTime(True)))
                    else:
                        lie_count = 0

                    # 비올레타
                    if (gsl.imageSearch("res/cctv/violetta.png")):
                        lib.playSound("violetta")
                        time.sleep(1)


            except Exception as e :
                print("cctv run()")
                print(e)