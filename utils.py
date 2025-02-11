import telebot


def main_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_status = telebot.types.KeyboardButton(text="Статус")
    button_connect = telebot.types.KeyboardButton(text="Подключиться")
    button_pay = telebot.types.KeyboardButton(text="Оплатить")
    button_help = telebot.types.KeyboardButton(text="Помощь")
    keyboard.add(button_status, button_connect)
    keyboard.add(button_pay, button_help)
    return keyboard


def make_back_inline_button_markup() -> telebot.types.InlineKeyboardMarkup:
    markup = telebot.types.InlineKeyboardMarkup()
    itembtn_str = telebot.types.InlineKeyboardButton("Назад", callback_data="back")
    markup.add(itembtn_str)
    return markup


def make_connect_markup() -> telebot.types.InlineKeyboardMarkup:
    markup = telebot.types.InlineKeyboardMarkup()
    # iOS
    download_ios = telebot.types.InlineKeyboardButton("Скачать iOS", url="https://apps.apple.com/ru/app/v2raytun/id6476628951")
    connect_ios = telebot.types.InlineKeyboardButton("Подключить iOS", callback_data="make_config")
    markup.add(download_ios, connect_ios)
    # Android
    download_android = telebot.types.InlineKeyboardButton("Скачать Android", url="https://play.google.com/store/apps/details?id=com.v2raytun.android")
    connect_android = telebot.types.InlineKeyboardButton("Подключить Android", callback_data="make_config")
    markup.add(download_android, connect_android)
    # PC
    download_pc = telebot.types.InlineKeyboardButton("Скачать PC", url="https://github.com/hiddify/hiddify-next/releases/latest/download/Hiddify-Windows-Setup-x64.exe")
    connect_pc = telebot.types.InlineKeyboardButton("Подключить PC", callback_data="make_config")
    markup.add(download_pc, connect_pc)
    # Back Button
    itembtn_str = telebot.types.InlineKeyboardButton("Назад", callback_data="back")
    markup.add(itembtn_str)
    return markup


# def make_pay_markup() -> telebot.types.InlineKeyboardMarkup:
#     markup = telebot.types.InlineKeyboardMarkup()
#     pay_1_month = telebot.types.InlineKeyboardButton("1 месяц", callback_data="pay_1")
#     markup.add(pay_1_month)
#     pay_4_month = telebot.types.InlineKeyboardButton("4 месяца", callback_data="pay_4")
#     markup.add(pay_4_month)
#     pay_12_month = telebot.types.InlineKeyboardButton("12 месяцев", callback_data="pay_12")
#     markup.add(pay_12_month)
#     itembtn_str = telebot.types.InlineKeyboardButton("Назад", callback_data="back")
#     markup.add(itembtn_str)
#     return markup


def make_help_markup() -> telebot.types.InlineKeyboardMarkup:
    markup = telebot.types.InlineKeyboardMarkup()
    iphone_ipad = telebot.types.InlineKeyboardButton("iPhone/iPad", url="https://telegra.ph/Podklyuchenie-iPhone--iPad-02-04")
    markup.add(iphone_ipad)
    android = telebot.types.InlineKeyboardButton("Android", url="https://telegra.ph/Podklyuchenie-Android-smartfona-02-04")
    markup.add(android)
    windows = telebot.types.InlineKeyboardButton("Windows", url="https://telegra.ph/Podklyuchenie-Windows-PK-02-04")
    markup.add(windows)
    macos = telebot.types.InlineKeyboardButton("MacOS", url="https://telegra.ph/Podklyuchenie-Apple-MacBook-02-04")
    markup.add(macos)
    appletv = telebot.types.InlineKeyboardButton("AppleTV", url="https://telegra.ph/Podklyuchenie-AppleTV-02-04")
    markup.add(appletv)
    androidtv = telebot.types.InlineKeyboardButton("AndroidTV", url="https://telegra.ph/Podklyuchenie-AndroidTV-02-04")
    markup.add(androidtv)
    itembtn_str = telebot.types.InlineKeyboardButton("Назад", callback_data="back")
    markup.add(itembtn_str)
    return markup



def make_pay_markup() -> telebot.types.InlineKeyboardMarkup:
    markup = telebot.types.InlineKeyboardMarkup()
    pay_1_month = telebot.types.InlineKeyboardButton("1 месяц", callback_data="pay_1_month")
    pay_4_month = telebot.types.InlineKeyboardButton("4 месяца", callback_data="pay_4_month")
    pay_12_month = telebot.types.InlineKeyboardButton("12 месяцев", callback_data="pay_12_month")
    markup.add(pay_1_month)
    markup.add(pay_4_month)
    markup.add(pay_12_month)
    back = telebot.types.InlineKeyboardButton("Назад", callback_data="back")
    markup.add(back)
    return markup

# def make_pay_markup() -> telebot.types.InlineKeyboardMarkup:
#     markup = telebot.types.InlineKeyboardMarkup()
#     stars = telebot.types.InlineKeyboardButton("Telegram Stars", callback_data="buy_tg_stars")
#     crypt = telebot.types.InlineKeyboardButton("Cryptomus", url="https://pay.cryptomus.com/pay/f60edfeb-b7de-4bfe-a06d-2a336f4fa8dc")
#     yoomoney = telebot.types.InlineKeyboardButton("YooMoney", callback_data="buy_yoomoney")
#     markup.add(stars)
#     markup.add(crypt)
#     markup.add(yoomoney)   
#     #Back
#     itembtn_str = telebot.types.InlineKeyboardButton("Назад", callback_data="back")
#     markup.add(itembtn_str)    
#     return markup
