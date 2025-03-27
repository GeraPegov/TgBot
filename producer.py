import telebot 
import sqlite3 
from telebot import types

bot = telebot.TeleBot('7973566766:AAFPYQn5qWijn3JepxfWZMvCLpmpenIoi2c')
API = 'c9b1adf4b73812eb368c4e105dfed0ed'

choice_user = None
choice_tovar = None
number_of_list = None
number_of_tovar = 0
end_choice = {}
all_price = 0
name_of_vakcina = ['1. Нобивак', '2. Эурикан', '3. Пуревакс', '4. Биокан', '5. Биофел']
choice_name_vakcina = {
1: ['', '1. Нобивак Dhppi', '2. Нобивак RL', '3. Нобивак Lepto', '4. Нобивак R 1/1', '5. Нобивак R 1/10', '6. Нобивак Tricat', '7. Нобивак KC', '8. Нобивак Puppy'],
2: ['', '1. Эурикан Dhppi-L', '2. Эурикан Rabisin'],
3: ['', '1. Пуревакс RcpCh', '2. Пуревакс Rcp'],
4: ['', 'Биокан+R', 'Биокан'],
5: ['', '1. Биофел', '2. Биофел+R'],
}

name_of_preparati = ['1. Бравекто', '2. Симпарика', '3. Нексгард', '4. Коронакэт', '5. Апоквел', '6. Кортавет', '7. Нептра', '8. Отоксолан']
choice_of_preparati = {
    1: ['', '1. Бравекто 2-5', '2. Бравекто 5-10', '3. Бравекто 10-20', '4. Бравекто 20-40', '5. Бравето 40-56'], 
    2: ['', '1. Симпарика 1-2.5', '2. Симпарика 2.5-5', '3. Симпарика 5-10', '4. Симпарика 10-20', '5. Симпарика 20-40', '6. Симпарика 40-60'],
    3: ['', '1. Нексгард 2-4', '2. Нексгард 4-10', '3. Нексгард 10-25', '4. Нексгард 25-50'],
    4: ['', '1. Коронакэт 10мг', '2. Коронакэт 30мг'],
    5: ['', '1. Апоквел 5.4мг', '2. Апоквел 16мг'],
    6: ['', '1. Кортавет'],
    7: ['', '1. Непра'],
    8: ['', '1. Отоксолан']
}

name_of_feed = ['1. Royal Canin', '2. Monge']
choice_of_feed = {
    1: ['1. RC Urinary Cat 85g', '2. RC Renal Cat 85g', '3. RC Gastro Cat 85g', '4. RC Gastro MD Cat 85g', '5. RC Recovery ', '6. RC Baby Cat 195g', '7. RC Baby Cat Milk', '8. RC Gastro Puppy 195g', '9. RC Gastro Dog 400g', '10. RC Gastro MD Dog 400g', '11. RC Baby Dog 195g', '12. RC Baby Dog Milk'],
    2: ['1. MG Hypo Duck Dog 400g', '2. MG Gastro Dog 400g', '3. MG Urinary Cat 100g', '4. MG Sterile Cat 1,5kg', '5. MG Gastro Dog 2kg', '6. MG Gastro Puppy 1,5kg', '7. MG Gastro Cat 1,5kg']
}


connection = sqlite3.connect('users_staff.db')
c = connection.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users_fiz(id INTEGER PRIMARY KEY, name_of_organization TEXT, name_of_product TEXT, price INTEGER)")
connection.commit()
c.close()
connection.close()

connection = sqlite3.connect('users_staff.db')
c = connection.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users_yr(id INTEGER PRIMARY KEY, name_of_organization TEXT, name_of_product TEXT, price INTEGER)")
connection.commit()
connection.close()

