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
    """Обработчик команды /start."""
    start_message = Answer.get_start()
    bot.send_message(message.from_user.id, start_message['text'])
    keyboard = types.InlineKeyboardMarkup()
    for ans in Answer.get_list(parent_id=start_message['id']):
        button = types.InlineKeyboardButton(
            text=ans['text'],
            callback_data=ans['id']
        )
        keyboard.add(button)
    bot.send_message(
        chat_id=message.from_user.id,
        text='Выберите пункт',
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: True)
def get_answer_on_click(call):
    """Обработчик нажатия на кнопку."""
    list_answers = Answer.get_list(parent_id=int(call.data)) \
                    + Answer.get_menu()
    buttons = []
    for ans in list_answers:
        if ans['type'] == 'text':
            bot.send_message(call.message.chat.id, ans['text'])
        else:
            button = types.InlineKeyboardButton(
                text=ans['text'],
                callback_data=ans['id']
            )
            buttons.append(button)

    if buttons:
        keyboard = types.InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(button)
        bot.send_message(
            chat_id=call.message.chat.id,
            text='Выберите пункт',
            reply_markup=keyboard)
