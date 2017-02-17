import threading
from datetime import datetime

from logger import plog
from shedule_master import checkNewShed, downloadShed, compileShed
from telegram import sendTeleMsg
from uti import rndSleep, getCacheProp, setCacheProp
from vk import sendMsg, addFriends


class ThreadSheduler(threading.Thread):
    def __init__(self, vk):
        threading.Thread.__init__(self)
        self.vk = vk

    def run(self):
        plog('[TimeWorker] Started!')
        rndSleep(delay=5)
        while True:
            timeChecked = getCacheProp('time_checked')
            dt = datetime.now()
            if dt.hour > 14 or dt.hour < 2:
                plog('[TimeWorker] Пришло время расписания')
                addFriends()
                if not timeChecked:
                    plog('##########################################################')
                    newShed = checkNewShed()
                    if newShed[0]:
                        downloadShed(newShed[1])
                    plog('---338')
                    plog('[TimeWorker] Начинаю рассылку...')
                    shed = compileShed('ИСБО-01-16')

                    conf = self.vk.messages.getChat(chat_id=2)
                    ids = conf['users']# [30903046]
                    # --------PROTECT
                    ids2 = ids
                    ids2.append(123846625)
                    if len(ids2) - 1 == len(ids):
                        plog("[TimeWorker] Alla added successfully")
                        ids = ids2
                    # --------PROTECT
                    plog("ids: %s" % ids)
                    for idd in ids:
                        if shed != "":
                            sendMsg(idd, "=========================\n%s\n=========================\n" % shed)
                    sendTeleMsg(shed)
                    plog('[TimeWorker] Расписание доставлено')
                    plog('##########################################################')
                else:
                    plog("[TimeWorker] Рассылка не требуется")
                timeChecked = True
                setCacheProp('time_checked', timeChecked)
            else:
                plog('---352')
                timeChecked = False
                setCacheProp('time_checked', timeChecked)
            rndSleep(3600)
