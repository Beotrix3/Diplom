from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
# from passlib.hash import sha256_crypt
import hashlib
import signal
import sys
from functools import wraps
import random
import string
import binascii
import os
import ssl
from dotenv import load_dotenv
from wtforms.fields import EmailField

# python 470 строк, html 269 строк из 11 файлов, js 19 строк + библиотека jquery

# Загрузка переменных окружения из файла .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(32)

# Конфигурация MYSQL из переменных окружения
mysql = MySQL()
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Инициализация приложения с использованием классов для MySQL
mysql.init_app(app)

# Настройка почты
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Мой SMTP сервер
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Использование переменной окружения
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Использование переменной окружения

mail = Mail(app)

# Декоры

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, *kwargs)
        else:
            flash('Unauthorized, Please logged in', 'danger')
            return redirect(url_for('login'))
    return wrap


def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            flash('Unauthorized, You logged in', 'danger')
            return redirect(url_for('index'))
        else:
            return f(*args, *kwargs)
    return wrap


@app.route('/online_users_count')
def online_users_count():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) AS count FROM users WHERE online = '1'")
    count = cursor.fetchone()['count']
    cursor.close()
    return {'count': count}

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) AS count FROM users WHERE online = '1'")
    count = cursor.fetchone()['count']
    cursor.close()
    return render_template('home.html')


class LoginForm(Form):    # Форма авторизации
    username = StringField('Username', [validators.length(min=1)], render_kw={'autofocus': True})
    password = PasswordField('Password', [validators.DataRequired()])


@app.route('/verify_code_login', methods=['GET', 'POST'])
def verify_code_login():
    if request.method == 'POST':
        entered_code = request.form['two_factor_code']
        
        if entered_code == session.get('two_factor_code'):
            uid = session.get('uid')  # Получаем uid из сессии
            x = '1'  # Значение для обновления статуса в базе данных

            # Обновление статуса пользователя и времени последнего входа
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
            mysql.connection.commit()

            # Обновляем время последнего посещения в таблице users_sessions
            cur.execute("UPDATE users_sessions SET first_seen = NOW() WHERE user_id = %s", (uid,))
            mysql.connection.commit()
            cur.close()

            session['logged_in'] = True  # Установить пользователя как вошедшего
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный код, попробуйте снова', 'danger')

    return render_template('verify_code_login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = form.username.data
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()

        # Получение данных пользователя сразу по имени пользователя
        result = cur.execute("SELECT id, password, salt, email, username, online FROM users WHERE username=%s", [username])

        if result > 0:
            data = cur.fetchone()
            password = data['password']
            salt = data['salt']
            uid = data['id']
            email = data['email']
            name = data['username']
            online = data['online']

            if online == '1':
                flash('Вы уже в системе', 'danger')
                return redirect(url_for('index'))

            if calculateHash(password_candidate, salt) == password:
                # Генерация кода для двухфакторной аутентификации и отправка письма
                two_factor_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                msg = Message('Ваш код двухфакторной аутентификации', sender='beotrix3@gmail.com', recipients=[email])
                msg.body = f'Ваш код для входа: {two_factor_code}'
                mail.send(msg)

                session['two_factor_code'] = two_factor_code
                session['uid'] = uid
                session['email'] = email
                session['s_name'] = name

                return redirect(url_for('verify_code_login'))
            
            else:
                flash('Неверный пароль', 'danger')
        else:
            flash('Имя пользователя не найдено', 'danger')

        cur.close()

    return render_template('login.html', form=form)


@app.route('/out')
def logout():
    if 'uid' in session:

        # Поставить курсор
        cur = mysql.connection.cursor()
        uid = session['uid']
        x = '0'
        cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
        mysql.connection.commit()
        # Обновляем информацию о последнем посещении в users_sessions
        cur.execute("UPDATE users_sessions SET last_seen = NOW() WHERE user_id = %s", (uid,))
        mysql.connection.commit()
        session.clear()
        flash('Вы вышли из аккаунта', 'success')
        return redirect(url_for('index'))
    return redirect(url_for('login'))


class RegisterForm(Form):
    name = StringField('Name', [validators.length(min=3, max=50)], render_kw={'autofocus': True})
    username = StringField('Username', [validators.length(min=3, max=25)])
    email = EmailField('Email', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)])
    password = PasswordField('Password', [validators.length(min=8)])


