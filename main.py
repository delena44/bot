# Импортируем в программу модуль flask. flask - веб-фреймворк, который облегачает процесс создания приложений.
from flask import Flask
from flask import request
from flask import jsonify
# Импортируем в программу модуль requests. requests - библиотека python.
import requests
# Импортируем в программу модуль datetime. Данный модуль предоставляет классы для обработки времени и даты.
import datetime
# Имеем дату на данный момент
now = datetime.datetime.now()
# Импортируем наш файл с базой данных
import bd
# Импортируем в программу нового клиента с сайта newsapi. предварительно регистрируемся.
from newsapi import NewsApiClient

# Ключ, который нам выдают при регистрации на сайте api новости
api_key_news='1a92cad925e44342a502e029792c44cf'
newsapi = NewsApiClient(api_key=api_key_news)

app = Flask(__name__)
app.secret_key = "tatsdlglhag"

# Тут начинается работа уже конкретно с ботом. Что будут делать наши команды
# Команда регистрации пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        reg = bd.tabUser(request.form["user_id"])
     
        if reg == 1:
            return jsonify({'is_registered': True}), 200
        else:
            bd.reg(request.form['user_id'],  request.form['name'], request.form['password'])
            return jsonify({'is_registered': True}), 201
    
    except Exception as e:
        print(f"Ошибка: {e}")
       
# Команда авторизации пользователя
@app.route('/auth', methods=['GET','POST'])
def auth():
    try:
        bd.auth(request.form['user_id'], request.form['password'])
        return jsonify({"Вы вошли в систему": True}), 200
    
    except Exception as e:
        print(f"Ошибка: {e}")

# Команда регистрации пользователя
@app.route("/subscrs", methods=["GET", "POST"])
def subscr():
    try:
        subscrs = bd.news(request.form['user_id'])
        abc = ''
        for subscr in subscrs:
            abc+=subscr[0]+' '
        
        print(abc)
        return jsonify(f"{abc}"), 200
    
    except Exception as e:
        print(f"Ошибка: {e}")


# Команда добавления категории, на которую хочет подписаться пользователь.
@app.route("/addSub", methods=["GET", "POST"])
def addSub():
    try:
        tabSub = bd.tabSub(request.form['user_id'], request.form['category_id'])
    
        if tabSub == 0:
            addSub = bd.addSub(request.form['user_id'], request.form['category_id'])
            return jsonify(f"Вы подписались на категорию {addSub}"), 200

        elif tabSub == 1: 
            addSub = bd.addSub(request.form['user_id'], request.form['category_id'])
            return jsonify(f"Вы уже подписаны на категорию {addSub}"), 201
    
    except Exception as e:
        print(f"Ошибка: {e}")


# Команда удаления категории, от которой хочет отписаться пользователь.
@app.route("/deleteSub", methods=["GET", "POST"])
def deeteSub():
    try:
        tabSub = bd.tabSub(request.form['user_id'], request.form['category_id'])
        
        if tabSub == 0:
            deleteSub = bd.deleteSub(request.form['user_id'], request.form['category_id'])
            return jsonify(f"Вы не были подписаны на категорию {deleteSub}"), 200

        else: 
            deleteSub = bd.deleteSub(request.form['user_id'], request.form['category_id'])
            return jsonify(f"Вы отписались от категории {deleteSub}"), 201
    
    except Exception as e:
        print(f"Ошибка: {e}")


# Команда, которая позволяет посмотреть наши новости
@app.route("/showNews", methods=["GET", "POST"])
def showNews():
    try:
        sub = bd.news(request.form['user_id'])
    
        result = []
        list=0
        for subs in sub:
            print(f"Подписки: {subs}")
            url = (f"https://newsapi.org/v2/everything?q={subs}&apiKey={api_key_news}&from={now.date}&sortBy=popularity?&language=ru&totalResults=5&pageSize=5")
            response = requests.get(url)
            response = response.json()
               
            print(f"!!!! {response}")
                
            for i in range(0, len(response)+1):
                title = response['articles'][i]['title']
                href = response['articles'][i]['url']
                list+=1  
                
                if list <=4:  
                    msg = f"{title}\n{href}\n"
                    result.append(msg)

            return jsonify(result), 200
    
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    app.run(host="localhost", port=5007)