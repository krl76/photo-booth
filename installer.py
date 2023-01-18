import os

print('Начинаю установку библиотек')
print(os.path)
os.system('pip install -r requirements.txt ')
print('Введите токен бота')
TOKEN = input()

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# os.environ.putenv('TOKEN', TOKEN)
os.environ['TOKEN'] = TOKEN

print('Завершение настроек. Для старта запустите main.py и tgbot.py')
