import random
import string
import datetime
import json  # Подключаем библиотеку для преобразования данных в формат JSON
import socket
import os # Подключаем библиотеку для работы с функциями операционной системы (для проверки файла)
import pymongo
from bson.json_util import dumps, loads
from bson import json_util
import win32event
import win32api
from winerror import ERROR_ALREADY_EXISTS
from sys import exit
import threading
from flask import Flask, request, render_template, flash, redirect, json
from flask_pymongo import PyMongo
import requests
from datetime import timedelta

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/HotelFA"
mongo = PyMongo(app)

def check_token(token):
    if ((len(token)) > 0):
        person = mongo.db["Persons"].find_one({"Token":str(token)})
        if person != None:
            chekingToken = person["Token"]
            if (chekingToken == token) & ((person["DateOfIssueToken"] + timedelta(minutes = 30)) > datetime.datetime.now()):
                return person
    return None

@app.route("/authorization", methods=['POST'])
def authorization():
    add_operation_in_journal('authorization')
    if ("Login" in request.form.keys() and "Password" in request.form.keys()):
        login = request.form["Login"]
        password = request.form["Password"]
        person = mongo.db["Persons"].find_one({"Login":login, "Password":password})
        if person != None:
            print("Попытка авторизоваться прошла успешно")
            token = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
            mongo.db["Persons"].update_one({ '_id': person["_id"] }, { "$set": { 'Token': token, 'DateOfIssueToken': datetime.datetime.now()}}) 
            return token
        else:
            print ("Ошибка авторизации.")
            return ("Ошибка авторизации.")
    else:
        print("Ошибка получения данных.")
        return("Ошибка получения данных.")

@app.route("/read_animals", methods=['GET'])
def read_animals():
    add_operation_in_journal('read_animals')
    if ("Token" in request.headers.keys()):
        token = str(request.headers["Token"])
        person = check_token(token)
        if person != None:
            col = mongo.db["Animals"]
            for x in col.find({"ClientID":person["_id"]}):
                print(x)
            cursor = col.find({"ClientID":person["_id"]})
            content = dumps(cursor)
            return content
        else:
            print("Ошибка доступа. Время сессии истекло.")
            return("Ошибка доступа. Время сессии истекло.")
    else:
        print("Ошибка получения данных.")
        return("Ошибка получения данных.")

@app.route("/read_reviews", methods=['GET'])
def read_reviews():
    add_operation_in_journal('read_reviews')
    col = mongo.db["Reviews"]
    for x in col.find():
        print(x)
    cursor = col.find()
    content = dumps(cursor)
    return content

@app.route("/read_animals_in_hotel", methods=['GET'])
def read_animals_in_hotel():
    add_operation_in_journal('read_animals_in_hotel')
    if ("Token" in request.headers.keys()):
        token = str(request.headers["Token"])
        person = check_token(token)
        if person != None:
            answer = []
            for z in  mongo.db["Orders"].find({"ClientID" : person["_id"], "DateStart": {"$lt": datetime.datetime.now()}, "DateEnd": {"$gte": datetime.datetime.now()}}):
                for y in mongo.db["Animals"].find({"_id" : z["AnimalID"]}):
                    answer.append(y)
                    print(y)
            cursor = answer
            content = dumps(cursor)
            return content
        else:
            print("Ошибка доступа. Время сессии истекло.")
            return "Ошибка доступа. Время сессии истекло."
    else:
        print("Ошибка получения данных.")
        return("Ошибка получения данных.")

@app.route("/read_journals", methods=['GET'])
def read_journal():
    add_operation_in_journal('read_journals')
    if ("Token" in request.headers.keys() and "Animalid" in request.headers.keys()):
        token = str(request.headers["Token"])
        AnimalID = str(request.headers["AnimalID"])
        person = check_token(token)
        if person != None:
            if AnimalID != "":
                answer = []
                if mongo.db["Orders"].find_one({"AnimalID":int(AnimalID)})!= None:
                    for order in mongo.db["Orders"].find({"AnimalID":int(AnimalID)}):
                        for journal in mongo.db["Journals"].find({"OrderID":order["_id"]}):
                            journal["AnimalID"] = mongo.db["Animals"].find_one({"_id": int(AnimalID)})["_id"]
                            journal["AnimalName"] = mongo.db["Animals"].find_one({"_id": int(AnimalID)})["Name"]
                            print(journal)
                            answer.append(journal)
                            cursor = answer
                    content = dumps(cursor)
                    return content
                else:
                    print ('Ошибка, бронирование данного животного не найдено.')
            else:
                person = mongo.db["Persons"].find_one({"Token":token})
                answer = []
                for x in mongo.db["Orders"].find({"ClientID":person["_id"]}):
                    for journal in mongo.db["Journals"].find({"OrderID":x["_id"]}):
                        journal["AnimalID"] = mongo.db["Animals"].find_one({"_id": x["AnimalID"]})["_id"]
                        journal["AnimalName"] = mongo.db["Animals"].find_one({"_id": x["AnimalID"]})["Name"]
                        print(journal)
                        answer.append(journal)
                        cursor = answer
                content = dumps(cursor)
                return content
        else:
            print("Ошибка доступа. Время сессии истекло.")
            return "Ошибка доступа. Время сессии истекло."
    else:
        print("Ошибка получения данных.")
        return("Ошибка получения данных.")

