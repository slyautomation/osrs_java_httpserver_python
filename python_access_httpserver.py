import json
import random
import re
import time

import cv2
import numpy as np
import pandas as pd
import pyautogui
import requests
from pandas.io.json import json_normalize

y_offset = 64

def call_http_osrs_stats():
    response = requests.get("http://localhost:8080/stats")
    stats = json.loads(response.text)
    print(stats)
    return stats


def call_http_osrs_doors():
    response = requests.get("http://localhost:8080/doors")
    stats = json.loads(response.text)
    print(stats)
    return stats


def call_http_osrs_objects():
    response = requests.get("http://localhost:8080/objects")
    stats = json.loads(response.text)
    print(stats)
    return stats


def determine_wall(id='1535', world_position=(3088, 3251)):
    list_doors = call_http_osrs_doors()
    test_pd = pd.DataFrame(json_normalize(list_doors))
    # print(test_pd)
    wall_count = test_pd.count(axis='columns')
    # print("test_pd count:", test_pd.iloc[0][1])
    i = 0
    b = test_pd.iloc[0][1]
    while i < wall_count[0]:
        b = test_pd.iloc[0][i]
        result = re.split(r',\s*(?![^()]*\))', b)
        # print(eval(result[1]))
        if result[0] == id and eval(result[1]) == world_position:
            print("result:", result)
            print('door is closed')
            print('mouse location:', eval(result[2]))
            print('world position:', eval(result[1]))
            mouse = eval(result[2])
            x = random.randrange(-10, 10)
            y = random.randrange(-10, 10)

            mouse = (mouse[0] + x, mouse[1] + y)
            pyautogui.moveTo(mouse)
            pyautogui.leftClick()
            return True
        if result[0] == '1536' and eval(result[1]) == (3088, 3250):
            print("result:", result)
            print('door is open')
            print('mouse location:', eval(result[2]))
            print('world position:', eval(result[1]))
            pyautogui.moveTo(eval(result[2]))
            pyautogui.leftClick()
        print("result:", result)
        i += 1


def determine_object(id='7079', world_postition=(3091, 3255)):
    list_object = call_http_osrs_objects()
    test_pd = pd.DataFrame(json_normalize(list_object))
    # print(test_pd)
    object_count = test_pd.count(axis='columns')
    # print("test_pd count:", test_pd.iloc[0][1])
    i = 0
    b = test_pd.iloc[0][1]
    while i < object_count[0]:
        b = test_pd.iloc[0][i]
        b = b.replace("[", "")
        b = b.replace("]", "")
        b = b.replace(":", ",")
        print("b:", b)
        result = re.split(r',\s*(?![^()]*\))', b)
        print(eval(result[1]))
        print("id:", result[0])
        if result[0] == id and eval(result[1]) == world_postition:
            print("result:", result)
            print('door is closed')
            print('mouse location:', eval(result[2]))
            print('world position:', eval(result[1]))
            mouse = eval(result[2])
            x = random.randrange(-10, 10)
            y = random.randrange(-10, 10)
            mouse = (mouse[0] + x, mouse[1] + y)
            pyautogui.moveTo(mouse)
            pyautogui.leftClick()
            return eval(result[2])
        # print("result:", result)
        i += 1

def http_query(query='(3091,3248)'):
    response = requests.get("http://localhost:8080/post?name=" + query)
    stats = json.loads(response.text)
    print(stats)
    return stats

def http_events():
    response = requests.get("http://localhost:8080/events")
    stats = json.loads(response.text)
    print(stats['animation pose'])
    return stats['animation pose']


def location_ready(query='(3091,3248)'):
    pos = http_query(query)
    print(pos['test'])
    ass = pos['test'].replace(r' |', ',')
    result = re.split(r',\s*(?![^()]*\))', ass)
    print(result)
    print(result[0])
    print(result[1])
    print(result[2])
    return result[2].replace(r'(', '').replace(r')', '')

def get_mouse_spot(spot='(3091,3248)'):
    coords = location_ready(spot)
    print(coords)
    final_coords = tuple(map(int, coords.split(', ')))
    print(final_coords[0])
    xi = random.randrange(-5, 5)
    yi = random.randrange(-5, 5)
    d = random.uniform(0.05, 0.4)
    pyautogui.moveTo(final_coords[0] + xi, final_coords[1] + yi, duration=d)
    pyautogui.click()


