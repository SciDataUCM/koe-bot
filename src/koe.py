#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" SciDataUCM's Telegram bot """

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import os
from src import commands
from src.logger import logger

# Configuration
BOTNAME = 'KoeBot'
TOKEN = os.environ['KOE_TOKEN']


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update {} caused error {}'.format(update, error))


def main():
    """ Start Koe """
    updater = Updater(token=TOKEN)

    # Adding every command handler
    updater.dispatcher.add_handler(MessageHandler(Filters.status_update, commands.empty_message))
    updater.dispatcher.add_handler(CommandHandler('start', commands.start))
    updater.dispatcher.add_handler(CommandHandler('help', commands.help))
    updater.dispatcher.add_handler(CommandHandler('where', commands.where))
    updater.dispatcher.add_handler(CommandHandler('weather', commands.weather))
    updater.dispatcher.add_handler(CommandHandler('news', commands.news))
    updater.dispatcher.add_handler(CommandHandler('collaborate', commands.collaborate))
    updater.dispatcher.add_handler(CommandHandler('membership', commands.membership))
    updater.dispatcher.add_handler(CommandHandler('calendar', commands.calendar))
    updater.dispatcher.add_handler(CommandHandler('social', commands.social))
    updater.dispatcher.add_handler(CommandHandler('learn', commands.learn))
    updater.dispatcher.add_handler(CommandHandler('forecast', commands.Forecast))
    updater.dispatcher.add_handler(CallbackQueryHandler(commands.Forecast.forecast_response)) #this is for the bot to notice wich forecast button was pressed

    # log all errors
    updater.dispatcher.add_error_handler(error)

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