@app.route("/look_account", methods=['GET'])
def look_account():
    add_operation_in_journal('look_account')
    if ("Token" in request.headers.keys()):
        token = str(request.headers["Token"])
        person = check_token(token)
        if person != None:
            print(person)
            cursor = mongo.db["Persons"].find({"Token":token})
            content = dumps(cursor) 
            return content
        else:
            print("Ошибка доступа. Время сессии истекло.")
            return "Ошибка доступа. Время сессии истекло."
    else:
        print("Ошибка получения данных.")
        return("Ошибка получения данных.")

@app.route("/look_account_worker", methods=['GET'])
def look_account_worker():
    add_operation_in_journal('look_account_worker')
    if ("Token" in request.headers.keys() and "Workerid" in request.headers.keys()):
        token = str(request.headers['Token'])
        WorkerID = str(request.headers["WorkerID"])
        person = check_token(token)
        if person != None:
            if WorkerID != "":
                if mongo.db["Persons"].find_one({"_id": int(WorkerID), "State": 0})!= None:
                    print(mongo.db["Persons"].find_one({"_id": int(WorkerID), "State": 0}))
                    cursor = mongo.db["Persons"].find_one({"_id": int(WorkerID), "State": 0})
                    content = dumps(cursor)
                    return content
                else:
                    return ""
            else:
                for x in mongo.db["Persons"].find({"State": 0}):
                    print(x)
                cursor = mongo.db["Persons"].find({"State": 0})
                content = dumps(cursor)
                return content
        else:
            print("Ошибка доступа. Время сессии истекло.")
            return "Ошибка доступа. Время сессии истекло."
    else:
        print("Ошибка получения данных.")
        return("Ошибка получения данных.")

@app.route("/read_orders", methods=['GET'])
def read_orders():
    add_operation_in_journal('read_orders')
    if ("Token" in request.headers.keys() and "Datestart" in request.headers.keys() and "Dateend" in request.headers.keys()):
        token = str(request.headers["Token"])
        stringdatestart = str(request.headers["DateStart"])
        stringdateend = str(request.headers["DateEnd"])
        person = check_token(token)
        if person != None:
            if (stringdatestart != "") & (stringdateend != ""):
                date1 = stringdatestart.split('-')
                date2 = stringdateend.split('-')
                from_date = datetime.datetime(int(date1[0]), int(date1[1]), int(date1[2]))
                to_date = datetime.datetime(int(date2[0]), int(date2[1]), int(date2[2]))
                for x in mongo.db["Orders"].find({"DateStart": {"$gte": from_date, "$lt": to_date}, "DateEnd": {"$gte": from_date, "$lt": to_date}, "ClientID":person["_id"]}):
                    print(x)
                cursor = mongo.db["Orders"].find({"DateStart": {"$gte": from_date, "$lt": to_date}, "DateEnd": {"$gte": from_date, "$lt": to_date}, "ClientID":person["_id"]}) 
            else:
                col = mongo.db["Orders"]
                for x in col.find({"ClientID":person["_id"]}):
                    print(x)
                cursor = col.find({"ClientID":person["_id"]})
            content = dumps(cursor, default = myconverter) 
            return content
        else:
            print("Ошибка доступа. Время сессии истекло.")
            return "Ошибка доступа. Время сессии истекло."
    else:
        print("Ошибка получения данных.")
        return("Ошибка получения данных.")

