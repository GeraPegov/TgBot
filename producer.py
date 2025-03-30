import telebot 
import sqlite3 
from telebot import types
from io import StringIO 





APIBOT = '7973566766:AAFPYQn5qWijn3JepxfWZMvCLpmpenIoi2c' 
bot = telebot.TeleBot(APIBOT)


quanity = 0
choice_user = None
choice_tovar = None
number_of_list = None
number_of_tovar = 0
end_choice = {}
all_price = 0
calculation_price_oneproduct = 0
result_calculation = 0
calculation_price_full = {}
price_for_admin = 0
exchange_rate = 0
admin = 0
profit = 0

name_of_vakcina = ['1. Нобивак', '2. Эурикан', '3. Пуревакс', '4. Биокан', '5. Биофел']
choice_name_vakcina = {
1: ['', '1. Нобивак Dhppi', '2. Нобивак RL', '3. Нобивак Lepto', '4. Нобивак R 1/1', '5. Нобивак R 1/10', '6. Нобивак Tricat', '7. Нобивак KC', '8. Нобивак Puppy'],
2: ['', '1. Эурикан Dhppi-L', '2. Эурикан Rabisin'],
3: ['', '1. Пуревакс RcpCh', '2. Пуревакс Rcp'],
4: ['', '1. Биокан+R', '2. Биокан'],
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
    1: ['', '1. RC Urinary Cat 85g', '2. RC Renal Cat 85g', '3. RC Gastro Cat 85g', '4. RC Gastro MD Cat 85g', '5. RC Recovery ', '6. RC Baby Cat 195g', '7. RC Baby Cat Milk', '8. RC Gastro Puppy 195g', '9. RC Gastro Dog 400g', '10. RC Gastro MD Dog 400g', '11. RC Baby Dog 195g', '12. RC Baby Dog Milk'],
    2: ['', '1. MG Hypo Duck Dog 400g', '2. MG Gastro Dog 400g', '3. MG Urinary Cat 100g', '4. MG Sterile Cat 1,5kg', '5. MG Gastro Dog 2kg', '6. MG Gastro Puppy 1,5kg', '7. MG Gastro Cat 1,5kg']
}


price_for_product = {'Бравекто 2-5': 3500, 'Бравекто 5-10': 3600, 'Бравекто 10-20': 4000, 'Бравекто 20-40': 4300, 'Бравето 40-56': 4600, 'Симпарика 1-2.5': 3100, 'Симпарика 2.5-5': 3450, 'Симпарика 5-10': 3600, 'Симпарика 10-20': 3950, 'Симпарика 20-40': 4300, 'Симпарика 40-60': 4550, 'Нексгард 2-4': 2600, 'Нексгард 4-10': 2900, 'Нексгард 10-25': 3200, 'Нексгард 25-50': 3500, 'Нобивак Dhppi': 1250, 'Нобивак RL': 950, 'Нобивак Lepto': 550, 'Нобивак R 1/1': 650, 'Нобивак R 1/10': 4300, 'Нобивак Tricat': 1800, 'Нобивак KC': 460, 'Нобивак Puppy': 900, 'Эурикан Dhppi-L': 1300, 'Пуревакс RcpCh': 1800, 'Пуревакс Rcp': 1400, 'Эурикан Rabisin': 700, 'Биокан+R': 1200, 'Биокан': 1100, 'Биофел': 1200, 'Биофел+R': 1350, 'Коронакэт 10мг': 2700, 'Коронакэт 30мг': 4600, 'Апоквел 5.4мг': 16000, 'Апоквел 16мг': 22000, 'Кортавет': 1450, 'Нептра': 1700, 'Отоксолан': 1300, 'RC Urinary Cat 85g': 140, 'RC Renal Cat 85g': 140, 'RC Gastro Cat 85g': 140, 'RC Gastro MD Cat 85g': 140, 'RC Recovery ': 210, 'RC Baby Cat 195g': 180, 'RC Baby Cat Milk': 2100, 'RC Gastro Puppy 195g': 210, 'RC Gastro Dog 400g': 290, 'RC Gastro MD Dog 400g': 290, 'RC Baby Dog 195g': 180, 'RC Baby Dog Milk': 2100, 'MG Hypo Duck Dog 400g': 280, 'MG Gastro Dog 400g': 300, 'MG Urinary Cat 100g': 140, 'MG Sterile Cat 1,5kg': 1600, 'MG Gastro Dog 2kg': 2600, 'MG Gastro Puppy 1,5kg': 2100, 'MG Gastro Cat 1,5kg': 2350}

