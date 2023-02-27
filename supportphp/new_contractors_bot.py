import logging
import time
import signal
import sys
import os
import django

import telebot
from environs import Env

os.environ['DJANGO_SETTINGS_MODULE'] = 'supportphp.settings'
django.setup()

from supportphp.settings import TG_TOKEN_CONTRACTOR_BOT
from orderbase.models import Client, Maker, Order, Conversation


# Настройки логирования
logging.basicConfig(filename='bot.log', level=logging.INFO)

env = Env()
env.read_env(override=True)
bot = telebot.TeleBot(TG_TOKEN_CONTRACTOR_BOT)


def signal_handler(signum, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def get_access(user_id):
    try:
        maker = Maker.objects.get(telegram_id=user_id)
        if maker.subscription_is_active:  # пользователь есть в БД и оплатил подписку
            return 2, maker
        else:  # пользователь есть в БД, но не оплатил подписку
            return 1, maker
    except Maker.DoesNotExist:  # пользователя нет в БД
        return 0, 0


@bot.message_handler(commands=['start'])
def bot_start(message):
    access, contractor = get_access(message.chat.id)
    if access:  # TODO - перечитал задачу, понял что подрядчику никакой подписки оплачивать не нужно. Т.е. нужно полностью удалить make_keyboard_pay_for_subscription, pay_for_subscription
        if access == 1:  # пользователь есть в БД, но не оплатил подписку
            bot.send_message(
                message.chat.id,
                f"Приветствую, {contractor.name}. Осталось оплатить подписку.",
                reply_markup=make_keyboard_pay_for_subscription()
            )
        else:  # пользователь есть в БД и оплатил подписку
            bot.send_message(
                message.chat.id,
                f"Приветствую, {contractor}.",
                reply_markup=get_bot_menu_keyboard_for_2()
            )
    else:  # пользователя нет в БД
        bot.send_message(
            message.chat.id,
            "Приветствую.\nДля регистрании на сервисе введите, пожалуйста, ваше имя:",
        )
        bot.register_next_step_handler(message, register_new_contractor_in_db)


def register_new_contractor_in_db(message):
    if message.text:
        try:
            Maker.objects.create(telegram_id=message.chat.id, name=message.text, subscription_is_active=False)
            bot.send_message(
                message.chat.id,
                "Позравляем, вы успешно зарегистрировались на сервисе, осталось оплатить подписку.",
                reply_markup=make_keyboard_pay_for_subscription(),
            )
        except Exception as error_text:
            bot.send_message(
                message.chat.id,
                "На сервисе произошёл сбой, подождите несколько минут и попробуйте ввести имя повторно:",
            )
            bot.register_next_step_handler(message, register_new_contractor_in_db)
            print(f"Error was occured: {error_text}")
    else:
        bot.send_message(
            message.chat.id,
            "Для регистрании на сервисе введите, пожалуйста, ваше имя:",
        )
        bot.register_next_step_handler(message, register_new_contractor_in_db)


def make_keyboard_pay_for_subscription():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Оплатить подписку'))
    keyboard.add(telebot.types.KeyboardButton('Изменить имя'))
    return keyboard


@bot.message_handler(func=lambda message: message.text == 'Оплатить подписку')
def pay_for_subscription(message):
    access, contractor = get_access(message.chat.id)
    if not access:
        bot.send_message(
            message.chat.id,
            "Прежде чем оплачивать пописку требуется пройти регистрацию. Введите, пожалуйста, ваше имя:",
        )
        bot.register_next_step_handler(message, register_new_contractor_in_db)
    elif contractor.subscription_is_active:
        bot.send_message(
            message.chat.id,
            "Вы уже оплатили подписку.",
            reply_markup=get_bot_menu_keyboard_for_2(),
        )
    else:
        try:  # TODO - пока что это только определение места, где будет происходить оплата.
            contractor.subscription_is_active = True
            contractor.save()
            bot.send_message(
                message.chat.id,
                "Поздравляем, вы оплатили подписку!",
                reply_markup=get_bot_menu_keyboard_for_2(),
            )
        except Exception as error_text:
            bot.send_message(
                message.chat.id,
                "Оплата не прошла, проверте баланс или подождите несколько минут и попробуйте повторно:",
            )
            print(f"Error was occured: {error_text}")


@bot.message_handler(func=lambda message: message.text == 'Изменить имя')
def change_contractors_name(message):
    access, _ = get_access(message.chat.id)
    if not access:
        bot.send_message(
            message.chat.id,
            "Прежде чем менять имя требуется пройти регистрацию. Введите, пожалуйста, ваше имя:",
        )
        bot.register_next_step_handler(message, register_new_contractor_in_db)
    else:
        bot.send_message(
            message.chat.id,
            "Введите, пожалуйста, ваше новое имя:",
        )
        bot.register_next_step_handler(message, change_name)


def change_name(message):
    access, contractor = get_access(message.chat.id)
    contractor.name = message.text
    contractor.save()
    if access==1:
        bot.send_message(
            message.chat.id,
            "Вы успешно изменили своё имя.",
            reply_markup=make_keyboard_pay_for_subscription(),
        )
    else:
        bot.send_message(
            message.chat.id,
            "Вы успешно изменили своё имя.",
            reply_markup=get_bot_menu_keyboard_for_2(),
        )



def get_bot_menu_keyboard_for_2():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Вывести список доступных заказов'))
    keyboard.add(telebot.types.KeyboardButton('Вывести список заказов, которые я взял'))
    keyboard.add(telebot.types.KeyboardButton('Вывести список непрочитанных ответов от клиентов'))
    keyboard.add(telebot.types.KeyboardButton('Написать вопрос по заказу'))
    keyboard.add(telebot.types.KeyboardButton('Завершить заказ'))
    keyboard.add(telebot.types.KeyboardButton('Изменить имя'))
    return keyboard


@bot.message_handler(func=lambda message: message.text == 'Вывести список доступных заказов')
def show_orders_list(message):
    active_untaken_orders = Order.objects.filter(order_is_done=False, maker=None)
    count = 0
    for order in active_untaken_orders:
        count += 1
        inline_btn = telebot.types.InlineKeyboardButton(f"Взять заказ №{order.id}", callback_data=f"order {order.id}")
        inline = telebot.types.InlineKeyboardMarkup().add(inline_btn)
        bot.send_message(
            message.chat.id,
            f"Заказ №{order.id}\nНазвание: {order.name}\nВремя на заказ: {order.exec_time}\nТекст: {order.problem}",
            reply_markup=inline,
        )
    bot.send_message(
        message.chat.id,
        f"Итого доступных заказов: {count}",
        reply_markup=get_bot_menu_keyboard_for_2(),
    )


@bot.callback_query_handler(func=lambda c: 'order' in c.data)
def process_callback_order_button(callback_query: telebot.types.CallbackQuery):
    _, order_id = callback_query.data.split(" ")
    order = Order.objects.get(id=order_id)
    contractor = Maker.objects.get(telegram_id=callback_query.from_user.id)

    bot.answer_callback_query(callback_query.id)
    if order.order_is_done:
        bot.send_message(
            callback_query.from_user.id,
            'Этот заказ уже закрыт.',
        )
    elif order.maker:
        bot.send_message(
            callback_query.from_user.id,
            'Другой подрядчик уже взял этот заказ.',
        )
    else:
        try:
            contractor.order_set.add(order)
            contractor.save()
            order.maker = contractor
            order.save()
            bot.send_message(
                callback_query.from_user.id,
                'Поздравляю, вы взяли этот заказ!'
            )
        except Exception as error_text:
            bot.send_message(
                callback_query.from_user.id,
                'Случилась непредвиденная ошибка, попробуйте ещё раз через несколько минут.'
            )
            print(f"Error was occured: {error_text}")


@bot.message_handler(func=lambda message: message.text == 'Вывести список заказов, которые я взял')
def show_my_orders_list(message):
    contractor = Maker.objects.get(telegram_id=message.chat.id)
    count = 0
    for order in contractor.order_set.all():
        bot.send_message(
            message.chat.id,
            f"Заказ №{order.id}\nНазвание: {order.name}\nВремя на заказ: {order.exec_time}\nТекст: {order.problem}",
        )
        count += 1
    bot.send_message(
        message.chat.id,
        f"Всего заказов = {count}.",
    )


@bot.message_handler(func=lambda message: message.text == 'Вывести список непрочитанных ответов от клиентов')
def show_my_clients_answers(message):
    try:
        conversations = Conversation.objects.filter(message_receiver=f"tg_id_{message.chat.id}", message_is_read=False)
    except Exception as error_text:
        bot.send_message(
            message.chat.id,
            "Произошла ошибка на стороне сервера, пожалуйсята, попробуйте позже.",
        )
        print(f"error was occured: {error_text}")
    count = 0
    for conversation in conversations:
        bot.send_message(
            message.chat.id,
            f"Ответ по заказу №{conversation.order_id.id}:\n{conversation.message_text}",
        )
        conversation.message_is_read = True
        conversation.save()
        count += 1
    bot.send_message(
        message.chat.id,
        f"Всего ответов = {count}.",
    )


@bot.message_handler(func=lambda message: message.text == 'Написать вопрос по заказу')
def send_question_to_client(message):
    bot.send_message(
        message.chat.id,
        "Введите пожалуйста номер заказа:",
    )
    bot.register_next_step_handler(message, get_order_id_to_send_question)


def get_order_id_to_send_question(message):
    try:
        order_id = int(message.text)
        order = Order.objects.get(id=order_id)
        if order.order_is_done:
            bot.send_message(
                message.chat.id,
                "Заказ уже закрыт.",
            )
        else:
            bot.send_message(
                message.chat.id,
                "Введите пожалуйста вопрос:",
            )
            bot.register_next_step_handler(message, get_message_to_send_question, order_id)
    except Order.DoesNotExist:
        bot.send_message(
            message.chat.id,
            "Заказа с таким номером не существует.",
        )


def get_message_to_send_question(message, order_id):
    try:
        order = Order.objects.get(id=order_id)
        Conversation.objects.create(
            message_sender=f"tg_id_{message.chat.id}",
            message_receiver=f"tg_id_{order.client.telegram_id}",
            order_id=order,
            message_text=message.text,
            message_is_read=False
        )
        bot.send_message(
            message.chat.id,
            "Вопрос успешно отправлен.",
        )
    except Exception as error_text:
        bot.send_message(
            message.chat.id,
            "На стороне сервера возникли непредвиденные сложности, пожалуйста, попробуйте снова через несколько минут.",
        )
        print(f"Error was occured: {error_text}")


@bot.message_handler(func=lambda message: message.text == 'Завершить заказ')
def send_question_to_client(message):
    bot.send_message(
        message.chat.id,
        "Введите пожалуйста номер заказа:",
    )
    bot.register_next_step_handler(message, get_order_id_to_close_order)


def get_order_id_to_close_order(message):
    try:
        order_id = int(message.text)
        order = Order.objects.get(id=order_id)
        if order.order_is_done:
            bot.send_message(
                message.chat.id,
                "Заказ уже закрыт.",
            )
        else:
            order.order_is_done = True
            order.save()
            Conversation.objects.create(
                message_sender=f"tg_id_{message.chat.id}",
                message_receiver=f"tg_id_{order.client.telegram_id}",
                order_id=order,
                message_text=f"Ваш заказ под номером {order_id} завершён.",
                message_is_read=False
            )
            bot.send_message(
                message.chat.id,
                "Заказ успешно завершён.",
            )
    except Order.DoesNotExist:
        bot.send_message(
            message.chat.id,
            "Заказа с таким номером не существует.",
        )


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(5)


# TODO
# 1) сообщения между пользователями требуют в моделе `Conversation` поля `order` = `id` из модели `Order`
# 2) функция оплаты - пока что шаблон.
# 3) requirements.txt не доделаны
