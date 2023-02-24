import logging
import time

import telebot
from environs import Env

# Настройки логирования
logging.basicConfig(filename='bot.log', level=logging.INFO)

env = Env()
env.read_env(override=True)
bot = telebot.TeleBot(env.str("TELEGRAM_CONTRSCTORS_BOT_API_TOKEN"))

# Словарь для хранения сообщений от пользователей
user_messages = {}

def get_access(user_id):
    if 0: # пользователя нет в БД
        return 0, 0
    elif 0: # пользователь есть в БД, но не оплатил подписку
        return 1, 0
    else: # пользователь есть в БД и оплатил подписку
        return 2, 0


@bot.message_handler(commands=['start'])
def bot_start(message):
    access, contractor = get_access(message.chat.id)
    if access:
        if access==1: # пользователь есть в БД, но не оплатил подписку
            bot.send_message(
                message.chat.id,
                f"Приветствую, {contractor}",
                reply_markup=get_bot_menu_keyboard_for_1()
            )
        else: # пользователь есть в БД и оплатил подписку
            bot.send_message(
                message.chat.id,
                f"Приветствую, {contractor}",
                reply_markup=get_bot_menu_keyboard_for_2()
            )
    else: # пользователя нет в БД
        bot.send_message(
            message.chat.id,
            f"Приветствую",
            reply_markup=get_bot_menu_keyboard_for_0()
        )


def get_bot_menu_keyboard_for_0():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Ввести Имя'))
    return keyboard


savedata = {}
@bot.message_handler(content_types = ['text'])
def main(message):
    if message.text == 'Ввести имя':
        bot.send_message(message.chat.id, 'Как тебя зовут?')
        savedata[str(message.chat.id) + 'password'] = 'wait'
        savedata[str(message.chat.id) + 'lastname'] = '0'
    print(f"savedata is {savedata}")


def get_bot_menu_keyboard_for_1():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Оплатить подписку'))
    return keyboard


def get_bot_menu_keyboard_for_2():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Вывести список заказов'))
    return keyboard


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(5)
