from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup

TOKEN = '5436507493:AAFNMNTR9qJGWJ9YcBEYsYy-blIiHb07hr8'
REQUEST_KWARGS = {'proxy_url': 'socks5://ip:port'}

reply_keyboard = [['/instruction']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

group = 1


def start(update, context):
    update.message.reply_text('''Добро пожаловать!)
Для получения фотографии отправьте код, указанный на экране фотобудки.''', reply_markup=markup)


def instruction(update, context):
    update.message.reply_text('''1. Сфотографируйтесь в фотобудке школы №1357.
2. Отправьте код, указанный на экране.''')


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("instruction", instruction))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
