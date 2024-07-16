# -*- coding: utf-8 -*-
import uuid

import requests
import telebot
from g4f.client import Client
from telebot import types
from fake_useragent import UserAgent
import json
import inflect

TOKEN = '6761411565:AAE5pFixORdpHF55IngLxWYHxz1fqg0Ygv4'

bot = telebot.TeleBot(TOKEN)
referrals = {}
users = {}
admin_users = [786320574, 1079020959]
questions = [
    "Имя Фамилия:",
    "Пол:",
    "Национальность:",
    "Возраст:",
    "Дата и место рождения:",
    "Семья:",
    "Место текущего проживания:",
    "Описание внешности:",
    "Детство (укажите пару слов о вашем персонаже, например, был добрым парнем):",
    "Юность и взрослая жизнь (например, стал бандитом):",
    "Взрослая жизнь (например, открыл свой бизнес):"
]


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.message.chat.id
    if call.data == 'give_balance':
        handle_give_balance(call)
    if call.data == 'your_ref':
        get_referral_link(call.message)
    if call.data == 'more_info_withdraw':
        more_info_withdraw(call)
    if call.data == 'hand_balance':
        hand_balance(call)
    if call.data == 'guides':
        handler_guides(call)
    if call.data == 'car_prices':
        handler_car_prices(call)
    if call.data == 'biznes_prices':
        handler_biznes_prices(call)
    if call.data == 'offer_news':
        handler_offer_news(call)
    if call.data == 'write_biography':
        handler_write_biography(call)
    if call.data == 'level_up_info':
        level_up_info(call)
    if call.data == 'main_menu':
        main_menu(call)
    if call.data == "withdraw":
        bot.send_message(call.message.chat.id, "Отлично, сейчас я задам вам несколько вопросов.")
        withdraw_process(call.message, {})
    elif call.data == 'low_class_cars':
        handler_low_class_cars(call)
    elif call.data == 'luxury_cars':
        handler_luxury_cars(call)
    elif call.data == 'luxury_cars_2':
        handler_luxury_cars_2(call)
    elif call.data == 'motorcycles':
        handler_motorcycles(call)

    if call.data == '24/7':
        show_biznes_prices(call, '24/7')
    if call.data == 'Магазин одежды':
        show_biznes_prices(call, 'Одежда')
    if call.data == 'Закусочные':
        show_biznes_prices(call, 'Закусочные')
    if call.data == 'Автосалоны/Мотосалоны':
        show_biznes_prices(call, 'Авто/Мото')
    if call.data == 'Амуниции':
        show_biznes_prices(call, 'Амуниция')
    if call.data == 'Казино':
        show_biznes_prices(call, 'Казино')
    if call.data == 'Автомастерские':
        show_biznes_prices(call, 'Автомастерские')
    if call.data == 'Магазины акссесуаров':
        show_biznes_prices(call, 'Аксессуары')
    if call.data == 'АЗС':
        show_biznes_prices(call, 'АЗС')

    if call.data == 'auc':
        bot.send_message(call.message.chat.id, "Этот раздел находиться в разработке")
        handler_guides(call)
    if call.data == 'generate_link':
        handle_generate_link(call)


COINS_PER_REFERRAL = 100


def more_info_withdraw(call):
    bot.send_photo(call.message.chat.id, photo=open('balance.jpg', 'rb'),
                   caption="HypeCoin - это игровая валюта внутри бота, которую можно получить выполняя простые задания.\n\nHypeCoin можно обменять на реальную игровую валюту, всего лишь указав ник, счет и сервер.\n\n— Приглашай друзей по своей реф. ссылке. За каждого ты получишь по 100 HypeCoin\n— Участвуй и побеждай в конкурсах от Black Russia Hype\n— За каждый первый комментарий под постом вы будете получать 25 HypeCoin\n\nИ не забывай ставить реакции! 🤯\n\n1000 HypeCoin - 1.000.000 виртуальной валюты.")


def get_user_info(user_id):
    user_id = str(user_id)
    if user_id not in users:
        users[user_id] = {
            'balance': 0,
            'referrals': [],
            'promocodes': []
        }
    return users[str(user_id)]


def handle_give_balance(call):
    bot.send_message(call.message.chat.id,
                     "Введите @username пользователя и количество HypeCoin (например: @username 100):")
    bot.register_next_step_handler(call.message, process_give_balance)


def hand_balance(call):
    user_id = call.message.chat.id
    button1 = types.InlineKeyboardButton("📃Вывести HypeCoin",
                                         callback_data='withdraw')
    button3 = types.InlineKeyboardButton("Узнать подробнее от системе",
                                         callback_data='more_info_withdraw')
    button2 = types.InlineKeyboardButton("Ваша реферальная ссылка",
                                         callback_data='your_ref')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)
    bot.send_message(call.message.chat.id, f"Ваш баланс: {users[str(user_id)]['balance']} HypeCoin.",
                     reply_markup=keyboard)


