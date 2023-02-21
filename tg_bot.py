import telebot
import time
from environs import Env


env = Env()
env.read_env(override=True)
bot = telebot.TeleBot(env.str("TG_TOKEN"))


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Отправляем сообщение приветствия и кнопки
    bot.send_message(
        message.chat.id,
        'Добро пожаловать! Что вы хотите сделать?',
        reply_markup=get_main_keyboard()
    )


def get_main_keyboard():
    # Создаем клавиатуру с основными действиями пользователя
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Оплатить подписку'))
    keyboard.add(telebot.types.KeyboardButton('Недоволен своим сайтом'))
    return keyboard


@bot.message_handler(func=lambda message: message.text == 'Оплатить подписку')
def check_subscription(message):
    # Отправляем сообщение о проверке подписки и кнопки
    bot.send_message(
        message.chat.id,
        'Хотите убедиться, что все в порядке?',
        reply_markup=get_check_subscription_keyboard()
    )


def get_check_subscription_keyboard():
    # Создаем клавиатуру с кнопкой "Да" и "Нет"
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Да'))
    keyboard.add(telebot.types.KeyboardButton('Нет'))
    return keyboard


@bot.message_handler(func=lambda message: message.text == 'Да')
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
    keyboard.add(telebot.types.KeyboardButton('Оставить заявку на доработку'))
    keyboard.add(telebot.types.KeyboardButton('Запросить помощь по заявке'))
    return keyboard


@bot.message_handler(func=lambda message: message.text == 'Нет')
def send_support_request(message):
    # Отправляем сообщение о том, что пользователь хочет получить помощь от PHPSupport и кнопки
    bot.send_message(
        message.chat.id,
        'Вы недовольны своим сайтом. Хотите получить помощь от PHPSupport?',
        reply_markup=get_support_request_keyboard()
    )


def get_support_request_keyboard():
    # Создаем клавиатуру с кнопкой "Да" и "Нет"
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Да'))
    keyboard.add(telebot.types.KeyboardButton('Нет'))
    return keyboard


@bot.message_handler(func=lambda message: message.text == 'Да')
def show_support_examples(message):
    # Отправляем сообщение с примерами заявок и кнопками
    bot.send_message(
        message.chat.id,
        'Чтобы оставить заявку на доработку, вам необходимо заполнить форму. Вот несколько примеров:',
        reply_markup=get_support_examples_keyboard()
    )


def get_support_examples_keyboard():
    # Создаем клавиатуру с кнопками для примеров заявок
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Заявка на добавление функционала')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Заявка на исправление ошибки')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            'Заявка на улучшение производительности'
        )
    )
    return keyboard


@bot.message_handler(
    func=lambda message: message.text == 'Запросить помощь по заявке'
)
def show_help_request(message):
    # Отправляем сообщение о том, что пользователь хочет получить помощь по заявке и кнопки
    bot.send_message(
        message.chat.id,
        'Вы хотите получить помощь по заявке. Что вы хотите сделать?',
        reply_markup=get_help_request_keyboard()
    )


def get_help_request_keyboard():
    # Создаем клавиатуру с кнопками для помощи по заявке
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton('Отправить заявку'))
    keyboard.add(telebot.types.KeyboardButton('Получить статус заявки'))
    return keyboard


@bot.message_handler(func=lambda message: message.text == 'Отправить заявку')
def send_help_request(message):
    # Отправляем сообщение о том, что пользователь хочет отправить заявку и кнопки
    bot.send_message(
        message.chat.id,
        'Вы хотите отправить заявку. Пожалуйста, заполните форму:',
        reply_markup=get_help_request_form_keyboard()
    )


def get_help_request_form_keyboard():
    # Создаем клавиатуру с кнопками для формы заявки на помощь
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('Заполнить форму'))
    return keyboard


@bot.callback_query_handler(func=lambda call: call.data == 'fill_form')
def fill_help_request_form(call):
    # Обрабатываем нажатие на кнопку для заполнения формы заявки
    bot.send_message(call.message.chat.id, 'Форма заявки на помощь')


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
    func=lambda message: message.text == 'Оставить заявку на доработку'
)
def resend_support_request(message):
    # Отправляем сообщение о том, что пользователь хочет оставить заявку на доработку и кнопки
    bot.send_message(
        message.chat.id,
        'Вы хотите оставить заявку на доработку. Пожалуйста, заполните форму:',
        reply_markup=get_support_request_form_keyboard()
    )


def get_support_request_form_keyboard():
    # Создаем клавиатуру с кнопками для формы заявки на доработку
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('Заполнить форму'))
    return keyboard


@bot.callback_query_handler(func=lambda call: call.data == 'fill_form')
def fill_support_request_form(call):
    # Обрабатываем нажатие на кнопку для заполнения формы заявки на доработку
    bot.send_message(call.message.chat.id, 'Форма заявки на доработку')


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


@bot.message_handler(func=lambda message: message.text == 'Ответить')
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
