import telebot
from telebot import apihelper, types

from chatbot.models import Answer


bot = telebot.TeleBot('911272762:AAFs7miGIt7K-pz9WLGBUUHjO1JZ3udVM54')
apihelper.proxy = {'https': 'socks5://5.128.100.109:9050'}


@bot.message_handler(commands=['start'])
def get_start_message(message):
    start_message = Answer.get_start()
    bot.send_message(message.from_user.id, start_message['text'])
    keyboard = types.InlineKeyboardMarkup()
    for ans in Answer.get_list(parent_id=start_message['id']):
        keyboard.add(types.InlineKeyboardButton(ans['text'], callback_data=ans['id']))
    bot.send_message(message.from_user.id, 'Выберете пункт', reply_markup=keyboard)


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