def withdraw_process(message, user_data):
    user_id = message.chat.id
    if message.text == "🏠 Главное меню":
        start(message)
        return
    try:
        if "nick" not in user_data:
            bot.send_message(user_id, "Введите ваш игровой ник/номер счета (Nick_Name, 123123)")
            bot.register_next_step_handler(message, lambda m: withdraw_process(m, {**user_data, "nick": m.text}))
        elif "server" not in user_data:
            bot.send_message(user_id, "Введите ваш сервер (например: индиго)")
            bot.register_next_step_handler(message, lambda m: withdraw_process(m, {**user_data, "server": m.text}))
        elif "amount" not in user_data:
            bot.send_message(user_id, "Введите количество HypeCoin для вывода (Минимальное число для вывода - 1000).")
            bot.register_next_step_handler(message, lambda m: withdraw_process(m, {**user_data, "amount": m.text}))
        elif "email" not in user_data:
            bot.send_message(user_id, "Введите вашу почту.")
            bot.register_next_step_handler(message, lambda m: withdraw_process(m, {**user_data, "email": m.text}))
        else:
            nick = user_data["nick"]
            server = user_data["server"]
            amount = float(user_data["amount"])  # Convert amount to float
            email = user_data["email"]
            if amount < 1000:
                bot.send_message(user_id, "Минимальное число для вывода - 1000 HypeCoin")
            elif amount > users[str(user_id)]["balance"]:
                bot.send_message(user_id, "Недостаточно средств на балансе.")
            else:
                # Send withdrawal request to admins
                admin_id = [786320574, 1079020959]
                for id in admin_id:
                    bot.send_message(id, f"Заявка на вывод HypeCoin:\n"
                                         f"Пользователь: @{message.from_user.username}\n"
                                         f"Ник/номер счета: {nick}\n"
                                         f"Сервер: {server}\n"
                                         f"Количество: {amount} HypeCoin\n"
                                         f"Почта: {email}")

                # Deduct HypeCoin from user's balance
                users[str(user_id)]["balance"] -= amount
                save_data()
                bot.send_message(user_id, f"Ваша заявка на вывод {amount} HypeCoin принята. "
                                          f"Средства будут отправлены в ближайшее время.")

    except ValueError:
        bot.send_message(user_id, "Некорректный формат количества HypeCoin. Пожалуйста, введите число.")
        bot.register_next_step_handler(message, lambda m: withdraw_process(m, user_data))


def process_give_balance(message):
    if message.text == '🏠 Главное меню':
        start(message)
        return
    try:
        username, amount = message.text.split()
        amount = int(amount)
        if username.startswith("@"):
            username = username[1:]

            user_id = None
            for uid, user_data in users.items():
                if user_data.get('username') == username:
                    user_id = int(uid)  # Convert uid to integer
                    break

            if user_id:
                user_info = get_user_info(user_id)
                user_info['balance'] += amount
                bot.send_message(message.chat.id,
                                 f"Баланс пользователя @{username} успешно пополнен на {amount} HypeCoin.")
                bot.send_message(user_id,
                                 f"Ваш баланс пополнен на {amount} HypeCoin. Текущий баланс: {user_info['balance']} HypeCoin.")
                save_data()
            else:
                bot.send_message(message.chat.id, f"Пользователь @{username} не найден.")
        else:
            bot.send_message(message.chat.id, "Неверный формат. Введите @username.")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Неверный формат. Введите @username и количество HypeCoin.")


def reward_promocode(referrer_id, amount):
    user_info = get_user_info(referrer_id)
    user_info['balance'] += amount
    bot.send_message(referrer_id, f"Вам начислено {amount} HypeCoin за промокод! ")


def reward_referrer(referrer_id):
    print("reward")
    user_info = get_user_info(referrer_id)
    user_info['balance'] += COINS_PER_REFERRAL
    bot.send_message(referrer_id, f"Вам начислено {COINS_PER_REFERRAL} HypeCoin за нового реферала! "
                                  f"Ваш баланс: {user_info['balance']} HypeCoin.")


def check_subscription_and_reward(user_id, referrer_id=None):
    chat_member = bot.get_chat_member(chat_id="@blackrussiahype", user_id=user_id)
    if chat_member.status in ['creator', 'administrator', 'member'] and int(user_id) != int(referrer_id):
        if referrer_id:
            print(f"{int(user_id)} ref {int(referrer_id)}")

            reward_referrer(referrer_id)
    else:
        users[str(referrer_id)]['referrals'].remove(user_id)