price_for_admin = {'Бравекто 2-5': 96.679, 'Бравекто 5-10': 99.649, 'Бравекто 10-20': 107.569, 'Бравекто 20-40': 119.185, 'Бравето 40-56': 132.319, 'Симпарика 1-2.5': 80.707, 'Симпарика 2.5-5': 94.974, 'Симпарика 5-10': 98.692, 'Симпарика 10-20': 107.998, 'Симпарика 20-40': 121.682, 'Симпарика 40-60': 130.361, 'Нексгард 2-4': 69.839, 'Нексгард 4-10': 76.78, 'Нексгард 10-25': 86.317, 'Нексгард 25-50': 95.777, 'Нобивак Dhppi': 26.422, 'Нобивак RL': 18.293, 'Нобивак Lepto': 8.657, 'Нобивак R 1/1': 12.782, 
'Нобивак R 1/10': 65.34, 'Нобивак Tricat': 33.561, 'Нобивак KC': 7.6978, 'Нобивак Puppy': 12.023, 'Эурикан Dhppi-L': 28.6, 'Пуревакс RcpCh': 48.18, 'Пуревакс Rcp': 35.926, 'Эурикан Rabisin': 12.0, 'Биокан+R': 28.578, 'Биокан': 27.797, 'Биофел': 
25.938, 'Биофел+R': 29.645, 'Коронакэт 10мг': 62.7, 'Коронакэт 30мг': 107.58, 'Апоквел 5.4мг': 15000.00, 'Апоквел 16мг': 21500.00, 'Кортавет': 39.248, 'Нептра': 1250.0, 'Отоксолан': 32.505, 'RC Urinary Cat 85g': 3.762, 'RC Renal Cat 85g': 3.762, 'RC Gastro Cat 85g': 3.762, 'RC Gastro MD Cat 85g': 3.762, 'RC Recovery ': 5.676, 'RC Baby Cat 195g': 4.488, 'RC Baby Cat Milk': 56.628, 'RC Gastro Puppy 195g': 5.676, 'RC Gastro Dog 400g': 8.58, 'RC Gastro MD Dog 400g': 8.58, 'RC Baby Dog 195g': 4.422, 'RC Baby Dog Milk': 60.918, 'MG Hypo Duck Dog 400g': 7.447, 'MG Gastro Dog 400g': 7.7, 'MG Urinary Cat 100g': 3.102, 'MG Sterile Cat 1,5kg': 41.206, 'MG Gastro Dog 2kg': 73.876, 'MG Gastro Puppy 1,5kg': 55.187, 'MG Gastro Cat 1,5kg': 63.58}

connection = sqlite3.connect('user_staff1.sql')
c = connection.cursor()
c.execute("CREATE TABLE IF NOT EXISTS user_all1(id INTEGER PRIMARY KEY, name_of_organization TEXT, name_of_product TEXT, price INTEGER, calculation_price_end TEXT, result_calculation_end INTEGER, admin INTEGER, admin_rus INTEGER, profit INTEGER)")
connection.commit()
c.close()
connection.close()

@bot.message_handler(commands=['start', 'showmeprice', 'deletefulltable'])
def price(message, from_callback = False):
    # try:
    if message.text == '/start' or from_callback:
        print(123456789876543)
        global and_choice, choice_user, choice_tovar, number_of_list, profit
        and_choice = {}
        choice_user = None
        choice_tovar = None
        number_of_list = None
        markup = types.InlineKeyboardMarkup()
        bt1 = types.InlineKeyboardButton('ВАКЦИНА', callback_data = 'vakcina')
        bt2 = types.InlineKeyboardButton('КОРМА', callback_data = 'korma')
        bt3 = types.InlineKeyboardButton('ПРЕПАРАТЫ', callback_data = 'preparati')
        markup.add(bt1, bt2, bt3)
        bot.send_message(message.chat.id, 'что вы хотите приобрести?', reply_markup=markup)
    # except:

    elif message.text == '/showmeprice':
        print('HUI')
        connection = sqlite3.connect('user_staff1.sql')
        c = connection.cursor()
        c.execute("SELECT name_of_organization, name_of_product,  result_calculation_end, admin, admin_rus, profit   FROM user_all1")

        yr_data = c.fetchall()
        lele = ''
        lili = ''
        for i in yr_data: 
            name, feed, result, admin, admin_rus, profit = i 
            lele += "\n\n" + '==НАКЛАДНАЯ==============='+ "\n" + "Наименование организации: " + str(name) + "\n" + '--------------------------------------------------' + "\n" +'   Добавленные товары:' +  "\n" + '--------------------------------------------------' +  "\n" + "Добавленные товары: " + '\n'.join(feed.split(',')) + "\n" + '--------------------------------------------------' + "\n" + '   Общие показатели:' + "\n" + '--------------------------------------------------' + "\n" + "* Итоговая стоимость: "  + str(result) + ' RUB' + "\n" + '* Цена закупа  РБ: ' + str(admin) + ' BYN' + "\n"  + '* Цена закупа РФ:  ' + str(round((admin/0.036+admin_rus), 2)) + ' RUB' + "\n"  + '* Выгода:  ' + str(round((result-(admin/0.036+admin_rus)), 2)) + ' RUB' + "\n"
            
        connection.close()
        file_data = StringIO(lele)
        file_data.name = 'ТАБЛИЦА ЗАКАЗОВ.txt'
        bot.send_document(message.chat.id,  file_data)
    elif message.text == '/deletefulltable':
        print('delete')
        connection = sqlite3.connect('user_staff1.sql')
        c = connection.cursor()
        c.execute("DELETE FROM user_all1")
        connection.commit()
        connection.close()


