"""Сервис бота.

"""

import telebot
from telebot import apihelper, types


bot = telebot.TeleBot('911272762:AAFs7miGIt7K-pz9WLGBUUHjO1JZ3udVM54')
apihelper.proxy = {'https': 'socks5://95.181.202.5:8888'}


bot.polling()
