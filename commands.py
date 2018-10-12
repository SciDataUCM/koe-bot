import telegram
import requests
import cachetools
import os
import json

from config import *
from logger import logger

from bs4 import BeautifulSoup

BOTNAME = 'KoeBot'
WEATHER_API_KEY = os.environ['WEATHER_API_KEY']


# Command handlers
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('¡Hola! Mi nombre es Koe 🐼, espero poder ayudarte.')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def welcome(bot, update):
    logger.info("{}(username={}) joined chat {}".format((user.first_name for user in update.message.new_chat_members),
                                                        (user.username for user in update.message.new_chat_members),
                                                        update.message.chat_id))

    bot.send_message(chat_id=update.message.chat_id, text=("¡Bienvenid@ ! Mi nombre es Koe 🐼 Aquí tienes información "
                                                           "sobre SciDataUCM "
                                                           "que tal vez te interese 😊\n[Website🌐]"
                                                           "(https://scidataucm.org/) - [Twitter🐤]("
                                                           "https://twitter.com/scidataucm) "
                                                           "- [Instagram📷](https://www.instagram.com/scidataucm/) - "
                                                           "[Github💻](https://github.com/SciDataUCM) "
                                                           " - Email✉: scidata@ucm.es"),
                     parse_mode=telegram.ParseMode.MARKDOWN)


def goodbye(bot, update):
    logger.info("{}(username={}) left chat {}".format(update.message.left_chat_member.first_name,
                                                      update.message.left_chat_member.username, update.message.chat_id))

    bot.send_message(chat_id=update.message.chat_id, text="¡Hasta pronto...!😥")


def empty_message(bot, update):
    if len(update.message.new_chat_members) is not 0 and update.message.new_chat_members[0].username != BOTNAME:
        welcome(bot, update)
    elif update.message.left_chat_member is not None:
        if update.message.left_chat_member.username != BOTNAME:
            return goodbye(bot, update)


def where(bot, update):
    update.message.reply_text('Vivo en el despacho 120 de la Facultad de Informatica de la Universidad Complutense de Madrid ☺')



def collaborate(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=("For the purpose of collaboration follow this link:"
                                                           "- [Link🌐](https://docs.google.com/forms/d/e"
                                                           "/1FAIpQLSeMJnOmN6xRua5CtTnwbYIv83gSL_EsjNUkNvV0HzKe82OAEQ"
                                                           "/viewform)"), parse_mode=telegram.ParseMode.MARKDOWN)


def membership(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=("New members should register at this link:"
                                                           "[Link🌐](https://docs.google.com/forms/d/e"
                                                           "/1FAIpQLSdKRf8Lah2-2LFcUv3TIIcKDUhtBv1WdrdfQjwf4M0-XChRxA"
                                                           "/viewform)"), parse_mode=telegram.ParseMode.MARKDOWN)


# Cache the news source for 30 minutes to avoid getting throttled and improve
# latency for repeated calls.
THIRTY_MINUTES = 30 * 60
@cachetools.cached(cachetools.TTLCache(maxsize=1, ttl=THIRTY_MINUTES))
def query_news_source():
    news_source = "https://www.reddit.com/r/machinelearning/hot.json?count=5"
    response = requests.get(news_source, headers={'user-agent': 'KoeBot by /u/SciDataUCM'}).json()
    return response


def news(bot, update):
    response = query_news_source()
    formatted_links = [
        "- {}; LINK({})".format(item['data']["title"], item['data']["url"])
        for item in response["data"]["children"]
    ]
    bot.send_message(chat_id=update.message.chat_id, text=("\n\n".join(formatted_links[:5])))

def weather(bot, update):
    """Send a message when the command /weather is issued."""
    try:
        r = requests.get('{}&appid={}'.format(WEATHER_BASE_URL, WEATHER_API_KEY))
        weather = json.loads(r.text)
    except:
        update.message.reply_text('Sorry, I cannot told to you the current weather!')
    else:
        K = 273.15
        CURRENT_TEMP = "{0:.2f}".format(weather['main']['temp'] - K)
        weather_message = 'It is {}({}) at the campus! The current temperature is {} ºC'.format(
            weather['weather'][0]['main'],
            weather['weather'][0]['description'].title(),
            CURRENT_TEMP)

        TEMP_MIN = weather['main']['temp_min'] - K
        TEMP_MAX = weather['main']['temp_max'] - K
        temperature_message = 'The MAX and MIN temperature are {} ºC and {} ºC, respectively.'.format(
            TEMP_MAX,
            TEMP_MIN)

        update.message.reply_text('{}\n{}\n'.format(
            weather_message,
            temperature_message))

def pollution(bot, update):
    try:
        r = requests.get('{}?appid={}'.format(CO_POLLUTION_BASE_URL, WEATHER_API_KEY))
        co_pollution = json.loads(r.text)
        r = requests.get('{}?appid={}'.format(O3_POLLUTION_BASE_URL, WEATHER_API_KEY))
        o3_pollution = json.loads(r.text)
        r = requests.get('{}?appid={}'.format(SO2_POLLUTION_BASE_URL, WEATHER_API_KEY))
        so2_pollution = json.loads(r.text)
        r = requests.get('{}?appid={}'.format(NO2_POLLUTION_BASE_URL, WEATHER_API_KEY))
        no2_pollution = json.loads(r.text)
    except:
        update.message.reply_text('Sorry, I cannot tell to you the current pollution level!')
    else:
        for read in co_pollution['data']:
            if read['pressure']<215 and read['pressure']>0.00464:
                co_pollution_message = 'CO pollution at the campus has level of {} '.format(read['value'])
                break
        for read in so2_pollution['data']:
            if read['pressure']<215 and read['pressure']>0.00464:
                so2_pollution_message = 'SO2 pollution at the campus has level of {} '.format(read['value'])
                break
        o3_pollution_message = 'O3 pollution at the campus has level of {} '.format(o3_pollution['data'])
        no2_pollution_message = 'NO2 pollution at the campus has level of {} '.format(no2_pollution['data']['no2']['value'])
        update.message.reply_text(co_pollution_message)
        update.message.reply_text(so2_pollution_message)
        update.message.reply_text(o3_pollution_message)
        update.message.reply_text(no2_pollution_message)

def calendar(bot, update):
    def __get_calendar():
        calendar = requests.get('https://calendar.google.com/calendar/'
                                'htmlembed?src=scidata@ucm.es&mode=AGENDA&ctz=Europe/Madrid')
        calendar = BeautifulSoup(calendar.text, features='html.parser')
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