@app.route("/read_messages", methods=['GET'])
def read_msg():
    add_operation_in_journal('read_messages')
    if ("Token" in request.headers.keys() and "Unreadmsg" in request.headers.keys() and "Datestart" in request.headers.keys() and "Dateend" in request.headers.keys()):
        token = str(request.headers["Token"])
        unread = int(request.headers["Unreadmsg"])#если 1 то показываются не прочитанные сообщения
        stringdatestart = request.headers["DateStart"]
        stringdateend = request.headers["DateEnd"]
        person = check_token(token)
        if person != None:
            messages = mongo.db["ChatMessages"]
            chat = mongo.db["Chats"].find_one({"ClientID":person["_id"]})
            if (unread == 1 and stringdatestart == "" and stringdateend == ""):#непрочитанные смс и нет дат для сортировки
                answer = []
                for msg in messages.find({"Chat._id":chat["_id"] , "Unread":1}):
                    pers = mongo.db["Persons"].find_one({"_id":chat["ClientID"]})
                    msg["Person"] = pers["Name"]
                    print (msg)
                    answer.append(msg)
                cursor = answer
                content = dumps(cursor, default = myconverter)
                messages.update({"Unread" : 1},{"$set": {"Unread" : 0}})
            elif (unread == 1 and stringdatestart != "" and stringdateend != ""):#непрочитанные смс и есть дата для сортировки
                answer = []
                date1 = stringdatestart.split('-')
                date2 = stringdateend.split('-')
                from_date = datetime.datetime(int(date1[0]), int(date1[1]), int(date1[2]), int(date1[3]), int(date1[4]))
                to_date = datetime.datetime(int(date2[0]), int(date2[1]), int(date2[2]), int(date2[3]), int(date2[4]))
                for msg in messages.find({"Time": {"$gte": from_date, "$lt": to_date}, "Chat._id":chat["_id"], "Unread": 1}):
                    pers = mongo.db["Persons"].find_one({"_id":chat["ClientID"]})
                    msg["Person"] = pers["Name"]
                    print (msg)
                    answer.append(msg)
                cursor = answer
                content = dumps(cursor, default = myconverter)
                messages.update( {"Time": {"$gte": from_date, "$lt": to_date}, "Chat._id":chat["_id"],"Unread" : 1} , { "$set": { "Unread" : 0} })
            elif (unread == 0 and stringdatestart != "" and stringdateend != ""):#все смс и есть дата для сортировки
                answer = []
                date1 = stringdatestart.split('-')
                date2 = stringdateend.split('-')
                from_date = datetime.datetime(int(date1[0]), int(date1[1]), int(date1[2]), int(date1[3]), int(date1[4]))
                to_date = datetime.datetime(int(date2[0]), int(date2[1]), int(date2[2]), int(date2[3]), int(date2[4]))
                for msg in messages.find({"Time": {"$gte": from_date, "$lt": to_date}, "Chat._id":chat["_id"]}):
                    pers = mongo.db["Persons"].find_one({"_id":chat["ClientID"]})
                    msg["Person"] = pers["Name"]
                    print(msg)
                    answer.append(msg)
                cursor = answer
                content = dumps(cursor, default = myconverter)
            else:#все смс и нет даты для сортировки
                answer = []
                for msg in messages.find({"Chat._id":chat["_id"]}):
                    pers = mongo.db["Persons"].find_one({"_id":chat["ClientID"]})
                    msg["Person"] = pers["Name"]
                    print(msg)
                    answer.append(msg)
                cursor = answer
                content = dumps(cursor, default = myconverter)
            return content
        else:
            print("Ошибка доступа. Время сессии истекло.")
            return "Ошибка доступа. Время сессии истекло."
    else:
        print("Ошибка получения данных.")
        return("Ошибка получения данных.")

def get_max_id(collection):
    col = mongo.db[collection]
    maxid = 0
    for x in col.find().sort("_id"):
        maxid = x["_id"]
    return maxid
def find_by_id(id, collection):
    col = mongo.db[collection]
    obj = {}
    for x in col.find():
        if x["_id"] == id:
            obj = x
    return obj

@app.route("/add_animal",  methods=['POST'])
def add_animal():
    add_operation_in_journal('add_animal')
    if ("Token" in request.headers.keys() and "AnimalTypeID" in request.form.keys() and "Name" in request.form.keys() and "Sex" in request.form.keys() and "Comment" in request.form.keys() and "Birthday" in request.form.keys()):#  "Comment" in request.form.keys() & "Birthday" in request.form.keys()
        token = str(request.headers["Token"])
        person = check_token(token)
        if person != None:
            AnimalTypeID = int(request.form["AnimalTypeID"])
            newanimal={}
            newanimal["_id"] = (get_max_id("Animals")) + 1
            newanimal["Name"] = request.form["Name"]
            newanimal["AnimalTypes"] = find_by_id(AnimalTypeID, "AnimalTypes")
            newanimal["Sex"] = request.form["Sex"]
            newanimal["Comment"] = request.form["Comment"]
            newanimal["Birthday"] = request.form["Birthday"]
            newanimal["ClientID"] = person["_id"]
            newanimal["DelTime"] = None
            mongo.db["Animals"].insert_one(newanimal)
            return "Животное успешно добавлено."
        else:
            print("Ошибка доступа. Время сессии истекло.")
            return "Ошибка доступа. Время сессии истекло."
    else:
        print("Ошибка получения данных.")
        return("Ошибка получения данных.")

