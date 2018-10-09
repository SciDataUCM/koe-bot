import telegram
import requests
import cachetools
import os
import json

from config import WEATHER_BASE_URL
from logger import logger

BOTNAME = 'KoeBot'
WEATHER_API_KEY =  'asd'

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
@cachetools.cached(cachetools.TTLCache(maxsize=1, ttl=THIRTY_MINUTES))
def query_news_source():
    news_source = "https://www.reddit.com/r/machinelearning/hot.json?count=5"
    response = requests.get(news_source, headers = {'user-agent': 'KoeBot by /u/SciDataUCM'}).json()
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
        CURRENT_TEMP = weather['main']['temp'] - K
        weather_message = 'It is {}({}) at the campus! The current temperature is {} ºC'.format(
            weather['weather'][0]['main'],
            weather['weather'][0]['description'].title(),
            CURRENT_TEMP)

        TEMP_MIN = weather['main']['temp_min'] - K
        TEMP_MAX = weather['main']['temp_max'] - K
        temperature_message = 'The MAX and MIN temperature are {} ºC and {} ºC, respectively.'.format(
            TEMP_MAX,
            TEMP_MIN)
        
        update.message.reply_text('{}\n{}\n\nFont: https://openweathermap.org'.format(
            weather_message,
            temperature_message))
