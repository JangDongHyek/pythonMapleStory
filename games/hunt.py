from PyQt5.QtCore import QThread, pyqtSignal
import time
import globals
import win32api
import gsl
import gml
import random
import lib
class Hunt(QThread) :
    update_signal = pyqtSignal(bool,str)

    def run(self):
        totalTime = 0
        startTime = None
        isCheck = True
        isRoom = True
        while globals.main:
            try :
                if win32api.GetKeyState(globals.mainKey):
                    # 룬먹는중일떈 멈추기
                    if globals.game_cctv :
                        time.sleep(1)
                        continue

                    isCheck = True

                    # 가동시간 체킹
                    if not startTime :
                        startTime = time.time()
                    # 미니맵 체킹
                    if not globals.minimap :
                        gml.getMinimapSize()

                    myPosition = gml.getMyposition()
                    movingPattern = globals.game_movings.copy()

                    # 현재 케릭터위치에 따른 x이동패턴 수정
                    if (globals.minimap_attr["center_x"] < myPosition[0]):
                        # 원래 지울패턴 (내케릭이 오른쪽에있을떄)
                        for i in range(globals.minimap_attr["repeat_x"]):
                            gsl.arrayTargetDelete(movingPattern, "이름", "오른쪽")
                        # 확률로 지워져야할 패턴
                        for i in range(random.randrange(0, globals.minimap_attr["repeat_x"])):
                            gsl.arrayTargetDelete(movingPattern, "이름", "왼쪽")
                    else:
                        # 원래 지울패턴 (내케릭이 왼쪽에있을떄)
                        for i in range(globals.minimap_attr["repeat_x"]):
                            gsl.arrayTargetDelete(movingPattern, "이름", "왼쪽")
                        # 확률로 지워져야할 패턴
                        for i in range(random.randrange(0, globals.minimap_attr["repeat_x"])):
                            gsl.arrayTargetDelete(movingPattern, "이름", "오른쪽")

                    if (globals.minimap_attr["center_y"] < myPosition[1]):
                        # 원래 지울패턴 (내케릭이 아래에있을떄)
                        for i in range(globals.minimap_attr["repeat_y"]):
                            gsl.arrayTargetDelete(movingPattern, "이름", "아래")
                        # 확률로 지워져야할 패턴
                        for i in range(random.randrange(0, globals.minimap_attr["repeat_y"] + 1)):
                            gsl.arrayTargetDelete(movingPattern, "이름", "위")
                    else:
                        # 원래 지울패턴 (내케릭이 위에있을떄)
                        for i in range(globals.minimap_attr["repeat_y"]):
                            gsl.arrayTargetDelete(movingPattern, "이름", "위")
                        # 확률로 지워져야할 패턴
                        for i in range(random.randrange(0, globals.minimap_attr["repeat_y"] + 1)):
                            gsl.arrayTargetDelete(movingPattern, "이름", "아래")

                    random.shuffle(movingPattern)

                    for 이동 in movingPattern:
                        if not win32api.GetKeyState(globals.mainKey) or globals.game_cctv:
                            break

                        for item in 이동["패턴"]:
                            if not win32api.GetKeyState(globals.mainKey) or globals.game_cctv:
                                break

                            gsl.hardKey(item[0], item[1])
                            if (item[2]):
                                time.sleep(item[2])

                        for 스킬 in globals.game_skills:
                            if not win32api.GetKeyState(globals.mainKey) or globals.game_cctv:
                                break

                            if (gsl.compareTime(스킬['time'], 스킬['cooldown'])):
                                time.sleep(스킬['before'])
                                gsl.hardKey(스킬['keycode'], None, 스킬['keydown'])
                                스킬['time'] = time.time()
                                time.sleep(스킬['after'])

                                for 연계 in 스킬["relations"]:
                                    if (gsl.compareTime(연계['time'], 연계['cooldown'])):
                                        time.sleep(연계['before'])
                                        gsl.hardKey(연계['keycode'], None, 연계['keydown'])
                                        연계['time'] = time.time()
                                        time.sleep(연계['after'])

                                break

                        time.sleep(random.uniform(0.1, 0.2))

                else :
                    if (isCheck):
                        if startTime :
                            totalTime = totalTime + (time.time() - startTime)
                        self.update_signal.emit(False, f'대기중 시작은 원하시면 시작 키를 눌러주세요. 현재 사냥시간 : {totalTime}초')
                        gsl.offHardKey()
                        startTime = None
                        globals.minimap = None
                        isCheck = False

            except Exception as e :
                if isRoom :
                    lib.playSound("special")
                    isRoom = False
                print(f"hunt run() : {e}")