@bot.message_handler(commands=['start'])
def price(message):
    global and_choice, all_price, choice_user, choice_tovar, number_of_list, number_of_tovar
    and_choice = {}
    all_price = 0
    choice_user = None
    choice_tovar = None
    number_of_list = None
    number_of_tovar = 0
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('ВАКЦИНА', callback_data = 'vakcina')
    bt2 = types.InlineKeyboardButton('КОРМА', callback_data = 'korma')
    bt3 = types.InlineKeyboardButton('ПРЕПАРАТЫ', callback_data = 'preparati')
    markup.add(bt1, bt2, bt3)
    bot.send_message(message.chat.id, 'что вы хотите приобрести?', reply_markup=markup)

@bot.callback_query_handler(func=lambda call:  True)
def backhome(call):
    '''ОБРАБОТКА КОЛЛБЕКОВ КНОПОК ТИПА 
    ФИЗ ЛИЦО 
    ЮР ЛИЦО 
    ДА 
    ВЕРНУТЬСЯ НАЗАД
    ДОБАВИТЬ В КОРЗИНУ'''
    global end_choice, all_price, number_of_tovar
    if call.data == 'backhome':
        price(call.message)
    elif call.data == 'yes':
        end_choice[choice_tovar] = end_choice.get(choice_tovar, number_of_tovar)
        all_price += number_of_tovar
        fiz_yr(call.message)
    elif call.data == 'yes_backhome':
        end_choice[choice_tovar] = end_choice.get(choice_tovar, number_of_tovar)
        all_price += number_of_tovar
        price(call.message)
    elif call.data == 'yr_lic':
        print("Кнопка 'yr_lic' была нажата")  # Это поможет отследить вызов функции
        bot.send_message(call.message.chat.id, 'Введите через один пробел Название клиники, номер телефона по типу +79991112233 и Адрес для доставки')
        bot.register_next_step_handler(call.message, join_bd_yr)
    elif call.data == 'fiz_lic':
        bot.send_message(call.message.chat.id, 'Введите через один пробел ФИО, номер телефона по типу +79991112233 и Адрес для доставки')
        bot.register_next_step_handler(call.message, join_bd_fiz)
    elif call.data == 'vakcina':
        bot.send_message(call.message.chat.id, f'введите номер вакцины: {"\n"} {'\n'.join(name_of_vakcina)}')
        bot.register_next_step_handler(call.message, vakcina)
    elif call.data == 'preparati':
        bot.send_message(call.message.chat.id, f'введите номер препарата: {"\n"} {'\n'.join(name_of_preparati)}')
        bot.register_next_step_handler(call.message, preparati)
    elif call.data == 'korma':
        bot.send_message(call.message.chat.id, f'введите номер препарата: {"\n"} {'\n'.join(name_of_feed)}')
        bot.register_next_step_handler(call.message, feed)

#ОБРАБОТКА ВАКЦИН

def vakcina(message):
    global choice_user, number_of_list
    number_of_list = int(message.text)
    choice_user = choice_name_vakcina[number_of_list]
    bot.send_message(message.chat.id, f'введите номер вакцины: {'\n'} {'\n'.join(choice_name_vakcina[number_of_list])}')
    bot.register_next_step_handler(message, quanity_vakcina)
def quanity_vakcina(message):
    global number_of_list, choice_tovar
    quanity = int(message.text)
    choice_tovar = choice_name_vakcina[number_of_list][quanity]
    bot.send_message(message.chat.id, f'введите количество {choice_tovar[2:]}')
    bot.register_next_step_handler(message, end_preparati)



#ОБРАБОТКА ПРЕПАРАТОВ

def preparati(message):
    global choice_user, number_of_list
    number_of_list = int(message.text)
    choice_user = choice_of_preparati[number_of_list]
    bot.send_message(message.chat.id, f'введите номер препарата: {'\n'} {'\n'.join(choice_of_preparati[number_of_list])}')
    bot.register_next_step_handler(message, quanity_preparati)
def quanity_preparati(message):
    global number_of_list, choice_tovar
    quanity = int(message.text)
    choice_tovar = choice_of_preparati[number_of_list][quanity]
    bot.send_message(message.chat.id, f'введите количество {choice_tovar[2:]}')
    bot.register_next_step_handler(message, end_preparati)






