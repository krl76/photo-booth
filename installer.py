import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

print('Начинаю установку библиотек')
os.system('pip install -r requirements.txt')
print('Введите токен бота')
TOKEN = input()
