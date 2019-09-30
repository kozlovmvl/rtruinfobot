import json
import os
import telebot
from telebot import apihelper, types

from chatbot.models import Answer


with open(os.path.join(os.path.dirname(__file__), 'config.json'),
          'r', encoding='utf-8') as f:
    config = json.load(f)

bot = telebot.TeleBot(config['token'])

if config.get('proxy'):
    apihelper.proxy = {'https': config['proxy']}


@bot.message_handler(commands=['start'])
def get_start_message(message):
    start_message = Answer.get_start()
    bot.send_message(message.from_user.id, start_message['text'])
    keyboard = types.InlineKeyboardMarkup()
    for ans in Answer.get_list(parent_id=start_message['id']):
        keyboard.add(types.InlineKeyboardButton(ans['text'], callback_data=ans['id']))
    bot.send_message(message.from_user.id, 'Выберите пункт', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def get_info_about_plan(call):
    buttons = []
    for ans in Answer.get_list(parent_id=int(call.data)):
        if ans['type'] == 'text':
            bot.send_message(call.message.chat.id, ans['text'])
        else:
            buttons.append(types.InlineKeyboardButton(ans['text'], callback_data=ans['id']))
    if buttons:
        keyboard = types.InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(button)
        bot.send_message(call.message.chat.id, 'Выберите пункт', reply_markup=keyboard)
