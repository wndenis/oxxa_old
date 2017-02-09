import random

import vk_api

import config
from logger import plog
from uti import rndSleep


def two_factor_handler():
    code = input('Code: ')
    return code, True


def auth():
    global vk

    vk_session = vk_api.VkApi(config.login, config.password, auth_handler=two_factor_handler, token=config.vkToken) # app_id=5271020, client_secret=config.clientSecret,
    try:
        #vk_session.vk_login()
        vk_session.authorization()

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
        plog("[Friends] Начинаю добавлять друзей")
        try:
            plog("[Friends] Добавляю [%s]" % each)
            vk.friends.add(user_id=each)
        except Exception as e:
            plog("[Friends] Ошибка: %s" % e)




def sendMeme(idd, guarant=False):
    global vk
    try:
        if str(idd) == str(314947049):
            sendMsg(idd, random.choice(['Никита, ищи себе мемы сам',
                                        'Не кину',
                                        'Я, конечно, нашла прикол, но, боюсь, ты его не поймешь',
                                        'Нит)',
                                        'Спроси мем у кого нибудь другого']))
            return
        if random.randint(0, 135) < 3 and not guarant:

            a = 5 / 0  # не повезло чуваку, идем в экспешн'''
        ownerId = random.choice([65596623, 90839309, 73598440, 45745333, 55307799, 66678575, 73319310])
        wall = vk.wall.get(owner_id=-ownerId, offset=random.randint(1, 300), count=1);
        post = "wall-%d_%d" % (ownerId, wall['items'][0]['id'])
        msg = random.choice(['Ня', 'Держи)', 'Воть', 'Прошу', 'Принимай мемос)', '', '', ''])
        sendMsg(idd, msg, attach=post)
        plog('[SendMeme] Отправила мемчик')
    except:
        sendMsg(idd, random.choice(['Для тебя не нашлось мемасика',
                                    'Не кину',
                                    'Я, конечно, нашла прикол, но, боюсь, ты его не поймешь',
                                    'Нит)',
                                    'Даже я не буду скидывать тебе мемы']))
