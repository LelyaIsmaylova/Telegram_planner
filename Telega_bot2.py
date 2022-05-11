import telebot                                                                   #библиотека api
from telebot import types                                                        #для указания типов
from Currency import check_dollar, check_euro                                    #проверка курсов валют из другого файла
from Classes import Notification                                                 #введение классов из другого файла
bot = telebot.TeleBot('5230225029:AAEh9WrTNULWtcckpFkRgNiOfX91wshrb-c')          #подключение бота через токен

data = ''
time = ''                                                                        #задаем переменные под редактирование
C = 0                                                                            #counter
Note = []
lnr = range(20)
lnr = [str(i) for i in lnr]
    
@bot.message_handler(commands=['start', 'help'])                                 #задаем команду "старт" и "на помощь"

def start(message):                                                              #стартовое меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)        #клава нужного нам размера
    btn1 = types.KeyboardButton('Расписание')                                    #кнопки
    btn2 = types.KeyboardButton('Курсы валют')
    markup.add(btn1, btn2)                                                       #список кнопок
    msg = bot.send_message(message.chat.id, text='Здравствуйте! Что вы хотите посмотреть?'.format(message.from_user),
                           reply_markup=markup)                                  #приветственное сообщение

@bot.message_handler(content_types=['text'])                                     #дальнейшие варианты ответов


def mainbtns (message):                                                          #основные кнопки
    if (message.text == 'Курсы валют'):                                          
        bot.send_message(message.chat.id, 'Сверяюсь с данными')                  #дабы люди не думали, что бот сломался
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) 
        btn1 = types.KeyboardButton('Редактирование')
        btn2 = types.KeyboardButton('Отправка уведомлений')
        btn3 = types.KeyboardButton('Показать расписание')
        btn4 = types.KeyboardButton('В главное меню')
        markup.add(btn1, btn2, btn3, btn4)
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
        
    elif (message.text == 'Отправка уведомлений'):
        msg = bot.send_message(message.chat.id, 'Извините, данная функция находится в разработке. Мы тоже ждем-не дождемся нового обновления!')  
        
    elif (message.text == 'Удалить'):
        global Note
        counter = 1
        st = ''
        for i in Note:
            st += f'{counter}. {"/".join( [str(i) for i in i.date] )}, {":".join([str(i) for i in i.time])}, {i.notes}\n\n'
            counter += 1
        bot.send_message(message.chat.id, st)   
        msg = bot.send_message(message.chat.id, 'Какое событие вы бы хотели удалить?')
        bot.register_next_step_handler(message, delete1)      

    elif message.text in lnr: 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Событие')
        btn2 = types.KeyboardButton('Время')
        btn3 = types.KeyboardButton('Дата')
        markup.add(btn1, btn2, btn3)               
        bot.send_message(message.chat.id, text = 'Что вы хотите изменить?', reply_markup=markup)
        if (message.text == 'Событие'):
            bot.register_next_step_handler(message, change)
        if (message.text == 'Время'):
            bot.register_next_step_handler(message, change_time)
        if (message.text == 'Дата'):
            bot.register_next_step_handler(message, change_date)
    
        
    elif message.text == 'Изменить':  
        #global Note
        counter = 1
        st = ''
        for i in Note:
            st += f'{counter}. {"/".join( [str(i) for i in i.date] )}, {":".join([str(i) for i in i.time])}, {i.notes}\n\n'
            counter = 1
        bot.send_message(message.chat.id, st)         
        message = bot.send_message(message.chat.id, 'Какое событие вы бы хотели поменять?') 
        if message.text == 'Событие':
            bot.register_next_step_handler(message, change)
        if message.text == 'Время':
            bot.register_next_step_handler(message, change_time)
            
        if message.text == 'Дата':
            bot.register_next_step_handler(message, change_date)      
        
        
    elif message.text == 'Показать расписание':  
        if len(Note) == 0:
            bot.send_message(message.chat.id, text='Извините, но в расписании еще ничего нет')
        else: 
            counter = 1
            st = ''
            for i in Note:
                st += f'{counter}. {"/".join( [str(i) for i in i.date] )}, {":".join([str(i) for i in i.time])}, {i.notes}\n\n'
                counter += 1
            bot.send_message(message.chat.id, st)
            
    else:
        bot.send_message(message.chat.id, text='Я вас не понимаю. Что вы хотите сделать?')
  
        