@bot.message_handler(commands=['start'])
def start(message):
    load_data()
    user_id = str(message.chat.id)
    if str(user_id) not in users:
        username = message.from_user.username
        users[user_id] = {"balance": 0, "promocodes": [], "referrals": [], "username": username}

    for ref in users[user_id]['referrals']:
        chat_member = bot.get_chat_member(chat_id="@blackrussiahype", user_id=ref)
        if chat_member.status not in ['creator', 'administrator', 'member']:
            bot.send_message(message.chat.id,
                             'Один из ваших рефералов отписался от группы, мы вынуждены снять с вас бонус')
            users[user_id]['balance'] -= COINS_PER_REFERRAL
            users[user_id]['referrals'].remove(ref)
    parts = message.text.split()
    if message.text == '🏠 Главное меню':
        pass
    elif len(parts) > 1 and parts[1].startswith('code_'):
        _, code = parts
        reward_data = reward_links.get(code)
        if reward_data and reward_data["uses"] > 0:
            if code not in users[user_id]['promocodes']:
                amount = reward_data["amount"]
                reward_promocode(message.chat.id, amount=amount)
                users[user_id]['promocodes'].append(code)
                reward_links[code]['uses'] -= 1

                if reward_links[code]['uses'] == 0:
                    del reward_links[code]

                    save_data()

    elif len(parts) > 1:
        referrers_id = int(parts[1])
        referrer_info = get_user_info(referrers_id)

        is_already_referred = False
        for referrer_id in users:
            if user_id in users[referrer_id]['referrals']:
                is_already_referred = True
                break

        if not is_already_referred and int(user_id) != referrers_id:
            referrer_info['referrals'].append(user_id)
            check_subscription_and_reward(user_id, referrers_id)

        user_info = get_user_info(user_id)


    chat_member = bot.get_chat_member(chat_id="@blackrussiahype", user_id=message.chat.id)
    if chat_member.status not in ['creator', 'administrator', 'member']:
        keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text_button = types.KeyboardButton("🏠 Главное меню")
        keyboard1.add(text_button)
        bot.send_message(message.chat.id, "Для использования бота, пожалуйста, подпишитесь на канал @blackrussiahype.",
                         reply_markup=keyboard1)
        return
    else:
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("📃Гайды и прочее",
                                             callback_data='guides')
        button2 = types.InlineKeyboardButton("Рынок",
                                             callback_data='market')
        button3 = types.InlineKeyboardButton("📩Предложить новость",
                                             callback_data='offer_news')
        button4 = types.InlineKeyboardButton("✨Написание биографии",
                                             callback_data='write_biography')
        button5 = types.InlineKeyboardButton("💸 Баланс",
                                             callback_data='hand_balance')
        keyboard.add(button5)
        keyboard.add(button1)
        # keyboard.add(button2)
        keyboard.add(button3)
        keyboard.add(button4)

        if message.chat.id in admin_users:
            button6 = types.InlineKeyboardButton("Создать чек",
                                                 callback_data='generate_link')
            keyboard.add(button6)
            button10 = types.InlineKeyboardButton("Выдать баланс", callback_data='give_balance')
            keyboard.add(button10)
        # server_info = get_server_info()
        button6 = types.InlineKeyboardButton("Онлайн серверов", callback_data='server_online')
        # keyboard.add(button6)
        bot.send_message(message.chat.id,
                         f"Добро пожаловать в нашего бота, выберите что вас интересует",
                         reply_markup=keyboard)
    save_data()


def handle_generate_link(call):
    bot.send_message(call.message.chat.id, "Введите количество использований:")
    bot.register_next_step_handler(call.message, get_max_uses)  # Start collecting information


def get_max_uses(message):
    try:
        if message.text == '/start' or message.text == '/admin' or message.text == '🏠 Главное меню' or message.text == '⚙️ Админ панель':
            start(message)
        else:
            max_uses = int(message.text)
            bot.send_message(message.chat.id, "Введите количество валюты:")
            bot.register_next_step_handler(message, get_amount, max_uses)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Пожалуйста, введите число.")
        bot.register_next_step_handler(message, get_max_uses)


def get_amount(message, max_uses):
    try:
        if message.text == '/start' or message.text == '/admin' or message.text == '🏠 Главное меню' or message.text == '⚙️ Админ панель':
            start(message)
        else:
            amount = int(message.text)
            link = generate_reward_link(amount, max_uses)
            bot.send_message(message.chat.id, f"Ссылка создана: {link}")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Пожалуйста, введите число.")
        bot.register_next_step_handler(message, get_amount, max_uses)


reward_links = {}


def generate_reward_link(amount, max_uses=1):
    code = 'code_' + str(uuid.uuid4())
    link = f"https://t.me/BlackRussiaHype_bot?start={code}"
    reward_links[code] = {"amount": amount, "uses": max_uses}
    save_data()
    return link


@bot.message_handler(commands=['balance'])
def show_balance(message):
    user_id = message.chat.id
    user_info = get_user_info(user_id)
    bot.send_message(user_id, f"Ваш баланс: {user_info['balance']} HypeCoin.\n")
    # f"Ваши рефералы: {', '.join([f'[{ref}](tg://user?id={ref})' for ref in user_info['referrals']])}", parse_mode="Markdown")


@bot.message_handler(commands=['ref'])
def get_referral_link(message):
    user_id = message.chat.id
    referral_link = f"https://t.me/BlackRussiaHype_bot?start={user_id}"
    bot.send_message(user_id,
                     f"Ваша реферальная ссылка: {referral_link}\n\nПриглашай друзей по этой ссылке и получай 100 HypeCoin!")


