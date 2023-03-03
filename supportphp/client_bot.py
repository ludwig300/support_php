import logging
import time

import telebot
from environs import Env

# Настройки логирования
logging.basicConfig(filename='bot.log', level=logging.INFO)

env = Env()
env.read_env(override=True)
bot = telebot.TeleBot(env.str("TG_TOKEN"))

# Словарь для хранения сообщений от пользователей
user_messages = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Отправляем сообщение приветствия и кнопки
    bot.send_message(
        message.chat.id,
        'Добро пожаловать! Для начала работы, оплатите подписку.',
        reply_markup=get_main_keyboard()
    )
    print('ID:', message.from_user.id)
    print('Name:', message.from_user.first_name, message.from_user.last_name)
    print('Username:', message.from_user.username)


def get_main_keyboard():
    # Создаем клавиатуру с основными действиями пользователя
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Оплатить подписку'))
    return keyboard


@bot.message_handler(func=lambda message: message.text == 'Оплатить подписку')
def check_subscription(message):
    # Отправляем сообщение о способе оплаты
    bot.send_message(
        message.chat.id,
        'Выберите способ оплаты',
        reply_markup=get_check_subscription_keyboard()
    )


def get_check_subscription_keyboard():
    # Создаем клавиатуру с кнопками выбора оплаты
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Bitcoin'))
    keyboard.add(telebot.types.KeyboardButton('Рубли СБЕР'))
    return keyboard


@bot.message_handler(func=lambda message: message.text == 'Bitcoin')
def get_btc_bill(message):
    # Отправляем сообщение с реквизитами и кнопками
    bot.send_message(
        message.chat.id,
        'Оплатите 0.026 btc на счет 1GSMZJT6kED5WGt6AnqapVt4dq7N2shbEr в течении 30 минут',
        reply_markup=check_payment_keyboard()
    )


@bot.message_handler(func=lambda message: message.text == 'Рубли СБЕР')
def get_sber_bill(message):
    # Отправляем сообщение с реквизитами и кнопками
    bot.send_message(
        message.chat.id,
        'Оплатите 47000р на номер карты 4000 4774 7438 6478',
        reply_markup=check_payment_keyboard()
    )


def check_payment_keyboard():
    # Создаем клавиатуру с кнопками для бота
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Проверить оплату'))
    return keyboard


@bot.message_handler(func=lambda message: message.text == 'Проверить оплату')
def show_bot_menu(message):
    # Отправляем сообщение с меню бота и кнопками
    bot.send_message(
        message.chat.id,
        'Вы получили доступ к чат-боту, где можете оставлять заявки.',
        reply_markup=get_bot_menu_keyboard()
    )


def get_bot_menu_keyboard():
    # Создаем клавиатуру с кнопками для бота
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Оставить заявку'))
    keyboard.add(telebot.types.KeyboardButton('Проверка статуса заявки'))
    return keyboard


@bot.message_handler(func=lambda message: message.text == 'Оставить заявку')
def show_support_examples(message):
    # Отправляем сообщение с примерами заявок и кнопками
    bot.send_message(
        message.chat.id,
        'Чтобы оставить заявку, вам необходимо заполнить форму. Вот несколько примеров: Тут нужен шаблон',
        reply_markup=get_help_request_status_keyboard()
    )
    # устанавливаем следующий обработчик на ответ с текстом заявки
    bot.register_next_step_handler(message, process_request)


# обработчик введенного текста заявки
def process_request(message):
    # выводим текст заявки в консоль
    print("Получена заявка: {}".format(message.text))
    # отправляем сообщение с подтверждением получения заявки
    bot.send_message(chat_id=message.chat.id, text="Заявка получена. Спасибо!", reply_markup=get_help_request_form_keyboard())


@bot.message_handler(
    func=lambda message: message.text == 'Проверка статуса заявки'
)
def show_help_request(message):
    # Отправляем сообщение о том, что пользователь хочет получить помощь по заявке и кнопки
    bot.send_message(
        message.chat.id,
        'Ваша заявка в работе. Подрядчик %name%. Срок исполнения %hours%.',
        reply_markup=get_help_request_keyboard()
    )


