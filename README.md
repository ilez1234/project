# Проектный описание телеграмм бота
### Проект выполнял `Картоев Ильяс Идрисович` стдуент ИнгГУ

## Описание

Проект представляет собой [телеграмм бота](https://t.me/journa1_bot), разработанного для защиты конфиденциальности успеваемости студентов. Пользователи могут получить доступ к своей ведомости, только используя индивидуальный логин.

#### Скриншоты с телеграмма
![скриншоты,  width="30" ](https://github.com/ilez1234/fghfghfg/blob/main/Images/bot_1.jpg)

---
## Немного о коде
- Функция с которой начнется знакомство *пользователя* с ***ботом*** это `start`
```python
async def start(update, context):
```

- Функция для получения большей информацияя о боте это `info`
```python
async def info(update, context):
```

- Функция для получения помощи`hel_p`
```python
async def hel_p(update, context):
```

- Задача регистрации пользоватля была разбита на три пункта (функции), реализованы это с помощью "диалого окна",  и двух глобальных перменныx. Переменная ```username``` чтобы сохранить в нем ФИО пользователя, и переменная ```LOGIN``` чтобы следить за сотоянием регистрации.

```python
username = None
LOGIN = 0

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('login', login_start)],
    states={
        LOGIN: [MessageHandler(filters.TEXT & ~ filters.COMMAND, register)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
```
  - Функция ```login_start``` нужна чтобы запросить у пользователя логин.
  ```python
  async def login_start(update, context):

    print(update.message.chat.first_name, update.message.chat.username, update.message.text)

    await update.message.reply_text("Введите логин для авторизации, или /cancel чтобы отменить",
                                    reply_markup=markup_cancel)
    return LOGIN
  ```
  - Функция ```register``` отвечает за регистрацию пользователя. Функция обращается к базе данных SQL, и ищет там логин, который ему скинул пользователь. Если его нет, это сообщится в мессенджере. 
  
  ```python
  import sqlite3

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
  ```
  - Функция ```cancel``` служит для отмены регистрации.
  ```python
  async def cancel(update, context):

    print(update.message.chat.first_name, update.message.chat.username, update.message.text)

    await update.message.reply_text("Авторизация отменена.")
    return ConversationHandler.END
  ```
- Для вывод таблицы по используется функции `lecture_create_table` и `seminar_create_table`. Функции друг от друг почти нечем не отличаются. В функциях есть проверка, что пользователь залогинился. Даные из **SQL** переводятся в **DataFrame** для упрошения работы с ними и  отправляются **пользователю**.

```python
import pandas as pd

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
```

```python
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
```
---
## Дальнейшие действия

**13 мая** - В настоящий момент бот функционирует, предоставляя пользователю ведомость после входе в аккаунт. Однако, планируется  расширение функционала. В частности, планируется добавление дополнительной статистики в ответах бота, такой как количество "+", "-", "н" и процент посещаемости. Также пользователи смогут выбирать период (например, месяц) и применять различные фильтры к статистике. Планируется доработка кода для исправления различных багов и повышения стабильности. Все функции будут перенесены в отдельный файл для удобства управления (modules_bot). Будет добавлен обработчик ошибок и команда удаления логина. Предвидится проведение обширного тестирования бота для выявления и исправления потенциальных проблем. Отправить проект на бесплатный хостин.

## Какие проблемы есть сейчас ?

- их нет)
___
## История обновлений

**Версия 1.0** - Бот работает в базовом функционале, но требует доработок. Подробное описание планов на доработку и улучшение функционала представлено в разделе "Дальнейшие действия" за 13 мая.
___
