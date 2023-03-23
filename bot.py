import asyncio
import datetime
import logging
import threading

import pytz
import functions
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from telebot import TeleBot
import config
from db import User, Username, Config, Task, Group
import pandas as pd

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dat = {}

admin_data = {}
user_data = {}

from aiogram.utils.callback_data import CallbackData

posts_cb: CallbackData = CallbackData('search', 'action', 'id', 'sum', 'other')


class SendResult(StatesGroup):
    result = State()
    result2 = State()
class Withdraw(StatesGroup):
    card = State()

class Change(StatesGroup):
    text = State()
    price = State()
    price2 = State()
class AddGroup(StatesGroup):
    username = State()


class Send(StatesGroup):
    send = State()


class Reg(StatesGroup):
    title = State()
    place = State()
    phone = State()
    tg = State()
    name = State()




class MakeSearch(StatesGroup):
    search = State()


def translate(texts, chat_id):
    user = User.get_or_none(User.chat_id == chat_id)
    if user.language == "ua":
        return texts[0]
    elif user.language == "ru":
        return texts[1]
    else:
        return texts[2]

def main_keyb(message):
    main_menu = translate([config.main_menu_ua,config.main_menu_ru,config.main_menu_en],message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(main_menu[0],main_menu[1])
    markup.row(main_menu[2], main_menu[3])
    return markup


@dp.message_handler(commands=['start'])
async def start_message(message):
    if message.chat.type != "private":
        await message.answer(message.chat.id)
        return
    user = User.get_or_none(User.chat_id == message.chat.id)
    if user:
        if not user.language:
            markup = types.InlineKeyboardMarkup()
            a = types.InlineKeyboardButton(
                text="🇺🇦 Українська",
                callback_data=posts_cb.new(action="language",
                                           id='ua',
                                           sum=0, other=0))
            markup.add(a)
            b = types.InlineKeyboardButton(
                text="🇷🇺 Русский",
                callback_data=posts_cb.new(action="language",
                                           id='ru',
                                           sum=0, other=0))
            markup.add(b)
            b = types.InlineKeyboardButton(
                text="🇬🇧 English",
                callback_data=posts_cb.new(action="language",
                                           id='en',
                                           sum=0, other=0))
            markup.add(b)
            await bot.send_message(message.from_user.id, config.select_language, reply_markup=markup,
                                       parse_mode='HTML')
            return
    else:
        User(chat_id=message.chat.id,reg_date=datetime.datetime.now(pytz.timezone('Europe/Kiev')).replace(tzinfo=None)).save()
        markup = types.InlineKeyboardMarkup()
        a = types.InlineKeyboardButton(
            text="🇺🇦 Українська",
            callback_data=posts_cb.new(action="language",
                                       id='ua',
                                       sum=0, other=0))
        markup.add(a)
        b = types.InlineKeyboardButton(
            text="🇷🇺 Русский",
            callback_data=posts_cb.new(action="language",
                                       id='ru',
                                       sum=0, other=0))
        markup.add(b)
        b = types.InlineKeyboardButton(
            text="🇬🇧 English",
            callback_data=posts_cb.new(action="language",
                                       id='en',
                                       sum=0, other=0))
        markup.add(b)
        await bot.send_message(message.from_user.id, config.select_language, reply_markup=markup,
                               parse_mode='HTML')
        return

    await bot.send_message(message.chat.id, translate(config.welcome_message,message.chat.id), reply_markup=main_keyb(message))


@dp.message_handler(commands=['admin'])
async def send_for_all(message):
    if message.chat.id in config.ADMINS:
        markup = types.InlineKeyboardMarkup()
        a = types.InlineKeyboardButton(
            text="Сменить текст и группу для рассылки",
            callback_data=posts_cb.new(action="changeText",
                                       id=0,
                                       sum=0, other=0))
        markup.add(a)
        a = types.InlineKeyboardButton(
            text="Добавить группу",
            callback_data=posts_cb.new(action="addGroup",
                                       id=0,
                                       sum=0, other=0))
        b = types.InlineKeyboardButton(
            text="Удалить группу",
            callback_data=posts_cb.new(action="delGroup",
                                       id=0,
                                       sum=0, other=0))
        markup.add(a,b)
        a = types.InlineKeyboardButton(
            text="Сменить цену за сообщение",
            callback_data=posts_cb.new(action="changePrice",
                                       id=0,
                                       sum=0, other=0))
        markup.add(a)
        a = types.InlineKeyboardButton(
            text="Сменить цену за жалобу",
            callback_data=posts_cb.new(action="changePrice2",
                                       id=0,
                                       sum=0, other=0))
        markup.add(a)
        await bot.send_message(message.chat.id, f"""Пользователей: {User.select().count()}
        
Что делаем?""", reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def menu_list(message):
    if message.text in [config.main_menu_ua[0],config.main_menu_ru[0],config.main_menu_en[0]]:
        active_task = Task.get_or_none(Task.chat_id == message.chat.id,Task.is_done == False)
        if active_task:
            markup = types.InlineKeyboardMarkup()
            a = types.InlineKeyboardButton(
                text=translate(config.cancel, message.chat.id),
                callback_data=posts_cb.new(action="cancelTask",
                                           id=active_task.id,
                                           sum=0, other=0))
            markup.add(a)
            await bot.send_message(message.chat.id, translate(config.you_have_not_complete_task,message.chat.id),reply_markup=markup)
            return
        markup = types.InlineKeyboardMarkup()
        a = types.InlineKeyboardButton(
            text=translate(config.spam,message.chat.id),
            callback_data=posts_cb.new(action="getTask",
                                       id=1,
                                       sum=0, other=0))
        markup.add(a)
        a = types.InlineKeyboardButton(
            text=translate(config.complaints,message.chat.id),
            callback_data=posts_cb.new(action="getTask",
                                       id=2,
                                       sum=0, other=0))
        markup.add(a)
        await bot.send_message(message.chat.id, translate(config.select_category,message.chat.id),reply_markup=markup)

    elif message.text in [config.main_menu_ua[1],config.main_menu_ru[1],config.main_menu_en[1]]:
        user = User.get_or_none(User.chat_id == message.chat.id)
        markup = types.InlineKeyboardMarkup()
        a = types.InlineKeyboardButton(
            text=translate(config.withdraw,message.chat.id),
            callback_data=posts_cb.new(action="withdraw",
                                       id=0,
                                       sum=0, other=0))
        markup.add(a)
        await bot.send_message(message.chat.id, translate(config.balance,message.chat.id).format(message.chat.id,user.balance),
                               reply_markup=markup)

    elif message.text in [config.main_menu_ua[2],config.main_menu_ru[2],config.main_menu_en[2]]:
        await bot.send_message(message.chat.id, translate(config.instructions,message.chat.id))
    elif message.text in [config.main_menu_ua[3],config.main_menu_ru[3],config.main_menu_en[3]]:
        await bot.send_message(message.chat.id, '@d_managerr')


@dp.callback_query_handler(posts_cb.filter())
async def json_box(query: types.CallbackQuery, callback_data: dict):
    callback_data_action = callback_data['action']
    callback_data_id = callback_data['id']
    callback_data_sum = callback_data['sum']
    callback_data_other = callback_data['other']
    print(callback_data_action, callback_data_id)
    if callback_data_action == 'language':
        await query.message.delete()
        user = User.get_or_none(User.chat_id == query.message.chat.id)
        user.language = callback_data_id
        user.save()
        m = await bot.send_message(query.message.chat.id, translate(config.welcome_message, query.message.chat.id).format(
            first_name=query.message.chat.first_name), reply_markup=main_keyb(query.message), parse_mode='HTML')
    if callback_data_action == 'getTask':
        active_task = Task.get_or_none(Task.chat_id == query.message.chat.id, Task.is_done == False)
        if active_task:
            await query.answer(translate(config.you_have_not_complete_task,query.message.chat.id),show_alert=True)
            return
        if callback_data_id == '1':
            message = query.message
            unms = Username.select().where(Username.is_active == True).limit(20)
            if unms.count() != 20:
                await bot.send_message(message.chat.id, translate(config.not_tasks,query.message.chat.id))
                return
            txt = ""
            uns = []
            for i in unms:
                i.is_active = False
                i.save()
                uns.append(i.username)
                txt += "@" + i.username + "\n"
            await bot.send_message(message.chat.id, txt)
            await bot.send_message(message.chat.id, translate(config.spam_rep,query.message.chat.id))
            text = Config.get_or_none(Config.key == "TEXT")
            task = Task(chat_id=message.chat.id, usernames=uns, text=text.value,type="SEND")
            task.save()
            await bot.send_message(message.chat.id, f"<code>{text.value}</code>", parse_mode='HTML')
            markup = types.InlineKeyboardMarkup()
            a = types.InlineKeyboardButton(
                text=translate(config.done,query.message.chat.id),
                callback_data=posts_cb.new(action="done",
                                           id=task.id,
                                           sum=0, other=0))
            markup.add(a)
            a = types.InlineKeyboardButton(
                text=translate(config.cancel,query.message.chat.id),
                callback_data=posts_cb.new(action="cancelTask",
                                           id=task.id,
                                           sum=0, other=0))
            markup.add(a)
            await bot.send_message(message.chat.id, translate(config.after_done,query.message.chat.id), parse_mode='HTML', reply_markup=markup)
        if callback_data_id == '2':
            message = query.message
            groups = Group.select()
            group = None
            if not groups:
                await bot.send_message(message.chat.id, translate(config.not_tasks,query.message.chat.id))
                return
            for i in groups:
                if message.chat.id not in i.users:
                    group = i
                    break
            if not group:
                await bot.send_message(message.chat.id, translate(config.not_tasks,query.message.chat.id))
                return
            await bot.send_message(message.chat.id, group.username)
            await bot.send_message(message.chat.id, translate(config.go_to_channel,query.message.chat.id))
            await bot.send_message(message.chat.id, translate(config.screen_recording,query.message.chat.id))
            task = Task(chat_id=message.chat.id, usernames=[group.username], type="REPORT")
            task.save()
            markup = types.InlineKeyboardMarkup()
            a = types.InlineKeyboardButton(
                text=translate(config.done,query.message.chat.id),
                callback_data=posts_cb.new(action="done",
                                           id=task.id,
                                           sum=0, other=0))
            markup.add(a)
            a = types.InlineKeyboardButton(
                text=translate(config.cancel,query.message.chat.id),
                callback_data=posts_cb.new(action="cancelTask",
                                           id=task.id,
                                           sum=0, other=0))
            markup.add(a)
            await bot.send_message(message.chat.id, translate(config.after_done,query.message.chat.id), parse_mode='HTML', reply_markup=markup)
    if callback_data_action == 'cancelTask':
        task = Task.get_or_none(Task.id == callback_data_id)
        if not task.is_done:
            await query.answer(translate(config.completing_canceled,query.message.chat.id))
            task.is_done = True
            task.save()
            await query.message.delete()

    if callback_data_action == 'done':
        admin_data[str(query.message.chat.id)] = {"task_id": callback_data_id}
        task = Task.get_or_none(Task.id == callback_data_id)

        if task.is_done:
            await query.answer(translate(config.task_already_completed,query.message.chat.id),show_alert=True)
            return
        if task.is_moderating:
            await query.answer(translate(config.task_in_moderation,query.message.chat.id),show_alert=True)
            return
        if task.type == "SEND":
            await bot.send_message(query.message.chat.id,translate(config.result1,query.message.chat.id))
            await SendResult.result.set()
        if task.type == "REPORT":
            await bot.send_message(query.message.chat.id,translate(config.result2,query.message.chat.id)
                                   )
            await SendResult.result2.set()
    if callback_data_action == 'confirm':
        await query.message.delete_reply_markup()
        await query.answer("✅ Подтверждено",show_alert=True)
        task = Task.get_or_none(Task.id == callback_data_id)
        if task.type == "SEND":
            task.is_done = True
            task.save()
            user = User.get_or_none(User.chat_id == task.chat_id)
            price = Config.get_or_none(Config.key == "PRICE")
            amount = 20 * float(price.value)
            user.balance = round(user.balance + amount,2)
            user.save()
            await bot.send_message(task.chat_id, translate(config.task_already_completed,query.message.chat.id).format(amount))
        if task.type == "REPORT":
            task.is_done = True
            task.save()
            user = User.get_or_none(User.chat_id == task.chat_id)
            price = Config.get_or_none(Config.key == "PRICE2")
            amount = float(price.value)
            user.balance = round(user.balance + amount,2)
            user.save()
            group = Group.get_or_none(Group.username == task.usernames[0])
            group.users.append(user.chat_id)
            group.save()
            await bot.send_message(task.chat_id, translate(config.task_already_completed,query.message.chat.id).format(amount))
    if callback_data_action == 'reject':
        await query.message.delete()
        await query.answer("❌ Отклонено",show_alert=True)
        task = Task.get_or_none(Task.id == callback_data_id)
        if task.type == "SEND":
            for i in task.usernames:
                u = Username.get_or_none(Username.username == i)
                u.is_active = True
                u.save()
        await bot.send_message(task.chat_id, translate(config.task_canceled,task.chat_id))
        task.delete_instance()
    if callback_data_action == 'confirmW':
        await query.message.delete_reply_markup()
        await query.answer("✅ Подтверждено",show_alert=True)
        await bot.send_message(callback_data_id, translate(config.withdraw_completed,query.message.chat.id))
    if callback_data_action == 'rejectW':
        await query.message.delete()
        await query.answer("❌ Отклонено",show_alert=True)
        await bot.send_message(callback_data_id, translate(config.withdraw_canceled,query.message.chat.id))

    if callback_data_action == 'withdraw':
        user = User.get_or_none(User.chat_id == query.message.chat.id)
        if user.balance < config.MIN_WITHDRAW:
            await query.answer(translate(config.min_withdraw,query.message.chat.id),show_alert=True)
            return
        await bot.send_message(query.message.chat.id, translate(config.enter_card,query.message.chat.id))
        await Withdraw.card.set()
    if callback_data_action == 'delGroup':
        groups = Group.select()
        markup = types.InlineKeyboardMarkup()
        for i in groups:
            a = types.InlineKeyboardButton(
                text=i.username,
                callback_data=posts_cb.new(action="deleteGroup",
                                           id=i.id,
                                           sum=0, other=0))
            markup.add(a)
        await bot.send_message(query.message.chat.id, "Выбери группу для удаления",reply_markup=markup)
    if callback_data_action == 'deleteGroup':
        await query.answer("Удалено",show_alert=True)
        group = Group.get_or_none(Group.id == callback_data_id)
        group.delete_instance()
        groups = Group.select()
        markup = types.InlineKeyboardMarkup()
        for i in groups:
            a = types.InlineKeyboardButton(
                text=i.username,
                callback_data=posts_cb.new(action="deleteGroup",
                                           id=i.id,
                                           sum=0, other=0))
            markup.add(a)
        await query.message.edit_reply_markup(markup)
    if callback_data_action == 'addGroup':
        await bot.send_message(query.message.chat.id,
                               'Пришли юзернейм группы. Если нужно более одного, то через перенос строки)')
        await AddGroup.username.set()
    if callback_data_action == 'changeText':
        await bot.send_message(query.message.chat.id,
                               'Пришли новый текст')
        await Change.text.set()
    if callback_data_action == 'changePrice':
        await bot.send_message(query.message.chat.id,
                               'Пришли новую цену')
        await Change.price.set()
    if callback_data_action == 'changePrice2':
        await bot.send_message(query.message.chat.id,
                               'Пришли новую цену')
        await Change.price2.set()
    if callback_data_action == 'selectSend':
        admin_data[str(query.message.chat.id)] = {"send": callback_data_id}
        await bot.send_message(query.message.chat.id,
                               'Пришлите рассылку (текст,документ,фото,видео) для отмены нажмите /start')
        await Send.send.set()
@dp.message_handler(state='*', commands=['start'])
async def start_state(message: types.Message, state: FSMContext):
    await state.finish()
    await start_message(message)


# @dp.message_handler(state='*', commands=['admin'])
# async def adm_state(message: types.Message, state: FSMContext):
#     await state.finish()
#     await adm(message)


@dp.message_handler(state='*', commands=['send'])
async def sendddd(message: types.Message, state: FSMContext):
    await state.finish()
    await send_for_all(message)


@dp.message_handler(lambda message: message.text in config.main_menu_en, state='*')
async def menu_state(message: types.Message, state: FSMContext):
    await state.finish()
    await menu_list(message)
@dp.message_handler(lambda message: message.text in config.main_menu_ua, state='*')
async def menu_state(message: types.Message, state: FSMContext):
    await state.finish()
    await menu_list(message)
@dp.message_handler(lambda message: message.text in config.main_menu_ru, state='*')
async def menu_state(message: types.Message, state: FSMContext):
    await state.finish()
    await menu_list(message)


def send_seller(message):
    tg = TeleBot(API_TOKEN, parse_mode="HTML", )
    for i in User.select().where(User.confirmed == True):
        try:
            tg.copy_message(i.chat_id, message.chat.id, message.message_id)
        except:
            pass
    tg.send_message(message.chat.id, f"""Рассылка закончена""")


def forward_poll_seller(message):
    tg = TeleBot(API_TOKEN, parse_mode="HTML", )
    for i in User.select().where(User.confirmed == True):
        try:
            tg.forward_message(i.chat_id, message.chat.id, message.message_id)
        except:
            pass
    tg.send_message(message.chat.id, f"""Рассылка закончена""")


def send_all(message):
    tg = TeleBot(API_TOKEN, parse_mode="HTML", )
    for i in User.select():
        try:
            tg.copy_message(i.chat_id, message.chat.id, message.message_id)
        except:
            pass
    tg.send_message(message.chat.id, f"""Рассылка закончена""")


@dp.message_handler(state=Send.send, content_types=types.ContentTypes.ANY)
async def send_state(message: types.Message, state: FSMContext):
    if admin_data[str(message.chat.id)]['send'] == "1":
        if message.poll:
            threading.Thread(target=forward_poll_seller, args=(message,)).start()
        else:
            threading.Thread(target=send_seller, args=(message,)).start()
    else:
        threading.Thread(target=send_all, args=(message,)).start()
    await bot.send_message(message.chat.id, f"""Рассылка начата""", parse_mode='HTML')
    await state.finish()


@dp.message_handler(state=[SendResult.result], content_types=types.ContentTypes.PHOTO)
async def send_state(message: types.Message, state: FSMContext):
    if await state.get_state() == SendResult.result.state:
        task_id = admin_data[str(message.chat.id)]["task_id"]
        task = Task.get_or_none(Task.id == task_id)
        task.is_moderating = True
        task.save()
        await bot.send_message(message.chat.id, translate(config.to_moder,message.chat.id), parse_mode='HTML')

        await state.finish()
        markup = types.InlineKeyboardMarkup()
        a = types.InlineKeyboardButton(
            text="✅",
            callback_data=posts_cb.new(action="confirm",
                                       id=task_id,
                                       sum=0, other=0))
        b = types.InlineKeyboardButton(
            text="❌",
            callback_data=posts_cb.new(action="reject",
                                       id=task_id,
                                       sum=0, other=0))
        markup.add(a, b)
        await bot.send_photo(config.MODERATION_GROUP_ID,message.photo[-1].file_id, caption="""Модерация РАССЫЛКИ
{}
{}""".format("@" + ";".join(task.usernames).replace(";","\n@"),message.caption if message.caption else ""), parse_mode='HTML', reply_markup=markup)


@dp.message_handler(state=[SendResult.result2], content_types=types.ContentTypes.VIDEO)
async def send_state(message: types.Message, state: FSMContext):
    if await state.get_state() == SendResult.result2.state:
        task_id = admin_data[str(message.chat.id)]["task_id"]
        task = Task.get_or_none(Task.id == task_id)
        task.is_moderating = True
        task.save()
        await bot.send_message(message.chat.id, translate(config.to_moder,message.chat.id), parse_mode='HTML')
        groups = Group.select()
        group = None
        if not groups:
            await bot.send_message(message.chat.id, translate(config.not_tasks, message.chat.id))
            return
        for i in groups:
            if message.chat.id not in i.users:
                group = i
                break
        if not group:
            await bot.send_message(message.chat.id, translate(config.not_tasks, message.chat.id))
            return
        await bot.send_message(message.chat.id, group.username)
        await bot.send_message(message.chat.id, translate(config.go_to_channel, message.chat.id))
        await bot.send_message(message.chat.id, translate(config.screen_recording, message.chat.id))
        task = Task(chat_id=message.chat.id, usernames=[group.username], type="REPORT")
        task.save()
        markup = types.InlineKeyboardMarkup()
        a = types.InlineKeyboardButton(
            text=translate(config.done, message.chat.id),
            callback_data=posts_cb.new(action="done",
                                       id=task.id,
                                       sum=0, other=0))
        markup.add(a)
        a = types.InlineKeyboardButton(
            text=translate(config.cancel, message.chat.id),
            callback_data=posts_cb.new(action="cancelTask",
                                       id=task.id,
                                       sum=0, other=0))
        markup.add(a)
        await bot.send_message(message.chat.id, translate(config.after_done, message.chat.id), parse_mode='HTML',
                               reply_markup=markup)
        await state.finish()
        markup = types.InlineKeyboardMarkup()
        a = types.InlineKeyboardButton(
            text="✅",
            callback_data=posts_cb.new(action="confirm",
                                       id=task_id,
                                       sum=0, other=0))
        b = types.InlineKeyboardButton(
            text="❌",
            callback_data=posts_cb.new(action="reject",
                                       id=task_id,
                                       sum=0, other=0))
        markup.add(a, b)
        await bot.send_video(config.MODERATION_GROUP_ID,message.video.file_id, caption="""Модерация ЖАЛОБЫ
{}
{}""".format("@" + ";".join(task.usernames).replace(";","\n@"),message.caption if message.caption else ""), parse_mode='HTML', reply_markup=markup)

@dp.message_handler(state=[AddGroup.username], content_types=types.ContentTypes.TEXT)
async def send_state(message: types.Message, state: FSMContext):
    if await state.get_state() == AddGroup.username.state:
        unms = message.text.split("\n")
        for u in unms:
            Group(username=u).save()
        await bot.send_message(message.chat.id, f"""Добавлено {len(unms)} групп""", parse_mode='HTML')
        await state.finish()
@dp.message_handler(state=[Change.text,Change.price,Change.price2], content_types=types.ContentTypes.TEXT)
async def send_state(message: types.Message, state: FSMContext):
    if await state.get_state() == Change.text.state:
        text = Config.get_or_none(Config.key == "TEXT")
        text.value = message.text
        text.save()
        await bot.send_message(message.chat.id, f"""Новый текст сохранен""", parse_mode='HTML')
        await state.finish()
    elif await state.get_state() == Change.price.state:
        a = functions.is_digit(message.text)
        if not a:
            await bot.send_message(message.chat.id, f"""Введи число""", parse_mode='HTML')
            return
        text = Config.get_or_none(Config.key == "PRICE")
        text.value = str(float(message.text))
        text.save()
        await bot.send_message(message.chat.id, f"""Новая цена сохранена""", parse_mode='HTML')
        await state.finish()
    elif await state.get_state() == Change.price2.state:
        a = functions.is_digit(message.text)
        if not a:
            await bot.send_message(message.chat.id, f"""Введи число""", parse_mode='HTML')
            return
        text = Config.get_or_none(Config.key == "PRICE2")
        text.value = str(float(message.text))
        text.save()
        await bot.send_message(message.chat.id, f"""Новая цена сохранена""", parse_mode='HTML')
        await state.finish()
@dp.message_handler(state=[Withdraw.card], content_types=types.ContentTypes.TEXT)
async def send_state(message: types.Message, state: FSMContext):
    if await state.get_state() == Withdraw.card.state:
        card = message.text.replace(" ","")
        user = User.get_or_none(User.chat_id == message.chat.id)
        if not len(card) == 16 or not functions.luhn(card):
            await bot.send_message(message.chat.id, translate(config.card_not_valid,message.chat.id), parse_mode='HTML')
            return
        await bot.send_message(message.chat.id, translate(config.withraw_app_send,message.chat.id), parse_mode='HTML')
        await state.finish()
        markup = types.InlineKeyboardMarkup()
        a = types.InlineKeyboardButton(
            text="✅",
            callback_data=posts_cb.new(action="confirmW",
                                       id=message.chat.id,
                                       sum=0, other=0))
        b = types.InlineKeyboardButton(
            text="❌",
            callback_data=posts_cb.new(action="rejectW",
                                       id=message.chat.id,
                                       sum=0, other=0))
        markup.add(a, b)
        await bot.send_message(config.WITHDRAW_GROUP_ID, f"""Вывод
{user.balance} UAH

{card}""",parse_mode='HTML', reply_markup=markup)
        user.balance = 0
        user.save()



@dp.message_handler(state="*", content_types=types.ContentTypes.VIDEO)
async def send_state(message: types.Message, state: FSMContext):
    print(message.video.file_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
