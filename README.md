# homework_bot
python telegram bot

## Описание
Телеграм бот для проверки статуса домашнего задания на курсе Yandex.Practicum.
Работает на базе «API сервиса Практикум.Домашка»

## Установка
Для работы бота необходимы:
- Токен от API сервиса Практикум.Домашка
- Токен от бота для телеграм
- ID чата, куда бот будет отправлять сообщения.

1. Склонируйте репозиторий ```git clone git@github.com:sanfootball/homework_bot.git```
2. Установите виртуальное окружение и зависимости.
```
# Для Linux/MacOS
python3 -m venv venv

# Для Windows
python -m venv venv

# Активируйте виртуальное окружение:
source venv/bin/activate

# Обновите pip
python -m pip install --upgrade pip 

# Установите зависимости
pip install -r requirements.txt
```
3. Запустите проект. В папке с проектом в терминале наберите: ```python homework.py```