@app.route("/logout", methods=['POST'])
def logout():
    add_operation_in_journal('logout')
    if ("Token" in request.headers.keys()):
        token = str(request.headers["Token"])
        person = check_token(token)
        if person != None:
            mongo.db["Persons"].update_one({ 'Token': token }, { "$set": { 'Token': None, 'DateOfIssueToken': None}})
            print("Выход был произведен успешно!")
            return "Выход был произведен успешно!"
        else:
            print("Ошибка доступа. Время сессии истекло.")
            return("Ошибка доступа. Время сессии истекло.")
    else:
        print("Ошибка получения данных.")
        return("Ошибка получения данных.")

@app.route("/add_person",  methods=['POST'])
def add_person():
    add_operation_in_journal('add_person')
    if ("Login" in request.form.keys() and "Password" in request.form.keys() and "Name" in request.form.keys() and "Phone" in request.form.keys() and "Email" in request.form.keys() and "Birthday" in request.form.keys() and "Address" in request.form.keys()):
        newperson = {}
        newperson["_id"] = (get_max_id("Persons")) + 1
        newperson["Token"] = None
        newperson["DateOfIssueToken"] = None
        newperson["State"] = 1
        newperson["Login"] = request.form["Login"]
        newperson["Password"] = request.form["Password"]
        newperson["Name"] = request.form["Name"]
        newperson["Phone"] = request.form["Phone"]
        newperson["Email"] = request.form["Email"]
        newperson["Birthday"] = request.form["Birthday"]
        newperson["Address"] = request.form["Address"]
        mongo.db["Persons"].insert_one(newperson)
        newchat = {}
        newchat["_id"] = (get_max_id("Chats")) + 1
        newchat["DelTime"] = None
        newchat["ClientID"] = newperson["_id"]
        mongo.db["Chats"].insert_one(newchat)
        return "Пользователь успешно зарегестрирован."
    else:
        print("Ошибка получения данных.")
        return("Ошибка получения данных.")

@app.route("/add_order",  methods=['POST'])
def add_order():
    add_operation_in_journal('add_order')
    if ("Token" in request.headers.keys() and "DateStart" in request.form.keys() and "DateEnd" in request.form.keys() and "AnimalID" in request.form.keys() and "DeliveryToTheHotel" in request.form.keys() and "FromDeliveryAddress" in request.form.keys() and "FromDeliveryTime" in request.form.keys() and "DeliveryFromHotel" in request.form.keys() and "ToDeliveryAddress" in request.form.keys() and "ToDeliveryTime" in request.form.keys() and "Comment" in request.form.keys()):
        token = str(request.headers["Token"])
        person = check_token(token)
        if person != None:
            neworder = {}
            neworder["_id"] = (get_max_id("Orders")) + 1
            neworder["Status"] = "В обработке"
            datest = request.form["DateStart"].split('-')
            dateend = request.form["DateEnd"].split('-')
            neworder["DateStart"] = datetime.datetime(int(datest[0]), int(datest[1]), int(datest[2]))
            neworder["DateEnd"] = datetime.datetime(int(dateend[0]), int(dateend[1]), int(dateend[2]))
            neworder["ClientID"] = person["_id"]
            neworder["AnimalID"] = int(request.form["AnimalID"])
            neworder["DeliveryToTheHotel"] = int(request.form["DeliveryToTheHotel"])
            neworder["FromDeliveryAddress"] = request.form["FromDeliveryAddress"]
            neworder["FromDeliveryTime"] = request.form["FromDeliveryTime"]
            neworder["DeliveryFromHotel"] = int(request.form["DeliveryFromHotel"])
            neworder["ToDeliveryAddress"] = request.form["ToDeliveryAddress"]
            neworder["ToDeliveryTime"] = request.form["ToDeliveryTime"]
            neworder["Comment"] = request.form["Comment"]
            neworder["DelTime"] = None
            neworder["Price"] = 5000
            mongo.db["Orders"].insert_one(neworder)
            return "Заказ успешно добавлен."
        else:
            print("Ошибка доступа. Время сессии истекло.")
            return "Ошибка доступа. Время сессии истекло."
    else:
        print("Ошибка получения данных.")
        return("Ошибка получения данных.")