@bot.callback_query_handler(func=lambda call:  True)
def backhome(call):
    global end_choice, all_price, number_of_tovar, for_user
    if call.data == 'backhome':
        price(call.message, from_callback = True)
    elif call.data == 'yes':
        end_choice[choice_tovar] = end_choice.get(choice_tovar, for_user)
        all_price += number_of_tovar
        fiz_yr(call.message)
    elif call.data == 'yes_backhome':
        end_choice[choice_tovar] = end_choice.get(choice_tovar, for_user)
        all_price += number_of_tovar
        price(call.message, from_callback = True)
    elif call.data == 'yr_lic':
        print("Кнопка 'yr_lic' была нажата")  # Это поможет отследить вызов функции
        bot.send_message(call.message.chat.id, 'Введите название клиники, номер телефона по типу +79991112233 и Адрес для доставки')
        bot.register_next_step_handler(call.message, join_bd_yr)
    elif call.data == 'fiz_lic':
        bot.send_message(call.message.chat.id, 'Введите ФИО, номер телефона по типу +79991112233 и Адрес для доставки')
        bot.register_next_step_handler(call.message, join_bd_fiz)
    elif call.data == 'vakcina':
        bot.send_message(call.message.chat.id, f'Введите номер вакцины: \n{'\n'.join(name_of_vakcina)}')
        bot.register_next_step_handler(call.message, vakcina)
    elif call.data == 'preparati':
        bot.send_message(call.message.chat.id, f'Введите номер препарата: \n{'\n'.join(name_of_preparati)}')
        bot.register_next_step_handler(call.message, preparati)
    elif call.data == 'korma':
        bot.send_message(call.message.chat.id, f'Введите номер корма: \n{'\n'.join(name_of_feed)}')
        bot.register_next_step_handler(call.message, feed)

#ОБРАБОТКА ВАКЦИН

def vakcina(message):
    global choice_user, number_of_list
    try:
        if not message.text.strip().isdigit():
            raise ValueError("Введите номер цифрой")
        number_of_list = int(message.text)
        if number_of_list not in choice_name_vakcina:
            raise IndexError("Неверный номер категории")
        choice_user = choice_name_vakcina[number_of_list]
        bot.send_message(message.chat.id, f'введите номер вакцины: \n{'\n'.join(choice_name_vakcina[number_of_list])}')
        bot.register_next_step_handler(message, quanity_vakcina)
    except ValueError as e:
        msg = bot.send_message(
            message.chat.id,
            "⚠️ Неверно. Попробуйте еще раз:"
        )
        bot.register_next_step_handler(msg, vakcina)
    except IndexError as e:
        msg = bot.send_message(
            message.chat.id,
            "⚠️ Неверно. Попробуйте еще раз:"
        )
        bot.register_next_step_handler(msg, vakcina)
        
def quanity_vakcina(message):
    
    global number_of_list, choice_tovar
    print(choice_name_vakcina[number_of_list])
    try:
        if not message.text.strip().isdigit():
            raise ValueError('Введите номер цифрой')
        quanity = int(message.text)
        if choice_name_vakcina[number_of_list][quanity] not in choice_name_vakcina[number_of_list]:
            raise IndexError('Неверный номер категории')
        choice_tovar = choice_name_vakcina[number_of_list][quanity]
        print(choice_tovar)
        bot.send_message(message.chat.id, f'Введите количество {choice_tovar[2:]}')
        bot.register_next_step_handler(message, end_preparati)
    except ValueError as e:
        msg = bot.send_message(
            message.chat.id,
            "⚠️ Неверно. Попробуйте еще раз:"
        )
        bot.register_next_step_handler(msg, quanity_vakcina)
    except IndexError as e:
        msg = bot.send_message(
            message.chat.id,
            "⚠️ Неверно. Попробуйте еще раз:"
        )
        bot.register_next_step_handler(msg, quanity_vakcina)


    



