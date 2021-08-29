import random
import string
import json
import requests
from os import system
from bson.json_util import dumps, loads
from bson import json_util
import socket
from datetime import datetime# реализовать всё для клиента добавление удаление заказов, просмотр услуг, скидок, заказов, чатов и тд
import re
import win32event
import win32api
from winerror import ERROR_ALREADY_EXISTS
from sys import exit
global URL

URL = 'http://127.0.0.1:5000'

def print_messages(messages):
    print("="*45)
    for message in messages:
        time = str(message["Time"])[0:10] + " " + str(message["Time"])[11:19]
        if message["FilePath"] == "":
            print("Время: %s\nТекст: %s\nОтправитель: %s\n" %(time, message["Text"], message["Person"]))
        else:
            print("Время: %s\nТекст: %s\nОтправитель: %s\nФото: %s\n" % (time, message["Text"], message["Person"], message["FilePath"]))

def print_animals(animals):
    print("="*45)
    for animal in animals:
        typean = animal["AnimalTypes"]
        if animal["Sex"] == 0:
            animalsex = "Мужской"
        else:
            animalsex = "Женский"
        print("ID животного: %s\nКличка: %s\nТип животного: %s\nПол: %s\nКомментарий: %s\nДата рождения: %s\n" % (animal["_id"], animal["Name"], typean["NameIfType"], animalsex, animal["Comment"], animal["Birthday"]))

def print_animals_in_hotel(animals):
    print("="*45)
    for animal in animals:
        typean = animal["AnimalTypes"]
        if animal["Sex"] == 0:
            animalsex = "Мужской"
        else:
            animalsex = "Женский"
        print("ID животного: %s\nКличка: %s\nТип животного: %s\nПол: %s\nКомментарий: %s\nДата рождения: %s\n" % (animal['_id'], animal['Name'], typean["NameIfType"], animalsex, animal['Comment'], animal['Birthday']))

def print_journals(journals):
    for journal in journals:
        data = str(journal["TimeStart"])[0:10]
        timestart = str(journal["TimeStart"])[11:19]
        timeend = str(journal["TimeEnd"])[11:19]
        print("ID журнала: %s\nДата: %s\nВремя начала: %s\nВремя конца: %s\nID заказа: %s\nID животного: %s\nКличка животного: %s\nID работника: %s\nПоручение: %s\nКомментарий: %s\nФото: %s\n" % (
            journal["_id"], data, timestart, timeend, journal["OrderID"], journal["AnimalID"], journal["AnimalName"], journal["WorkerID"], journal["Task"], journal["Comment"], journal["Filepath"]))

def print_orders(orders):
    print("="*45)
    for order in orders:
        datestart = str(order["DateStart"])[0:10]
        dateend = str(order["DateEnd"])[0:10]
        if (int(order["DeliveryToTheHotel"]) == 1) & (int(order["DeliveryFromHotel"]) == 1):
            print("ID заказа: %s\nЦена: %s\nID животного: %s\nДата заезда: %s\nДата выезда: %s\nДоставка до отеля: %s\nДоставка из отеля: %s\nАдрес доставки до отеля: %s\nАдрес доставки из отеля: %s\nВремя доставки до отеля: %s\nВремя доставки из отеля: %s\nКомментарий: %s\nСтатус: %s\n" % (
                order["_id"], order["Price"], order["AnimalID"], datestart, dateend, order["DeliveryToTheHotel"], order["DeliveryFromHotel"], order["FromDeliveryAddress"], order["ToDeliveryAddress"], order["FromDeliveryTime"], order["ToDeliveryTime"], order["Comment"], order["Status"]))
        if (int(order["DeliveryToTheHotel"]) == 0) & (int(order["DeliveryFromHotel"]) == 0):
            print("ID заказа: %s\nЦена: %s\nID животного: %s\nДата заезда: %s\nДата выезда: %s\nКомментарий: %s\nСтатус: %s\n" % (
                order["_id"], order["Price"], order["AnimalID"], datestart, dateend, order["Comment"], order["Status"]))
        if (int(order["DeliveryToTheHotel"]) == 1) & (int(order["DeliveryFromHotel"]) == 0):
            print("ID заказа: %s\nЦена: %s\nID животного: %s\nДата заезда: %s\nДата выезда: %s\nДоставка до отеля: %s\nАдрес доставки до отеля: %s\nВремя доставки до отеля: %s\nКомментарий: %s\nСтатус: %s\n" % (
                order["_id"], order["Price"], order["AnimalID"], datestart, dateend, order["DeliveryToTheHotel"], order["FromDeliveryAddress"], order["FromDeliveryTime"], order["Comment"], order["Status"]))
        if (int(order["DeliveryToTheHotel"]) == 0) & (int(order["DeliveryFromHotel"]) == 1):
            print("ID заказа: %s\nЦена: %s\nID животного: %s\nДата заезда: %s\nДата выезда: %s\nДоставка из отеля: %s\nАдрес доставки из отеля: %s\nВремя доставки из отеля: %s\nКомментарий: %s\nСтатус: %s\n" % (
                order["_id"], order["Price"], order["AnimalID"], datestart, dateend,  order["DeliveryFromHotel"], order["ToDeliveryAddress"], order["ToDeliveryTime"], order["Comment"], order["Status"]))

