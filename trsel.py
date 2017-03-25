import os
import requests
from subprocess import call


# yandex translation api key
api_key = 'get your yandex api key here: https://tech.yandex.ru/translate/'
app_name = 'notify-send-translate-selection'


def notify(title, message):
    call(['notify-send', title, message, '-h', 'string:x-canonical-private-synchronous:' + app_name])


error_code_descriptions = {
    401: 'Invalid API key',
    402: 'Blocked API key',
    404: 'Exceeded the daily limit on the amount of translated text',
    413: 'Exceeded the maximum text size',
    422: 'The text cannot be translated',
    501: 'The specified translation direction is not supported'
}


if __name__ == '__main__':
    text = os.popen('xsel').read()
    payload = {'key': api_key, 'text': text, 'lang': 'ru', 'format': 'plain'}
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    response = requests.get(url, params=payload)
    if response.status_code == 200:
        notify(text, response.json().get('text')[0])
    else:
        notify('Невозможно перевести', error_code_descriptions.get(response.status_code, 'Неизвестная проблема'))
