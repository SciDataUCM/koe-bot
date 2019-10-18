import telegram
import requests
import cachetools
import os
import json

from src.config import *
from src.logger import logger

from bs4 import BeautifulSoup
from datetime import datetime

BOTNAME = 'KoeBot'
WEATHER_API_KEY = os.environ['WEATHER_API_KEY']
COLLABORATE_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSeMJnOmN6xRua5CtTnwbYIv83gSL_EsjNUkNvV0HzKe82OAEQ/viewform"
MEMBERSHIP_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSdKRf8Lah2-2LFcUv3TIIcKDUhtBv1WdrdfQjwf4M0-XChRxA/viewform"
WEB_SCIDATA = "https://scidataucm.org/"
TWITTER_SCIDATA = "https://twitter.com/scidataucm"
INSTAGRAM_SCIDATA = "https://www.instagram.com/scidataucm"
GITHUB_SCIDATA = "https://github.com/SciDataUCM"
EMAIL_SCIDATA = "scidata@ucm.es"
CALENDAR_SCIDATA = "https://calendar.google.com/calendar/htmlembed?src=scidata@ucm.es&mode=AGENDA&ctz=Europe/Madrid"

# Command handlers
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('¡Hola! Mi nombre es Koe 🐼, espero poder ayudarte.')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def welcome(bot, update):
    logger.info("{}(username={}) joined chat {}".format((
        user.first_name for user in update.message.new_chat_members),
        (user.username for user in update.message.new_chat_members),
        update.message.chat_id
    ))

    bot.send_message(
        chat_id=update.message.chat_id,
        text=(
            "¡Bienvenid@ ! Mi nombre es Koe 🐼 Aquí tienes información"
            "sobre SciDataUCM que tal vez te interese 😊\n"
            "[Website🌐] ({WEB})\n"
            "- [Twitter🐤] (TWITTER)\n"
            "- [Instagram📷](INSTAGRAM)\n"
            "- [Github💻](GITHUB)\n"
            "- [Email✉]: {EMAIL}".format(WEB=WEB_SCIDATA, TWITTER=TWITTER_SCIDATA, INSTAGRAM=INSTAGRAM_SCIDATA,
                                         GITHUB=GITHUB_SCIDATA, EMAIL=EMAIL_SCIDATA)
        ),
        parse_mode=telegram.ParseMode.MARKDOWN)


def social(bot, update):
    social_media = [GITHUB_SCIDATA, TWITTER_SCIDATA,
                    INSTAGRAM_SCIDATA, WEB_SCIDATA]
    bot.send_message(
        chat_id=update.message.chat_id,
        text=("Redes sociales de SciDataUCM:\n"
              "[Github💻]({})\n"
              "[Twitter🐤]({})\n"
              "[Instagram📷]({})\n"
              "[Email ✉]: ({})".format(*social_media[:4])),
        parse_mode=telegram.ParseMode.MARKDOWN
    )


def goodbye(bot, update):
    logger.info("{}(username={}) left chat {}".format(
        update.message.left_chat_member.first_name,
        update.message.left_chat_member.username,
        update.message.chat_id
    ))

    bot.send_message(chat_id=update.message.chat_id, text="¡Hasta pronto...!😥")


def empty_message(bot, update):
    if len(update.message.new_chat_members) is not 0 and update.message.new_chat_members[0].username != BOTNAME:
        welcome(bot, update)
    elif update.message.left_chat_member is not None:
        if update.message.left_chat_member.username != BOTNAME:
            return goodbye(bot, update)


def where(update):
    update.message.reply_text('Vivo en el despacho 120 de la Facultad de Informatica de la Universidad '
                              'Complutense de Madrid ☺')


def collaborate(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=(
            "Para colaborar con SciDataUCM accede al siguiente enlace:"
            " - [Link🌐]({})".format(COLLABORATE_LINK)
        ),
        parse_mode=telegram.ParseMode.MARKDOWN)


def membership(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=(
            "Para ser miembro de SciDataUCM rellena el siguiente formulario:"
            "[Link🌐]()".format(MEMBERSHIP_LINK)
        ),
        parse_mode=telegram.ParseMode.MARKDOWN
    )


