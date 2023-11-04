from PyQt5.QtCore import QThread, pyqtSignal
import time
import globals
import win32api
import gsl
class Disassemble(QThread) :
    update_signal = pyqtSignal(bool,str)

    def run(self):
        images = ["res/disassemble/110.png", "res/disassemble/120.png", "res/disassemble/130.png",
                  "res/disassemble/140.png", "res/disassemble/150.png"]
        count = 0
        isCheck = True
        try :
            while globals.main:
                time.sleep(1)
                if win32api.GetKeyState(globals.mainKey):
                    isCheck = True
                    for item in images:
                        point = gsl.imageSearch(item)
                        if (point):
                            gsl.hardClick((point[0], point[1]), True)
                            time.sleep(0.7)
                            break

                    if (point):
                        for i in range(9):
                            if not win32api.GetKeyState(globals.mainKey):
                                break
                            gsl.hardClick(None,True)
                            time.sleep(0.7)

                        if not win32api.GetKeyState(globals.mainKey):
                            isCheck = True
                            continue

                        ok = gsl.imageSearch("res/disassemble/ok.png")
                        if (ok):
                            gsl.hardClick((ok[0], ok[1]))
                            time.sleep(0.2)
                            gsl.hardKey(globals.enter)
                            time.sleep(3)
                            gsl.hardKey(globals.enter)
                            count += 1
                        else:
                            self.update_signal.emit(True,"어느부분? 분해모드 종료")
                            time.sleep(1)

                    else:
                        self.update_signal.emit(True,"환생의 불꽃이 없습니다. 분해모드 종료")
                        time.sleep(1)

                else:
                    if isCheck :
                        self.update_signal.emit(False,f'대기중 시작은 원하시면 시작 키를 눌러주세요. 현재 분해횟수 {count}')
                        isCheck = False
        except Exception as e:
            print(e)