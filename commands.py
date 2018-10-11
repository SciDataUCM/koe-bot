import requests
import telegram

from logger import logger

from bs4 import BeautifulSoup


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('¡Hola! Mi nombre es Koe 🐼, espero poder ayudarte.')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def where(bot, update):
    update.message.reply_text('Vivo en el despacho 120 de la Facultad de Informatica de la Universidad Complutense de Madrid ☺')

def calendar(bot, update):
    def __get_calendar():
        calendar = requests.get('https://calendar.google.com/calendar/htmlembed?src=scidata@ucm.es&mode=AGENDA&ctz=Europe/Madrid')
        calendar = BeautifulSoup(calendar.text, features='html5lib')
        return calendar.find_all('div', {'class': 'view-container'}, limit=1)

    def __parse_calendar_date(calendar_date):
        date = calendar_date.upper()
        date = date.split(' ', 1)
        return '{0} - {1}'.format(date[0], date[1].replace(" ", "/"))

    def __get_events():
        calendar = __get_calendar()
        if calendar[0].div.div is False:
            response = ''
            for event_day in calendar:
                day = __parse_calendar_date(event_day.div.div.text)
                events = []
                for event in event_day.div.table.tbody:
                    time = event.find('td', {'class': 'event-time'}).text
                    title = event.find('span', {'class': 'event-summary'}).text
                    events.append('* {0} - {1}'.format(time, title))
                response = response + '{}:\n\n{}\n'.format(day, '\n'.join(events))
        else:
            return 'No scheduled events!'
        return response
    
    update.message.reply_text(__get_events())
