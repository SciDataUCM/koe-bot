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
from logger import logger

# Configuration
BOTNAME = 'KoeBot'
TOKEN = os.environ['KOE_TOKEN']

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
    empty_handler = MessageHandler(Filters.status_update, commands.empty_message)
    dispatcher.add_handler(empty_handler)
    news_handler = CommandHandler('news', commands.news)
    dispatcher.add_handler(news_handler)
    collaborate_handler = CommandHandler('collaborate', commands.collaborate)
    dispatcher.add_handler(collaborate_handler)
    membership_handler = CommandHandler('membership', commands.membership)
    dispatcher.add_handler(membership_handler)
    calendar_command = CommandHandler('calendar', commands.calendar)
    dispatcher.add_handler(calendar_command)
    social_command = CommandHandler('social', commands.social)
    dispatcher.add_handler(social_command)

    # log all errors
    dispatcher.add_error_handler(error)

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':  
    main()
