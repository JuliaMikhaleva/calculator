# Использую библиотеку pyTelegramBotAPI (установила с помощью pip3)
# Познакомилась с документацией на https://github.com/eternnoir/pyTelegramBotAPI
import telebot

# Types дает кнопочки
from telebot import types
# В этом файле я спрятала свой токен, который получила от BotFather
from secret import TOKEN

# Подключаюсь к созданному боту
bot = telebot.TeleBot(TOKEN, parse_mode=None)


# Здесь буду хранить информацию о пользователе
class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.first_name = None
        self.last_name = None
        self.department = None
        self.training_day = None

    def is_registered(self):
        # Проверяю, что ребенок уже был записан
        # Ввод фамилии является последним этапом при записи ребенка
        return self.last_name is not None


# Создаю структуру для поиска информации о пользователе по user_id
my_clients = dict()


# Создаю карточку для новых пользователей
def user_registration(user_id):
    if user_id not in my_clients:
        my_clients[user_id] = User(user_id)


# Прописываю стартовое сообщение и возможные опции в виде кнопочек
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Нахожу куда отправлять ответное сообщение
    chat_id = message.chat.id
    # Нахожу пользователя
    user_id = message.from_user.id
    # Регистрирую пользователя в системе
    user_registration(user_id)
    # Место для хранения кнопочек по одной в ряд
    # Нашла здесь https://github.com/eternnoir/pyTelegramBotAPI#reply-markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    # Создаю сами кнопочки
    itembtns = list()
    if my_clients[user_id].is_registered():
        itembtns.append("Ваш ребенок уже записан!")
    else:
        itembtns.append("Записать ребенка на пробное занятие")
    itembtns += [
        "Получить дополнительную информацию"
    ]
    # Добавляю их в выделенную выше структуру
    markup.add(*itembtns)
    # Отправляю стартовое сообщение и прикрепляю структуру с кнопочками
    bot.send_message(chat_id, "Здраствуйте, чем я могу Вам помочь?", reply_markup=markup)


@bot.message_handler(regexp="Получить дополнительную информацию")
def additional_info(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    itembtns = [
        types.KeyboardButton("Узнать расписание"),
        types.KeyboardButton("Узнать стоимость"),
        types.KeyboardButton("Узнать адрес"),
    ]
    markup.add(*itembtns)
    # Добавляю к сообщению палец вниз для мотивации нажатия на кнопочки
    bot.send_message(chat_id, "Выберите один из вариантов ниже \U0001F447", reply_markup=markup)


@bot.message_handler(regexp="Записать ребенка на пробное занятие")
def registration_training(message):
    # Запускаю поэтапную запись на занятие
    send_choose_department(message)


def send_choose_department(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
    itembtns = [
        types.KeyboardButton("Филиал ЦСКА"),
        types.KeyboardButton("Филиал Электрозаводская"),
    ]
    markup.add(*itembtns)
    bot.send_message(chat_id, "Выберите интересующий вас филиал", reply_markup=markup)
    # Выбираю функцию для обработки следующего сообщения
    bot.register_next_step_handler(message, training_choose_date)


def training_choose_date(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    # Записываю филиал в карточку пользователя
    my_clients[user_id].department = message.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
    if "ЦСКА" in message.text:
        itembtns = [
            types.KeyboardButton("Среда"),
            types.KeyboardButton("Пятница"),
        ]
    else:
        itembtns = [
            types.KeyboardButton("Вторник"),
            types.KeyboardButton("Четверг"),
        ]
    markup.add(*itembtns)
    bot.send_message(chat_id, "Выберите день недели", reply_markup=markup)
    bot.register_next_step_handler(message, enter_personal_info)


def enter_personal_info(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    my_clients[user_id].training_day = message.text
    bot.send_message(chat_id, "Введите имя ребенка")
    bot.register_next_step_handler(message, enter_surname)


def enter_surname(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    my_clients[user_id].first_name = message.text
    bot.send_message(chat_id, "Введите фамилию ребенка")
    bot.register_next_step_handler(message, enter_success)


def enter_success(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    my_clients[user_id].last_name = message.text
    bot.send_message(chat_id, "Ребенок записан!")


# Обрабатываю "Узнать расписание"
@bot.message_handler(regexp="Узнать расписание")
def send_timetable(message):
    chat_id = message.chat.id
    message = """
На ЦСКА занятия проходят по средам и пятницам с 19:00 до 20:00"
На Электрозаводской занятия проходят по вторникам и четвергам с 18:00 до 19:00
"""
    bot.send_message(chat_id, message)


# Запускаю бота на обработку поступающих запросов
bot.polling()
