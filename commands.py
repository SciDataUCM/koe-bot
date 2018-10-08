import requests
import json

import telegram

from config import WEATHER_BASE_URL, WEATHER_API_KEY
from logger import logger


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('¡Hola! Mi nombre es Koe 🐼, espero poder ayudarte.')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def where(bot, update):
    update.message.reply_text('Vivo en el despacho 120 de la Facultad de Informatica de la Universidad Complutense de Madrid ☺')


def weather(bot, update):
    """Send a message when the command /weather is issued."""
    try:
        r = requests.get('{}&appid={}'.format(WEATHER_BASE_URL, WEATHER_API_KEY))
        weather = json.loads(r.text)
    except:
        update.message.reply_text('Sorry, I cannot told to you the current weather!')
    else:
        weather_message = 'It is {}({}) at the campus! The current temperature is {} K'.format(
            weather['weather'][0]['main'],
            weather['weather'][0]['description'].title(),
            weather['main']['temp']) 
        temperature_message = 'The MAX and MIN temperature are {} K and {} K, respectively.'.format(
            weather['main']['temp_min'],
            weather['main']['temp_max'])
        
        update.message.reply_text('{}\n{}\n\nFont: https://openweathermap.org'.format(
            weather_message,
            temperature_message))
