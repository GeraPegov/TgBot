import os
import json

import telebot 
import sqlite3 
import toml
from telebot import types
from io import StringIO 
from dotenv import load_dotenv
from pathlib import Path

from database import engine, start_table
from schemasdb import Base

Base.metadata.create_all(bind=engine)

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

env_path = Path(__file__).parent / 'file.env'
if env_path.exists():
    print(f"Файл .env найден по пути: {env_path}")
else:
    print(f"Файл .env не найден! Ожидаемый путь: {env_path}")

load_dotenv(dotenv_path=env_path)
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
ADMIN = os.getenv('ADMIN')

quanity = 0 #ИНДЕКС СПИСКА ПО КЛЮЧУ В СЛОВАРЕ ВЫБОРА ТОВАРА
choice_tovar = None # ЗНАЧЕНИЕ ИЗ СЛОВАРЯ ВЫБОРА ТОВАРА
number_of_list = None # КЛЮЧ ИЗ СЛОВАРЯ ВЫБОРА ТОВАРА
quanity_of_goods = 0 # ВВОД КОЛИЧЕСТВА ТОВАРА 
end_choice = {} # СЛОВАРЬ ДЛЯ ИТОГОВЫХ ЗНАЧЕНИЙ ТОВАРОВ И КОЛИЧЕСТВА
all_price = 0 # ОБЩЕЕ КОЛИЧЕСТВО ТОВАРОВ 
calculation_price_oneproduct = 0 # ЦЕНА ДЛЯ ВЫБРАННОГО КОЛИЧЕСТВА ТОВАРОВ
result_calculation = 0 # ОБЩАЯ ЦЕНА СО ВСЕХ ВЫБРАННЫХ ТОВАРОВ
calculation_price_full = {} # СЛОВАРЬ С КЛЮЧОМ ПО ТОВАРУ И ЗНАЧЕНИЕМ ПО ЦЕНЕ ЗАДАННОГО КОЛИЧЕСТВА ТОВАРА
price_for_admin = 0 # ЦЕНА ЗАКУПА ВЫБРАННОГО ТОВАРА ВЫБРАННОГО КОЛИЧЕСТВА
for_user = 0 # КЛЮЧ = ТОВАР, ЗНАЧЕНИЕ = ЦЕНА И КОЛИЧЕСТВО (ДЛЯ УДОБНОГО ВЫВОДА)
zakup = 0 # СУММИРУЕТ price_for_admin ДЛЯ ИТОГОВОЙ ЦЕНЫ БЕЗ РУССКОГО ПРАЙСА(АПОКВЕЛ И НЕПТРА)
zakup_rus = 0 # СУММИРУЕТ price_for_admin ДЛЯ ИТОГОВОЙ ЦЕНЫ РУССКОГО ПРАЙСА(АПОКВЕЛ И НЕПТРА)
last_id = 0 # ПРИ УДАЛЕНИИ ПОЛЬЗОВАТЕЛЕМ ДАННЫХ




def get_main_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Главное меню'))
    return markup

