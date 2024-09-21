import sqlite3
import os
import random as rn
from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, session
from DataBase import DataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin


#Конфигурация
DATABASE = '/tmp/app.py'
DEBUG = True
SECRET_KEY = 'fljahglahlvfdvln.n.xbvrea;ih3#5434343!'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'hack.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Войдите в аккаунт для доступа к закрытым страницам'

@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    
    return g.link_db


dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = DataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()
        

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if request.form['password'] == request.form['confirm_password']:
            hash = generate_password_hash(request.form['password'])
            res = dbase.addUser(request.form['username'], request.form['email'], hash)
            if res:
                return redirect(url_for('login'))
            else:
                flash('Ошибка в регистрации', 'error')
        else:
            flash('Пароли не совпадают', 'error')

    return render_template('register.html', title='Регистрация')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('notes'))
    
    if request.method == 'POST':
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['hpsw'], request.form['password']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(url_for('notes'))
        
        flash('Неверная пара логин/пароль', 'error')
    
    return render_template('login.html', title='Авторизация')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта')
    return redirect(url_for('login'))


@app.route('/notes')
def notes():
    notes = [
        {'preview': 'Текст заметки 1', 'title': 'Заметка 1', 'date': '2024-09-21'},
        {'preview': 'Текст заметки 2', 'title': 'Заметка 2', 'date': '2024-09-20'},
    ]
    return render_template('notes.html', notes=notes)

@app.route('/document')
def document():
    return render_template('document.html')




if __name__ == '__main__':
    app.run(debug=True)