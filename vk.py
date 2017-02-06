import random
import config
import vk_api

from logger import plog
from uti import rndSleep


def auth():
    global vk

    vk_session = vk_api.VkApi(login, password, app_id=5271020, client_secret=clientSecret, token=vkToken)
    try:
        vk_session.vk_login()

    except vk_api.AuthorizationError as error_msg:
        plog(error_msg)
    vk = vk_session.get_api()
    return vk


def sendMsg(idd, msg, forward=None, attach=None):
    global vk
    try:
        vk.messages.setActivity(user_id=353056438, type='typing', peer_id=int(idd));  # Типа печатаем
        vk.messages.send(peer_id=int(idd), message=msg, forward_messages=forward, attachment=attach)
    except:
        plog("[MSG] %s не может принять сообщение" % (idd))
        try:
            vk.messages.setActivity(user_id=353056438, type='typing', peer_id=int(idd));  # Типа печатаем
            rndSleep();
            vk.messages.send(user_id=int(idd), message=msg, attachment=attach)
        except:
            plog("[MSG] %s не смог принять сообщение!!!!" % (idd))
        else:
            rndSleep()
    else:
        rndSleep()

def addFriends():
    global vk
    for each in vk.users.getFollowers()["items"]:
        try:
            vk.friends.add(user_id=int(each))
        except Exception as e:
            print(e)




def sendMeme(idd, guarant=False):
    global vk;
    try:
        if random.randint(0, 135) < 3 and not guarant:
            a = 5 / 0;  # не повезло чуваку, идем в экспешн'''
        ownerId = random.choice([65596623, 90839309, 42923159, 73598440, 45745333, 55307799, 66678575, 73319310])
        wall = vk.wall.get(owner_id=-ownerId, offset=random.randint(1, 1700), count=1);
        post = "wall-%d_%d" % (ownerId, wall['items'][0]['id'])
        msg = random.choice(['Ня', 'Держи)', 'Воть'])
        sendMsg(idd, msg, attach=post)
        plog('[SendMeme] Отправила мемчик')
    except:
        sendMsg(idd, random.choice(['Для тебя не нашлось мемасика',
                                    'Не кину',
                                    'Я, конечно, нашла прикол, но, боюсь, ты его не поймешь',
                                    'Нит)',
                                    'Даже я не буду скидывать тебе мемы']))
