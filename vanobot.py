import telebot as tb
import sqlite3
import requests
import json
from telebot import types 
bot = tb.TeleBot('7589388547:AAEmHZsb3VIg6w0BuGEk8MGU6yzt7v944zY', parse_mode = None)
API = '4ba6660caf9bba080d0cac486b545c1d'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'take me your city')

@bot.message_handler(content_types=['text'])
def get_weather(message):
        city = message.text.strip().lower()
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'now weather: {temp}')

        image = 'suny.jpg' if temp > 5.0 else 'nonsuny.jpg'
        file = open('/Users/georgegoetze/python/tgbot/'+image, 'rb')
        bot.send_photo(message.chat.id, file)
bot.polling()

#lambda, call, sqlite