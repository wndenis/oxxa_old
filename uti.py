import json
import os
import random
import re
import time

from logger import plog


def rndSleep(delay=0.79, alert=True):
    toSleep = delay + random.randint(2, 4)
    time.sleep(toSleep)


def removeGarbage(text):
    clearText = re.sub(u"[^а-яА-Яa-zA-Z0-9: ]", "", text)
    return clearText


def jDump(file, j):
    with open(file, mode='w', encoding='utf-8') as f:
        json.dump(j, f, indent=1, sort_keys=True, ensure_ascii=False)


def check_and_create_dir(path):
    if not os.path.exists(path):
        plog("Создана директория %s" % path)
        os.makedirs(path)
    else:
        plog("%s существует" % path)


def get_json_data():
    try:
        with open("data\\cache.json", mode='r', encoding='utf-8') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        plog("[Json] Кэш не обнаружен")
        plog("[Json] Создаю файл")
        json_data = {"lastm": "Mon, 28 Nov 2016 01:01:01 GMT", "st_shed": 0, "time_checked": False}
        check_and_create_dir("data")
        jDump('data\\cache.json', json_data)
        return get_json_data()
    return json_data


def getCacheProp(prop):
    json_data = get_json_data()
    s = json_data[prop]
    return s


def setCacheProp(prop, val):
    with open("data\\cache.json", mode='r', encoding='utf-8') as f:
        json_data = json.load(f)
    json_data[prop] = val
    jDump('data\\cache.json', json_data)


def getLastModified():
        with open("data\\cache.json", mode='r', encoding='utf-8') as f:
            json_data = json.load(f)
        lastm = json_data['lastm']
        '''
        except:
            plog("[get_st_shed] Error in st_shed")
            st_shed = 0;
        '''
        plog("old lastm: %s" % lastm)
        return lastm
