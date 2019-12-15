import logging

import configparser
from telegram.ext import Updater, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

config = configparser.ConfigParser()
config.read('develop.conf')

BOT_TOKEN = config['telegram-bot']['token']
REQUEST_KWARGS={
    'proxy_url': config['proxy']['url'],
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'username': config['proxy']['user'],
        'password': config['proxy']['password'],
    }
}

updater = Updater(token=BOT_TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)

dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='hello')


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()

