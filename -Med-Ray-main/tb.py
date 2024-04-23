import telebot
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import webbrowser
TOKEN = "7101042755:AAGrbtSaiGPZyMiNQ091AZsTN-k3Unv1efo"
user_basket ={}
def show_good(message,key):
    murkup = InlineKeyboardMarkup()
    button1=InlineKeyboardButton('добавить в корзину',callback_data=f"add_to_basket {key}")
    button2=InlineKeyboardButton("перейти в корзину", callback_data='basket')
    murkup.row(button1,button2)
    item=goods_data['goods'][key]
    bot.send_photo(message.chat.id, open(item['photo'], 'rb'), caption=f'{key}\nгод производства:{item["harvest"]}\nV={item["container"]}\n цена:{item["price"]}',reply_markup=murkup)
user_basket[''] = {}
def show_basket(message, name):
    if name in user_basket:
        for i in user_basket[name]:
            bot.send_message(message.chat.id, f'{i}\nгод производства:{user_basket[name][i]["harvest"]}\nV={user_basket[name][i]["container"]}\n цена:{user_basket[name][i]["price"]}\nзаказано:{user_basket[name][i]["quantity"]}')
    else:
        bot.send_message(message.chat.id, 'Ваша корзина пуста!')
def file_read(file_name):
    try:
        with open(file_name,"r",encoding="utf-8") as file:
            data = goods_data.json.load(file)
    except FileNotFoundError:
        data = {"не определен"}
    return data
goods_data = file_read("goods_data.json")
print(goods_data)
bot = telebot.TeleBot(TOKEN)
def menu():
    keyboard = telebot.types.ReplyKeyboardMarkup( row_width=4, resize_keyboard=True, one_time_keyboard=True)
    button1 = telebot.types.KeyboardButton("Полка с товарами")
    button2 = telebot.types.KeyboardButton("Корзина")
    button3 = telebot.types.KeyboardButton("На сайт")
    button4 = telebot.types.KeyboardButton("Доставка")
    button5 = telebot.types.KeyboardButton("Оформить заказ")
    keyboard.add(button1, button2, button3, button4, button5)
    return keyboard
@bot.message_handler(commands=["start"])
def handle_start(message):
    print(message.text)
    global user_name
    user_name=f'{message.from_user.first_name} {message.from_user.last_name}'
    bot.send_message(message.chat.id, f"Уважаемый {user_name}, добро пожаловать в телеграмм бот сайта Медовый Рай!", reply_markup=menu())
@bot.message_handler(commands=["help"])
def handle_start(message):
    bot.send_message(message.chat.id, message)
@bot.message_handler(content_types=['text'])
def handle_all(message):
    if message.text=='Корзина':
        if len(user_basket)==0:
            bot.send_message(message.chat.id, 'Ваша карзина пуста!\nПерейдите в раздел "Полка с товарами"')
        else:
            show_basket(message, user_name)
    if message.text == 'Полка с товарами':
        for item in goods_data["goods"]:
            show_good(message,item)
    if message.text == 'Оформить заказ':
        if len(user_basket) == 0:
            bot.send_message(message.chat.id, 'Ваша карзина пуста!\nПерейдите в раздел "Полка с товарами"')
        else:
            bot.send_message(message.chat.id,'Укажите ваш телефон')
            bot.register_next_step_handler_by_chat_id(message.chat.id,change(), name,quantity)
    if message.text == 'На сайт':
        bot.reply_to(message, f' {message.text}')
        webbrowser.open('https://google.com')
    if message.text == 'Доставка':
        bot.reply_to(message, "Перейдите в корзину, оформите заказ. Обязательно укажите ваш телефон для связи")
        print(f'you chose {message.text}')
@bot.callback_query_handler(func = lambda calback:True)
def callback_message(calback):
    if 'add_to_basket' in  calback.data:
        key=calback.data.replace("add_to_basket ","")
        if len(user_basket)==0:
            user_basket[f'{user_name}']={}
        if not key in user_basket[f'{user_name}']:
            user_basket[f'{user_name}'][key]=goods_data['goods'][key]
            user_basket[f'{user_name}'][key]['quantity']=1
        else:
            user_basket[f'{user_name}'][key]['quantity'] += 1
    if calback.data=="basket":
        bot.send_message(calback.message.chat.id, '<b><u>Вы в корзине</u></b>',parse_mode='html')
        show_basket(calback.message, user_name)
        show_basket(message,calback.message)
