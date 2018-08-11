from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler


class TelegramBuilder:

    def __init__(self, token):
        self.updater = Updater(token=token)

    # Bind command
    def command(self, command):
        print("Bind new command with text | " + command)

        # handler is decorator function
        def bind(handler):
            # botter and update is decorator function arguments
            def wrapped_handler(bot, update):
                handler(bot, update)

            self.updater.dispatcher.add_handler(CommandHandler(command, wrapped_handler))
        return bind


    # Bind message
    def message(self, message):
        print("Bind new message with text | " + message)

        # handler is decorator function
        def bind(handler):
            # botter and update is decorator function arguments
            def wrapped_handler(bot, update):
                handler(bot, update)
            self.updater.dispatcher.add_handler(CommandHandler(message, wrapped_handler))
        return bind


    def common_message(self, handler):
        print("Bind common message")

        def wrapped_handler(bot, update):
            handler(bot, update)
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, wrapped_handler))


    def start(self):
        self.updater.start_polling()
        print("Bot is started")


def start(bot, update):
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data='1')],
        [InlineKeyboardButton("Option 1", callback_data='2')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Selected option: %s" % query.data,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def help(bot, update):
    update.message.reply_text("Use /start to test this botter.")


def build_help(bot, update):
    chat_id = update.message.chat_id
    message = '''
    Для сборки приложения необходимо отправить сообщение по шаблону
    APP_ID PLATFORM(ios/android) VERSION_CODE VERSION_NUMBER
    32 android sargeras701@gmail.com 1 1
    '''

    bot.send_message(chat_id=chat_id, text=message)