def handler_guides(call):
    user_id = call.message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    # Add buttons for guides with links
    button1 = types.InlineKeyboardButton("✨Промокоды", url="https://telegra.ph/PROMOKODY-03-28")
    button2 = types.InlineKeyboardButton("🔒NonRP обманы",
                                         url="https://telegra.ph/Kak-izbezhat-NonRP-obmana-i-ego-popytki-03-28")
    button3 = types.InlineKeyboardButton("📌Основные ресурсы проекта",
                                         url="https://telegra.ph/Osnovnye-resursy-proekta-03-27")
    button4 = types.InlineKeyboardButton("🗒Шаблоны для хелперов",
                                         url="https://telegra.ph/25-SHABLONY-OTVETOV-NA-VOPROSY-IGROKOV-DLYA-HELPEROV-03-27")
    button5 = types.InlineKeyboardButton("📈Прокачать уровень", callback_data='level_up_info')
    button6 = types.InlineKeyboardButton("📃Все команды", url="https://telegra.ph/SPISOK-VSEH-KOMAND-03-28")
    button7 = types.InlineKeyboardButton("📊Открытие нового сервера",
                                         url="https://telegra.ph/Kak-zaletat-na-otkrytie-novogo-servera-03-28")
    button8 = types.InlineKeyboardButton("💻 РП отыгровки", url="https://telegra.ph/Black-Russia--RP-otygrovki-04-08")
    button9 = types.InlineKeyboardButton("💼Высокооплачиваемые работы и ЗП", url="https://telegra.ph/Raboty-04-08")
    button11 = types.InlineKeyboardButton("🚗 Цены на Авто",
                                          callback_data='car_prices')
    button13 = types.InlineKeyboardButton("💸 Цены госс бизнесов",
                                          callback_data='biznes_prices')
    button12 = types.InlineKeyboardButton("🛠Аукцион",
                                          callback_data='auc')

    # Add buttons to go back to main menu
    button10 = types.InlineKeyboardButton("Назад", callback_data='main_menu')

    keyboard.add(button1, button2)
    keyboard.add(button5, button6)
    keyboard.add(button3)
    keyboard.add(button4)
    keyboard.add(button7)
    keyboard.add(button8)
    keyboard.add(button9)
    keyboard.add(button11)
    keyboard.add(button12)
    keyboard.add(button13)
    keyboard.add(button10)

    bot.send_message(call.message.chat.id,
                     f"Выберите интересующий вас гайд:",
                     reply_markup=keyboard)


def main_menu(call):
    load_data()
    user_id = str(call.message.chat.id)

    for ref in users[user_id]['referrals']:
        chat_member = bot.get_chat_member(chat_id="@blackrussiahype", user_id=ref)
        if chat_member.status not in ['creator', 'administrator', 'member']:
            bot.send_message(call.message.chat.id,
                             'Один из ваших рефералов отписался от группы, мы вынуждены снять с вас бонус')
            users[user_id]['balance'] -= COINS_PER_REFERRAL
            users[user_id]['referrals'].remove(ref)

    chat_member = bot.get_chat_member(chat_id="@blackrussiahype", user_id=call.message.chat.id)
    if chat_member.status not in ['creator', 'administrator', 'member']:
        keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text_button = types.KeyboardButton("🏠 Главное меню")
        keyboard1.add(text_button)
        bot.send_message(call.message.chat.id, "Для использования бота, пожалуйста, подпишитесь на канал @blackrussiahype.",
                         reply_markup=keyboard1)
        return
    else:
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("📃Гайды и прочее",
                                             callback_data='guides')
        button2 = types.InlineKeyboardButton("Рынок",
                                             callback_data='market')
        button3 = types.InlineKeyboardButton("📩Предложить новость",
                                             callback_data='offer_news')
        button4 = types.InlineKeyboardButton("✨Написание биографии",
                                             callback_data='write_biography')
        button5 = types.InlineKeyboardButton("💸 Баланс",
                                             callback_data='hand_balance')
        keyboard.add(button5)
        keyboard.add(button1)
        # keyboard.add(button2)
        keyboard.add(button3)
        keyboard.add(button4)

        if call.message.chat.id in admin_users:
            button6 = types.InlineKeyboardButton("Создать чек",
                                                 callback_data='generate_link')
            keyboard.add(button6)
            button10 = types.InlineKeyboardButton("Выдать баланс", callback_data='give_balance')
            keyboard.add(button10)
        # server_info = get_server_info()
        button6 = types.InlineKeyboardButton("Онлайн серверов", callback_data='server_online')
        # keyboard.add(button6)
        bot.send_message(call.message.chat.id,
                         f"Добро пожаловать в нашего бота, выберите что вас интересует",
                         reply_markup=keyboard)
    save_data()


# def get_server_info():
#    response = requests.get("https://api-backup111.blackrussia.online/servers.json")
#    res = response.json()
#    return res

def create_online_button(server_data):
    if server_data:
        server_name = server_data["name"]
        online = server_data["online"]
        max_online = server_data["maxonline"]
        return f"**{server_name}**: {online}/{max_online}"
    else:
        return "Ошибка получения данных"


def handler_low_class_cars(call):
    show_car_prices(call, "Низкий класс")


def handler_luxury_cars(call):
    show_car_prices(call, "Класс Люкс")


def handler_luxury_cars_2(call):
    show_car_prices(call, "Класс Люкс 2")


def handler_motorcycles(call):
    show_car_prices(call, "Мототранспорт")