@app.route("/add_review",  methods=['POST'])
def add_review():
    add_operation_in_journal('add_review')
    if ("Token" in request.headers.keys() and "AnimalTypeID" in request.form.keys() and "Body" in request.form.keys()):
        token = str(request.headers["Token"])
        person = check_token(token)
        if person != None:
            AnimalTypeID = int(request.form['AnimalTypeID'])
            newreview = {}
            newreview["_id"] = (get_max_id("Reviews")) + 1
            newreview["AnimalTypes"] = find_by_id(AnimalTypeID, "AnimalTypes")
            newreview["Body"] = request.form["Body"]
            newreview["AddTime"] = datetime.datetime.now()
            newreview["DelTime"] = None
            newreview["ClientID"] = person["_id"]
            mongo.db["Reviews"].insert_one(newreview)
            return "Отзыв успешно добавлен."
        else:
            print("Ошибка доступа. Время сессии истекло.")
            return "Ошибка доступа. Время сессии истекло."
    else:
        print("Ошибка получения данных.")
        return("Ошибка получения данных.")

@app.route("/add_message", methods=['POST'])
def add_message():
    add_operation_in_journal('add_message')
    if ("Token" in request.headers.keys() and "Text" in request.form.keys() and "FilePath" in request.form.keys()):
        token = str(request.headers["Token"])
        person = check_token(token)
        if person != None:
            newmessage = {}
            col = mongo.db["Chats"]
            for x in col.find({"ClientID":person["_id"]}):
                chat = x
            newmessage["_id"] = (get_max_id("ChatMessages")) + 1
            newmessage["Chat"] = chat
            newmessage["Time"] = datetime.datetime.now()
            newmessage["Text"] = request.form['Text']
            newmessage["FilePath"] = request.form['FilePath']
            newmessage["DelTime"] = None
            newmessage["Unread"] = 1 #непрочитано
            mongo.db["ChatMessages"].insert_one(newmessage)
            return "Сообщение успешно отправлено!"
        else:
            print("Ошибка доступа. Время сессии истекло.")
            return "Ошибка доступа. Время сессии истекло."
    else:
        print("Ошибка получения данных.")
        return("Ошибка получения данных.")

@app.route("/changepass", methods=['POST'])
def changepass():
    add_operation_in_journal('changepass')
    if ("Token" in request.headers.keys() and "Password" in request.form.keys()):
        token = str(request.headers['Token'])
        password = request.form['Password']
        person = check_token(token)
        if person != None:
            mongo.db["Persons"].update_one({ 'Token': token }, { "$set": { 'Password': password}})
            print("Попытка смены пароля прошла успешно")
            return "Ваш пароль был успешно изменён!"
        else:
            print("Ошибка доступа. Время сессии истекло.")
            return "Ошибка доступа. Время сессии истекло."
    else:
        print("Ошибка получения данных.")
        return("Ошибка получения данных.")
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


class FileMutex:
    def __init__(self):
        self.mutexname = "hotelFA_filemutex"

        self.mutex = win32event.CreateMutex(None, 1, self.mutexname)
        self.lasterror = win32api.GetLastError()
    
    def release(self):

        return win32event.ReleaseMutex(self.mutex)

mutex = FileMutex()
mutex.release()

def add_operation_in_journal(opeartion):
    import time
    mutex = FileMutex()
    date=datetime.datetime.now()
    date = str(date)
    row = str(opeartion) + "=====" + str(date) + '\n'
    while True:
        win32event.WaitForSingleObject(mutex.mutex, win32event.INFINITE )
        f = open('journalflask.txt', 'a')
        f.write(row)
        f.close()
        mutex.release()
        return

class singleinstance:
    """ Limits application to single instance """

    def __init__(self):
        self.mutexname = "testmutex_{87c75f97-7a06-47c0-accf-0d139e50328d}" #GUID сгенерирован онлайн генератором
        self.mutex = win32event.CreateMutex(None, False, self.mutexname)
        self.lasterror = win32api.GetLastError()
    
    def aleradyrunning(self):
        return (self.lasterror == ERROR_ALREADY_EXISTS)
        
    def __del__(self):
        if self.mutex:
            win32api.CloseHandle(self.mutex)


from sys import exit
myapp = singleinstance()


if myapp.aleradyrunning():
    print("Another instance of this program is already running")
    exit(0)


if __name__ == '__main__':
    app.run()