# Cache the news source for 30 minutes to avoid getting throttled and improve
# latency for repeated calls.
THIRTY_MINUTES = 30 * 60  # 30 * 60 seconds
@cachetools.cached(cachetools.TTLCache(maxsize=1, ttl=THIRTY_MINUTES))
def query_news_source():
    news_source = "https://www.reddit.com/r/machinelearning/hot.json?count=5"
    try:
        response = requests.get(news_source, headers={'user-agent': 'KoeBot by /u/SciDataUCM'}).json()
        return response
    except requests.exceptions.HTTPError as error:
        logger.log(mesg=error)
        raise Exception()


def news(bot, update):
    try:
        response = query_news_source()
    except Exception:
        update.message.reply_text('Lo siento, ¡no puedo conseguir noticias en este momento!')
    formatted_links = [
        "- {}; LINK({})".format(item['data']["title"], item['data']["url"])
        for item in response["data"]["children"]
    ]
    bot.send_message(chat_id=update.message.chat_id, text=("\n\n".join(formatted_links[:5])))


def weather(bot, update):
    """Send a message when the command /weather is issued."""
    try:
        r = requests.get('{}&appid={}'.format(WEATHER_BASE_URL, WEATHER_API_KEY))
        weather_info = json.loads(r.text)
    except Exception as error:
        logger.log(msg=error.__str__)
        update.message.reply_text('Lo siento, ¡desconozco el tiempo atmosférico actual!')
    else:
        K = 273.15
        CURRENT_TEMP = "{0:.2f}".format(weather_info['main']['temp'] - K)
        weather_message = '{}({}) en la facultad! La temperatura actual es {} ºC'.format(
            weather_info['weather'][0]['main'],
            weather_info['weather'][0]['description'].title(),
            CURRENT_TEMP
        )

        temperature_message = 'La temperatura MIN y MAX son {0:.2f} ºC y {1:.2f} ºC, respectivamente.'.format(
            weather_info['main']['temp_min'] - K,
            weather_info['main']['temp_max'] - K
        )

        update.message.reply_text('{}\n{}\n'.format(
            weather_message,
            temperature_message))


def pollution(bot, update):
    try:
        co_pollution = json.loads(requests.get('{}?appid={}'.format(CO_POLLUTION_BASE_URL, WEATHER_API_KEY)).text)
        o3_pollution = json.loads(requests.get('{}?appid={}'.format(O3_POLLUTION_BASE_URL, WEATHER_API_KEY)).text)
        so2_pollution = json.loads(requests.get('{}?appid={}'.format(SO2_POLLUTION_BASE_URL, WEATHER_API_KEY)).text)
        no2_pollution = json.loads(requests.get('{}?appid={}'.format(NO2_POLLUTION_BASE_URL, WEATHER_API_KEY)).text)
    except Exception as error:
        logger.log(msg=error.__str__)
        update.message.reply_text('Lo siento, ¡desconozco el nivel de contaminación actual!')

    for read in co_pollution['data']:
        if 215 > read['pressure'] > 0.00464:
            co_pollution_message = 'Polución de CO en la facultad tiene un nivel de {} '.format(read['value'])
            break
    for read in so2_pollution['data']:
        if 215 > read['pressure'] > 0.00464:
            so2_pollution_message = 'Polución de SO2 en la facultad tiene un nivel de {} '.format(read['value'])
            break
    o3_pollution_message = 'Polución de O3 en la facultad tiene un nivel de {} '.format(o3_pollution['data'])
    no2_pollution_message = 'Polución de NO2 en la facultad tiene un nivel de {} '.format(no2_pollution['data']['no2']['value'])
    update.message.reply_text(co_pollution_message)
    update.message.reply_text(so2_pollution_message)
    update.message.reply_text(o3_pollution_message)
    update.message.reply_text(no2_pollution_message)


def calendar(bot, update):
    def __get_calendar():
        calendar_info = requests.get(CALENDAR_SCIDATA)
        calendar_info = BeautifulSoup(calendar_info.text, features='html.parser')
        return calendar_info.find_all('div', {'class': 'view-container'}, limit=1)

    def __parse_calendar_date(calendar_date):
        date = calendar_date.upper()
        date = date.split(' ', 1)
        return '{0} - {1}'.format(date[0], date[1].replace(" ", "/"))

    def __get_events():
        calendar_info = __get_calendar()
        if calendar_info[0].div.div is False:
            response = ''
            for event_day in calendar_info:
                day = __parse_calendar_date(event_day.div.div.text)
                events = []
                for event in event_day.div.table.tbody:
                    time = event.find('td', {'class': 'event-time'}).text
                    title = event.find('span', {'class': 'event-summary'}).text
                    events.append('* {0} - {1}'.format(time, title))
                response = response + '{}:\n\n{}\n'.format(day, '\n'.join(events))
        else:
            return '¡No hay eventos programados!'
        return response

    update.message.reply_text(__get_events())