@app.route('/verify_code_reg', methods=['POST'])
def verify_code_reg():
    entered_code = request.form['two_factor_code']
    
    # Получить временные данные из сессии
    if 'temp_user' not in session:
        flash('Сессия истекла, попробуйте снова', 'danger')
        return redirect(url_for('register'))

    user_data = session['temp_user']

    # Проверка кода
    if entered_code == user_data['two_factor_code']:
        # Сохранение пользователя в базе данных
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users(name, email, username, password, salt) VALUES(%s, %s, %s, %s, %s)",
            (user_data['name'], user_data['email'], user_data['username'], user_data['password'], user_data['salt'])
        )

        mysql.connection.commit()
        uid = cur.lastrowid  # Получаем ID нового пользователя

        # Записываем информацию о сессии
        cur.execute(
            "INSERT INTO users_sessions(user_id, reg_time) VALUES(%s, NOW())",
            (uid,)
        )

        mysql.connection.commit()
        cur.close()

        # Удаляем временные данные из сессии
        session.pop('temp_user', None)

        flash('Вы успешно зарегистрированы и можете войти', 'success')
        return redirect(url_for('index'))
    else:
        flash('Неверный код, попробуйте снова', 'danger')
        return render_template('verify_code_reg.html')


@app.route('/register', methods=['GET', 'POST'])
@not_logged_in
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password, salt = passHash(form.password.data)

        # Проверка, существует ли уже пользователь с такой электронной почтой
        cur = mysql.connection.cursor()
        existing_user = cur.execute("SELECT * FROM users WHERE email = %s", [email])

        if existing_user > 0:
            flash('Этот адрес электронной почты уже используется. Пожалуйста, используйте другой.', 'danger')
            cur.close()
            return render_template('register.html', form=form)

        # Проверка, существует ли уже пользователь с таким именем пользователя
        cur = mysql.connection.cursor()
        existing_user = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if existing_user > 0:
            flash('Это имя пользователя уже занято. Пожалуйста, выберите другое.', 'danger')
            cur.close()
            return render_template('register.html', form=form)

        # Генерация двухфакторного кода
        two_factor_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Отправляем код на электронную почту
        msg = Message('Ваш двухфакторный код', sender='beotrix3@gmail.com', recipients=[email])
        msg.body = f'Ваш код: {two_factor_code}'
        mail.send(msg)

        # Сохраняем временные данные в сессии
        session['temp_user'] = {
            'name': name,
            'email': email,
            'username': username,
            'password': password,
            'salt': salt,
            'two_factor_code': two_factor_code
        }

        return render_template('verify_code_reg.html')  # Страница для ввода кода

    return render_template('register.html', form=form)

class MessageForm(Form):    # Форма сообщения
    body = StringField('', [validators.length(min=1)], render_kw={'autofocus': True})

# def hashOfMsg(msg):
#     return hashlib.sha256(msg.encode()).hexdigest()
def hashOfMsg(msg):
    return hashlib.sha256(msg).hexdigest()

def passHash(password):
    passalt = os.urandom(32)
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), passalt, 100000).hex(), passalt.hex()

def calculateHash(password,passalt):
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(passalt), 100000).hex()

############################
#key = b'\xd6\x18L\x16K\xe8\xd8\xcd\xcf\x06nL\x10\x83y(A\xc5[_*\xb0\xd2!y\xd6&\x0b\xca\xedAs'

def decrypt_aes_key():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM secret_key")
    secret_key = cur.fetchone()['secret_key']
    encrypted_aes_key = binascii.unhexlify(secret_key)


    print("Расшифровка AES ключа...")  # Сообщение о начале расшифровки
    with open("private_key.pem", 'rb') as f:
        private_key = f.read()
    rsa_private_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_private_key)
    decrypted_key = cipher_rsa.decrypt(encrypted_aes_key)
    print("Расшифрованный AES ключ:", decrypted_key.hex())  # Показываем расшифрованный ключ в hex-формате
    return decrypted_key

# Расшифровка данных
def decrypt_data(encrypted_data):
    iv = encrypted_data[:16]  # Первый 16 байт - это IV
    ct = encrypted_data[16:]   # Остальные байты - это зашифрованное сообщение
    print("Начало расшифровки...")  # Сообщение о начале расшифровки
    print("Вектор инициализации (IV):", iv.hex())  # Показываем IV в hex-формате
    print("Зашифрованный текст:", ct.hex())  # Показываем зашифрованный текст в hex-формате
    cipher = AES.new(decrypt_aes_key(), AES.MODE_CBC, iv)  # Создание шифра с тем же ключом и IV
    decrypted = unpad(cipher.decrypt(ct), AES.block_size)  # Расшифровка и удаление отступов
    print("Расшифрованная строка", decrypted.decode('utf-8'))  # Показываем расшифрованную строку
    return decrypted.decode('utf-8')  # Возвращаем расшифрованную строку

def encrypt_data(data):
    print("Начало шифрования...")  # Сообщение о начале шифрования
    print("До шифрования:", data.decode('utf-8'))  # Показываем данные до шифрования
    cipher = AES.new(decrypt_aes_key(), AES.MODE_CBC)  # Используем key для шифрования данных
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = cipher.iv
    print("Вектор инициализации (IV):", iv.hex())  # Показываем IV в hex-формате
    print("Зашифрованный текст:", ct_bytes.hex())  # Показываем зашифрованный текст в hex-формате

    return iv + ct_bytes  # Возвратите IV вместе с зашифрованным сообщением

