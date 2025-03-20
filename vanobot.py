import telebot as tb
import sqlite3
import requests
import json
from currency_converter import CurrencyConverter
from telebot import types 

bot = tb.TeleBot('7589388547:AAEmHZsb3VIg6w0BuGEk8MGU6yzt7v944zY', parse_mode = None)
API = '4ba6660caf9bba080d0cac486b545c1d'
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'take me your money')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'error')
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:

        markup = types.InlineKeyboardMarkup(row_width = 2)
        bt1 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        bt2 = types.InlineKeyboardButton('RUB/BYN', callback_data='rub/byn')
        bt3 = types.InlineKeyboardButton('more', callback_data='more')
        markup.add(bt1, bt2)
        bot.send_message(message.chat.id, 'choice valuette', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'error')
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call: call.data == 'eur/usd')
def callback(call):
    bot.send_message(call.message.chat.id, '123')






bot.polling()

#lambda, call, sqlite