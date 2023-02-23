import os
from platform import system

print('Начинаю установку библиотек')
if system() == 'Windows':
    os.system('pip install -r requirements.txt ')
else:
    os.system('pip3 install -r requirements.txt ')
print('Завершение настроек. Для старта запустите main.py и tgbot.py')
