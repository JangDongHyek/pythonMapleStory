from PyQt5.QtCore import QThread, pyqtSignal
import time
import globals
import win32api
import gsl

class Auction(QThread) :
    update_signal = pyqtSignal(bool,str)

    def run(self):
        image_search = "res/auction/search.png"
        image_buy = "res/auction/buy.png"
        image_max = "res/auction/max.png"
        image_none = "res/auction/none.png"
        image_search_result = "res/auction/search_result.png"
        image_get = "res/auction/get.png"
        image_complete = "res/auction/complete.png"
        image_main_search = "res/auction/main_search.png"
        search = None
        isCheck = True
        count = 0
        try:
            while globals.main :
                time.sleep(1)
                if win32api.GetKeyState(globals.mainKey):
                    isCheck = True
                    if not search :
                        search = gsl.imageSearch(image_search)

                    if search :
                        gsl.hardClick(search)
                        time.sleep(0.5)
                        gsl.hardKey(globals.enter)
                        time.sleep(0.25)
                        gsl.hardKey(globals.enter)
                        time.sleep(0.25)

                        none = gsl.imageSearch(image_none)
                        if none :
                            time.sleep(10)
                            continue
                        else :
                            search_result = gsl.imageSearch(image_search_result)

                            if search_result :
                                for i in range(9) :
                                    gsl.hardClick([search_result[0],search_result[1] + 70])
                                    time.sleep(0.5)
                                    buy = gsl.imageSearch(image_buy)

                                    if buy :
                                        gsl.hardClick(buy)
                                        time.sleep(0.5)

                                        gsl.hardClick(gsl.imageSearch(image_max))
                                        time.sleep(0.5)

                                        gsl.hardKey(globals.enter)
                                        time.sleep(0.25)
                                        gsl.hardKey(globals.enter)
                                        time.sleep(0.25)
                                        count += 1

                                    else :
                                        break

                                complete = gsl.imageSearch(image_complete)
                                if complete :
                                    gsl.hardClick(complete)
                                    time.sleep(0.5)

                                    gsl.hardClick(gsl.imageSearch(image_get))
                                    time.sleep(0.5)
                                    gsl.hardKey(globals.enter)
                                    time.sleep(7)
                                    gsl.hardKey(globals.enter)
                                    time.sleep(0.5)

                                    main_search = gsl.imageSearch(image_main_search)
                                    if main_search :
                                        gsl.hardClick(main_search)
                                    else :
                                        self.update_signal.emit(True, "검색 탭 위치를 찾을수없습니다. 중지합니다")
                                        time.sleep(1)
                                else :
                                    self.update_signal.emit(True, "완료 위치를 찾을수없습니다. 중지합니다")
                                    time.sleep(1)

                            else :
                                self.update_signal.emit(True, "상품 위치를 찾을수없습니다. 중지합니다")
                                time.sleep(1)
                    else :
                        self.update_signal.emit(True, "검색 위치를 찾을수없습니다. 중지합니다")
                        time.sleep(1)

                else :
                    if(isCheck) :
                        self.update_signal.emit(False, f'대기중 시작은 원하시면 시작 키를 눌러주세요. 현재 구매횟수 {count}')
                        isCheck = False

        except Exception as e :
            print(e)