@bot.message_handler(func=lambda message: True)  # Place this handler after the start handler
def handle_all_messages(message):
    chat_member = bot.get_chat_member(chat_id="@blackrussiahype", user_id=message.chat.id)
    if chat_member.status not in ['creator', 'administrator', 'member']:
        keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text_button = types.KeyboardButton("🏠 Главное меню")
        keyboard1.add(text_button)
        bot.send_message(message.chat.id, "Для использования бота, пожалуйста, подпишитесь на канал @blackrussiahype.",
                         reply_markup=keyboard1)
        return
    else:
        if hasattr(message, 'text') and message.text == "🏠 Главное меню":
            start(message)
        else:  # Handle other types of messages or do nothing
            pass


def show_car_prices(call, car_type):
    user_id = call.message.chat.id

    # Словарь с информацией о ценах
    car_prices = {
        "Низкий класс": """
    MAZDA SEDAN 3 | 380.000 | (218км/ч)| (8.1)
TOYOTA MARK  |  420.000| (223км/ч) (9) |
MERCEDES-BENZ W124 |  440.000
JEEP GRAND CHEROKEE |  450.000
AUDI 100 C4|520.000| | (242км/ч) (5.6)
BMW M3 E36 |  600.000 | (239км/ч)| (5.0)
MERCEDES-BENZ E420 W210 | 700.000 | (250км/ч) (6)
LADA VESTA SEDAN | 700.000 |(184км/ч) (9.3)
AUDI A6 C5 | 1.000.000 |(248км/ч) (5.8)
    """,
        "Класс Люкс": """
    VOLVO XC90|4.200.000| (248км/ч) (5.6)
CHEVROLETTE CAMARO ZL1|4.600.000|(скрин) (315км/ч) (4)
BMW Z4 M40I|4.900.000| (259км/ч) (4.5)
BMW M4 F84|5.500.000| (261км/ч) (4)
FORD RAPTOR F-150|5.757.000| (211км/ч) (6.1)
AUDI Q8|6.000.000| (248км/ч) (4.5)
DODGE DEMON SRT|6.100.000|(322км/ч) (2.5)
MERCEDES-BENZ C63s AMG| 6.200.000 (278км/ч) (3.9)
MERCEDES-BENZ GT63s|7.000.000| (313км/ч) (3.2)
AUDI Q7|7.000.000|(скрин) (238км/ч) (6.1)
TOYOTA LAND CRUISER 200 |7.800.000|(скрин) (220км/ч) (8.6)
CADILLAC ESCALADE|7.200.000| (248км/ч) (6.4)
NISSAN GT-R R35|7.900.000| (319км/ч) (2.7)
BMW X6M F16|8.200.000| (284км/ч) (4.1)
PORSHE PANAMERA S|8.400.000| (310км/ч) (3.7)
AUDI RS6|8.500.000| (306км/ч) (3.9)
PORSCHE 911 CARRERA S |9.000.000|  (309км/ч) (3.7)
MERCEDES-BENZ GLS 400 |9.150.000|(скрин) (240км/ч) (6.4)
BMW M5 F90|9.500.000| (312км/ч) (3.4)
AUDI RS7 SPORT|9.500.000| (252км/ч) (3.2)
RANGE ROVER SVR|10.000.000| (262км/ч) (4.9)
AUDI RS6 C7 рестайлинг|10.000.000| (310км/ч) (3.7)
Mercedes-Benz CLS53 AMG|11.300.000| (305км/ч) (3.5)
BMW X7 M50I|10.500.000| (250км/ч) (4.6)
Lexus LX570|11.450.000| (230км/ч) (6.9)
    """,
        "Класс Люкс 2": """
    CADILLAC ESCALADE|11.500.000| (210км/ч) (6.4)
MERCEDES-BENZ E63S |11.500.000| (314км/ч) (3.2)
BMW I8 EDRIVE |12.600.000| (320км/ч) (4.5)
MERCEDES-BENZ GT-R |13.500.000| (319км/ч) (3.5)
McLaren 600LT|14.000.000| (329км/ч) (2.9)
TESLA MODEL S|15.000.000| (252км/ч) (3.2)
LAMBORDGHINI URUS|15.300.000| (305км/ч) (3.5)
LAMBORGHINI HURACAN|16.500.000| (330км/ч) (2.9)
MERCEDES-BENZ G65 AMG|17.050.000| (223км/ч) (5.3)
BMW M8 F92|17.200.000| (312км/ч) (3.4)
FERRARI 488 GTB|17.500.000| (336км/ч) (3)
PORSCHE TAYCAN TURBO S|18.300.000| (254км/ч) (3.2)
ASTON MARTIN DB11|18.500.000| (322км/ч) (3.9)
BMW M8 F93 GRAN COUPE|19.000.000| (312км/ч) (3.2)
LAMBORGHINI AVENTADOR S|20.000.000| (351км/ч) (2.7)
TESLA MODEL X|21.000.000| (256км/ч) (3.4)
MERCEDES-BENZ G63 AMG|23.000.000| (223км/ч) (5.0)
MERCEDES-BENZ MB S650|25.000.000| (248км/ч) (5)
Rolls-Royce Wraith|35.000.000| (264км/ч) (4.5)
Rolls-Royce Cullinan|40.000.000| (260км/ч) (5.1)
Rolls-Royce Phantom|50.000.000| (265км/ч) (5.3)
Bugatti Divo|380.000.000| (380км/ч) (2.4)
Bugatti La Noire|1.000.000.000|(400км/ч) (2.2)
    """,
        "Мототранспорт": """ 
    Racer Sport|20.000|(130км/ч) (10)
Минск 125|300.000|(205км/ч) (4)
Aprilla MXV 450|90.000|(200км/ч) (4.1)
Ducati SuperSport S|1.830.000|(240км/ч) (3.5)
Ducati XDiavel S|3.000.000|(260км/ч) (3)
Yamaha FZ-10|4.500.000|(257км/ч) (2.5)
Yamaha YZF-R6|5.000.000|(260км/ч) (3.2)
BMW S 1000 RR|7.000.000|(295км/ч) (3)
Suzuki GSX-R750|8.000.000|(276км/ч) (3.2)
Kawasaki Ninja H2R|10.000.000| (340км/ч) (2.5)
    """
    }
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("🏠Меню", callback_data='main_menu')
    keyboard.add(button1)
    # Отправка списка автомобилей
    bot.send_message(user_id, car_prices[car_type], reply_markup=keyboard)