#ОБРАБОТКА КОРМОВ

def feed(message):
    global choice_user, number_of_list
    number_of_list = int(message.text)
    choice_user = choice_of_feed[number_of_list]
    bot.send_message(message.chat.id, f'введите номер вакцины: {'\n'} {'\n'.join(choice_of_feed[number_of_list])}')
    bot.register_next_step_handler(message, quanity_feed)

def quanity_feed(message):
    global number_of_list, choice_tovar
    quanity = int(message.text)
    choice_tovar = choice_of_feed[number_of_list][quanity]
    bot.send_message(message.chat.id, f'введите количество {choice_tovar[2:]}')
    bot.register_next_step_handler(message, end_preparati)

# ДОБАВЛЕНИЕ В БД 

def end_preparati(message):
    global number_of_tovar
    number_of_tovar = int(message.text)
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('добавить и вернуться к выбору товаров', callback_data='yes_backhome')
    bt2 = types.InlineKeyboardButton('добавить и закончить с выбором товаров', callback_data='yes')
    bt3 = types.InlineKeyboardButton('вернуться в начало', callback_data='backhome')
    markup.add(bt1)
    markup.add(bt2)
    markup.add(bt3)
    bot.send_message(message.chat.id, f'вы выбрали: {choice_tovar[3:]}, количество: {number_of_tovar}, добавить в корзину?', reply_markup=markup)
def fiz_yr(message):
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('Юр. лицо', callback_data='yr_lic')
    bt2 = types.InlineKeyboardButton('Физ. лицо', callback_data='fiz_lic')
    markup.add(bt1, bt2)
    bot.send_message(message.chat.id, "Укажите кем вы являетесь", reply_markup=markup)
def join_bd_yr(message): 
    print("Кнопка 'yr_lic' нажимается")  
    global information_yr, all_price, end_choice
    end_choice_1 = str(end_choice)
    information_yr = message.text.strip()
    connection = sqlite3.connect('users_staff.db')
    c = connection.cursor()
    c.execute("INSERT INTO users_yr(name_of_organization, name_of_product, price) VALUES (?, ?, ?)", (information_yr, end_choice_1, all_price))
    connection.commit()
    c.close()
    connection.close()
    print('инфа добавляется')
    bot.send_message(message.chat.id, 'хотите увидеть ваши заказы?')
    bot.register_next_step_handler(message, show_yr)
def show_yr(message):
    print('эта залупа вызывается')
    if message.text == 'да':
        connection = sqlite3.connect('users_staff.db')
        c = connection.cursor()
        c.execute("SELECT * FROM  users_yr")
        yr_data = c.fetchone()
        illi = "" 
        for i in yr_data:
             illi += str(i) 
        connection.close()
        bot.send_message(message.chat.id, illi)
        print("а сюда походу не доставляется")
def join_bd_fiz(message):
    print(f"Received data for юр. лицо: {message.text}")  
    global information_yr, all_price, end_choice
    information_yr = message.text.strip()
    end_choice_2 = str(end_choice)
    connection = sqlite3.connect('users_staff.db')
    c = connection.cursor()
    c.execute("INSERT INTO users_fiz(name_of_organization, name_of_product, price) VALUES (?, ?, ?)", (information_yr, end_choice_2, all_price))
    connection.commit()
    c.close()
    connection.close()
    bot.send_message(message.chat.id, 'хотите увидеть ваши заказы?')
    bot.register_next_step_handler(message, show_fiz)

def show_fiz(message):
    print('эта залупа вызывается')
    if message.text == 'да':
        connection = sqlite3.connect('users_staff.db')
        c = connection.cursor()
        c.execute("SELECT * FROM  users_fiz")
        yr_data = c.fetchone()
        illi = "" 
        for i in yr_data:
             illi += str(i) 
        connection.close()
        bot.send_message(message.chat.id, illi)
        print("а сюда походу не доставляется")

bot.polling() 