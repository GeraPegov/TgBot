import telebot 
import sqlite3 
from telebot import types
from io import StringIO 
import os
from dotenv import load_dotenv
from pathlib import Path
env_path = Path(__file__).parent / 'api.env'

if env_path.exists():
    print(f"Файл .env найден по пути: {env_path}")
else:
    print(f"Файл .env не найден! Ожидаемый путь: {env_path}")

load_dotenv(dotenv_path=env_path)
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)



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
    7: ['', '1. Нептра'],
    8: ['', '1. Отоксолан']
}

name_of_feed = ['1. Royal Canin', '2. Monge']
choice_of_feed = {
    1: ['', '1. RC Urinary Cat 85g', '2. RC Renal Cat 85g', '3. RC Gastro Cat 85g',
            '4. RC Gastro MD Cat 85g', '5. RC Recovery ', '6. RC Baby Cat 195g', '7. RC Baby Cat Milk',
            '8. RC Gastro Puppy 195g', '9. RC Gastro Dog 400g', '10.RC Gastro MD Dog 400g', '11.RC Baby Dog 195g', '12.RC Baby Dog Milk'],
    2: ['', '1. MG Hypo Duck Dog 400g', '2. MG Gastro Dog 400g', '3. MG Urinary Cat 100g', '4. MG Sterile Cat 1,5kg',
            '5. MG Gastro Dog 2kg', '6. MG Gastro Puppy 1,5kg', '7. MG Gastro Cat 1,5kg']
}


price_for_product = {
    'Бравекто 2-5': 3500, 'Бравекто 5-10': 3600, 'Бравекто 10-20': 4000, 'Бравекто 20-40': 4300, 'Бравето 40-56': 4600,
    'Симпарика 1-2.5': 3100, 'Симпарика 2.5-5': 3450, 'Симпарика 5-10': 3600, 'Симпарика 10-20': 3950, 'Симпарика 20-40': 4300,
    'Симпарика 40-60': 4550, 'Нексгард 2-4': 2600, 'Нексгард 4-10': 2900, 'Нексгард 10-25': 3200, 'Нексгард 25-50': 3500, 'Нобивак Dhppi': 1250,
    'Нобивак RL': 950, 'Нобивак Lepto': 550, 'Нобивак R 1/1': 650, 'Нобивак R 1/10': 4300, 'Нобивак Tricat': 1800, 'Нобивак KC': 460,
    'Нобивак Puppy': 900, 'Эурикан Dhppi-L': 1300, 'Пуревакс RcpCh': 1800, 'Пуревакс Rcp': 1400, 'Эурикан Rabisin': 700, 'Биокан+R': 1200,
    'Биокан': 1100, 'Биофел': 1200, 'Биофел+R': 1350, 'Коронакэт 10мг': 2700, 'Коронакэт 30мг': 4600, 'Апоквел 5.4мг': 16000,
    'Апоквел 16мг': 22000, 'Кортавет': 1450, 'Нептра': 1700, 'Отоксолан': 1300, 'RC Urinary Cat 85g': 140, 'RC Renal Cat 85g': 140,
    'RC Gastro Cat 85g': 140, 'RC Gastro MD Cat 85g': 140, 'RC Recovery ': 210, 'RC Baby Cat 195g': 180, 'RC Baby Cat Milk': 2100,
    'RC Gastro Puppy 195g': 210, 'RC Gastro Dog 400g': 290, 'RC Gastro MD Dog 400g': 290, 'RC Baby Dog 195g': 180, 'RC Baby Dog Milk': 2100,
    'MG Hypo Duck Dog 400g': 280, 'MG Gastro Dog 400g': 300, 'MG Urinary Cat 100g': 140, 'MG Sterile Cat 1,5kg': 1600, 'MG Gastro Dog 2kg': 2600,
    'MG Gastro Puppy 1,5kg': 2100, 'MG Gastro Cat 1,5kg': 2350
}