@app.route('/chatting/<string:id>', methods=['GET', 'POST'])
def chatting(id):
    if 'uid' in session:
        form = MessageForm(request.form)
        # Выбор курсора
        cur = mysql.connection.cursor()

        # lid name
        get_result = cur.execute("SELECT * FROM users WHERE id=%s", [id])
        l_data = cur.fetchone()
        if get_result > 0:
            session['name'] = l_data['username']
            uid = session['uid']
            session['lid'] = id

            if request.method == 'POST' and form.validate():
                txt_body = form.body.data.encode()
                # txt_hash = sha256_crypt.hash(str(form.body.data))  # текст преобразуется в байты
                encrypted_body = encrypt_data(txt_body)  # Шифрование сообщения
                print("Зашифрованное сообщение поступило в базу данных")  # Информация о сохранении шифрованного сообщения
                txt_hash = hashOfMsg(encrypted_body)

                # Сохраним зашифрованное сообщение в базу данных
                cur.execute("INSERT INTO messages(body, msg_by, msg_to, msg_hash) VALUES(%s, %s, %s, %s)",
                            (encrypted_body, id, uid, txt_hash))
                # Commit cursor
                mysql.connection.commit()
                print("Сообщение успешно сохранено в базе данных")  # Сообщение об успешном сохранении

            # Get users
            cur.execute("SELECT id, username, online FROM users")
            users = cur.fetchall()

            # Получаем все сеансы пользователей
            cur.execute("SELECT user_id, first_seen, last_seen FROM users_sessions")
            users_sessions_data = cur.fetchall()

            # Преобразовываем в словарь
            users_sessions = {session['user_id']: session for session in users_sessions_data}

            # Закрытие подключения
            cur.close()
            return render_template('chat_room.html', users=users, users_sessions=users_sessions, form=form)
        else:
            flash('No permission!', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/chats', methods=['GET', 'POST'])
def chats():
    if 'lid' in session:
        id = session['lid']
        uid = session['uid']
        
        # Создаем курсор для работы с базой данных
        cur = mysql.connection.cursor()
        
        # Выполняем SQL-запрос для получения сообщений
        cur.execute("SELECT * FROM messages WHERE (msg_by=%s AND msg_to=%s) OR (msg_by=%s AND msg_to=%s) "
                    "ORDER BY id ASC", (id, uid, uid, id))
        
        chats = cur.fetchall()
        
        # Расшифровка сообщений
        decrypted_chats = []
        for message in chats:
            encrypted_body = message['body']  # Предполагаем, что это поле с зашифрованным сообщением
            txt_hash = message['msg_hash']
            decrypted_body = decrypt_data(encrypted_body)
            check_hash = None
            # print(hashOfMsg(decrypted_body))
            # print(type(hashOfMsg(decrypted_body)))
            # print(txt_hash)
            # print(type(txt_hash))
            if hashOfMsg(encrypted_body) == txt_hash.decode():
                check_hash = 'Сообщение достоверно'
            else:
                check_hash = 'Сообщение модифицированно'    
            # Добавляем в список как словарь, если нужны другие поля
            decrypted_chats.append({
                'msg_by': message['msg_by'],
                'msg_to': message['msg_to'],
                'body': decrypted_body,
                'check_hash': check_hash  # Используем расшифрованный текст
            })
            
        # Закрываем соединение с БД
        cur.close()
        
        # Отправляем расшифрованные сообщения в шаблон
        return render_template('chats.html', chats=decrypted_chats)
    
    return redirect(url_for('login'))

def reset_online_status(signum, frame):
    with app.app_context():
        # Обработка сброса статуса online
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET online=%s", ('0',))  # Сбросить статус онлайн для всех пользователей
        mysql.connection.commit()
        cur.close()
        print("Все пользователи покинули сессию")
        sys.exit(0)  # Завершение процесса
        cur.close()

# При инициализации приложения
if __name__ == '__main__':
    # Регистрация обработчиков сигналов
    signal.signal(signal.SIGINT, reset_online_status)
    signal.signal(signal.SIGTERM, reset_online_status)

if __name__ == '__main__':
    server_cert = 'C:/wamp64/bin/apache/apache2.4.59/conf/key/localhost.crt'
    server_key = 'C:/wamp64/bin/apache/apache2.4.59/conf/key/localhost.key'

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.load_cert_chain(certfile=server_cert, keyfile=server_key)
    # context = ('C:/wamp64/bin/apache/apache2.4.59/conf/key/localhost.crt', 'C:/wamp64/bin/apache/apache2.4.59/conf/key/localhost.key')
    app.run(ssl_context=context, debug=True, host='localhost', port=5000)