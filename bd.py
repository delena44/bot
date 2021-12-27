# Импортируем в программу модуль sqlite3
import sqlite3
# С помощью метода connect() выполняем подключение к базе данных
def connect():
    try:
        con = sqlite3.connect("users.db")
# С помощью объекта соединения создается объект cursor, который позволяет выполнять SQLite-запросы
        cursor = con.cursor()
#  Начинаем работу с базой данных, создаем таблицу subscribes (наши подписки), а так же создаем связи с другими таблицами
        cursor.execute("""CREATE TABLE IF NOT EXISTS subscribes(
                user_id int,
                category_id int,
                FOREIGN KEY (user_id) REFERENCES users (ID),  
                FOREIGN KEY (category_id) REFERENCES category (ID),
                primary key(user_id, category_id));""")
        con.commit()
# Затем создаем таблицу users, где будут все наши пользователи, которые зарегистрировались  
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL, 
                name TEXT NOT NULL,
                password TEXT NOT NULL);""")
        con.commit()
# Так же создаем таблицу category, где будут перечислены наши категории (музыка, спорт и т.д.)
        cursor.execute("""CREATE TABLE IF NOT EXISTS category(
                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL);""")
        con.commit()
# Если происходит успешная работа с базой данных то выводим
        print("Вы успешно подключились")
# Выводим сообщение об ошибке
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
# Закрываем наше соединение с базой
    finally:
        con.close()
        print("Соединение с SQLite закрыто")
  
  # Метод, с помощью которого мы передаем category.name в таблицу subscribes
def news(user_id):
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()
                info = cursor.execute(""" SELECT category.name FROM subscribes        
                                        INNER JOIN category ON subscribes.category_id = category.ID
                                        where user_id = ?
                                        """, (user_id,)).fetchall()

                return info
                        
        except sqlite3.Error as err:
                print(err)
                return "false"
        finally:
                con.close()

# Метод, с помощью которого происходит регистрация пользователя. Все данные записываются в базу данных.
def register(user_id, login, password):
        print("Регистрация")
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()
                cursor.execute(""" INSERT INTO users(user_id, name, password) VALUES (?, ?, ?);                 """, (user_id, login, password))
                con.commit()
                print("Вы зарегистрированы")
                return "Вы зарегистрированы :)"       
        except:
                print ('Ошибка при регистрации')
        finally:
                con.close()
                

# Метод аутентификации пользователя. Происходит поиск в базе данных. Есть ли у нас такой пользователь или нет.
# Если есть, то выводится сообщение, что пользователь зашел в систему.
def auth(user_id, password):
        print("Вход в систему")
        con = sqlite3.connect("users.db")
        cursor = con.cursor()
        info = cursor.execute("""SELECT * FROM users WHERE user_id = ? AND password = ?""",                               (user_id, password,)).fetchall()
        print("Вы вошли в систему :)")

# Метод, позволяющий посмотреть в бд, есть ли такой пользователь.
def tabUser(user_id):
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()
                user = cursor.execute("""SELECT user_id FROM users where user_id = ?""",                        (user_id,)).fetchone()
                print(user)
                if not user:
                        return 0
                else:
                        return 1
                
        except:
                print ('Не могу достать пароль :(')
                return 'Что-то пошло не так'
        finally:
                con.close()

def tabSub(user_id, category_id):
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()

                subscrs = cursor.execute(""" SELECT * FROM subscribes 
                                        where user_id = ? and
                                         category_id=?""", (user_id,category_id)).fetchone()

                if subscrs == None:
                        return 0
                else:
                        return 1

        except sqlite3.Error as err:
                print(err)
                return "false"
        finally:
                con.close()

# Метод, с помощью которого происходит подписка на определенную категорию
def addSub(user_id, category_id):
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()

                catName = cursor.execute("""SELECT name FROM category where ID = ? """, (category_id,)).fetchall()
                print(catName[0][0])

                subscrs = cursor.execute(""" SELECT * FROM subscribes 
                                        where user_id = ? and
                                         category_id=?""", (user_id,category_id)).fetchone()

                if subscrs == None:
                        info = cursor.execute(""" INSERT INTO subscribes (user_id, category_id) values (?, ?)""", (user_id,category_id,))
                        con.commit()
                        print(f"Вы подписались на категорию {catName[0][0]}")
                        return catName[0][0]
                else:
                        print(f"Вы уже подписаны на категорию {catName[0][0]}")
                        return catName[0][0]

        except sqlite3.Error as err:
                print(err)
                return "false"
        finally:
                con.close()

# Метод, с помощью которого происходит отписка на определенную категорию
def deleteSub(user_id, category_id):
        try:
                con = sqlite3.connect("users.db")
                cursor = con.cursor()

                catName = cursor.execute("""SELECT name FROM category where ID = ? """, (category_id,)).fetchall()

                subscrs = cursor.execute(""" SELECT category_id FROM subscribes 
                                        where user_id = ? and
                                        category_id=?""", (user_id,category_id,)).fetchone()

                if not subscrs:
                        print(f"Вы не подписаны на категорию {catName[0][0]}")
                        return catName[0][0]
                else:
                        deleteSub = cursor.execute(""" DELETE FROM subscribes 
                                        where category_id = ?""", (category_id,))
                        con.commit()
                        
                        print(f"Вы отписались от категории {catName[0][0]}")
                        return catName[0][0]
                
        except sqlite3.Error as err:
                print(err)
                return "false"
        finally:
                con.close()

try:
        con = sqlite3.connect("users.db")
        cursor = con.cursor()

except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

finally:
        con.close()