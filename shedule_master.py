# -*- coding: utf-8 -*-
import json
import re
from datetime import datetime, timedelta
from urllib.request import urlretrieve

import xlrd

from grabber import getWeekNum, getWeather, getShedUrl, getLastModifiedS
from logger import plog
from uti import getCacheProp, jDump, setCacheProp, getLastModified
from vk import sendMsg


def downloadShed(url):

    try:
        st_shed = getCacheProp('st_shed')
    except:
        plog("[DownloadShed] ошибка в st_shed")
        st_shed = -1

    dest = "data\\shedules\\xls\\%s.xls" % st_shed
    plog("[DownloadShed] Скачиваю %s" % url)
    try:
        urlretrieve(url, dest)
    except Exception as e:
        plog("[DownloadShed] Я не смогла скачать расписание: %s" % e)
        return
    plog("[DownloadShed] Расписание скачано!")
    plog("%s.xls\n" % st_shed)
    parse_file_to_json("%s" % st_shed)


def parse_file_to_json(file):
    plog('[ParseFileToJson] Начинаю парсинг...')

    shed = xlrd.open_workbook("data\\shedules\\xls\\%s.xls" % file)  # , formatting_info=True)

    sheet = shed.sheet_by_index(0)
    jsonShedules = dict()
    for group in ["ИСБО-01-16"]:
        y = -1
        for rownum in range(sheet.nrows):
            y += 1
            x = -1
            row = sheet.row_values(rownum)
            for c_el in row:
                x += 1
                if str(c_el).rstrip() == group:
                    timeStartData = sheet.col_values(x + 5, start_rowx=y + 2, end_rowx=y + 2 + 12 * 6)
                    timeEndData = sheet.col_values(x + 6, start_rowx=y + 2, end_rowx=y + 2 + 12 * 6)
                    lessonData = sheet.col_values(x, start_rowx=y + 2, end_rowx=y + 2 + 12 * 6)
                    workData = sheet.col_values(x + 1, start_rowx=y + 2, end_rowx=y + 2 + 12 * 6)
                    workData = [x.upper() for x in workData]
                    auditoryData = sheet.col_values(x + 2, start_rowx=y + 2, end_rowx=y + 2 + 12 * 6)
                    summary = [(lessonData[i], workData[i], auditoryData[i]) for i in range(12*6)]
                    parsedData = [
                        ([start, end, lesson, work, auditory
                          ]) if lesson != "" else [start, end, "НЕТ ПАРЫ", "", ""] for start, end, lesson, work, auditory in
                        zip(timeStartData, timeEndData, lessonData, workData, auditoryData)]

                    report = "Вот что я там нашла:\n"
                    for elem in parsedData:
                        report += str(elem) + "\n"
                    sendMsg("30903046", report)

                    # пакуем пары 1/2
                    packedData = [parsedData[i * 2:i * 2 + 2] for i in range(len(parsedData) // 2)]
                    # пакуем дни 12 12 12 12 12 12
                    packedData = [packedData[i * 6:i * 6 + 6] for i in range(len(packedData) // 6)]

        jsonWeek = []
        for day in packedData:
            jsonDay = {}  # Разобранное расписание ДНЯ
            pairNum = 0
            for pair in day:
                jsonPair = {}
                pairNum += 1
                for i in (0, 1):
                    lesson = pair[i]
                    lessonName = lesson[2]

                    lessonWork = ""
                    if lesson[3] != "":
                        lessonWork = lesson[3]

                    lessonAuditory = ""
                    if lesson[4] != "":
                        lessonAuditory = "(" + lesson[4] + ")"

                    jsonLesson = {"lesson": "%s %s %s" % (lessonName, lessonWork, lessonAuditory)}

                    if i % 2 == 0:  # нечетный
                        pairTimeStart = re.sub('-', ':', lesson[0])
                        pairTimeEnd = re.sub('-', ':', lesson[1])
                        jsonPair["odd"] = jsonLesson
                        jsonPair["time"] = "[%s-%s]" % (pairTimeStart, pairTimeEnd)
                    else:  # четный
                        jsonPair["even"] = jsonLesson
                    jsonDay[pairNum] = jsonPair
                jsonDay[pairNum] = jsonPair
            jsonWeek.append(jsonDay)
        jsonShedules[group] = jsonWeek

    jDump("data\\shedules\\json\\%s.json" % file, jsonShedules)
    plog('[ParseFileToJson] Парсинг завершен.')
    plog('====================')


def getDailyShed(day, week, group):
    with open("data\\shedules\\json\\%s.json" % getCacheProp('st_shed'), mode='r', encoding='utf-8') as f:
        json_data = json.load(f)
    dayData = json_data[group][day]

    if week % 2 == 0:
        weekType = "even"
    else:
        weekType = "odd"

    ans = ""
    pairNum = 0
    shed = [dayData[pair] for pair in sorted(dayData)]
    # Если пара пустая, то не добавлять ее
    for pair in reversed(shed):
        if "НЕТ ПАРЫ" in pair[weekType]["lesson"]:
            shed.pop()
        else:
            break

    for pair in shed:
        pairNum += 1
        ans += "%s) %s\n%s\n\n" % (pairNum, pair["time"], pair[weekType]["lesson"])
    return ans


def compileShed(group):
    days_of_week = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']
    plog("[ShedCompiler] Начал сборку...")
    dt = datetime.now() + timedelta(days=1, hours=-3)
    day = datetime.weekday(dt)
    if day != 6:
        plog('[CompileShed] Day != 5')
        week = getWeekNum()
        if day == 6 or day == 0:
            day = 0
            week += 1
        date = datetime.strftime(dt, "%d.%m.%y")
        dOw = days_of_week[day]
        weather = getWeather()

        s = '''Информация на %s (%s)
%s-я неделя.
%s
Погода:
%s''' % (date, dOw, week, getDailyShed(day, week, 'ИСБО-01-16'), weather)
        plog("%s" % s)
        plog("[ShedCompiler] Сборка завершена!")
        return s
    else:
        plog("[ShedCompiler] Сборка НЕ завершена!")
        return ''



def checkNewShed():
    plog("====================")
    try:
        st_shed = getCacheProp('st_shed')
    except:
        plog('eRRRRRRRRRRRROr')
        st_shed = 0
    s = getShedUrl()
    plog("Url: %s" % s)
    try:
        new = getLastModifiedS(s)
        old = getLastModified()
        if new != old:
            plog("Найдено новое расписание")
            sendMsg(30903046, "Я нашла новое расписание, загружаю")
            setCacheProp('st_shed', st_shed + 1)
            setCacheProp('lastm', new)
            return True, s
        else:
            plog("Новое расписание не найдено")
            return False, False

    except:
        plog("Ошибка при проверке нового расписания")
