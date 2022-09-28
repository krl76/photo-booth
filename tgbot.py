from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

TOKEN = '5436507493:AAFNMNTR9qJGWJ9YcBEYsYy-blIiHb07hr8'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

button_instruction = KeyboardButton('Инструкция')

markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup.add(button_instruction)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('''Добро пожаловать!)
Для получения фотографии отправьте код, указанный на экране фотобудки.''',
                        reply_markup=markup)


@dp.message_handler(text=['Инструкция'])
async def process_start_command(message: types.Message):
    await message.reply('''1. Сфотографируйтесь в фотобудке школы №1357.
2. Отправьте код, указанный на экране.''',
                        reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp)
