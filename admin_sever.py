import os
import psutil
import telebot
from settings import *
from datetime import datetime
import subprocess

#def message_handler(hadle_log):
#    hadle_log()

# hadle_log = message_handler(hadle_log) - Жи есть декоратор


bot = telebot.TeleBot(token)
START = "Добро пожаловать в админ-панель сервера"
HELP = "/startserver - Запуск сервера\n" \
       "/stopserver - Выключение сервера\n" \
       "/loadcpu - Информация о загрузке процессора и оперативной памяти\n" \
       "/log - Отправляет лог-файл сервера за сегодняшний день\n" \
       # "/map - Смена карты\n" \
       # "/kick -  Кикнуть игрока\n" \
       # "/ban - Выдать БАН игроку\n" \
       # "/rcon - rcon-консоль сервера\n"
LOG = "Используйте /log today - Для получение лог-файла за сегодняшний день\n" \
      "или\n" \
      "/log ММ-ДД-ГГ, для получение лог-файла за определенный день. например: /log 05-13-17\n"

def log(message, answer):
    file_log = open("bot.log", 'a')
    file_log.writelines(str(datetime.now()) + " " + "Сообщение от: {0} {1}. (id = {2}) Текст:{3} \n".format(message.from_user.first_name,
                                                                   message.from_user.last_name,
                                                                   str(message.from_user.id),
                                                                   message.text))
    print((str(datetime.now()) + " " + "Сообщение от: {0} {1}. (id = {2}) Текст: {3} \n".format(message.from_user.first_name,
                                                                   message.from_user.last_name,
                                                                   str(message.from_user.id),
                                                                   message.text)))

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, HELP)
    answer = HELP
    log(message,answer)


@bot.message_handler(commands=["start"])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row("/startserver", "/stopserver", "/loadcpu")
    user_markup.row ("/log", "/map", "/kick", "/ban", "/rcon", "/help")
    bot.send_message(message.from_user.id, START, reply_markup=user_markup)
    answer = START
    log(message, answer)

@bot.message_handler(commands=['startserver'])
def handle_startsrv(message):
    run_server()
    strserv = "Сервер запущен"
    bot.send_message(message.chat.id, strserv)
    log(message, strserv)

@bot.message_handler(commands=['stopserver'])
def handle_stopsrv(message):
    stpserv = "Сервер выключен"
    subprocess.call("Taskkill /F /IM srcds.exe")
    bot.send_message(message.chat.id, stpserv)
    log(message, stpserv)

@bot.message_handler(commands=['loadcpu'])
def handle_cpu(message):
    cpu = psutil.cpu_percent(interval=3)
    ram = psutil.virtual_memory()
    cpu_log = "Процент использования CPU: " + str(cpu) + "% "  + "Процент использования RAM: " + str(ram.percent) + "%"
    bot.send_message(message.chat.id, cpu_log)
    log(message, cpu_log)

@bot.message_handler(commands=['log'])
def handle_log(message):
    if len(message.text) < 13:
        if message.text == '/log today':
            my_date = datetime.today()
            dt = datetime.strftime(my_date, "%m-%d-%y")
            answer = "Отправка лог-файла за " + dt
            log(message, answer)
            os.chdir(pathLog)
            logf = open(dt + ".txt", "rb")
            bot.send_chat_action(message.chat.id, "upload_document")
            bot.send_document(message.chat.id, logf)
        bot.send_message(message.chat.id, LOG)
        log(message, LOG)
    elif len(message.text) == 13:
        command = message.text
        textdata = command.split(' ')
        data = textdata[1]
        answer = "Отправка лог-файла за " + data
        log(message, answer)
        os.chdir(pathLog)
        logf = open(data + ".txt", "rb")
        bot.send_chat_action(message.chat.id, "upload_document")
        bot.send_document(message.chat.id, logf)

# @bot.message_handler(commands=['map'])
# def handle_map(message):
#     arg = "users"
#     bot.send_message(message.chat.id, "Тест")


def run_server():
    os.chdir(newpath)
    PIPE = subprocess.PIPE
    Popen = subprocess.Popen
    process = Popen(r"newstart.bat", stdin=PIPE, stdout=PIPE)



bot.polling(none_stop=True, interval=0)
input()


def main():
    pass

if __name__ == '__main__':
    main()
