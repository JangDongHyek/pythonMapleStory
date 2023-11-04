import globals
import pyautogui
import win32gui
import win32api
import time
import numpy as np
import cv2
import gsl
import lib
import json
import math

def getMyposition() :
    position = gsl.pixelSearch(globals.minimap,globals.minimap_me)

    return position

def setMovings() :
    왼쪽 = {
        "이름": "왼쪽",
        "패턴": []
    }
    오른쪽 = {
        "이름": "오른쪽",
        "패턴": []
    }
    위 = {
        "이름": "위",
        "패턴": []
    }
    아래 = {
        "이름": "아래",
        "패턴": []
    }
    for item in globals.movings:
        data = (eval("globals.{}".format(item['keycode'])), item['keydown'], item['delay'])

        eval(item['direction'])["패턴"].append(data)

    left = (왼쪽,globals.minimap_attr["repeat_x"])
    right = (오른쪽, globals.minimap_attr["repeat_x"])
    up = (위, globals.minimap_attr["repeat_y"])
    down = (아래, globals.minimap_attr["repeat_y"])
    arrays = [left, right, up, down]
    results = []

    for item in arrays:
        for i in range(item[1]):
            results.append(item[0])

    globals.game_movings = results

def setSkills() :
    skills = globals.skills.copy()
    results = []
    for skill in skills:
        skill["keycode"] = eval("globals.{}".format(skill['keycode']))
        skill["time"] = eval(skill['time'])
        skill["relations_id"] = json.loads(skill["relations_id"])
        skill["relations"] = json.loads(skill["relations"])

    for skill in skills:
        if not skill['relation']:
            for _id in skill['relations_id']:
                for relation in skills:
                    if _id == relation['_id']:
                        skill['relations'].append(relation)
            results.append(skill)

    globals.game_skills = results

def getMinimapSize(Bool = False) :
    # 미니맵 크기
    x = None
    y = None
    for image in globals.minimap_x_images:
        x = gsl.imageSearch(image)  # + 40
        if (x):
            break

    for image in globals.minimap_y_images:
        y = gsl.imageSearch(image)  # + 40
        if (y):
            break

    if (x == None or y == None):
        lib.alert("미니맵 크기 확인 불가")
        return None

    if Bool :
        obj = {
            "end_x": x[0],
            "end_y": y[1],
        }
        return obj

    if globals.character['move'] == "텔포":
        repeat_x = math.floor(x[0] / 35)
    else :
        repeat_x = math.floor(x[0] / 55)

    repeat_y = math.floor((y[1] / 60))


    globals.minimap_attr = {
        "start_x" : 10,
        "start_y": 22,
        "end_x" : x[0],
        "end_y": y[1],
        "center_x" : (x[0] / 2) + 10,
        "center_y": (y[1] / 2) + 11,
        "repeat_x" : repeat_x,
        "repeat_y" : repeat_y
    }

    globals.minimap = [globals.minimap_attr["start_x"], globals.minimap_attr["start_y"], globals.minimap_attr["end_x"],
                       globals.minimap_attr["end_y"]]
    setMovings()
