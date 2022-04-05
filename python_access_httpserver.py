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

from functions import mini_map_image, Image_count, image_Rec_clicker, invent_crop, release_drop_item, drop_item, \
    screen_Image, invent_enabled, random_breaks, Image_Rec_single
from woodcutting import bank_spot

y_offset = 64

def take_tinderbox(image='take_tinderbox.png', iheight=1, iwidth=1, threshold=0.7):
    global icoord
    global iflag
    screen_Image(0, 0, 600, 750)
    img_rgb = cv2.imread('screenshot.png')
    # print('screenshot taken')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    w, h = template.shape[::-1]
    pt = None
    # print('getting match requirements')
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = threshold
    loc = np.where(res >= threshold)
    # print('determine loc and threshold')
    # if len(loc[0]) == 0:
    # exit()
    iflag = False
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    # print('result of pt')
    if pt is None:
        iflag = False
        icoord = None
        # print(event, 'Not Found...')
    else:
        iflag = True
        # cv2.imwrite('res.png', img_rgb)
        # print(event, 'Found...')
        x = random.randrange(iwidth, iwidth + 40)
        y = random.randrange(iheight, iheight + 10)
        icoord = pt[0] + iheight + x
        icoord = (icoord, pt[1] + iwidth + y)
        b = random.uniform(0.2, 0.7)
        pyautogui.moveTo(icoord, duration=b)
        b = random.uniform(0.1, 0.3)
        pyautogui.click(icoord, duration=b, button='left')
    return iflag, icoord

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

def bank_action():
    Image_Rec_single('tinderbox.png','deposit tinderboxes', playarea=False)

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

def add_tinderboxes_inv(b=28):
    i = 0
    while i < b:
        y_tinder = 476 + random.randrange(0, 29) - 64
        x_tinder = 422 + random.randrange(-10, 10)
        pyautogui.moveTo(x_tinder, y_tinder)
        pyautogui.rightClick()
        take_tinderbox()
        d = random.uniform(0.3, 1)
        time.sleep(d)
        i += 1
def grab_inv_full_tinderboxes(b=28):
    i = 0
    drop_item()
    while i < b:
        determine_object()
        time.sleep(random.uniform(0.15, 0.2))
        print(Image_count('tinderbox.png', 0.8))
        # while http_events() != 808:
        # http_events()
        image_Rec_clicker('tinderbox.png', 'dropping item', 5, 5, 0.8, 'left', 15, False, True)
        i += 1
        print('items left:', i)
    release_drop_item()
def draynor_tinderbox_1():
    coords = location_ready('(3091,3248)')
    print(coords)
    final_coords = tuple(map(int, coords.split(', ')))
    print(final_coords[0])
    xi = random.randrange(-5, 5)
    yi = random.randrange(-5, 5)
    d = random.uniform(0.05, 0.4)
    pyautogui.moveTo(final_coords[0] + xi, final_coords[1] + yi, duration=d)
    pyautogui.click()

def draynor_spot(spot='(3091,3248)'):
    coords = location_ready(spot)
    print(coords)
    final_coords = tuple(map(int, coords.split(', ')))
    print(final_coords[0])
    xi = random.randrange(-5, 5)
    yi = random.randrange(-5, 5)
    d = random.uniform(0.05, 0.4)
    pyautogui.moveTo(final_coords[0] + xi, final_coords[1] + yi, duration=d)
    pyautogui.click()

x = random.randrange(100, 250)
y = random.randrange(400, 500)
pyautogui.click(x, y, button='right')

draynor_tinderbox_1()
time.sleep(1)
while http_events() != 808:
    http_events()
determine_wall()
time.sleep(1)
while http_events() != 808:
    http_events()
determine_object()
time.sleep(1)
while http_events() != 808:
    http_events()
grab_inv_full_tinderboxes(28)
add_tinderboxes_inv(28)
d = random.uniform(0.3,1.5)
time.sleep(d)
determine_wall()
time.sleep(2)
while http_events() != 808:
    http_events()
draynor_spot('(3090,3249)')
time.sleep(2)
while http_events() != 808:
    http_events()
determine_object(id='10355', world_postition=(3091, 3245))
time.sleep(2)
while http_events() != 808:
    http_events()
bank_action()