def print_reviews(reviews):
    print("="*45)
    for review in reviews:
        animaltypes = review["AnimalTypes"]
        time = str(review["AddTime"])[0:10] + " " + str(review["AddTime"])[11:19]
        # time = datetime.strptime(review["AddTime"],"%Y-%m-%d %I:%M")
        print("ID отзыва: %s\nТекст: %s\nТип животного: %s\nВремя добавления: %s\n" % (review["_id"], review["Body"], animaltypes["NameIfType"], time))

def print_account(account):
    for acc in account:
        print("ID: %s\nФИО: %s\nТелефон: %s\nE-mail: %s\nДата рождения: %s\n" %(acc["_id"], acc["Name"], acc["Phone"], acc["Email"], acc["Birthday"]))
def print_account_worker(acc):
        print("ID: %s\nФИО: %s\nТелефон: %s\nE-mail: %s\nДата рождения: %s\n" %(acc["_id"], acc["Name"], acc["Phone"], acc["Email"], acc["Birthday"]))
def start_client():  # Основная функция, запускающая клиента. Эта функция вызывается в конце файла, после определения всех нужных деталей

    token = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16)) 
    isauth = 0
    print("Подключились к серверу")
    while True:
        print("Главное меню:")
        print("1 - Авторизоваться")
        print("2 - Зарегистрироваться")
        print("3 - Посмотреть отзывы")
        print("4 - Выйти из программмы")
        if isauth == 1:
            print("5 - Просмотреть список животных")
            print("6 - Добавить заказ")
            print("7 - Добавить животное")
            print("8 - Добавить отзыв")
            print("9 - Смотреть свой профиль")
            print("10 - Выйти из профиля")
            print("11 - Просмотреть журнал")
            print("12 - Смена пароля")
            print("13 - Посмотреть заказы")
            print("14 - Отправить сообщение в чат")
            print("15 - Смотреть чат")
            print("16 - Смотреть список животных в отеле")
            print("17 - Смотреть информацию о работнике")
        task = input()
        if not task.isdigit() or int(task) > 18:
            print("Неправильная команда!")
            continue
        task = int(task)
        msg = {}
        if task == 1 and isauth == 0:
            url = URL + '/authorization'
            msg = {}
            msg["Login"] = str(input("Введите логин:"))
            msg["Password"] = str(input("Введите пароль:"))
            response = requests.post(url, data=msg)
            if response.text == "Ошибка авторизации.":
                print("Неправильный логин или пароль")
            elif response.text == "Ошибка получения данных.":
                print("Ошибка получения данных.")
            else: 
                token = response.text
                isauth = 1
                print("Вы авторизовались")
        if task == 2:
            url = URL + '/add_person'
            response = requests.get(url)
            person = {}
            person["Login"] = str(input("Введите логин:\n"))
            person["Password"] = str(input("Введите пароль:\n"))
            person["Name"] = str(input("Введите ФИО:\n"))
            person["Phone"] = str(input("Введите телефон:\n"))
            person["Email"] = str(input("Введите e-mail:\n"))
            person["Birthday"] = str(input("Введите дату рождения:\n"))
            person["Address"] = str(input("Введите адрес:\n"))
            response = requests.post(url, data=person)
            if response.text == "Ошибка доступа. Время сессии истекло.":
                print("Время сессии истекло. Пожалуйста, авторизуйтесь заново.")
            else:
                print(response.text)
        if task == 3:
            url = URL + '/read_reviews'
            response = requests.get(url)
            reviews = loads(response.text)
            print_reviews(reviews)
        if task == 4:
            exit(0)
        if task == 5 and isauth == 1:
            url = URL + '/read_animals'
            response = requests.get(url, headers={'Token':str(token)})
            if response.text == "Ошибка доступа. Время сессии истекло.":
                print("Время сессии истекло. Пожалуйста, авторизуйтесь заново.")
            else:
                animals = loads(response.text)
                print_animals(animals)
        if task == 6 and isauth == 1:
            url = URL + '/add_order'
            order = {}
            order["AnimalID"] = int(input("Введите ID животного:"))
            orderdatestart = str(input("Введите дату заезда в отель в формате\nгггг-мм-дд: "))
            while re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', orderdatestart) == []:
                orderdatestart = str(input("Неправильный формат! Введите дату заезда в отель в формате\nгггг-мм-дд: "))
            order["DateStart"] = orderdatestart
            orderdateend = str(input("Введите дату отъезда из отеля в формате\nгггг-мм-дд: "))
            while re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', orderdateend) == []:
                orderdateend = str(input("Неправильный формат! Введите дату заезда в отель в формате\nгггг-мм-дд: "))
            order["DateEnd"] = orderdateend
            order["DeliveryToTheHotel"] = int(input("Вы согласны на доставку животного до отеля: 0-нет, 1-да "))
            if order["DeliveryToTheHotel"] == 1:
                order["FromDeliveryAddress"] = str(input("Введите адрес, откуда мы сможем забрать вашего питомца: "))
                order["FromDeliveryTime"] = str(input("Во сколько мы можем забрать вашего питомца: "))
            else:
                order["FromDeliveryAddress"] = ""
                order["FromDeliveryTime"] = ""
            order["DeliveryFromHotel"] = int(input("Вы согласны на доставку животного из отеля к вам: 0-нет, 1-да "))
            if order["DeliveryFromHotel"] == 1:
                order["ToDeliveryAddress"] = str(input("Введите адрес, куда мы можем привезти вашего питомца: "))
                order["ToDeliveryTime"] = str(input("Во сколько мы можем привезти вашего питомца: "))
            else:
                order["ToDeliveryAddress"] = ""
                order["ToDeliveryTime"] = ""
            order["Comment"] = str(input("Введите комментарий к заказу: "))
            response = requests.post(url, headers={'Token':str(token)},  data=order)
            if response.text == "Ошибка доступа. Время сессии истекло.":
                print("Время сессии истекло. Пожалуйста, авторизуйтесь заново.")
            else:
                print(response.text)
        if task == 7 and isauth == 1:
            url = URL + '/add_animal' 
            animal = {}
            # animal["Token"] = token
            animal['Name'] = str(input("Введите кличку животного:\n"))
            animal['AnimalTypeID'] = int(input("Введите тип животного: 1-кошка, 2-собака, 3-попугай\n"))
            animal['Sex'] = int(input("Введите пол животного: 0-мужской, 1-женский\n"))
            animal['Comment'] = str(input("Введите комментарий:\n"))
            animal['Birthday'] = str(input("Введите дату рождения:\n"))
            # response = requests.post(url, data=animal)
            response = requests.post(url, headers={'Token':str(token)},  data=animal)
            if response.text == "Ошибка доступа. Время сессии истекло.":
                print("Время сессии истекло. Пожалуйста, авторизуйтесь заново.")
            else:
                print(response.text) 
        if task == 8 and isauth == 1:
            url = URL + '/add_review'
            review = {}
            review["AnimalTypeID"] = int(input("Введите тип животного: 1-кошка\n2-собака\n3-попугай\n"))  # animaltype
            review["Body"] = str(input("Введите текст отзыва:\n"))
            response = requests.post(url, headers={'Token':str(token)},  data=review)
            response = requests.post(url, data=review)
            if response.text == "Ошибка доступа. Время сессии истекло.":
                print("Время сессии истекло. Пожалуйста, авторизуйтесь заново.")
            else:
                print(response.text)
        if task == 9 and isauth == 1:
            url = URL + '/look_account'
            response = requests.get(url, headers={'Token':str(token)})
            if response.text == "Ошибка доступа. Время сессии истекло.":
                print("Время сессии истекло. Пожалуйста, авторизуйтесь заново.")
            else:
                acc = loads(response.text)
                print_account(acc)
        if task == 10 and isauth == 1:
            url = URL + '/logout'
            response = requests.post(url, headers={'Token':str(token)})
            isauth = 0
            print(response.text)
        if task == 11 and isauth == 1:
            url = URL + '/read_journals'
            AnimalID = str(input("Введите ID животного:\n"))
            response = requests.get(url, headers={'Token':str(token), 'AnimalID':AnimalID})
            if response.text == "Ошибка доступа. Время сессии истекло.":
                print("Время сессии истекло. Пожалуйста, авторизуйтесь заново.")
            elif response.text=="":
                print ("Неправильный ID животного")
            else:
                journals = loads(response.text)
                print_journals(journals)
        if task == 12 and isauth == 1:
            url = URL + '/changepass'
            password = str(input("Введите новый пароль:"))
            msg = {}
            msg["Password"] = password
            response = requests.post(url, headers={'Token':str(token)},  data=msg)
            if response.text == "Ошибка доступа. Время сессии истекло.":
                print("Время сессии истекло. Пожалуйста, авторизуйтесь заново.")
            else:
                print(response.text)
        if task == 13 and isauth == 1:
            orderdatestart = ""
            orderdateend = ""
            orderdatestart = str(input("Введите начальную дату для поиска в формате\nгггг-мм-дд: "))
            if orderdatestart !="":
                while re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', orderdatestart) == []:
                    orderdatestart = str(input("Неправильный формат! Введите начальную дату для поиска в формате\nгггг-мм-дд: "))
            orderdateend = str(input("Введите конечную дату для поиска в формате\nгггг-мм-дд: "))
            if orderdateend !="":
                while re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', orderdateend) == []:
                    orderdateend = str(input("Неправильный формат! Введите конечную дату для поиска в формате\nгггг-мм-дд: "))
            url = URL + '/read_orders'
            response = requests.get(url, headers={'Token':str(token), 'DateStart':orderdatestart, 'DateEnd':orderdateend})
            if response.text == "Ошибка доступа. Время сессии истекло.":
                print("Время сессии истекло. Пожалуйста, авторизуйтесь заново.")
            else:
                orders = loads(response.text)
                print_orders(orders)
        if task == 14 and isauth == 1:
            url = URL + '/add_message'
            msg = {}
            msg["FilePath"] = str(input("Введите путь до файла:"))
            msg["Text"] = str(input("Введите текст сообщения:"))
            if response.text == "Ошибка доступа. Время сессии истекло.":
                print("Время сессии истекло. Пожалуйста, авторизуйтесь заново.")
            else:
                response = requests.post(url, headers={'Token':str(token)},  data=msg)
                print(response.text)
        if task == 15 and isauth == 1:
            DateStart =""
            DateEnd=""
            unread = int(input("Показать непрочитанные сообщения? 0 - нет, 1 - да: "))
            sorting = int(input("Отсортировать сообщения по дате? 0 - нет, 1 - да: "))
            if sorting == 1:
                msgdatestart = str(input("Введите начальную дату для поиска в формате\nгггг-мм-дд-чч-мм : "))
                while re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}', msgdatestart) == []:
                    msgdatestart = input(("Неправильный формат! Введите начальную дату для поиска в формате\nгггг-мм-дд: "))
                DateStart = msgdatestart
                msgdateend = str(input("Введите конечную дату для поиска в формате\nгггг-мм-дд-чч-мм: "))
                while re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}', msgdateend) == []:
                    msgdateend = input(("Неправильный формат! Введите конечную дату для поиска в формате\nгггг-мм-дд-чч-мм: "))
                DateEnd = msgdateend
            url = URL + '/read_messages'
            response = requests.get(url, headers={'Token':str(token), 'DateStart':DateStart, 'DateEnd':DateEnd, 'Unreadmsg':str(unread)})
            if response.text == "Ошибка доступа. Время сессии истекло.":
                print("Время сессии истекло. Пожалуйста, авторизуйтесь заново.")
            else:
                messages = loads(response.text)
                print_messages(messages)
        if task == 16 and isauth == 1:
            url = URL + '/read_animals_in_hotel'
            response = requests.get(url, headers={'Token':str(token)})
            if response.text == "Ошибка доступа. Время сессии истекло.":
                print("Время сессии истекло. Пожалуйста, авторизуйтесь заново.")
            else:
                animals = loads(response.text)
                print_animals(animals)
        if task == 17 and isauth == 1:
            url = URL + '/look_account_worker'
            WorkerID = str(input("Введите ID работника: "))
            response = requests.get(url, headers={'Token':str(token),'WorkerID':WorkerID})
            if response.text == "Ошибка доступа. Время сессии истекло.":
                print("Время сессии истекло. Пожалуйста, авторизуйтесь заново.")
            elif response.text=="":
                print ("Неправильный ID работника")
            elif WorkerID == "":
                account = loads(response.text)
                print_account(account)
            else:
                account = loads(response.text)
                print_account_worker(account)
start_client()  # Запускаем функцию старта клиента. Вызов функции должен быть ниже, чем определение этой функции в файле
