from PyQt5.QtCore import QThread, pyqtSignal
import time
import globals
import win32api
import gsl
import gml
import random
import lib
import os


class HuntAssist(QThread) :
    update_signal = pyqtSignal(bool,str)
    def run(self):
        roonTime = None
        lie_count = 0
        logCount = 0
        gameTimer = time.time()
        serverTimver = time.time()

        while globals.main:
            try :
                if not globals.minimap :
                    time.sleep(1)
                    continue

                if win32api.GetKeyState(globals.mainKey):
                    # 죽음
                    if (gsl.imageSearch("res/cctv/die.png")):
                        lib.playSound("die")
                        globals.main = False
                        gsl.offHardKey()

                    # 포탈
                    if (gsl.imageSearch("res/cctv/potal.png")):
                        globals.game_cctv = True
                        time.sleep(1)
                        gsl.offHardKey()
                        time.sleep(1)
                        gsl.hardKey(globals.esc)
                        time.sleep(1)
                        globals.game_cctv = False

                    # # 타이머
                    # if gsl.compareTime(gameTimer,7200) :
                    #     lib.playSound("timer")
                    #     globals.main = False
                    #     gsl.offHardKey()
                    #     time.sleep(1)
                    #     gsl.hardKey(globals.f12)

                    # 1시간1분마다 채널변경
                    if gsl.compareTime(serverTimver, 3660) :
                        globals.game_cctv = True
                        self.changeServer()
                        serverTimver = time.time()

                    # 미니맵확인
                    getMap = gml.getMinimapSize(True)
                    if globals.minimap_attr['end_x'] != getMap['end_x'] :
                        if(getMap['end_x'] > 1000) :
                            continue
                        lib.playSound("map")
                        print(globals.minimap_attr)
                        print(getMap)
                        globals.main = False
                        gsl.offHardKey()

                    if globals.minimap_attr['end_y'] != getMap['end_y'] :
                        lib.playSound("map")
                        print(globals.minimap_attr)
                        print(getMap)
                        globals.main = False
                        gsl.offHardKey()


                    # 룬
                    if gsl.compareTime(globals.game_roon_time,900) :

                        if (gsl.pixelSearch(globals.minimap, globals.minimap_roon)):
                            globals.game_cctv = True
                            if (not roonTime or gsl.compareTime(roonTime, 30)):
                                roonTime = time.time()
                                self.findRoon()
                            else:
                                serverTimver = time.time()
                                self.changeServer()

            except Exception as e :
                print(f"hunt_assist run() : {e}")

    def checkUser(self):
        users = gsl.pixelseSerarch(globals.minimap, globals.minimap_user, 5)
        if (len(users) >= 2):
            return True

        images = ["res/cctv/userCheck1.png","res/cctv/userCheck2.png"]
        for image in images :
            if(gsl.imageSearch(image)) :
                return True

        return False

    def changeServer(self):
        main = True
        first = True
        gsl.offHardKey()

        while main:
            try:
                if not win32api.GetKeyState(globals.mainKey):
                    break

                gsl.hardKey(globals.esc)
                time.sleep(0.5)
                time.sleep(0.5)
                image = gsl.imageSearch("res/cctv/chageServer.png")
                if (image):
                    gsl.hardKey(globals.enter)
                    time.sleep(0.5)
                    gsl.hardKey(globals.right)

                    if (first):
                        time.sleep(3)
                        first = False
                    else:
                        time.sleep(0.5)

                    gsl.hardKey(globals.enter)
                    time.sleep(0.5)
                    if (gsl.imageSearch("res/cctv/changeServerOK.png")):
                        gsl.hardKey(globals.enter)
                    else:
                        subWhile = True
                        while subWhile :
                            time.sleep(0.5)
                            if gsl.imageSearch("res/cctv/minimap.png") :
                                subWhile = False

                        time.sleep(1)
                        if (self.checkUser()):
                            self.update_signal.emit(False, "유저 발견 다시 채널이동")
                        else :
                            self.update_signal.emit(False, "채널이동 완료")
                            main = False
                            globals.game_cctv = False
                time.sleep(0.5)
            except Exception as e:
                print("cctv changeServer()")
                print(e)

    def operateRoon(self):
        try :
            gsl.offHardKey()
            time.sleep(0.5)
            gsl.hardKey(globals.space)
            time.sleep(0.5)
            imageName = "res/roon/{}.bmp".format(lib.getTime(True))

            if globals.windowMode:
                x1 = 697
                x2 = 1237
                y1 = 200
                y2 = 380
            else:
                x1 = 690
                x2 = 1230
                y1 = 170
                y2 = 350

            gsl.screenshot(imageName,[x1, y1, x2, y2])

            time.sleep(0.5)
            roon = gsl.imageYolo("roon", None, [x1, y1, x2, y2])
            time.sleep(0.5)
            if (len(roon) == 4):
                for item in roon:
                    gsl.hardKey(eval("globals.{}".format(item["label"])))
                    time.sleep(0.1)

                time.sleep(1)

                images = ["res/cctv/roon1.png","res/cctv/roon2.png","res/cctv/roon3.png"]
                roonResult = False
                for image in images :
                    if gsl.imageSearch(image) :
                        self.update_signal.emit(False, "룬활성화")
                        roonResult = True
                        globals.game_roon_time = time.time()

                if roonResult :
                    os.remove(imageName)

                globals.game_cctv = False
            else:
                gsl.hardKey(globals.esc)
                time.sleep(1)
                gsl.hardKey(globals.esc)
                time.sleep(1)

                self.update_signal.emit(False, "룬을 인식하지 못했습니다")
                globals.game_cctv = False
        except Exception as e:
            print("cctv operateRoon()")
            print(e)

    def findRoon(self):
        main = True
        roon = time.time()
        while main:
            time.sleep(0.05)
            try :
                if not win32api.GetKeyState(globals.mainKey):
                    self.update_signal.emit(False, "룬찾기 사용자 취소")
                    gsl.offHardKey()
                    globals.game_cctv = False
                    main = False
                    break

                if (gsl.compareTime(roon, 23)):
                    self.update_signal.emit(False, "23초동안 룬을 못찾음 룬찾기 해제")
                    gsl.offHardKey()
                    main = False
                    break

                위치 = gsl.pixelSearch(globals.minimap, globals.minimap_roon)
                if (위치):
                    케릭터위치 = gsl.pixelSearch(globals.minimap, globals.minimap_me)
                    # x축
                    if (abs(위치[0] - 케릭터위치[0]) < 7):
                        gsl.offHardKey()
                        time.sleep(0.7)

                        if (abs(위치[1] - 케릭터위치[1]) < 7):
                            time.sleep(1)
                            self.operateRoon()
                            main = False


                        elif (위치[1] < 케릭터위치[1]):
                            # 로프커넥터
                            gsl.hardKey(globals.v)
                            time.sleep(1)

                            # 무빙 위패턴으로 가는법
                            # for item in globals.game_movings:
                            #     if (item['이름'] == "위"):
                            #         for move in item["패턴"]:
                            #             gsl.hardKey(move[0], move[1])
                            #             if (move[2]):
                            #                 time.sleep(move[2])
                            time.sleep(1)
                        elif (위치[1] > 케릭터위치[1]):
                            gsl.hardKey(globals.down, True)
                            time.sleep(0.1)
                            gsl.hardKey(globals.alt, None)
                            gsl.hardKey(globals.down, False)
                            time.sleep(1)

                    elif (위치[0] < 케릭터위치[0]):
                        gsl.offHardKey()
                        gsl.hardKey(globals.left, True)
                    elif (위치[0] > 케릭터위치[0]):
                        gsl.offHardKey()
                        gsl.hardKey(globals.right, True)

                else:
                    self.operateRoon()
                    main = False
            except Exception as e :
                print(f"cctv findRoon() {e}")
