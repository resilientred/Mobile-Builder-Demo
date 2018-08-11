import traceback

import requests
from requests import Response

from botter.bot_helper import parse_application_status, parse_param_required, generate_build_params
from botter.build_bot import TelegramBuilder
from builder.lib.network.builder_api import MobileApi
from std.config import TELEGRAM_SECRET, BASE_URL, HOST


bot_builder = TelegramBuilder(TELEGRAM_SECRET)


@bot_builder.command(command="start")
def handler_start(bot, update):
    chat_id: int = update.message.chat_id
    message = "Добро пожаловать в Gootax Mobile Builder Bot, введите /help, чтобы получить список доступных команд"
    bot.send_message(chat_id=chat_id, text=message)


@bot_builder.command(command="about")
def handler_start(bot, update):
    chat_id: int = update.message.chat_id
    message = "Данный бот позволяет собирать приложения, получать список активных сборок в очереди и статусы их " \
              "выполнения."
    bot.send_message(chat_id=chat_id, text=message)


@bot_builder.command(command="build_help")
def handler_start(bot, update):
    chat_id: int = update.message.chat_id
    message = '''
    Для сборки приложения необходимо отправить сообщение <b>-build</b> со следющими параметрами:

    <b>Обязательные поля:</b>
    i - идентификатор приложения
    p - платформа для сборки приложения(ios или android)
    v - глобальная версия
    n - весрия сборки

    <b>Необязательные поля:</b>
    m - email получателя(по-умолчанию: 3colors@gmail.com)

    <b>Пример:</b>
    <b>-build i=32 p=android v=12 n=1</b>'''
    bot.send_message(chat_id=chat_id, text=message, parse_mode="html")


@bot_builder.command(command="help")
def handler_help(bot, update):
    chat_id: int = update.message.chat_id
    message = '''
    <b>Доступный список команд:</b>
    <b>Общие:</b>
    /start - сообщение привествия
    /help - список доступных команд
    /about - общая информация о боте

    <b>Приложение:</b>
    /applist - вывести полный список

    <b>Сборки:</b>
    /build_help - как собрать приложение через бота
    /builds - состояние очереди сборки приложений

    '''
    bot.send_message(chat_id=chat_id, text=message, parse_mode="html")


@bot_builder.command(command="applist")
def handler_applist(bot, update):
    chat_id: int = update.message.chat_id
    app_list: str = ""
    try:
        response: Response = requests.get(url=BASE_URL + "/get_app_list")
        apps = response.json()
        for application in apps:
            str_app = str("ID - %s| Name - %s\n" % (application['id'], application['app_name']))
            app_list += str_app
    except:
        app_list = "Произошла ошибка при получении спика приложения"

    bot.send_message(chat_id=chat_id, text=app_list)


@bot_builder.command(command="builds")
def handler_applist(bot, update):
    chat_id: int = update.message.chat_id
    app_list: str = ""
    try:
        response: Response = requests.get(url=BASE_URL + "/build_list")
        apps = response.json()
        for application in apps:
            str_app = str("ID - %s| Name - %s | Status - %s\n" % (application['id'],
                                                                  application['app_name'],
                                                                  parse_application_status(application['status'])))
            app_list += str_app
    except:
        app_list = "Произошла ошибка при получении спика приложения"

    bot.send_message(chat_id=chat_id, text=app_list)


# -build i=32 p=android v=12 n=1
@bot_builder.common_message
def common_message(bot, update):
    chat_id: int = update.message.chat_id
    text: str = update.message.text

    if text.startswith("-build "):
        try:
            params = text.strip().replace('-build ', '').split(' ')

            parse_params = {}

            for param in params:
                param_map = param.split('=')
                parse_params[param_map[0]] = param_map[1]

            build_params = generate_build_params(parse_params)
            print(build_params)

            MobileApi.post_app_build(BASE_URL, build_params)
        except:
            traceback.print_exc()


if __name__ == '__main__':
    bot_builder.start()