def show_biznes_prices(call, car_type):
    user_id = call.message.chat.id

    # Словарь с информацией о ценах
    business_prices = {
        "24/7": """
            Магазин 24/7 г. Южный (3) около автоугона - 700.000 рублей
            \nМагазин 24/7 г. Южный (18) около ГИБДД - 500.000 рублей
            \nМагазин 24/7 г. Южный (20) около УМВД - 500.000 рублей
            \nМагазин 24/7 г. Южный (21) около СМИ - 450.000 рублей
            \nМагазин 24/7 пгт. Батырево (6) около ФСБ - 650.000 рублей
            \nМагазин 24/7 г. Арзамас, около спавна - 1.000.000 рублей
            \nМагазин 24/7 'Перекресток'(10) г. Арзамас - 1.000.000 рублей
            \nМагазин 24/7 г. Арзамас (13) выезд из города - 500.000 рублей
            \nМагазин 24/7 пгт. Батырево (15) около автошколы - 500.000 рублей
            \nМагазин 24/7 АЗС (16) по трассе в сторону Батырево - 450.000 рублей
            \nМагазин 24/7 АЗС (22) около автосалона Н/К - 450.000 рублей
            \nМагазин 24/7 (23) около Рублёвки - 700.000 рублей
            \nМагазин 24/7 (24) г. Лыткарино - 350.000 рублей
            \nМагазин 24/7 АЗС (25) около завода - 450.000 рублей
            \nМагазин 24/7 АЗС (26) шоссе в сторону Батырево - 450.000 рублей
            \nМагазин 24/7 АЗС (37) р. Егоровка - 450.000 рублей
            \nМагазин 24/7 АЗС (39) около автоугона - 450.000 рублей
            \nМагазин 24/7 АЗС (40) шоссе из Батырево в Арзамас - 450.000 рублей
        """,
        "Одежда": """
            Магазин одежды г. Южный (1) - 5.000.000 рублей
            \nМагазин одежды пгт. Батырево (5) - 2.000.000 рублей
            \nМагазин одежды г. Арзамас (9) - 5.000.000 рублей
        """,
        "Закусочные": """
            Закусочная пгт. Батырево (4) около автошколы - 500.000 рублей
            \nЗакусочная г. Южный (2) около автоуна - 900.000 рублей
            \nЗакусочная пгт. Батырево (7) около армии - 650.000 рублей
            \nЗакусочная г. Арзамас (11) около спавна - 1.000.000 рублей
            \nЗакусочная г. Арзамас, около перекрестка - 1.000.000 рублей
            \nЗакусочная г. Арзамас на спавне - 900.000 рублей
            \nЗакусочная р. Егоровка (36) - 700.000 рублей
        """,
        "Авто/Мото": """
            Автосалон низкого класса (0) - 10.000.000 рублей
            \nАвтосалон среднего класса (28) - 100.000.000 рублей
            \nАвтосалон премиум класса (27) - 200.000.000 рублей
            \nАвтосалон грузовых автомобилей (38) - 50.000.000 рублей
            \nМотосалон 'Harley Dayson' (41) место неизвестно - 50.000.000 рублей
        """,
        "Амуниция": """
            Амуниция г. Арзамас (14) - 1.200.000 рублей
            \nАмуниция г. Южный (19) - 1.200.000 рублей
        """,
        "Казино": "Казино (30) - 150.000.000 рублей",
        "Автомастерские": """
            СТО (29) - 50.000.000 рублей
            \nТюнинг Тонировки (33) - 70.000.000 рублей
            \nТюнинг Занижения (34) - 70.000.000 рублей
            \nЧип-тюнинг (35) - 70.000.000 рублей
        """,
        "Аксессуары": """
            Аксессуары г. Южный (31) около амуниции - 10.000.000 рублей
            \nАксессуары г. Арзамас (32) около перекрестка - 10.000.000 рублей
        """,
        "АЗС": """
            АЗС (0) около автоугона - 800.000 рублей
            \nАЗС (1) около автосалона низкого класса - 800.000 рублей
            \nАЗС (2) около деревни "Гарель" - 800.000 рублей
            \nАЗС (3) около завода - 800.000 рублей
            \nАЗС (4) шоссе в сторону Батырево - 800.000 рублей
            \nАЗС (5) пгт. Егоровка - 800.000 рублей
            \nАЗС (6) г. Лыткарино - 800.000 рублей
            \nАЗС (7) шоссе из г. Арзамаса в Батырево - 800.000 рублей
        """,
    }
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("🏠Меню", callback_data='main_menu')
    keyboard.add(button1)
    # Отправка списка автомобилей
    bot.send_message(user_id, business_prices[car_type], reply_markup=keyboard)


