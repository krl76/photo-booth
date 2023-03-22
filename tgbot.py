from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

import datetime

from random import choices

from db_data import db_session
from db_data.__all_models import Photo, User, PhotoUser, Statistics
import sqlite3

import threading
import schedule
import time

from main import admin_password

TOKEN = '5436507493:AAFNMNTR9qJGWJ9YcBEYsYy-blIiHb07hr8'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

button_instruction = KeyboardButton('Инструкция')
button_otzyv = KeyboardButton('Отзыв')

button_statistics_day = KeyboardButton('Статистика за день')
button_statistics_week = KeyboardButton('Статистика за неделю')
button_send_message = KeyboardButton('Рассылка')
button_admin_password = KeyboardButton('Пароль для админки')
button_count_users = KeyboardButton('Количество пользователей')
button_count_admins = KeyboardButton('Количество админов')

markup_user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_user.row(button_instruction, button_otzyv)

markup_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_admin.add(button_instruction)
markup_admin.row(button_statistics_day, button_statistics_week)
markup_admin.row(button_count_users, button_count_admins)
markup_admin.row(button_send_message, button_admin_password)


text_message = 0
text_otzyv = 0


def new_user(user_id):
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    users_id = cursor.execute(f'''SELECT user_id FROM users''').fetchall()
    if (user_id,) not in users_id:
        db_session.global_init('db/photo-booth.sqlite')
        session = db_session.create_session()
        new_user = User(
            user_id=user_id
        )
        session.add(new_user)
        session.commit()

    connection.close()


def status(user_id):
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    status = int(cursor.execute(f'''SELECT status FROM users WHERE user_id="{user_id}"''').fetchone()[0])
    connection.close()
    return status


def new_status(user_id):
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    new_status = cursor.execute(f'''UPDATE users SET status=1 WHERE user_id="{user_id}"''').fetchall()
    connection.commit()
    connection.close()


def if_code(code):
    db_session.global_init('db/photo-booth.sqlite')
    session = db_session.create_session()
    return session.query(Photo).filter(Photo.code == code).first()


def send_photo(user_id, code):
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    user = cursor.execute(f'''UPDATE users SET count_photo=count_photo+1 WHERE user_id="{user_id}"''').fetchall()
    path = cursor.execute(f'''SELECT photo FROM photos WHERE code="{code}"''').fetchone()[0]
    statistics = cursor.execute(
        f'''UPDATE statistics SET count_send=count_send+1 WHERE photo="{path}"''').fetchall()
    connection.commit()
    db_session.global_init('db/photo-booth.sqlite')
    session = db_session.create_session()
    photo = PhotoUser(
        user_id=user_id,
        photo=path
    )
    session.add(photo)
    session.commit()
    return path


def make_statictics_day():
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    make_day = len(cursor.execute(
        f'''SELECT photo FROM statistics WHERE time>"{datetime.datetime.now() - datetime.timedelta(days=1)}"''').fetchall())
    send_day = cursor.execute(
        f'''SELECT count_send FROM statistics WHERE time>"{datetime.datetime.now() - datetime.timedelta(days=1)}"''').fetchall()
    send_day = sum([int(i[0]) for i in send_day])
    connection.close()
    return [make_day, send_day]


def make_statictics_week():
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    make_week = len(cursor.execute(
        f'''SELECT photo FROM statistics WHERE time>"{datetime.datetime.now() - datetime.timedelta(weeks=1)}"''').fetchall())
    send_week = cursor.execute(
        f'''SELECT count_send FROM statistics WHERE time>"{datetime.datetime.now() - datetime.timedelta(weeks=1)}"''').fetchall()
    send_week = sum([int(i[0]) for i in send_week])
    connection.close()
    return [make_week, send_week]


def last_using(user_id):
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    last_using = cursor.execute(
        f'''UPDATE users SET date_last_using="{datetime.datetime.now()}" WHERE user_id="{user_id}"''').fetchall()
    connection.commit()


def count_users():
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    cu = len(cursor.execute(f'''SELECT id FROM users WHERE status=2''').fetchall())
    connection.close()
    return cu


def count_admins():
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    ca = len(cursor.execute(f'''SELECT id FROM users WHERE status=1''').fetchall())
    connection.close()
    return ca


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.chat.id
    nnu = new_user(user_id)
    st = status(user_id)
    markup = markup_admin if st == 1 else markup_user
    await message.reply('''Добро пожаловать!)
Для получения фотографии отправьте код, указанный на экране фотобудки''',
                        reply_markup=markup)


