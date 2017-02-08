import telebot

import config
from logger import plog


def sendTeleMsg(msg):
    channel = "@isbo0116"
    try:
        bot = telebot.TeleBot(config.telegram_api_token)
        bot.send_message(channel, msg)
        plog("[TLGRM] В телеграм тоже скинула")
    except Exception as e:
        plog("[TLGRM] Не смогла отправить в телеграм: %s" % e)
