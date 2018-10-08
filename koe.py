#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" SciDataUCM's Telegram bot """
import os
import commands

import telegram

from logger import logger
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Configuration
BOTNAME = 'KoeBot'
#with open('config.txt', 'r') as cfg:
    #TOKEN = cfg.readline().rstrip('\n')
#  Heroku Config vars
TOKEN = os.environ['KOE_TOKEN']

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

    # log all errors
    dispatcher.add_error_handler(error)

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':  
    main()
