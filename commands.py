import telegram
import requests
import cachetools
import os
import json

from config import *
from logger import logger

from bs4 import BeautifulSoup
from datetime import datetime

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
    logger.info("{}(username={}) joined chat {}".format((
        user.first_name for user in update.message.new_chat_members),
        (user.username for user in update.message.new_chat_members),
        update.message.chat_id
    ))

    bot.send_message(
        chat_id=update.message.chat_id,
        text=(
            """¡Bienvenid@ ! Mi nombre es Koe 🐼 Aquí tienes información
            sobre SciDataUCM
            que tal vez te interese 😊\n[Website🌐]
            (https://scidataucm.org/) - [Twitter🐤](
            https://twitter.com/scidataucm)
            - [Instagram📷](https://www.instagram.com/scidataucm/) -
            [Github💻](https://github.com/SciDataUCM)
             - Email✉: scidata@ucm.es"""
        ),
        parse_mode=telegram.ParseMode.MARKDOWN)

def social(bot, update):
    social_media = ["https://github.com/SciDataUCM", "https://twitter.com/scidataucm", "https://www.instagram.com/scidataucm/", "scidata@ucm.es"]
    bot.send_message(
        chat_id=update.message.chat_id,
        text=(
            """Redes sociales de SciDataUCM:\n[Github💻]({})\n[Twitter🐤]({})\n
            [Instagram📷]({})\n
             - Email ✉: {}""").format(*social_media[:4]),
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


def where(bot, update):
    update.message.reply_text('Vivo en el despacho 120 de la Facultad de Informatica de la Universidad Complutense de Madrid ☺')



def collaborate(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=(
            "Para colaborar con SciDataUCM accede al siguiente enlace:"
            "- [Link🌐](https://docs.google.com/forms/d/e"
            "/1FAIpQLSeMJnOmN6xRua5CtTnwbYIv83gSL_EsjNUkNvV0HzKe82OAEQ"
            "/viewform)"
        ),
        parse_mode=telegram.ParseMode.MARKDOWN)


def membership(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=(
            "Para ser miembro de SciDataUCM rellena el siguiente formulario:"
            "[Link🌐](https://docs.google.com/forms/d/e"
            "/1FAIpQLSdKRf8Lah2-2LFcUv3TIIcKDUhtBv1WdrdfQjwf4M0-XChRxA"
            "/viewform)"
        ),
        parse_mode=telegram.ParseMode.MARKDOWN
    )


# Cache the news source for 30 minutes to avoid getting throttled and improve
# latency for repeated calls.
THIRTY_MINUTES = 30 * 60
@cachetools.cached(cachetools.TTLCache(maxsize=1, ttl=THIRTY_MINUTES))
def query_news_source():
    news_source = "https://www.reddit.com/r/machinelearning/hot.json?count=5"
    try:
        response = requests.get(news_source, headers={'user-agent': 'KoeBot by /u/SciDataUCM'}).json()
        return response
    except requests.exceptions.HTTPError as error:
        print error
        sys.exit(1)
    
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
        update.message.reply_text('Lo siento, ¡desconozco el tiempo atmosférico actual!')
    else:
        K = 273.15
        CURRENT_TEMP = "{0:.2f}".format(weather['main']['temp'] - K)
        weather_message = '{}({}) en la facultad! La temperatura actual es {} ºC'.format(
            weather['weather'][0]['main'],
            weather['weather'][0]['description'].title(),
            CURRENT_TEMP
        )

        temperature_message = 'La temperatura MIN y MAX son {0:.2f} ºC y {1:.2f} ºC, respectivamente.'.format(
            weather['main']['temp_min'] - K,
            weather['main']['temp_max'] - K
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
    except:
        update.message.reply_text('Lo siento, ¡desconozco el nivel de contaminación actual!')
    else:
        for read in co_pollution['data']:
            if read['pressure']<215 and read['pressure']>0.00464:
                co_pollution_message = 'Polución de CO en la facultad tiene un nivel de {} '.format(read['value'])
                break
        for read in so2_pollution['data']:
            if read['pressure']<215 and read['pressure']>0.00464:
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
        calendar = requests.get('https://calendar.google.com/calendar/htmlembed?src=scidata@ucm.es&mode=AGENDA&ctz=Europe/Madrid')
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

class forecast:
    


    def __init__(self):
        self.w = 0
    """Send a message to select between dates when the command /forecast is issued."""	
    def forecast(self,bot, update):
        try:
            r = requests.get('{}&appid={}'.format(FORECAST_BASE_URL, WEATHER_API_KEY))
            weather = json.loads(r.text)
            self.w = weather
        except:
            update.message.reply_text('Lo siento, ¡desconozco el tiempo atmosférico actual!')
        else:
            days = []
            for i in range(weather['cnt']):
                date_time_str = weather['list'][i]['dt_txt']
                date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                d = date_time.strftime("%d")
                if(d not in days):
                     days.append(d)
            keyboard = []
            keyboard_inside = []

            for x in days:
                #print(x)
                keyboard_button = telegram.InlineKeyboardButton("dia: {0}".format(x), callback_data=x )
                keyboard_inside.append(keyboard_button)
        
            keyboard.append(keyboard_inside)
            reply_markup = telegram.InlineKeyboardMarkup(keyboard)
            update.message.reply_text("Indicame que dia quieres: {0} - {1}".format([days[i] for i in (0, -1)][0] , [days[i] for i in (0, -1)][-1]) , reply_markup=reply_markup)
        
    """handle the reply of the button selected, sended by the funcion above"""
    def forecast_response(self, bot, update):
        K = 273.15
        query = update.callback_query
        #query.message.reply_text("selected option: {}".format(query.data))
        msg = ["PREVISION DEL TIEMPO PARA EL DIA: {} \n".format(query.data)]
        for i in range(self.w['cnt']):

            if(query.data in self.w['list'][i]['dt_txt']):
                weather = self.w['list'][i]
                date_time_str = weather['dt_txt']
                date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                h = date_time.strftime("%H")                
                temp = "{0:.2f}".format(weather['main']['temp'] -K)
                weather_id = weather['weather'][0]['id'] #for the icons
                #print(weather_id)
                icon = self.getEmoji(weather_id)
                msg.append("hora: {} , tiempo: {}{} , temperatura: {} ºC \n".format(h, weather['weather'][0]['description'] , icon , temp ))
        query.edit_message_text(''.join(msg))

    def getEmoji(self, weatherID):

        #handling emojis: credit to: https://github.com/mustafababil/Telegram-Weather-Bot/blob/master/responseController.py#L11

        thunderstorm = u'\U0001F4A8'    # Code: 200's, 900, 901, 902, 905
        drizzle = u'\U0001F4A7'         # Code: 300's
        rain = u'\U00002614'            # Code: 500's
        snowflake = u'\U00002744'       # Code: 600's snowflake
        snowman = u'\U000026C4'         # Code: 600's snowman, 903, 906
        atmosphere = u'\U0001F301'      # Code: 700's foogy
        clearSky = u'\U00002600'        # Code: 800 clear sky
        fewClouds = u'\U000026C5'       # Code: 801 sun behind clouds
        clouds = u'\U00002601'          # Code: 802-803-804 clouds general
        hot = u'\U0001F525'             # Code: 904
        defaultEmoji = u'\U0001F300'    # default emojis

        if weatherID:
            if str(weatherID)[0] == '2' or weatherID == 900 or weatherID==901 or weatherID==902 or weatherID==905:
                return thunderstorm
            elif str(weatherID)[0] == '3':
                return drizzle
            elif str(weatherID)[0] == '5':
                return rain
            elif str(weatherID)[0] == '6' or weatherID==903 or weatherID== 906:
                return snowflake + ' ' + snowman
            elif str(weatherID)[0] == '7':
                return atmosphere
            elif weatherID == 800:
                return clearSky
            elif weatherID == 801:
                return fewClouds
            elif weatherID==802 or weatherID==803 or weatherID==803:
                return clouds
            elif weatherID == 904:
                 return hot
            else:
                 return defaultEmoji    # Default emoji

        else:
             return defaultEmoji   # Default emoji