#ОБРАБОТКА ПРЕПАРАТОВ

def preparati(message):
    global choice_user, number_of_list
    try:
        if not message.text.strip().isdigit():
            raise ValueError()
        number_of_list = int(message.text)
        if number_of_list not in choice_of_preparati:
            raise IndexError()
        choice_user = choice_of_preparati[number_of_list]
        bot.send_message(message.chat.id, f'Введите номер препарата: \n{'\n'.join(choice_of_preparati[number_of_list])}')
        bot.register_next_step_handler(message, quanity_preparati)
    except ValueError as e:
        msg = bot.send_message(message.chat.id, f"⚠️ Неверно. Попробуйте еще раз: ")
        bot.register_next_step_handler(msg, preparati)
    except IndexError as e :
        msg = bot.send_message(message.chat.id, f"⚠️ Неверно. Попробуйте еще раз: ")
        bot.register_next_step_handler(msg, preparati)


def quanity_preparati(message):
    global number_of_list, choice_tovar
    try:
        if not message.text.strip().isdigit():
            raise ValueError() 
        
        quanity = int(message.text)
        if choice_of_preparati[number_of_list][quanity] not in choice_of_preparati[number_of_list]:
            raise IndexError()
        choice_tovar = choice_of_preparati[number_of_list][quanity]
        bot.send_message(message.chat.id, f'Введите количество {choice_tovar[2:]}')
        bot.register_next_step_handler(message, end_preparati)
    except ValueError as e:
        msg = bot.send_message(message.chat.id, f"⚠️ Неверно. Попробуйте еще раз: ")
        bot.register_next_step_handler(msg, quanity_preparati)
    except IndexError as e :
        msg = bot.send_message(message.chat.id, f"⚠️ Неверно. Попробуйте еще раз: ")
        bot.register_next_step_handler(msg, quanity_preparati)









#ОБРАБОТКА КОРМОВ

def feed(message):
    global choice_user, number_of_list
    try:
        if not message.text.strip().isdigit():
            raise ValueError()
        number_of_list = int(message.text)
        if number_of_list not in choice_of_feed:
            raise IndexError()
        choice_user = choice_of_feed[number_of_list]
        bot.send_message(message.chat.id, f'Введите номер корма: \n{'\n'.join(choice_of_feed[number_of_list])}')
        bot.register_next_step_handler(message, quanity_feed)
    except ValueError as e:
        msg = bot.send_message(message.chat.id, f"⚠️ Неверно. Попробуйте еще раз: ")
        bot.register_next_step_handler(msg, feed)
    except IndexError as e :
        msg = bot.send_message(message.chat.id, f"⚠️ Неверно. Попробуйте еще раз: ")
        bot.register_next_step_handler(msg, feed)

def quanity_feed(message):
    global number_of_list, choice_tovar
    try:
        if not message.text.strip().isdigit():
            raise ValueError()
        quanity = int(message.text)
        if choice_of_feed[number_of_list][quanity] not in choice_of_feed[number_of_list]:
            raise IndexError()
        choice_tovar = choice_of_feed[number_of_list][quanity]
        bot.send_message(message.chat.id, f'Введите количество: {choice_tovar[2:]}')
        bot.register_next_step_handler(message, end_preparati)
    except ValueError as e:
        msg = bot.send_message(message.chat.id, f"⚠️ Неверно. Попробуйте еще раз: ")
        bot.register_next_step_handler(msg, quanity_feed)
    except IndexError as e :
        msg = bot.send_message(message.chat.id, f"⚠️ Неверно. Попробуйте еще раз: ")
        bot.register_next_step_handler(msg, quanity_feed)




