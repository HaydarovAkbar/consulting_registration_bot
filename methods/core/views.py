import time

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from states import States as st
from db.models import User, Country, Message, ChannelMessage
from decouple import config

CHANNEL_ID = config('CHANNEL_ID')


def start(update: Update, context: CallbackContext):
    update.message.reply_html(text="<b>Ism Familiyangizni kiriting:</b>")
    return st.get_fullname


def get_fullname(update: Update, context: CallbackContext):
    context.user_data['fullname'] = update.message.text
    update.message.reply_html(text="<b>Yoshingizni kiriting:</b>")
    return st.get_age


def get_age(update: Update, context: CallbackContext):
    if not update.message.text.isdigit() or int(update.message.text) < 0 or int(update.message.text) > 100:
        update.message.reply_html(text="<b>Yoshingizni raqamda kiriting:</b>")
        return st.get_age
    context.user_data['age'] = update.message.text
    update.message.reply_html(text="<b>Telefon raqamingizni qoldiring:</b>\n\n(Namuna: +998901234567)")
    return st.get_phone


def get_phone(update: Update, context: CallbackContext):
    msg = update.message.text
    if not msg.startswith('+') or not msg[1:].isdigit():
        update.message.reply_html(text="<b>Telefon raqamingizni xato kiritildi:\n\n(Namuna +998901234567)</b>")
        return st.get_phone
    context.user_data['phone'] = update.message.text
    update.message.reply_html(text="<b>IELTS & Ingliz tili darajangizni yozing: (IELTS, Duolingo yoki TOEFL):</b>")
    return st.get_level


def country_keyboard():
    all_country = Country.objects.all()
    keyboard = []
    for i in range(len(all_country)):
        keyboard.append([InlineKeyboardButton(text=all_country[i].icon + " " + all_country[i].name,
                                              callback_data=str(all_country[i].id))])
    return InlineKeyboardMarkup(keyboard)


def get_level(update: Update, context: CallbackContext):
    context.user_data['level'] = update.message.text
    update.message.reply_html(text="<b>Qaysi davlatga qiziqyapsiz?</b>", reply_markup=country_keyboard())
    return st.get_country


def get_country(update: Update, context: CallbackContext):
    query = update.callback_query
    country = Country.objects.get(id=query.data)
    if not User.objects.filter(chat_id=update.effective_user.id).exists():
        User.objects.create(
            fullname=context.user_data['fullname'],
            age=context.user_data['age'],
            phone=context.user_data['phone'],
            level=context.user_data['level'],
            country=country,
            chat_id=update.effective_user.id,
            username=update.effective_user.username
        )
    last_msg = ChannelMessage.objects.last()
    if last_msg:
        counter = last_msg.message_id + 1
    else:
        counter = 1
    ChannelMessage.objects.create(message_id=counter, text=f"""
#{update.effective_user.id}
Ismi: {context.user_data['fullname']}
Yoshi: {context.user_data['age']}
Raqami: {context.user_data['phone']}
Darajasi: {context.user_data['level']}
Davlat: {country.icon} {country.name}
""")
    channel_msg = f"""
#{counter}
<b>Ismi: <code>{context.user_data['fullname']}</code>
Yoshi: <code>{context.user_data['age']}</code>
Raqami: <code>{context.user_data['phone']}</code>
Darajasi: <code>{context.user_data['level']}</code>
Davlat: <code>{country.icon} {country.name}</code></b>
--------------------------
"""
    context.bot.send_message(chat_id=CHANNEL_ID, text=channel_msg, parse_mode="HTML")
    time.sleep(0.4)
    last_msg = Message.objects.last()
    if last_msg.text:
        query.edit_message_text(text=last_msg.text)
    else:
        query.edit_message_text(text="<b>Ma'lumotlaringiz jo'natildi</b>", parse_mode="HTML")
    context.user_data.clear()
    context.bot.send_location(chat_id=update.effective_user.id, latitude=last_msg.latitude,
                              longitude=last_msg.longitude)
    time.sleep(0.1)
    context.bot.send_photo(chat_id=update.effective_user.id, photo=last_msg.photo)
    return st.menu
