# Обработчик сообщений
import random
import re

import threading

import requests

from logger import plog
from uti import rndSleep, removeGarbage, getCacheProp
from vk import sendMsg, sendMeme, addFriends


class ThreadMessages(threading.Thread):
    def __init__(self, vk):
        threading.Thread.__init__(self)
        self.vk = vk
        self.m_ts = 0

    def run(self):
        pollServ = self.vk.messages.getLongPollServer()
        self.m_ts = pollServ['ts']
        m_key = pollServ['key']
        m_server = pollServ['server']
        plog('[MessageListener] Started!')
        rndSleep(delay=5)
        while True:
            try:
                self._getUpdate_(m_key=m_key, m_server=m_server, m_ts=self.m_ts)
            except Exception as error_msg:
                plog("[MessageListener] " + str(error_msg))
                while True:
                    try:
                        # auth()
                        pollServ = self.vk.messages.getLongPollServer()
                        m_ts = pollServ['ts']
                        m_key = pollServ['key']
                        m_server = pollServ['server']
                        break
                    except Exception as error_msg:
                        plog("[MessageListener] Login error" + str(error_msg))

    def _getUpdate_(self, m_key=0, m_server=0, m_ts=0):
        r = requests.get("https://%s?act=a_check&key=%s&ts=%s&wait=20&mode=2" % (m_server, m_key, m_ts))
        r = r.json()
        self.m_ts = r['ts']
        r = r['updates']
        r = [x for x in r if (x[0] == 4)]  # Выкидываем все события, кроме сообщений
        r = [x for x in r if (self.vk.messages.getById(message_ids=x[1])['items'][0]['out'] == 0)]  # Выкидываем собств сообщ

        # if r:
        #     plog(r)

        for message in r:
            idd = message[3]
            msg = message[6]
            if len(msg) > 0:
                pass
            # plog("<%s> %s"%(idd, msg))
            command = str(removeGarbage(msg)).lower().strip()  # В нижний регистр
            # plog("---->%s"%command)
            # command = list(scommand.split(' ')); # Переводим в список

            if 'окс' in command and 'расп' in command:
                timeChecked = getCacheProp('time_checked')
                if timeChecked:
                    msg = random.choice(('Я уже рассыла сегодня расписание',
                                         'Сегодня я уже рассылала расписание',
                                         'Нет, я уже рассылала расписание сегодня'))
                else:
                    msg = random.choice(('Я отправляю расписание по вечерам',
                                         'Я сама отправлю расписание вечером'))
                sendMsg(idd, msg)

            if 'окс' in command:
                if 'вконф' in command:  # окса вконф текст
                    sendMsg(2, command[1:])

                elif 'мем' in command:  # окса мем
                    if random.randint(0, 100) < 21:
                        sendMsg(idd, random.choice(['Ща, сек)', 'Сейчас, выберу годненький и отправлю)', 'Сейчас)']))
                        rndSleep()
                        sendMeme(idd, guarant=True)
                    else:
                        sendMeme(idd)

                elif 'скажи' in command:  # окса мем
                    if random.randint(0, 100) > 10:
                        try:
                            end_id = re.search('скажи', command).span()[1]
                            plog(command[end_id:])
                            sendMsg(idd, command[end_id:])
                        except Exception as err:
                            plog(err)
                            sendMsg(idd, 'Ну и что мне сказать?')
                    else:
                        sendMsg(idd, random.choice(['Не скажу', 'Не хочу', 'Не буду']))

                elif any(x in command for x in ['прив', 'хай', 'здравств']):
                    sendMsg(idd, random.choice(['Приветик)',
                                                'Привет',
                                                'Здравствуй']))
            elif 'жопа' in command:
                sendMsg(idd, "Да, жопа!")

            elif 'красава' in command:
                sendMsg(idd, random.choice(["КРАСАВА", "КРАСАААВА", "Красава!!!"]))
            elif 'молодцы' in command:
                m = "Сами знаем! &#128079;    &#128079;   &#128079;&#128079;&#128079;  &#128079;&#128079;&#128079;&#128079; Московский Технологический Университет!!!"
                sendMsg(idd, m)
            elif 'добавь' in command:
                addFriends()