for_user = 0
zakup = 0
zakup_rus = 0
# ДОБАВЛЕНИЕ В БД 
#добавление в корзину проход дальше или к началу
def end_preparati(message):
    global number_of_tovar, quanity, calculation_price_full, result_calculation, calculation_price_oneproduct, choice_tovar, price_for_admin, exchange_rate, zakup, for_user, zakup_rus
    exchange_rate = 0.036
    number_of_tovar = int(message.text) 
    if choice_tovar[3:] != "Апоквел 5.4мг" and choice_tovar[3:] !=  "Апоквел 16мг" and choice_tovar[3:] != "Нептра": 
        zakup += round((price_for_admin[choice_tovar[3:]]  * number_of_tovar), 2)
    else:
        zakup_rus += round((price_for_admin[choice_tovar[3:]]  * number_of_tovar), 2)
    

    calculation_price_oneproduct = price_for_product[choice_tovar[3:]] * number_of_tovar
    for_user = " Количество: " +  str(number_of_tovar) + ' , ' + " Цена: " +  str(calculation_price_oneproduct)
    print(calculation_price_oneproduct)
    result_calculation += calculation_price_oneproduct
    calculation_price_full[choice_tovar[3:]] = calculation_price_full.get(choice_tovar[3:], price_for_product[choice_tovar[3:]] * number_of_tovar )
    basket = ''
    for i, e in calculation_price_full.items():
        basket += str(i) + ', цена: ' + str(e) + ' RUB' + '\n'
    total_amount = 0
    for i in calculation_price_full:
        total_amount+= calculation_price_full[i]
    

    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('добавить и вернуться к выбору товаров', callback_data='yes_backhome')
    bt2 = types.InlineKeyboardButton('добавить и закончить с выбором товаров', callback_data='yes')
    bt3 = types.InlineKeyboardButton('вернуться в начало', callback_data='backhome')
    markup.add(bt1)
    markup.add(bt2)
    markup.add(bt3)
    bot.send_message(message.chat.id, f'Вы выбрали: \n* {choice_tovar[3:]}, количество: {number_of_tovar} \n$ Стоимость: {calculation_price_oneproduct} RUB \nОставить в корзине? \n\nКорзина: \n{basket} \nОбщая сумма корзины: {total_amount} RUB', reply_markup=markup)
#выбор физ или юр лицо
def fiz_yr(message):
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('Юр. лицо', callback_data='yr_lic')
    bt2 = types.InlineKeyboardButton('Физ. лицо', callback_data='fiz_lic')
    markup.add(bt1, bt2)
    bot.send_message(message.chat.id, "Укажите, кем вы являетесь:", reply_markup=markup)
#добавление в базу данных юр лица
def join_bd_yr(message): 
    print("Кнопка 'yr_lic' нажимается")  
    global information_yr, all_price, end_choice, calculation_price_full, result_calculation, zakup, profit, zakup_rus
    end_choice_1 = ''
    for i, e in end_choice.items():
        end_choice_1 += "," '*' + i[3:] + ", " + str(e) + ' RUB'  + "\n"
    calculation_str = ''
    for i, e in calculation_price_full.items():
        calculation_str += i + "   общая цена:  " + str(e) + '; '
    information_yr = message.text.strip()
    connection = sqlite3.connect('user_staff1.sql')
    c = connection.cursor()
    c.execute("INSERT INTO user_all1(name_of_organization, name_of_product, price, calculation_price_end, result_calculation_end, admin, admin_rus, profit) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (information_yr, end_choice_1, all_price, calculation_str, result_calculation, zakup, zakup_rus, profit))
    connection.commit()
    c.close()
    connection.close()
    print(information_yr, end_choice_1)
    bot.send_message(message.chat.id, f'{information_yr} \nТовары:  \n{" ".join(end_choice_1.split(','))} \nОбщее количество:  {all_price} \nОбщая цена {result_calculation} RUB')
    


def join_bd_fiz(message): 
    print("Кнопка 'yr_lic' нажимается")  
    global information_yr, all_price, end_choice, calculation_price_full, result_calculation, zakup, profit
    end_choice_2 = ''
    for i, e in end_choice.items():
        end_choice_2 += ", " '*' + i[3:] + ", " + str(e)  + ' RUB'  + "\n"
    calculation_str = ''
    for i, e in calculation_price_full.items():
        calculation_str += i + "   общая цена:  " + str(e) + '; '
    print(calculation_str)
    
    information_yr = message.text.strip()
    connection = sqlite3.connect('user_staff1.sql')
    c = connection.cursor()
    c.execute("INSERT INTO user_all1(name_of_organization, name_of_product, price, calculation_price_end, result_calculation_end, admin, profit) VALUES (?, ?, ?, ?, ?, ?, ?)", (information_yr, end_choice_2, all_price, calculation_str, result_calculation, zakup, profit))
    connection.commit()
    c.close()
    connection.close()
    print(information_yr, end_choice_2)
    bot.send_message(message.chat.id, f'{information_yr} \nТовары:  \n{" ".join(end_choice_2.split(','))} \nОбщее количество:  {all_price} \nОбщая цена {result_calculation} RUB')




bot.polling() 