def get_help_request_keyboard():
    # Создаем клавиатуру с кнопками для помощи по заявке
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Получить статус заявки'))
    return keyboard


@bot.message_handler(func=lambda message: message.text == 'Отправить заявку')
def send_help_request(message):
    # Отправляем сообщение о том, что пользователь хочет отправить заявку и кнопки
    bot.send_message(
        message.chat.id,
        'Заявка отправлена',
        reply_markup=get_help_request_form_keyboard()
    )


def get_help_request_form_keyboard():
    # Создаем клавиатуру с кнопками для формы заявки на помощь
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Задать дополнительный вопрос'))
    return keyboard


@bot.message_handler(
        func=lambda message: message.text == 'Задать дополнительный вопрос'
    )
def ask_extra_question(message):
    # Отправляем сообщение с примерами заявок и кнопками
    bot.send_message(
        message.chat.id,
        'Отправьте в чат все дополнительные вопросы одним сообщением.',
        reply_markup=get_help_request_status_keyboard()
    )
    # устанавливаем следующий обработчик на ответ с текстом заявки
    bot.register_next_step_handler(message, extra_question_request)


# обработчик введенного текста заявки
def extra_question_request(message):
    # выводим текст заявки в консоль
    print("Дополнительные вопросы от клиента: {}".format(message.text))
    # отправляем сообщение с подтверждением получения заявки
    bot.send_message(
        chat_id=message.chat.id,
        text="Ваш вопрос передан. Спасибо!",
        reply_markup=get_help_request_form_keyboard()
    )


@bot.message_handler(
    func=lambda message: message.text == 'Получить статус заявки'
)
def get_help_request_status(message):
    # Отправляем сообщение о том, что пользователь хочет получить статус заявки и кнопки
    bot.send_message(
        message.chat.id,
        'Вы хотите получить статус заявки. Пожалуйста, введите номер заявки:',
        reply_markup=get_help_request_status_keyboard()
    )


def get_help_request_status_keyboard():
    # Создаем клавиатуру с кнопкой "Отмена"
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Отмена'))
    return keyboard


@bot.message_handler(func=lambda message: message.text == 'Отмена')
def cancel_help_request_status(message):
    # Отправляем сообщение о том, что пользователь отменил запрос статуса заявки и кнопки
    bot.send_message(
        message.chat.id,
        'Вы отменили запрос статуса заявки.',
        reply_markup=get_help_request_keyboard()
    )


@bot.message_handler(
    func=lambda message: message.text == 'Получил уточняющие вопросы от подрядчика'
)
def answer_contractor_questions(message):
    # Отправляем сообщение о том, что пользователь получил уточняющие вопросы от подрядчика и кнопки
    bot.send_message(
        message.chat.id,
        'Вы получили уточняющие вопросы от подрядчика. Пожалуйста, ответьте на них:',
        reply_markup=get_answer_questions_keyboard()
    )


def get_answer_questions_keyboard():
    # Создаем клавиатуру с кнопкой "Ответить"
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Ответить'))
    return keyboard


@bot.message_handler(
    func=lambda message: message.text == 'Ответить'
)
def send_contractor_answer(message):
    # Отправляем сообщение о том, что пользователь хочет отправить ответ подрядчику и кнопки
    bot.send_message(
        message.chat.id,
        'Вы отправили ответ на уточняющие вопросы. Ждите ответа от подрядчика.',
        reply_markup=get_wait_contractor_keyboard()
    )


def get_wait_contractor_keyboard():
    # Создаем клавиатуру с кнопкой "Ожидать ответа"
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Ожидать ответа'))
    return keyboard


@bot.message_handler(func=lambda message: message.text == 'Ожидать ответа')
def wait_contractor_answer(message):
    # Отправляем сообщение о том, что пользователь ждет ответа подрядчика и кнопки
    bot.send_message(
        message.chat.id,
        'Вы ждете ответа от подрядчика.',
        reply_markup=get_help_request_keyboard()
    )


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(5)  # Ожидаем 5 секунд, если произошла ошибка, и продолжаем работу