@bot.message_handler(commands=['start', 'showmeprice', 'deletefulltable'])
def price(message, from_callback = False):
    if message.text == '/start' or from_callback:
        global choice_tovar, number_of_list, calculation_price_full, calculation_price_oneproduct, all_price, end_choice, result_calculation, zakup, zakup_rus
        if from_callback == False:
            calculation_price_full = {}
            calculation_price_oneproduct = 0
            all_price = 0
            end_choice = {}
            result_calculation = 0
            zakup = 0
            zakup_rus = 0
        choice_tovar = None
        number_of_list = None
        
        markup = types.InlineKeyboardMarkup()
        
        bt1 = types.InlineKeyboardButton('ВАКЦИНА', callback_data = 'vakcina')
        bt2 = types.InlineKeyboardButton('КОРМА', callback_data = 'korma')
        bt3 = types.InlineKeyboardButton('ПРЕПАРАТЫ', callback_data = 'preparati')
        markup.add(bt1, bt2, bt3)
        bot.send_message(message.chat.id, 'что вы хотите приобрести?', reply_markup=markup)
    if message.from_user.id in ADMIN:
            if message.text == '/showmeprice':
                exchange_rate = 0.036 # ЦЕНА КУРСА РБ 
                connection = sqlite3.connect('user_staff1.sql')
                c = connection.cursor()
                c.execute("SELECT name_of_organization, name_of_product,  result_calculation_end, admin, admin_rus   FROM user_all1")

                yr_data = c.fetchall()
                table_file = ''
                for i in yr_data: 
                    name, feed, result, admin, admin_rus = i 
                    table_file += "\n\n" + '==НАКЛАДНАЯ==============='+ "\n" + "Наименование организации: " + str(name) + "\n" 
                    table_file += '--------------------------------------------------' + "\n" +'   Добавленные товары:' +  "\n"
                    table_file += '--------------------------------------------------' +  "\n" + "Добавленные товары: " + '\n'.join(feed.split(',')) + "\n"
                    table_file += '--------------------------------------------------' + "\n" + '   Общие показатели:' + "\n"
                    table_file += '--------------------------------------------------' + "\n" + "* Итоговая стоимость: "  + str(result) + ' RUB' + "\n"
                    table_file += '* Цена закупа  РБ: ' + str(admin) + ' BYN' + "\n"  + '* Цена закупа РФ:  ' + str(round((admin/exchange_rate+admin_rus), 2)) + ' RUB' + "\n" 
                    table_file += '* Выгода:  ' + str(round((result-(admin/exchange_rate+admin_rus)), 2)) + ' RUB' + "\n"
                    
                connection.close()
                file_data = StringIO(table_file)
                file_data.name = 'ТАБЛИЦА ЗАКАЗОВ.txt'
                bot.send_document(message.chat.id,  file_data)

            elif message.text == '/deletefulltable':
                connection = sqlite3.connect('user_staff1.sql')
                c = connection.cursor()
                c.execute("DELETE FROM user_all1")
                connection.commit()
                connection.close()



@bot.callback_query_handler(func=lambda call:  True)
def backhome(call):
    global end_choice, all_price, quanity_of_goods, for_user, last_id, number_of_list,  quanity_of_goods, calculation_price_full, result_calculation, calculation_price_oneproduct, choice_tovar, price_for_admin, zakup, for_user, zakup_rus
    if call.data == 'backhome':
        calculation_price_full = {}
        calculation_price_oneproduct = 0
        all_price = 0
        end_choice = {}
        result_calculation = 0
        zakup = 0
        zakup_rus = 0
        price(call.message, from_callback = True)
    elif call.data == 'yes_next':
        end_choice[choice_tovar] = end_choice.get(choice_tovar, for_user)
        all_price += quanity_of_goods
        fiz_yr(call.message)
    elif call.data == 'yes_backhome':
        end_choice[choice_tovar] = end_choice.get(choice_tovar, for_user)
        all_price += quanity_of_goods
        price(call.message, from_callback = True)
    elif call.data == 'yr_lic':
        bot.send_message(call.message.chat.id, 'Введите название клиники, номер телефона по типу +79991112233 и Адрес для доставки')
        bot.register_next_step_handler(call.message, join_bd)
    elif call.data == 'fiz_lic':
        bot.send_message(call.message.chat.id, 'Введите ФИО, номер телефона по типу +79991112233 и Адрес для доставки')
        bot.register_next_step_handler(call.message, join_bd)
    elif call.data == 'vakcina':
        try:
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=None  
            )
        except:
            pass
        msg = bot.send_message(call.message.chat.id, f'Введите номер вакцины: \n{'\n'.join(data['vaccines']['name'])}')
        bot.register_next_step_handler(msg, lambda m: choice_buy(m, category='vakcina'))
    elif call.data == 'preparati':
        try:
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=None  
            )
        except:
            pass
        msg = bot.send_message(call.message.chat.id, f'Введите номер препарата: \n{'\n'.join(data['preparation']['name'])}')
        bot.register_next_step_handler(msg, lambda m: choice_buy(m, category='preparati'))
    elif call.data == 'korma':
        try:
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=None  
            )
        except:
            pass
        msg = bot.send_message(call.message.chat.id, f'Введите номер корма: \n{'\n'.join(data['feed']['name'])}')
        bot.register_next_step_handler(msg, lambda m: choice_buy(m, category='feed'))
    elif call.data == 'end':
        bot.send_message(call.message.chat.id, f"Спасибо за заказ, если хотите начать заново - напишите команду {'/start'}")
    elif call.data == 'delete':
        connection = sqlite3.connect('user_staff1.sql')
        c = connection.cursor()
        c.execute('DELETE FROM user_all1 WHERE id = ?', (last_id,)
        )
        connection.commit()
        c.close()
        connection.close()
        bot.send_message(call.message.chat.id, f"Все ваши записи удалены, если хотите начать заново, напишите команду {'/start'}")

    


