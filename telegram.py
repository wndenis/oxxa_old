import config
import telebot

from logger import plog


def sendTeleMsg(msg):
    bot = telebot.TeleBot(config.telegram_api_token)
    channel = "@isbo0116"
    try:
        bot.send_message(channel, msg)
        plog("[TLGRM] В телеграм тоже скинула")
    except:
        plog("[TLGRM] В телеграм не скинула")