def handler_car_prices(call):
    user_id = call.message.chat.id
    keyboard = types.InlineKeyboardMarkup(row_width=2)  # 2 кнопки в ряд

    # Кнопки для типов машин
    button1 = types.InlineKeyboardButton("Низкий класс", callback_data='low_class_cars')
    button2 = types.InlineKeyboardButton("Класс Люкс", callback_data='luxury_cars')
    button3 = types.InlineKeyboardButton("Класс Люкс 2", callback_data='luxury_cars_2')
    button4 = types.InlineKeyboardButton("Мототранспорт", callback_data='motorcycles')
    button5 = types.InlineKeyboardButton("Назад", callback_data='guides')

    keyboard.add(button1, button2, button3, button4, button5)
    bot.send_message(call.message.chat.id, "Выберите тип автомобилей:", reply_markup=keyboard)


def handler_biznes_prices(call):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("24/7", callback_data='24/7')
    button2 = types.InlineKeyboardButton("Магазин одежды", callback_data='Магазин одежды')
    button3 = types.InlineKeyboardButton("Закусочные", callback_data='Закусочные')
    button4 = types.InlineKeyboardButton("Автосалоны/Мотосалоны", callback_data='Автосалоны/Мотосалоны')
    button6 = types.InlineKeyboardButton("Амуниции", callback_data='Амуниции')
    button7 = types.InlineKeyboardButton("Казино", callback_data='Казино')
    button8 = types.InlineKeyboardButton("Автомастерские", callback_data='Автомастерские')
    button9 = types.InlineKeyboardButton("Магазины акссесуаров", callback_data='Магазины акссесуаров')
    button10 = types.InlineKeyboardButton("АЗС", callback_data='АЗС')
    button5 = types.InlineKeyboardButton("Назад", callback_data='guides')

    keyboard.add(button1, button2, button3, button4, button6, button7, button8, button9, button10, button5)
    bot.send_message(call.message.chat.id, "Выберите тип бизнеса:", reply_markup=keyboard)


def handler_offer_news(call):
    user_id = call.message.chat.id
    bot.send_message(user_id,
                     "Отправьте нам фотографии, видео и любую другую информацию, которую вы хотите поделиться.\n\nВсе ваши сообщения будут рассмотрены администрацией!\n\nВ случае актуальной новость администратор начислит вам 100 HypeCoin")
    bot.register_next_step_handler(call.message, process_news_suggestion)


biographies = {}


def get_biography_info(message):
    user_id = message.chat.id
    biographies[user_id] = {}
    bio_data = {}
    current_question = 0  # Keep track of the current question

    def ask_next_question():
        nonlocal current_question
        if current_question < len(questions):
            question = questions[current_question]
            bot.send_message(user_id, question)
            bot.register_next_step_handler(message, collect_bio_data, bio_data)
        else:
            bot.send_message(user_id, "Подождите, идет генерация...")
            generate_biography(user_id, bio_data)  # All questions answered

    def collect_bio_data(message, bio_data):
        nonlocal current_question
        user_id = message.chat.id
        data = message.text
        if data == "🏠 Главное меню":
            start(message)
            return

        # Check if the message is a reply to a question
        if message.reply_to_message:
            question = message.reply_to_message.text
            bio_data[question] = data
            biographies[user_id][question] = data
            print(bio_data)
            current_question += 1  # Move to the next question only if the user replied correctly
        else:
            bot.send_message(user_id, "Пожалуйста, ответьте на вопрос, используя функцию 'Ответить'.")
        ask_next_question()  # Ask the same question again if the user didn't reply correctly

    ask_next_question()  # Start the conversation


def process_news_suggestion(message):
    news_suggestion = message.text
    user_mention = f"@{message.from_user.username}"

    if news_suggestion == "🏠 Главное меню":
        start(message)
        return

    admin_id = [786320574, 1079020959]  # ID of the user to receive suggestions
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("🏠Меню", callback_data='main_menu')
    keyboard.add(button1)

    for id in admin_id:
        # If it's a text message, send it directly
        if message.content_type == 'text':
            bot.send_message(id, f"Новое предложение новости от {user_mention}:\n\n{news_suggestion}")
        # If it's a photo, send it with the caption
        elif message.content_type == 'photo':
            bot.send_photo(id, message.photo[-1].file_id,
                           caption=f"Новое предложение новости от {user_mention}:\n\n{message.caption}")
        # If it's a video, send it with the caption
        elif message.content_type == 'video':
            bot.send_video(id, message.video.file_id,
                           caption=f"Новое предложение новости от {user_mention}:\n\n{message.caption}")
        # Handle other content types as needed

    bot.send_message(message.chat.id, "Спасибо за предложение новости!", reply_markup=keyboard)