def learn(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=(
            "Data Science:\n"
            "[For begginers](https://github.com/amrrs/For-Data-Science-Beginners)\n"
            "[Good tutorials + books&vides](http://jasdumas.com/ds-resources/)\n"
            "[Learn AI with GOOGLE](https://ai.google/education/)\n"
        ),
        parse_mode=telegram.ParseMode.MARKDOWN)


class Forecast:
    def __init__(self):
        self.weather_info = None
    """Send a message to select between dates when the command /forecast is issued."""	
    def forecast(self, update):
        try:
            r = requests.get('{}&appid={}'.format(FORECAST_BASE_URL, WEATHER_API_KEY))
            weather_info = json.loads(r.text)
            self.weather_info = weather_info
        except:
            update.message.reply_text('Lo siento, ¡desconozco el tiempo atmosférico actual!')
        else:
            days = []
            for i in range(weather_info['cnt']):
                date_time_str = weather_info['list'][i]['dt_txt']
                date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                d = date_time.strftime("%d")
                if d not in days:
                    days.append(d)
            keyboard = []
            keyboard_inside = []

            for x in days:
                keyboard_button = telegram.InlineKeyboardButton("dia: {0}".format(x), callback_data=x)
                keyboard_inside.append(keyboard_button)
        
            keyboard.append(keyboard_inside)
            reply_markup = telegram.InlineKeyboardMarkup(keyboard)
            update.message.reply_text("Indicame que dia quieres: {0} - {1}".format([days[i] for i in (0, -1)][0],
                                                                                   [days[i] for i in (0, -1)][-1]),
                                      reply_markup=reply_markup)
        
    """handle the reply of the button selected, sended by the funcion above"""
    def forecast_response(self, update):
        K = 273.15
        query = update.callback_query
        msg = ["PREVISION DEL TIEMPO PARA EL DIA: {} \n".format(query.data)]
        for i in range(self.weather_info['cnt']):
            if query.data in self.weather_info['list'][i]['dt_txt']:
                weather_info_elem = self.weather_info['list'][i]
                date_time_str = weather_info_elem['dt_txt']
                date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                h = date_time.strftime("%H")
                temp = "{0:.2f}".format(weather_info_elem['main']['temp'] -K)
                weather_id = weather_info_elem['weather'][0]['id']  #for the icons
                icon = self.get_emoji(weather_id)
                msg.append("hora: {} , tiempo: {}{} , temperatura: {} ºC \n"
                           .format(h, weather_info_elem['weather'][0]['description'] , icon , temp ))
        query.edit_message_text(''.join(msg))

    def get_emoji(self, weather_id):
        #handling emojis:
        # credit to: https://github.com/mustafababil/Telegram-Weather-Bot/blob/master/responseController.py#L11

        thunderstorm = u'\U0001F4A8'    # Code: 200's, 900, 901, 902, 905
        drizzle = u'\U0001F4A7'         # Code: 300's
        rain = u'\U00002614'            # Code: 500's
        snowflake = u'\U00002744'       # Code: 600's snowflake
        snowman = u'\U000026C4'         # Code: 600's snowman, 903, 906
        atmosphere = u'\U0001F301'      # Code: 700's foogy
        clear_sky = u'\U00002600'        # Code: 800 clear sky
        few_clouds = u'\U000026C5'       # Code: 801 sun behind clouds
        clouds = u'\U00002601'          # Code: 802-803-804 clouds general
        hot = u'\U0001F525'             # Code: 904
        default_emoji = u'\U0001F300'    # default emojis

        if weather_id:
            if 200 <= weather_id < 300 or weather_id in [900, 901, 902, 905]:
                return thunderstorm
            elif 300 <= weather_id < 400:
                return drizzle
            elif 500 <= weather_id < 600:
                return rain
            elif 600 <= weather_id < 700 or weather_id in [903, 906]:
                return snowflake + ' ' + snowman
            elif 700 <= weather_id < 800:
                return atmosphere
            elif weather_id == 800:
                return clear_sky
            elif weather_id == 801:
                return few_clouds
            elif weather_id in [802, 803, 804]:
                return clouds
            elif weather_id == 904:
                return hot
            else:
                return default_emoji    # Default emoji

        else:
            return default_emoji   # Default emoji