@bot.message_handler()
def handle_all(message):
     print(message.text)
     if "купить" == message.text:
         bot.send_message(message.chat.id, "Что купить хотите?", reply_markup=menu)
         bot.register_next_step_handler(message, lambda message: by(message,x=2))
     elif "информация" == message.text:
         bot.send_message(message.chat.id, "Выберите продукт у которого хотите узнать информацию", reply_markup=menu)
         bot.register_next_step_handler(message, lambda message: by(message,x=1))
def by(item, x):
         if x == 2:
             if item.text == 'Липовый Мед':
                 print(f"Вы заказали {item}")
                 bot.send_message(item.chat.id, f"Вы выбрали {item.text}")
             if item.text == 'Цветочный Мед':
                 print(f"Вы заказали {item}")
                 bot.send_message(item.chat.id, f"Вы выбрали {item.text}")
             if item.text == 'Сотовый Мед':
                 print(f"Вы заказали {item}")
                 bot.send_message(item.chat.id, f"Вы выбрали {item.text}")
             if item.text == 'Настойка восковой моли':
                 print(f"Вы заказали {item}")
                 bot.send_message(item.chat.id, f"Вы выбрали {item.text}")
         if x == 1:
             if item.text == 'Липовый Мед':
                 print(f"Вы выбрали информацию у {item}")
                 bot.send_message(item.chat.id,
                                  f"Вы выбрали информацию у {item.text}  \n цена: {goods_data[item.text]['price1']} \n объем: {goods_data[item.text]['V']} \n информация: {goods_data[item.text]['info']} ")
             if item.text == 'Цветочный Мед':
                 print(f"Вы выбрали информацию у {item}")
                 bot.send_message(item.chat.id,
                                  f"Вы выбрали информацию у {item.text} \n цена: {goods_data[item.text]['price2']} \n объем: {goods_data[item.text]['V1']} \n информация: {goods_data[item.text]['info1']} ")
             if item.text == "Сотовый Мед":
                 print(f"Вы выбрали информацию у {item}")
                 bot.send_message(item.chat.id,
                                  f"Вы выбрали информацию у {item.text} \n цена: {goods_data[item.text]['price3']} \n объем: {goods_data[item.text]['V2']} \n информация: {goods_data[item.text]['info2']} ")
             if item.text == 'Настойка восковой моли':
                 print(f"Вы выбрали информацию у {item}")
                 bot.send_message(item.chat.id,f"Вы выбрали информацию у {item.text} \n цена: {goods_data[item.text]['price4']} \n объем: {goods_data[item.text]['V3']} \n информация: {goods_data[item.text]['info3']} ")
def write_to_support(update, context):
     chat_id = update.effective_chat.id
     if update.message.text == 'Написать пасечнику':
         bot.send_message(chat_id, 'Введите своё имя')
         users[chat_id] = {}
bot.register_next_step_handler(update, save_username)
def save_username(update, context):
     username = update.message.text
     users[update.effective_chat.id]['username'] = username
     bot.send_message(update.effective_chat.id, 'Спасибо! Теперь я могу обращаться к вам по имени. Что бы вы хотели обсудить?')
     bot.register_next_step_handler(update, write_message)
def write_message(update, context):
     content = update.message.text
     users[update.effective_chat.id]['content'] = content
     bot.send_message(update.effective_chat.id, 'Отлично! Ваше сообщение было отправлено пасечнику. Он свяжется с вами в ближайшее время.')
     bot.register_next_step_handler(update, handle_next_step)
def handle_next_step(update, context):
     if update.message.text == 'Что дальше?':
         keyboard = InlineKeyboardMarkup([[InlineKeyboardButton('Следующий шаг', callback_data='next_step')]])
         bot.send_message(update.effective_chat.id, "Что дальше?", reply_markup=keyboard)
     bot.message_handler(commands=['begin'])(write_to_support)
bot.polling()
