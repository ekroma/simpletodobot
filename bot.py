import telebot
from telebot import types


token='Ваш токен'
bot=telebot.TeleBot(token)
adding_task = False

class ToDoList():
    def __init__(self):
        self.tasks = []

    def add_task(self,task):
        self.tasks.append(task)

    def remove_task(self,task):
        self.tasks.remove(task)

    def list_of_tasks(self):
        return self.tasks

todo = ToDoList()

@bot.message_handler(commands=['start'])
def start_message(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='список задач')
    btn2 = types.KeyboardButton(text='добавить задачу')
    kb.add(btn1,btn2)
    bot.send_message(message.chat.id, 'Привет',
        reply_markup=kb)


@bot.message_handler(content_types=['text'])
def get_text(message):
    global adding_task
    if adding_task:
        todo.add_task(message.text)
        bot.send_message(message.chat.id, 'Задача добавлена в ToDoList')
        adding_task = False

    if message.text == 'добавить задачу':
        bot.send_message(message.chat.id, 'Введите задачу')
        adding_task = True

    elif message.text == 'список задач':
        if todo.list_of_tasks() == []:
            bot.send_message(message.chat.id, 'У вас пока нет задач')
            return


        for i in todo.list_of_tasks():
            markup_inline = types.InlineKeyboardMarkup()
            item = types.InlineKeyboardButton(text='Завершить',callback_data=i)
            markup_inline.row(item)
            bot.send_message(message.chat.id, i,
                reply_markup=markup_inline)

@bot.callback_query_handler(func=lambda call: True)
def complete(call):
    todo.remove_task(call.data)
    bot.send_message(call.message.chat.id, 'Задача завершена')
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)


bot.infinity_polling()