@dp.message_handler()
async def other_command(message: types.Message):
    global text_message
    global  text_otzyv
    global admin_password
    user_id = message.chat.id
    nu = new_user(user_id)
    st = status(user_id)
    markup = markup_admin if st == 1 else markup_user
    lu = last_using(user_id)
    if message.text == 'Инструкция':
        await message.reply(f'''1. Сфотографируйтесь в фотобудке школы №1357
2. Отправьте код, указанный на экране
3. Через 15 минут фотография удалится из памяти фотобудки''',
                            reply_markup=markup)
    elif message.text == admin_password:
        if st == 1:
            await message.reply('''Вы уже админ''',
                                reply_markup=markup_admin)
        else:
            ns = new_status(user_id)
            await message.reply('''Теперь вы админ''',
                                reply_markup=markup_admin)

    elif message.text == 'Статистика за день':
        if st == 1:
            s = make_statictics_day()
            await message.reply(f'''Количество сделанных фотографий: {s[0]}
Количество отправленных фотографий: {s[1]}''',
                                reply_markup=markup)
        else:
            await message.reply('''Некорректный запрос''',
                                reply_markup=markup)
    elif message.text == 'Статистика за неделю':
        if st == 1:
            s = make_statictics_week()
            await message.reply(f'''Количество сделанных фотографий: {s[0]}
Количество отправленных фотографий: {s[1]}''',
                                reply_markup=markup)
        else:
            await message.reply('''Некорректный запрос''',
                                reply_markup=markup)

    elif message.text == 'Пароль для админки':
        if st == 1:
            print(admin_password)
            await message.reply(f'''{admin_password}''',
                                reply_markup=markup)
        else:
            await message.reply('''Некорректный запрос''',
                                reply_markup=markup)
    elif message.text == 'Рассылка':
        if st == 1:
            text_message = 1
            await message.reply('''Введите текст для рассылки''')
        else:
            await message.reply('''Некорректный запрос''',
                                reply_markup=markup)
    elif message.text == 'Отзыв':
        if st == 2:
            text_otzyv = 1
            await message.reply('''Напишите отзыв''')
        else:
            await message.reply('''Некорректный запрос''',
                                reply_markup=markup)
    elif message.text == 'Количество пользователей':
        if st == 1:
            cu = count_users()
            await message.reply(f'''Количество пользователей: {cu}''')
        else:
            await message.reply('''Некорректный запрос''',
                                reply_markup=markup)
    elif message.text == 'Количество админов':
        if st == 1:
            ca = count_admins()
            await message.reply(f'''Количество админов: {ca}''')
        else:
            await message.reply('''Некорректный запрос''',
                                reply_markup=markup)
    elif message.text.isdigit():
        code = message.text
        if if_code(code):
            path = send_photo(user_id, code)
            await bot.send_photo(chat_id=user_id, photo=open(path, 'rb'))
        else:
            await message.reply('''Неверный код''',
                                reply_markup=markup)
    elif text_message:
        text_message = message.text
        await mailing(message.text, user_id)
    elif text_otzyv:
        text_otzyv = message.text
        await otzyv(message.text)
    else:
        await message.reply('''Некорректный запрос''',
                            reply_markup=markup)


@dp.message_handler()
async def mailing(message, admin):
    global text_message
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    chats = cursor.execute(f'''SELECT user_id FROM users''').fetchall()
    for chat in chats:
        if int(chat[0]) == admin:
            await bot.send_message(chat_id=chat[0], text='Рассылка выполнена')
        else:
            await bot.send_message(chat_id=chat[0], text=message)
    text_message = 0


@dp.message_handler()
async def otzyv(message):
    global text_otzyv
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    chats = cursor.execute(f'''SELECT user_id FROM users WHERE status=1''').fetchall()
    for chat in chats:
        await bot.send_message(chat_id=chat[0], text=message)
    text_otzyv = 0


@dp.message_handler()
def reminder():
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    users = cursor.execute(
        f'''SELECT user_id FROM users WHERE date_last_using<"{datetime.datetime.now() - datetime.timedelta(minutes=1)}"''').fetchall()
    connection.commit()
    connection.close()
    for user in users:
        bot.send_message(chat_id=user[0], text='''Добрый день! Вы давно не пользовались нашей фотобудкой(
Напоминаем, что она расположена на первом этаже школы №1357''')


if __name__ == '__main__':
    executor.start_polling(dp)
