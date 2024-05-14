from telegram.ext import Application, MessageHandler, CommandHandler, filters, ConversationHandler
from telegram import ReplyKeyboardMarkup

from key import BOT_TOKEN

import sqlite3
import pandas as pd

username = None
LOGIN = 0

bd = sqlite3.connect("database/database.sqlite")
cursor = bd.cursor()


async def start(update, context):

    print(update.message.chat.first_name, update.message.chat.username, update.message.text)

    await update.message.reply_text("Привет, дорогой пользователь! \n"
                                    "Это бот поможет вам получить доступ к своей ведомости! \n"
                                    "Войдите в свой аккаунт чтобы пользоваться ботом! Для этого нажмите /login. \n"
                                    "Для получения больше информации используйте команду /info. \n"
                                    "Если вам нужно помощь нажмите /help. \n",
                                    reply_markup=markup_login)


async def info(update, context):

    print(update.message.chat.first_name, update.message.chat.username, update.message.text)

    await update.message.reply_text("С помощью этого бота вы сможете просмотреть свою ведомость. \n"
                                    "Чтобы пользоваться ботом вам нужен свой индивидуальный логин. \n"
                                    "/login - с помощью этой команды вы сможете войти в свой логин. \n"
                                    "/seminar - ведомость семинара \n"
                                    "/lecture - ведомость лекции \n")


async def hel_p(update, context):

    print(update.message.chat.first_name, update.message.chat.username, update.message.text)

    await update.message.reply_text("Если у вас нет логина, или другие проблемы то напишите "
                                    "своему администратору @journa1_bot")


async def login_start(update, context):

    print(update.message.chat.first_name, update.message.chat.username, update.message.text)

    await update.message.reply_text("Введите логин для авторизации, или /cancel чтобы отменить",
                                    reply_markup=markup_cancel)
    return LOGIN


async def register(update, context):
    global username

    login = update.message.text

    print(update.message.chat.first_name, update.message.chat.username, update.message.text)

    user = cursor.execute("SELECT ФИО FROM Ключи WHERE Логины = ?", (login,)).fetchone()

    if user is None:
        await update.message.reply_text("Введен неправильный логин. Попробуйте еще раз, или  /cancel чтобы отменить.", reply_markup=markup_cancel)

        return LOGIN

    username = user[0]
    await update.message.reply_text(f"Вы успешно авторизованы, как {username}!", reply_markup=markup_table)
    return ConversationHandler.END


async def cancel(update, context):

    print(update.message.chat.first_name, update.message.chat.username, update.message.text)

    await update.message.reply_text("Авторизация отменена.")
    return ConversationHandler.END


async def lecture_create_table(update, context):
    global username

    print(update.message.chat.first_name, update.message.chat.username, update.message.text)

    if username is not None:
        lesson = 'Лекция'
        grade = cursor.execute(f"SELECT * FROM {lesson}  WHERE ФИО = ?", [username]).fetchall()
        grade = [grade[0][i] for i in range(1, len(grade[0]))]

        for i in range(len(grade)):
            if grade[i] is None:
                grade[i] = ''

        columns = ['|' + cursor.description[i][0] + '|' for i in range(1, len(cursor.description))]

        data = {lesson: grade}
        table = pd.DataFrame(data, index=columns)

        table_str = table.to_string()

        await update.message.reply_text(table_str, reply_markup=markup_table)
    else:
        await update.message.reply_text("Войдите в аккаунт. Нажмите /login", reply_markup=markup_login)


async def seminar_create_table(update, context):
    global username

    print(update.message.chat.first_name, update.message.chat.username, update.message.text)

    if username is not None:
        lesson = 'Семинар'
        grade = cursor.execute(f"SELECT * FROM {lesson}  WHERE ФИО = ?", [username]).fetchall()
        grade = [grade[0][i] for i in range(1, len(grade[0]))]

        for i in range(len(grade)):
            if grade[i] is None:
                grade[i] = ''

        columns = ["|" + cursor.description[i][0] + "|" for i in range(1, len(cursor.description))]

        data = {lesson: grade}
        table = pd.DataFrame(data, index=columns)
        table_str = table.to_string()

        await update.message.reply_text(table_str, reply_markup=markup_table)
    else:
        await update.message.reply_text("Войдите в аккаунт, Нажмите /login", reply_markup=markup_login)


login_keyboard = [["/login"],
                  ["/help", "/info"]]
markup_login = ReplyKeyboardMarkup(login_keyboard, one_time_keyboard=True)


table_keyboard = [["/lecture"], ["/seminar"]]
markup_table = ReplyKeyboardMarkup(table_keyboard, one_time_keyboard=True)

cancel_keyboard = [["/cancel"]]
markup_cancel = ReplyKeyboardMarkup(cancel_keyboard, one_time_keyboard=True)


def main():
    bot = Application.builder().token(BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    hel_p_handler = CommandHandler("help", hel_p)
    info_handler = CommandHandler("info", info)
    lecture_handler = CommandHandler("lecture", lecture_create_table)
    seminar_handler = CommandHandler("seminar", seminar_create_table)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('login', login_start)],
        states={
            LOGIN: [MessageHandler(filters.TEXT & ~ filters.COMMAND, register)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    bot.add_handler(start_handler)
    bot.add_handler(hel_p_handler)
    bot.add_handler(info_handler)
    bot.add_handler(conv_handler)
    bot.add_handler(lecture_handler)
    bot.add_handler(seminar_handler)

    bot.run_polling()


main()
