from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

import sqlite3

import datetime

from db_data import db_session
from db_data.__all_models import Photo, User

TOKEN = '5436507493:AAFNMNTR9qJGWJ9YcBEYsYy-blIiHb07hr8'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

button_instruction = KeyboardButton('Инструкция')

markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup.add(button_instruction)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    db_session.global_init('db/photo-booth.sqlite')
    session = db_session.create_session()
    connection = sqlite3.connect('db/photo-booth.sqlite')
    cursor = connection.cursor()
    user_id = message.chat.id
    users_id = cursor.execute(f'SELECT chat_id FROM chats').fetchall()
    if user_id not in users_id:
        new_user = User(
            user_id=user_id,
            date_registration=datetime.datetime.now(),
        )
        session.add(new_user)
        session.commit()
    await message.reply('''Добро пожаловать!)
Для получения фотографии отправьте код, указанный на экране фотобудки.''',
                        reply_markup=markup)


@dp.message_handler()
async def process_start_command(message: types.Message):
    if message.text == 'Инструкция':
        await message.reply('''1. Сфотографируйтесь в фотобудке школы №1357.
2. Отправьте код, указанный на экране.''',
                            reply_markup=markup)
    else:
        db_session.global_init('db/photo-booth.sqlite')
        session = db_session.create_session()
        user_id = message.chat.id
        code = session.query(Photo).filter(Photo.code == message.text).first()
        if code:
            connection = sqlite3.connect('db/photo-booth.sqlite')
            cursor = connection.cursor()
            user = cursor.execute(f'''UPDATE photos SET count_photo=count_photo+1 WHERE user_id="{user_id}"''')
            connection.commit()
            cursor.execute(f'''SELECT image FROM photos WHERE code="{message.text}"''')
            path = cursor.fetchone()[0]
            await bot.send_photo(chat_id=message.chat.id, photo=open(path, 'rb'))
            connection.close()
        else:
            await message.reply('''Неверный код''')


if __name__ == '__main__':
    executor.start_polling(dp)
