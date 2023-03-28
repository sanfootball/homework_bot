import sys
import os
import telegram
import logging
import json
import time

import requests

from http import HTTPStatus
from exceptions import JsonException, APIError, APIRequestError

from dotenv import load_dotenv


load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def check_tokens():
    """Проверяет доступность переменных окружения, если нет хотя бы одной.
    переменной, прерываем работу программы.
    """
    ENV_VARS = [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]

    for var in ENV_VARS:
        if var is None:
            logging.critical('Ошибка! Отсутствует обязательная'
                             f'переменная окружения: {var}.')
            sys.exit()
    return True


def send_message(bot, message):
    """Отправляет сообщения в Телеграм о статусе проверки.
    домашней работы.
    """
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug('Сообщение о статусе успешно отправлено')
    except telegram.error.TelegramError:
        logging.error('Бот не смог отправить сообщение о статусе')


def get_api_answer(timestamp):
    """Запрос к эндпоинту АPI-сервиса Яндекса. При успешном.
    запросе, возвращает статус проверки домашней работы.
    """
    payload = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
    except requests.RequestException as error:
        raise APIRequestError(f'Ошибка ответа сервера: {error}')

    if response.status_code != HTTPStatus.OK:
        raise APIError(f'Ответ сервера не равен 200! Код'
                       f'ответа: {response.status_code}')
    try:
        response = response.json()
        return response
    except json.JSONDecodeError:
        raise JsonException(
            'API вернул недопустимый json. '
            f'ответ: {response.text}.'
        )


def check_response(response):
    """Проверяет ответ API-сервиса на соответствие документации."""
    if not isinstance(response, dict):
        raise TypeError('Полученный ответ не является словарем.')

    if 'homeworks' not in response:
        raise KeyError('Нет ключа: homeworks')

    if 'current_date' not in response:
        raise KeyError('Нет ключа: current_date')

    if not isinstance(response['homeworks'], list):
        raise TypeError('Значение ключа "homeworks" не является списком')


def parse_status(homework):
    """извлекает из информации о конкретной домашней работе.
    статус этой работы.
    """
    if not isinstance(homework, dict):
        raise TypeError('Полученная домашка не является словарем.')

    homework_status = homework.get('status')
    if not homework_status:
        raise KeyError('Нет ключа: "homework_status"')

    homework_name = homework.get('homework_name')
    if not homework_name:
        raise KeyError('В ответе API нет ключа "homework_name"')

    if homework_status not in HOMEWORK_VERDICTS:
        raise ValueError('Недокументированный статус домашней работы')
    verdict = HOMEWORK_VERDICTS[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    check_tokens()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(timestamp)
            check_response(response)
            if response['homeworks']:
                homework = response['homeworks'][0]
                message = parse_status(homework)
                send_message(bot, message)
            else:
                message = 'Данные не обновлялись.'
                logging.info(message)
                send_message(bot, message)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
