#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" SciDataUCM's Telegram bot """

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
import cachetools
import os
import commands

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
BOTNAME = 'KoeBot'
#with open('config.txt', 'r') as cfg:
    #TOKEN = cfg.readline().rstrip('\n')
#  Heroku Config vars
TOKEN = os.environ['KOE_TOKEN']


# Command handlers
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('¡Hola! Mi nombre es Koe 🐼, espero poder ayudarte.')

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def welcome(bot, update):
    logger.info("{}(username={}) joined chat {}".format((user.first_name for user in update.message.new_chat_members), (user.username for user in update.message.new_chat_members), update.message.chat_id))

    bot.send_message(chat_id=update.message.chat_id, text=("¡Bienvenid@ ! Mi nombre es Koe 🐼 Aquí tienes información sobre SciDataUCM"
                                                            " que tal vez te interese 😊\n[Website🌐](https://scidataucm.org/) - [Twitter🐤](https://twitter.com/scidataucm)"
                                                            " - [Instagram📷](https://www.instagram.com/scidataucm/) - [Github💻](https://github.com/SciDataUCM)"
                                                            " - Email✉: scidata@ucm.es"), parse_mode=telegram.ParseMode.MARKDOWN)

def goodbye(bot, update):
    logger.info("{}(username={}) left chat {}".format(update.message.left_chat_member.first_name, update.message.left_chat_member.username, update.message.chat_id))

    bot.send_message(chat_id=update.message.chat_id, text="¡Hasta pronto...!😥")

def empty_message(bot, update):
    if(len(update.message.new_chat_members) is not 0 and update.message.new_chat_members[0].username != BOTNAME):
        welcome(bot, update)
    elif update.message.left_chat_member is not None:
        if update.message.left_chat_member.username != BOTNAME:
            return goodbye(bot, update)

def where(bot, update):
    update.message.reply_text('Vivo en el despacho 120 de la Facultad de Informatica de la Universidad Complutense de Madrid ☺')
   
def collaborate(bot,update):
    bot.send_message(chat_id=update.message.chat_id, text=("For the purpose of collaboration follow this link:"
                                                         " - [Link🌐](https://docs.google.com/forms/d/e/1FAIpQLSeMJnOmN6xRua5CtTnwbYIv83gSL_EsjNUkNvV0HzKe82OAEQ/viewform)"), parse_mode=telegram.ParseMode.MARKDOWN)

def membership(bot,update):
    bot.send_message(chat_id=update.message.chat_id, text=("New members should register at this link:"
                                                            " [Link🌐](https://docs.google.com/forms/d/e/1FAIpQLSdKRf8Lah2-2LFcUv3TIIcKDUhtBv1WdrdfQjwf4M0-XChRxA/viewform)"), parse_mode=telegram.ParseMode.MARKDOWN)


# Cache the news source for 30 minutes to avoid getting throttled and improve
# latency for repeated calls.
THIRTY_MINUTES = 30 * 60
@cachetools.TTLCache(maxsize=1, ttl=THIRTY_MINUTES)
def query_news_source():
    news_source = "https://www.reddit.com/r/machinelearning/hot.json?count=5"
    response = requests.get(news_source).json()
    return response

def news(bot, update):
    response = query_news_source()
    formatted_links = [
        "- [{}]({})".format(item["title"], item["url"])
        for item in response["data"]["children"]
    ]
    update.message.reply_text("\n".join(formatted_links))

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """ Start Koe """
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    
        # Adding every command handler
    start_handler = CommandHandler('start', commands.start)
    dispatcher.add_handler(start_handler)
    help_handler = CommandHandler('help', commands.help)
    dispatcher.add_handler(help_handler)
    where_handler = CommandHandler('where', commands.where)
    dispatcher.add_handler(where_handler)
    weather_handler = CommandHandler('weather', commands.weather)
    dispatcher.add_handler(weather_handler)
    empty_handler = MessageHandler(Filters.status_update, empty_message)
    dispatcher.add_handler(empty_handler)
    news_handler = CommandHandler('news', news)
    dispatcher.add_handler(news_handler)
    collaborate_handler = CommandHandler('collaborate', collaborate)
    dispatcher.add_handler(collaborate_handler)
    membership_handler = CommandHandler('membership', membership)
    dispatcher.add_handler(membership_handler)
    weather_handler = CommandHandler('weather', commands.weather)
    dispatcher.add_handler(weather_handler)

    # log all errors
    dispatcher.add_error_handler(error)

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':  
    main()
