import requests


offset = 539210982  # параметр необходим для подтверждения обновления
URL = 'https://api.telegram.org/bot'  # URL на который отправляется запрос
TOKEN = '324952871:AAEI94LF9VitVYdKARABxknQSJKy4vHUymA'  # токен вашего бота, полученный от @BotFather
data = {'timeout': 100, 'offset': 3}


def send_message(text):
    message_data = {  # формируем информацию для отправки сообщения
        'chat_id': -204554547,  # куда отправляем сообщение
        'text': text,  # само сообщение для отправки
    }

    requests.post(URL + TOKEN + '/sendMessage', data=message_data)
