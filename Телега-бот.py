import telebot
from telebot import types                                                        #для указания типов
from Currency import check_dollar, check_euro                                    #проверка курсов валют

bot = telebot.TeleBot('5230225029:AAEh9WrTNULWtcckpFkRgNiOfX91wshrb-c')          #подключение бота через токен

data = ''
time = ''                                                                        #задаем переменные под редактирование
C = 0                                                                            #counter
Note = []
    
@bot.message_handler(commands=['start', 'help'])                                 #задаем команду "старт" и "на помощь"

def start(message):                                                              #стартовое меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)        #клава нужного нам размера
    btn1 = types.KeyboardButton('Расписание')                                    #кнопки
    btn2 = types.KeyboardButton('Курсы валют')
    markup.add(btn1, btn2)                                                       #список кнопок
    msg = bot.send_message(message.chat.id, text='Здравствуйте! Что вы хотите посмотреть?'.format(message.from_user),
                           reply_markup=markup)                                  #приветственное сообщение

@bot.message_handler(content_types=['text'])                                     #дальнейшие варианты ответов


def mainbtns (message):
    if (message.text == 'Курсы валют'):
        bot.send_message(message.chat.id, 'Сверяюсь с данными')
        bot.send_message(message.chat.id, f'<b>Курс доллара:</b> {check_dollar()} <b>\nКурс евро:</b> {check_euro()}', parse_mode='html')   #добавляем фичу из htlm(форматирование)
        
        
    elif (message.text == 'Расписание'):                                         
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)    
        btn1 = types.KeyboardButton('Редактирование')
        btn2 = types.KeyboardButton('Отправка уведомлений')
        btn3 = types.KeyboardButton('Показать расписание')
        btn4 = types.KeyboardButton('В главное меню')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Жду ваших действий', reply_markup=markup)
        
    elif (message.text == 'Редактирование'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) 
        btn1 = types.KeyboardButton('Добавить')
        btn2 = types.KeyboardButton('Изменить')
        btn3 = types.KeyboardButton('Удалить')
        btn4 = types.KeyboardButton('Назад')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=markup)
        
    elif (message.text == 'Назад'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1) 
        btn1 = types.KeyboardButton('Редактирование')
        btn2 = types.KeyboardButton('Отправка уведомлений')
        btn3 = types.KeyboardButton('В главное меню')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'Жду ваших действий', reply_markup=markup)        

    elif (message.text =='В главное меню'):                                   
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Расписание')
        btn2 = types.KeyboardButton('Курсы валют')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text='Вы вернулись в главное меню. Что вы хотите посмотреть?', reply_markup=markup)
        
    elif (message.text == 'Добавить'):
        msg = bot.send_message(message.chat.id, 'На какую дату запланировано событие? Введите её в формате ДД/ММ/ГГГГ')
        bot.register_next_step_handler(message, get_date)
        bot.send_message(message.chat.id, 'На какое время запланировано событие? Введите его в формате ЧЧ:ММ')
        bot.register_next_step_handler(message, get_time)         
        bot.send_message(message.chat.id, 'Сделайте заметку о событии в любом удобном вам формате')
        bot.register_next_step_handler(message, get_notes)  
        
    elif (message.text == 'Удалить'):
        msg = bot.send_message(message.chat.id, 'Какое событие вы бы хотели удалить?')
        bot.register_next_step_handler(message, delete1)
        
    elif (message.text == 'Изменить'):     
        bot.send_message(message.chat.id, 'Какое событие вы бы хотели поменять?', reply_markup=markup)        
        bot.register_next_step_handler(message, change)
    
    else:
        bot.send_message(message.chat.id, text='Я вас не понимаю. Что вы хотите сделать?')
        
def get_date(message):   
    global date
    date = message.text.split('/')
    date = [int(i) for i in date]
    
    
def get_time(message):                                          
    global time
    time = message.text.split(':')
    time = [int(i) for i in time]   
    
    
def get_notes(message):
    global notes, C
    notes = message.text
    notes = [str(i) for i in notes]
    Note.append(Notification(date, time, notes, C))
    C +=1
    

def delete1(message):
    global Note
    bot.send_message(message.chat.id, f'Выберите номер объетка для удаления(all для удаления всего):')
    toprint = []
    for i in Note:
        toprint.append(i.date)
        toprint.append(i.time)
        toprint.append(i.notes)
        toprint.append('\n\n')
    msg = bot.send_message(message.chat.id, f'1. {*toprint}')
    bot.register_next_step_handler(msg, delete2)
    
def delete2(message):
    global Note
    n = messege.text
    if n == 'all':
        Note = []
        C = 0
    
    
def change():
    
    
    
 

bot.polling(none_stop=True)


markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn1 = types.KeyboardButton('Время')
btn2 = types.KeyboardButton('Дату')
markup.add(btn1, btn2)        