def choice_buy(message, category):
# ОБРАБОТКА КЛЮЧА СЛОВАРЕЙ С ТОВАРАМИ
    
    global number_of_list
    try:
        if not message.text.strip().isdigit():
            raise ValueError("Введите номер цифрой")
        number_of_list = int(message.text)

        if category == 'preparati':
            if number_of_list not in data['preparation']['name'] or number_of_list < 1:
                raise IndexError("Неверный номер категории")
            msg = bot.send_message(message.chat.id, f'введите номер препарата: \n{'\n'.join(data['preparation']['name'][number_of_list])}' )
            bot.register_next_step_handler(msg, lambda m: quanity_choice_buy(m, category='preparati'))

        if category == 'vakcina':
            if number_of_list not in data['vaccines']['name']  or number_of_list < 1:
                raise IndexError("Неверный номер категории")
            msg = bot.send_message(message.chat.id, f'введите номер вакцины: \n{'\n'.join(data['vaccines']['name'][number_of_list])}' )
            bot.register_next_step_handler(msg, lambda m: quanity_choice_buy(m, category='vakcina'))

        if category == 'feed':
            if number_of_list not in data['feed']['name']  or number_of_list < 1:
                raise IndexError("Неверный номер категории")
            msg = bot.send_message(message.chat.id, f'введите номер корма: \n{'\n'.join(data['feed']['name'][number_of_list])}' )
            bot.register_next_step_handler(msg, lambda m: quanity_choice_buy(m, category='feed'))
    except ValueError as e:
        msg = bot.send_message(
            message.chat.id,
            f"⚠️ Неверно. Попробуйте еще раз: {e}"
        )
        bot.register_next_step_handler(msg, lambda m: choice_buy(m, category))
    except IndexError as e:
        msg = bot.send_message(
            message.chat.id,
            f"⚠️ Неверно. Попробуйте еще раз: {e}"
        )
        bot.register_next_step_handler(msg, lambda m: choice_buy(m, category))
        
def quanity_choice_buy(message, category):
# ОБРАБОТКА ЗНАЧЕНИЙ ПО КЛЮЧУ ИЗ СЛОВАРЯ С ТОВАРАМИ
    global number_of_list, choice_tovar
    markup_menu = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('В главное меню', callback_data='menu')
    markup_menu.add(bt1)
    try:
        
        if not message.text.strip().isdigit():
            raise ValueError('Введите номер цифрой')
        quanity = int(message.text)

        if category == 'preparati':
            if choice_of_preparati[number_of_list][quanity] not in choice_of_preparati[number_of_list]  or quanity < 1:
                raise IndexError('Неверный номер категории')
            choice_tovar = choice_of_preparati[number_of_list][quanity]
            msg = bot.send_message(message.chat.id, f'Введите количество {choice_tovar[2:]}' )
            bot.register_next_step_handler(msg, quanity_goods)
            
        if category == 'vakcina':
            if data['vaccines']['name'][number_of_list][quanity] not in data['vaccines']['name'][number_of_list] or quanity < 1:
                raise IndexError('Неверный номер категории')
            choice_tovar = data['vaccines']['name'][number_of_list][quanity]
            msg = bot.send_message(message.chat.id, f'Введите количество {choice_tovar[2:]}' )
            bot.register_next_step_handler(msg, quanity_goods)

        if category == 'feed':
            if data['feed']['name'][number_of_list][quanity] not in data['feed']['name'][number_of_list] or quanity < 1:
                raise IndexError('Неверный номер категории')
            choice_tovar = data['feed']['name'][number_of_list][quanity]
            msg = bot.send_message(message.chat.id, f'Введите количество {choice_tovar[2:]}' )
            bot.register_next_step_handler(msg, quanity_goods)

    except ValueError as e:
        msg = bot.send_message(
            message.chat.id,
            f"⚠️ Неверно. Попробуйте еще раз:{e}"
        )
        bot.register_next_step_handler(msg, lambda m: quanity_choice_buy(m, category))
    except IndexError as e:
        msg = bot.send_message(
            message.chat.id,
           f"⚠️ Неверно. Попробуйте еще раз:{e}"
        )
        bot.register_next_step_handler(msg, lambda m: quanity_choice_buy(m, category))