price_for_admin = {
    'Бравекто 2-5': 0, 'Бравекто 5-10': 0, 'Бравекто 10-20': 0, 'Бравекто 20-40': 0, 'Бравето 40-56': 0,
    'Симпарика 1-2.5': 0, 'Симпарика 2.5-5': 0, 'Симпарика 5-10': 0, 'Симпарика 10-20': 0, 'Симпарика 20-40': 0,
    'Симпарика 40-60': 0, 'Нексгард 2-4': 0, 'Нексгард 4-10': 0, 'Нексгард 10-25': 0, 'Нексгард 25-50': 0, 'Нобивак Dhppi': 0,
    'Нобивак RL': 0, 'Нобивак Lepto': 0, 'Нобивак R 1/1': 0, 'Нобивак R 1/10': 0, 'Нобивак Tricat': 0, 'Нобивак KC': 0, 'Нобивак Puppy': 0,
    'Эурикан Dhppi-L': 0, 'Пуревакс RcpCh': 0, 'Пуревакс Rcp': 0, 'Эурикан Rabisin': 0, 'Биокан+R': 0, 'Биокан': 0, 'Биофел': 0, 'Биофел+R': 0,
    'Коронакэт 10мг': 0, 'Коронакэт 30мг': 0, 'Апоквел 5.4мг': 0, 'Апоквел 16мг': 0, 'Кортавет': 0, 'Нептра': 0, 'Отоксолан': 0, 'RC Urinary Cat 85g': 0,
    'RC Renal Cat 85g': 0, 'RC Gastro Cat 85g': 0, 'RC Gastro MD Cat 85g': 0, 'RC Recovery ': 0, 'RC Baby Cat 195g': 0, 
    'RC Baby Cat Milk': 0, 'RC Gastro Puppy 195g': 0, 'RC Gastro Dog 400g': 0, 'RC Gastro MD Dog 400g': 0, 'RC Baby Dog 195g': 0, 'RC Baby Dog Milk': 0,
    'MG Hypo Duck Dog 400g': 0, 'MG Gastro Dog 400g': 0, 'MG Urinary Cat 100g': 0, 'MG Sterile Cat 1,5kg': 0, 'MG Gastro Dog 2kg': 0, 'MG Gastro Puppy 1,5kg': 0,
     'MG Gastro Cat 1,5kg': 0}

connection = sqlite3.connect('user_staff1.sql')
c = connection.cursor()
c.execute("CREATE TABLE IF NOT EXISTS user_all1(id INTEGER PRIMARY KEY AUTOINCREMENT, name_of_organization TEXT, name_of_product TEXT, price INTEGER, result_calculation_end INTEGER, admin INTEGER, admin_rus INTEGER, profit INTEGER)")
connection.commit()
c.close()
connection.close()

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
        msg = bot.send_message(call.message.chat.id, f'Введите номер вакцины: \n{'\n'.join(name_of_vakcina)}')
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
        msg = bot.send_message(call.message.chat.id, f'Введите номер препарата: \n{'\n'.join(name_of_preparati)}')
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
        msg = bot.send_message(call.message.chat.id, f'Введите номер корма: \n{'\n'.join(name_of_feed)}')
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
            if number_of_list not in choice_of_preparati or number_of_list < 1:
                raise IndexError("Неверный номер категории")
            msg = bot.send_message(message.chat.id, f'введите номер препарата: \n{'\n'.join(choice_of_preparati[number_of_list])}' )
            bot.register_next_step_handler(msg, lambda m: quanity_choice_buy(m, category='preparati'), )

        if category == 'vakcina':
            if number_of_list not in choice_name_vakcina  or number_of_list < 1:
                raise IndexError("Неверный номер категории")
            msg = bot.send_message(message.chat.id, f'введите номер вакцины: \n{'\n'.join(choice_name_vakcina[number_of_list])}' )
            bot.register_next_step_handler(msg, lambda m: quanity_choice_buy(m, category='vakcina'))

        if category == 'feed':
            if number_of_list not in choice_of_feed  or number_of_list < 1:
                raise IndexError("Неверный номер категории")
            msg = bot.send_message(message.chat.id, f'введите номер корма: \n{'\n'.join(choice_of_feed[number_of_list])}' )
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
            if choice_name_vakcina[number_of_list][quanity] not in choice_name_vakcina[number_of_list] or quanity < 1:
                raise IndexError('Неверный номер категории')
            choice_tovar = choice_name_vakcina[number_of_list][quanity]
            msg = bot.send_message(message.chat.id, f'Введите количество {choice_tovar[2:]}' )
            bot.register_next_step_handler(msg, quanity_goods)

        if category == 'feed':
            if choice_of_feed[number_of_list][quanity] not in choice_of_feed[number_of_list] or quanity < 1:
                raise IndexError('Неверный номер категории')
            choice_tovar = choice_of_feed[number_of_list][quanity]
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