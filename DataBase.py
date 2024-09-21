import math
import time
import sqlite3
import re
from flask import url_for




class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    
    #Работа с пользователем
    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f'SELECT COUNT() as "count" FROM users WHERE email LIKE "{email}"')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Пользователь с таким email уже существует')
                return False
            
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO users VALUES(NULL, ?, ?, ?, ?)', (name, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления пользователя в БД'+str(e))
            return False
        
        return True
    
    def getUser(self, user_id):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE id = {user_id} LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
            
            return res
        except sqlite3.Error as e:
            print('Ошибка во входе пользователя getUser'+str(e))
            
        return False
    
    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE email = "{email}" LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
            
            return res
        except sqlite3.Error as e:
            print('Ошибка во входе пользователя getUserByEmail'+str(e))
    
    # Работа с заметками
    def getNotes(self, user_id):
        try:
            self.__cur.execute(f'SELECT id, title, preview, date FROM notes WHERE user_id = {user_id}')
            res = self.__cur.fetchall()
            if not res:
                print('Заметки не найдены')
                return []
            return res
        except sqlite3.Error as e:
            print('Ошибка получения заметок: ' + str(e))
        return []

    def addNote(self, user_id, title, preview):
        try:
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO notes (user_id, title, preview, date) VALUES (?, ?, ?, ?)', 
                               (user_id, title, preview, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления заметки: ' + str(e))
            return False
        return True

    def deleteNote(self, note_id):
        try:
            self.__cur.execute(f'DELETE FROM notes WHERE id = {note_id}')
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка удаления заметки: ' + str(e))
            return False
        return True

    def updateNote(self, note_id, title, preview):
        try:
            tm = math.floor(time.time())
            self.__cur.execute(f'UPDATE notes SET title = ?, preview = ?, date = ? WHERE id = ?', 
                               (title, preview, tm, note_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка обновления заметки: ' + str(e))
            return False
        return True