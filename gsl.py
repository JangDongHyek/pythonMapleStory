import globals
import pyautogui
import win32gui
import win32api
import time
import numpy as np
import cv2

def offHardKey() :
    arrays = ["right","left","down","up","alt",
              "ctrl","shift","end","pagedown","insert","delete","pageup","n1","n2","a","s","r"
              ]
    for key in arrays :
        hardKey(eval("globals.{}".format(key)),False)


def compareTime(value,elapse) :
    if not value :
        return False

    if(time.time() - value >= elapse) :
        return True
    return False

def arrayTargetDelete(array,field,target) :
    for index in range(0, len(array)):
        data = array[index]
        if (data[field] == target):
            del array[index]
            break

def pixelSearch(points, pixcels) :
    screen = screenshot().load()

    main = True
    x = points[0]
    y = points[1]

    while main:
        if x == points[2] and y == points[3]:
            main = False
        if screen[x, y] in pixcels:
            return (x, y)

        if x == points[2]:
            y += 1
            x = points[0]
        x += 1
    return None

def hardKey(key,bool = None,push = 0.1) :
    if(bool == None or bool == 2) :
        globals.ddl.DD_key(key, 1)
        time.sleep(push)
        globals.ddl.DD_key(key, 2)
    elif (bool == True) :
        globals.ddl.DD_key(key, 1)
    elif(bool == False) :
        globals.ddl.DD_key(key, 2)

def hardClick(point,right = False,time = 0.2) :
    if point :
        if globals.windowMode :
            x = point[0] + globals.windowPlusX
            y = point[1] + globals.windowPlusY
        else :
            x = point[0]
            y = point[1]

        pyautogui.moveTo(x, y, duration=time)

    if(right) :
        globals.ddl.DD_btn(4)
        globals.ddl.DD_btn(8)
    else :
        globals.ddl.DD_btn(1)
        globals.ddl.DD_btn(2)

def imageSearch(img,confidence = 0.85,image = None) :
    # 한글이름 이미지 읽게하기
    img_array = np.fromfile(img, np.uint8)
    template = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if image :
        result = pyautogui.locate(template, image, confidence=confidence)
    else :
        result = pyautogui.locate(template,screenshot(),confidence=confidence)

    return result

def screenshot(name = None,scale = []):
    win32gui.SetForegroundWindow(globals.hwnd)
    x, y, x1, y1 = win32gui.GetClientRect(globals.hwnd)
    x, y = win32gui.ClientToScreen(globals.hwnd, (x, y))
    x1, y1 = win32gui.ClientToScreen(globals.hwnd, (x1 - x, y1 - y))
    if (len(scale)):
        im = pyautogui.screenshot(region=(scale[0], scale[1], scale[2] - scale[0], scale[3] - scale[1]))
    else:
        im = pyautogui.screenshot(region=(x, y, x1, y1))

    if name:
        if ".bmp" in name :
            im.save(name)
        else :
            im.save(name + ".bmp")

    return im

def imageYolo(weights,name = None, scale = []) :
    net = cv2.dnn.readNet("yolo/" + weights + ".weights","yolo/" + weights + ".cfg")
    classes = []
    arrays = []
    with open("yolo/" + weights + ".names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 4))

    # 이미지 가져오기
    if name :
        img = cv2.imread(name)
    else :
        if(len(scale)) :
            screen = screenshot(name,scale)
        else :
            screen = screenshot()

        img = np.array(screen)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # 좌표
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 3)

            obj = {
                "x": x,
                "y": y,
                "label": label
            }

            arrays.append(obj)

    arrays.sort(key = lambda x: x["x"])

    return arrays