def get_date(message):                                                           #функция задает дату события
    global date                                                                  #глобальная переменная(из списка выше)
    date = message.text.split('/')                                               #сплитим циферки, удаляем /
    date = [int(i) for i in date]                                                #список дат
    bot.send_message(message.chat.id, 'На какое время запланировано событие? Введите его в формате ЧЧ:ММ')
    bot.register_next_step_handler(message, get_time)                            #к следующему шагу
    
    
def get_time(message):                                          
    global time
    time = message.text.split(':')
    time = [int(i) for i in time] 
    bot.send_message(message.chat.id, 'Сделайте заметку о событии в любом удобном вам формате')
    bot.register_next_step_handler(message, get_notes)        
         
        
def get_notes(message):
    global time, notes, C, Note
    notes = message.text
    Note.append(Notification(date, time, notes, C))                              #вводим класс заметок
    C +=1                                                                        #индекс события
    snm(Note[-1])


def delete1(message):                                                            #функция запроса на удаление
    global Note
    
    msg = bot.send_message(message.chat.id,'Подтвердите объект для удаления (Attention: команда all предназначена для удаления всего):')
    bot.register_next_step_handler(msg, delete2)
 
    
def delete2(message):                                                            #функция удаления
    global Note, C
    n = message.text
    if n == 'all':
        Note = []
        C = 0
        
    else:
        n = int(n)
        if n < 0 or n > len(Note):
            bot.send_message(message.chat.id,'Вы наделали что-то странное, такого номера не существует')
        else:
            del Note[C-1]
            for i in range(C-1, len(Note)-1):
                Note[i].ind -= 1
            

def change2(message):
    global Note, n                                                               #публикация переменной n
    n = int(message.text)
    if n > 0 and n <= len(Note):
        msg = bot.send_message(message.chat.id,'Напишите заметку к новому событию')
        bot.register_next_step_handler(msg, change3)    
    
    
def change3(message):
    global Note, n
    Note[n-1].notes = message.text
    

def change(message):
    global Note, n
    msg = bot.send_message(message.chat.id, "Введите номер изменяемого атрибута")    



def change2_date(message):
    global Note, n
    n = int(message.text)
    if n > 0 and n <= len(Note):
        msg = bot.send_message(message.chat.id,'Обозначьте новую дату, соответствующую данному событию')
        bot.register_next_step_handler(msg, change3_date)      

def change3_date(message):
    global Note, n
    Note[n-1].date = message.text.split('/')
    Note[n-1].date = [int(i) for i in Note[n-1].date] 
    

def change_date(message):
    global Note, n
    msg = bot.send_message(message.chat.id, "Введите номер изменяемого атрибута")
  
    
def change2_time(message):
    global Note, n                                                               
    n = int(message.text)
    if n > 0 and n <= len(Note):
        msg = bot.send_message(message.chat.id,'Обозначьте новое время, соответствующую данному событию')
        bot.register_next_step_handler(msg, change3_time)      


def change3_time(message):
    global Note, n
    Note[n-1].time = message.text.split(':')
    Note[n-1].time = [int(i) for i in Note[n-1].time] 


def change_time(message):
    global Note, n
    msg = bot.send_message(message.chat.id, "Введите номер изменяемого атрибута")
    
    
def snm(sm):
    t = (sm.date[2], sm.date[1], sm.date[0], )

    
bot.polling(none_stop=True)