def quanity_goods(message):
# ВВОД КОЛИЧЕСТВА ТОВАРА И ДОБАВЛЕНИЕ В КОРЗИНУ
    global quanity_of_goods, calculation_price_full, result_calculation, calculation_price_oneproduct, choice_tovar, price_for_admin, zakup, for_user, zakup_rus
    try:
        if not message.text.strip().isdigit() and message.text: 
            raise ValueError("Введите количество цифрой")
        if int(message.text) > 1000:
            raise ValueError('Слишком большое значение')
    except ValueError as e:
        msg = bot.send_message(message.chat.id, f"⚠️ Неверно. Попробуйте еще раз: {e}")
        bot.register_next_step_handler(msg, quanity_goods)
        return

    quanity_of_goods = int(message.text)
    if choice_tovar[3:] != "Апоквел 5.4мг" and choice_tovar[3:] !=  "Апоквел 16мг" and choice_tovar[3:] != "Нептра": 
        zakup += round((price_for_admin[choice_tovar[3:]]  * quanity_of_goods), 2)
    else:
        zakup_rus += round((price_for_admin[choice_tovar[3:]]  * quanity_of_goods), 2)
    
price_for_admin
    calculation_price_oneproduct = price_for_product[choice_tovar[3:]] * quanity_of_goods
    for_user = " Количество: " +  str(quanity_of_goods) + ' , ' + " Цена: " +  str(calculation_price_oneproduct)
    result_calculation += calculation_price_oneproduct
    calculation_price_full[choice_tovar[3:]] = calculation_price_full.get(choice_tovar[3:], price_for_product[choice_tovar[3:]] * quanity_of_goods )
    basket = ''
    for i, e in calculation_price_full.items():
        basket += str(i) + ', цена: ' + str(e) + ' RUB' + '\n'
    total_amount = 0
    for i in calculation_price_full:
        total_amount+= calculation_price_full[i]
    

    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('добавить и вернуться к выбору товаров', callback_data='yes_backhome')
    bt2 = types.InlineKeyboardButton('добавить и закончить с выбором товаров', callback_data='yes_next')
    bt3 = types.InlineKeyboardButton('вернуться в начало', callback_data='backhome')
    markup.add(bt1)
    markup.add(bt2)
    markup.add(bt3)
    bot.send_message(message.chat.id, f'Вы выбрали: \n{choice_tovar[3:]}, количество: {quanity_of_goods} \nСтоимость: {calculation_price_oneproduct} RUB \nОставить в корзине? \n\nКорзина: \n{basket} \nОбщая сумма корзины: {total_amount} RUB', reply_markup=markup)

def fiz_yr(message):
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('Юр. лицо', callback_data='yr_lic')
    bt2 = types.InlineKeyboardButton('Физ. лицо', callback_data='fiz_lic')
    markup.add(bt1, bt2)
    bot.send_message(message.chat.id, "Укажите, кем вы являетесь:", reply_markup=markup)

def join_bd(message): 
    global information_yr, all_price, end_choice, calculation_price_full, result_calculation, zakup, zakup_rus, last_id
    end_choice_1 = '' #формат для вывода и добавления имени товара и количества
    for i, e in end_choice.items():
        end_choice_1 += "," '*' + i[3:] + ", " + str(e) + ' RUB'  + "\n"
    information_yr = message.text.strip()
    connection = sqlite3.connect('user_staff1.sql')
    c = connection.cursor()
    c.execute("INSERT INTO user_all1(name_of_organization, name_of_product, price, result_calculation_end, admin, admin_rus) VALUES (?, ?, ?, ?, ?, ?)", (information_yr, end_choice_1, all_price, result_calculation, zakup, zakup_rus))
    last_id = c.lastrowid
    connection.commit()
    c.close()
    connection.close()
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('Удалить все записи', callback_data='delete')
    bt2 = types.InlineKeyboardButton('Закончить', callback_data='end')
    markup.add(bt1, bt2)
    bot.send_message(message.chat.id, f'{information_yr} \nТовары:  \n{" ".join(end_choice_1.split(','))} \nОбщее количество:  {all_price} \nОбщая цена {result_calculation} RUB', reply_markup=markup)




bot.polling() 