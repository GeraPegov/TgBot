import telebot 
import sqlite3 
from telebot import types

bot = telebot.TeleBot('7973566766:AAFPYQn5qWijn3JepxfWZMvCLpmpenIoi2c')
API = 'c9b1adf4b73812eb368c4e105dfed0ed'

name_of_vakcina = ['1. Бравекто', '2. Симпарика', '3. Нексгард', '4. Нобивак', '5. Эурикан', '6. Пурикан', '7. Биокан', '8. Биофел', '9. Коронакет', '10. Апоквел']
bravekto = ['', '1. Бравекто 2-5', '2. Бравекто 5-10', '3. Бравекто 10-20', '4. Бравекто 20-40', '5. Бравето 40-56']
simparika = ['', '1. Симпарика 1-2.5', '2. Симпарика 2.5-5', '3. Симпарика 5-10', '4. Симпарика 10-20', '5. Симпарика 20-40', '6. Симпарика 40-60']
nexgard = ['', '1. Нексгард 2-4', '2. Нексгард 4-10', '3. Нексгард 10-25', '4. Нексгард 25-50']
nobivac = ['', '1. Нобивак Dhppi', '2. Нобивак RL', '3. Нобивак Lepto', '4. Нобивак R 1/1', '5. Нобивак R 1/10', '6. Нобивак Tricat', '7. Нобивак KC', '8. Нобивак Puppy']
eurikan = ['', '1. Эурикан Dhppi-L', '2. Эурикан Rabisin']
purevacs = ['', '1. Пуревакс RcpCh', '2. Пуревакс Rcp']
biocan = ['', 'Биокан+R', 'Биокан']
biofel = ['', '1. Биофел', '2. Биофел+R']
koronaket = ['', '1. Коронакэт 10мг', '2. Коронакэт 30мг']
apokvel = ['', '1. Апоквел 5.4мг', '2. Апоквел 16мг']

connection = sqlite3.connect('users_staff.db')
c = connection.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name_of_organization TEXT, name_of_product TEXT, price INTEGER)")
connection.commit()
connection.close()

@bot.message_handler(commands=['start'])
def price(message):
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('ВАКЦИНА', callback_data = 'vakcina')
    bt2 = types.InlineKeyboardButton('КОРМА', callback_data = 'korma')
    bt3 = types.InlineKeyboardButton('ПРЕПАРАТЫ', callback_data = 'preparati')
    markup.add(bt1, bt2, bt3)
    bot.send_message(message.chat.id, 'что вы хотите приобрести?', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def name(call):
    if call.data == 'vakcina':
        bot.send_message(call.message.chat.id, f'выберите номер: {"\n"} {'\n'.join(name_of_vakcina)}')
        bot.register_next_step_handler(call.message, vakcina)

def vakcina(call):
    global bravecto
    num = int(call.message.text)
    bot.send_message(call.message.chat.id, '')





bot.polling() 