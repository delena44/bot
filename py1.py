# Импортируем в программу модуль telebot. telebot - библиотека для создания бота для телеграмма.
import telebot
from telebot import types
# Импортируем наш файл с базой данных
import bd
# Импортируем наш ключ
from newsapi import NewsApiClient
# Импортируем в программу модуль datetime. Данный модуль предоставляет классы для обработки времени и даты.
import datetime
# Импортируем в программу модуль requests. requests - библиотека python.
import requests
# Запускаем базу данных
bd.connect()

name = ""
password = ""
now = datetime.datetime.now()

# Ключ, который нам выдают при регистрации на сайте api новости
api_key_news='1a92cad925e44342a502e029792c44cf'
newsapi = NewsApiClient(api_key=api_key_news)

# Создаем переменную, в которой будет хранится наш токен.
bot = telebot.TeleBot("5083161259:AAG7ceMBNypx5NOsRpgZkMOOtgnNmfQLHcQ")

# С помощью данных функций наш бот может нас приветствовать.
@bot.message_handler(commands=['start', 'help', 'Привет'])
def send_welcome(message):
        bot.reply_to(message, "Приветик, что ты хочешь посмотреть?\n\nВведи Регистрация, если хочешь зарегистрироваться\nВведи Войти, если хочешь войти в свой кабинет\n")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
        if message.text == "Регистрация":
                bot.send_message(message.chat.id, "Познакомимся? Давай вместе придумаем пароль. Введи свой пароль тут ↓")
                bot.register_next_step_handler(message, register)

        elif(message.text == "Войти"):
                bot.send_message(message.chat.id, "Введите пароль")
                bot.register_next_step_handler(message, auth)

        elif(message.text == "Подписки"):
                bot.send_message(message.chat.id, "Ваши подписки: ")
                answer=news(message)
                bot.send_message(message.chat.id, answer)

        elif(message.text == "Подписаться"):
                add = "Введите цифру, чтобы подписаться на категорию:\n 1 - Развлечения \n 2 - Музыка \n 3 - Спорт \n 4 - Игры \n 5 - Сериалы"

                bot.send_message(message.chat.id, add)
                bot.register_next_step_handler(message, tabSub)

        elif(message.text == "Отписаться"):
                delete = "Введите цифру, чтобы отписаться от категории:\n 1 - Развлечения \n 2 - Музыка \n 3 - Спорт \n 4 - Игры \n 5 - Сериалы"

                bot.send_message(message.chat.id, delete)
                bot.register_next_step_handler(message, deleteSubs)

        elif(message.text == "Новости"):
                showNewses = showNews(message)
                bot.send_message(message.chat.id, showNewses)

# Список наших категорий под цифрами от 1 до 5
def tabSub(message):
        sub = message.text

        if sub == "1":
                answer = addSub(user_id = message.from_user.id, category_id = 1)
                bot.send_message(message.chat.id, answer)

        elif sub == "2":
                answer = addSub(user_id = message.from_user.id, category_id = 2)
                bot.send_message(message.chat.id, answer)

        elif sub == "3":
                answer = addSub(user_id = message.from_user.id, category_id = 3)
                bot.send_message(message.chat.id, answer)

        elif sub == "4":
                answer = addSub(user_id = message.from_user.id, category_id = 4)
                bot.send_message(message.chat.id, answer)

        elif sub == "5":
                answer = addSub(user_id = message.from_user.id, category_id = 5)
                bot.send_message(message.chat.id, answer)

# Удаление наших категорий от 1 до 5
def deleteSubs(message):
        sub = message.text

        if sub == "1":
                answer = deleteSub(user_id = message.from_user.id, category_id = 1)
                bot.send_message(message.chat.id, answer)

        elif sub == "2":
                answer = deleteSub(user_id = message.from_user.id, category_id = 2)
                bot.send_message(message.chat.id, answer)

        elif sub == "3":
                answer=  deleteSub(user_id = message.from_user.id, category_id = 3)
                bot.send_message(message.chat.id, answer)

        elif sub == "4":
                answer = deleteSub(user_id = message.from_user.id, category_id = 4)
                bot.send_message(message.chat.id, answer)

        elif sub == "5":
                answer=deleteSub(user_id = message.from_user.id, category_id = 5)
                bot.send_message(message.chat.id, answer)

# Происходит регистрация в нашем телеграм боте
def register(message):
        password = message.text

        data={
                'user_id': message.from_user.id,
                'name' : f'{message.from_user.first_name}',
                'password' : password,
        }

        response = requests.post('http://127.0.0.1:5007/register', data)

        if response.status_code == 200:
                bot.send_message(message.chat.id, "Вы уже регистрировались")
        elif response.status_code == 201:
                bot.send_message(message.chat.id, "Регистрация прошла успешно")


# Происходит авторизация в нашем телеграм боте
def auth(message):
        password = message.text

        response = requests.post('http://127.0.0.1:5007/auth', data={
                'user_id': message.from_user.id,
                'password' : password,
        })

        if response.status_code == 200:
                bot.send_message(message.chat.id, "Вы вошли в систему")
        elif response.status_code == 201:
                bot.send_message(message.chat.id, "Пароль введен неверно")


# Смотрим наши новости
def news(message):

        user_id = message.from_user.id

        response = requests.post('http://127.0.0.1:5007/subscrs', data={
                'user_id': user_id,
        })

        if response.status_code == 200:
                news = response.json()
                return news

# Подписываемся на новую категорию
def addSub(user_id, category_id):
        response = requests.post('http://127.0.0.1:5007/addSub', data={
                'user_id': user_id,
                'category_id': category_id
        })

        if response.status_code == 200:
                msg = response.json()
                return msg
        elif response.status_code == 201:
                msg = response.json()
                return msg

# Отписываемся от категории
def deleteSub(user_id, category_id):
        response = requests.post('http://127.0.0.1:5007/deleteSub', data={
                'user_id': user_id,
                'category_id': category_id
        })

        if response.status_code == 200:
                msg = response.json()
                return msg
        elif response.status_code == 201:
                msg = response.json()
                return msg

# Смотрим все наши новости
def showNews(message):
        user_id = message.from_user.id

        response = requests.post('http://127.0.0.1:5007/showNews', data={
                'user_id': user_id,
        })

        if response.status_code == 200:
                news = response.json()
                res = ""
                for new in news:
                        res += new+'\n'

                print(res)
                return res

if __name__ == "__main__":
        bot.polling()