def handler_write_biography(call):
    user_id = call.message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🏠 Главное меню"))
    bot.send_message(user_id,
                     "Давайте создадим вашу RP-биографию!\nПожалуйста, отвечайте на вопросы, используя функцию 'Ответить'.",
                     reply_markup=keyboard)
    get_biography_info(call.message)


def generate_biography(user_id, bio_data):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("🏠Меню", callback_data='main_menu')
    keyboard.add(button1)

    for key, value in bio_data.items():
        if isinstance(value, set):
            bio_data[key] = list(value)
    # Create the prompt for ChatGPT
    prompt = (
            "Напиши подробную roleplay биографию исходя из этих данных:\n\n"
            + "\n".join(f"{question}: {answer}" for question, answer in biographies[user_id].items())
            + "\n\n( От сюда требуется расписать каждый из пунктов по примеру, не переписывай в тупуб текст из примера, придумай свою историю исходя из данных)\n\nПример: Детство: все детство Саи прошло в Пгт. Батырево,рос он в не самой богатой семье,Папа изначально был лейтенантом ГИБДД.но зарплаты хватало лишь на пропитание детей,после того как отца подставили на работе,и обманули на 2-х месячную зарплату,у него затаилась глубокая обида на всех тех людей которые учавствовали в его обмане,через некоторое время папа узнал о ОПГ города Батырево,там ему обещали большие деньги,и очень громкие дела,папе не оставалось выбора т.к нужно было содержать семью и он вступил в группировку,изначально его там никто не уважал,и так называемого «авторитета» он там не имел,но после пары громких дел в Г.Южный и в Г. Арзамас,он был повышен по масти и зарабатывал не самым честным путем большие деньги,но в конце концов,был убит при ограблении Грузовика Инкосаторов перевозящих больше миллиона рублей,в то время как мама была обычной домохозяйкой,и не о каких его преступных делах не знала,сам же ребенок в столь раннем возрасте не понимал чем занимается его отец,после его смерти мама лгала ему что он погиб при неудачном случае в дтпЮность и взрослая жизнь: в осознанном возрасте,обеспечивая семью,став единственным мужчиной в раннем возрасте,парень бросил учебу после 9-го класса и не стал заниматься своим образованием т.к маму нужно было обеспечивать,он работал обычным поваром,в забегаловке г.Арзамас,куда они переехали вместе с мамой после смерти отца,зарплаты хватало лишь на оплату квартиры,в один день парню достался счастливый билет, и его узнали члены ОПГ г.Арзамас,т.к фамилия его отца была на слуху,они проявили должное уважение к парню и приняли к себе в банду,со временем Сая был все более уважаемым и стал лидером данной группировки,и нажил себе хорошее имущество за счет успешных ограблений в Г.Лыткарино Настоящее время: Сая был очень уважаем во всей области,его фамилия была во всех заголовках газет,но правоохранительные органы не могли добраться до лидера группировки,Сая был владельцем транспортного средства Гелентваген нового поколения и был «крышей» многих бизнесов,которые выплачивали ему за крышевание их бизнесов ")

    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{f"role": "user", "content": {prompt}}],
        headers=headers
    )
    print(response.choices[0].message.content)
    # Extract the generated biography text
    biography_text = response.choices[0].message.content

    # Send the biography to the user
    bot.send_message(user_id, biography_text, reply_markup=keyboard)


def handle_main_menu(message):
    user_id = message.chat.id
    main_menu(message)


def level_up_info(call):
    user_id = call.message.chat.id
    message = """
Это оставлять ваш телефон на так называемый "РП сон" это означает что с 23:00 по 6:00 по мск вас не кикает с сервера за AFK .Поэтому вы просто идете в какой-то ближайший подъезд делаете /anim 31 и оставляете телефон на ночь, Лучше всего перед этим закупиться по фулам в ларьке , так как если вы не закупитесь то у вас быстро закончится HP и вы окажитесь в Больнице, оттуда вас уже могут кикнуть за помеху.Лучше всего чтоб когда вы оставляли телефон на РП Сон у вас бы была VIP.
    """
    bot.send_message(user_id, message)
    handler_guides(call)


def save_data():
    global new_users
    try:
        with open("users.json", "r") as f:
            existing_users = json.load(f)
        for user_id, user_data in users.items():
            if str(user_id) in existing_users:
                existing_users[str(user_id)].update(user_data)
            else:
                existing_users[str(user_id)] = user_data

        new_users = existing_users  # Update users in data to be saved

    except FileNotFoundError:
        print(1)

    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(new_users, f, ensure_ascii=False, indent=4)

    with open('reward_links.json', 'w', encoding='utf-8') as f:
        json.dump(reward_links, f, ensure_ascii=False, indent=4)


def load_data():
    global users, referrals, reward_links
    try:
        with open('users.json') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}

    try:
        with open('referrals.json', 'r') as f:
            referrals = json.load(f)
    except FileNotFoundError:
        referrals = {}

    try:
        with open('reward_links.json', 'r') as f:
            reward_links = json.load(f)
    except FileNotFoundError:
        reward_links = {}


load_data()

if __name__ == '__main__':
    try:
        bot.infinity_polling(none_stop=True, timeout=90, long_polling_timeout=10)
    except Exception as e:
        print(f"Произошла ОШИБКА!: {e}")