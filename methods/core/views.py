from telegram import Update
from telegram.ext import CallbackContext
from states import States as st
from db.models import User


def start(update: Update, context: CallbackContext):
    # await User.objects.get_or_create(chat_id=update.message.chat_id)
    update.message.reply_html(text="<b>Ism Familiyangizni kiriting:</b>")
    return st.get_fullname


def get_fullname(update: Update, context: CallbackContext):
    context.user_data['fullname'] = update.message.text
    update.message.reply_html(text="<b>Yoshingizni kiriting:</b>")
    return st.get_age


def get_age(update: Update, context: CallbackContext):
    context.user_data['age'] = update.message.text
    update.message.reply_html(text="<b>Telefon raqamingizni kiriting:</b>")
    return st.get_phone


def get_phone(update: Update, context: CallbackContext):
    context.user_data['phone'] = update.message.text
    update.message.reply_html(text="<b>Qaysi darajadasiz kiriting:</b>")
    return st.get_level


def get_level(update: Update, context: CallbackContext):
    context.user_data['level'] = update.message.text
    update.message.reply_html(text="<b>Mamlakatingizni kiriting:</b>")
    return st.get_country


def get_country(update: Update, context: CallbackContext):
    context.user_data['country'] = update.message.text
    User.objects.create(
        fullname=context.user_data['fullname'],
        age=context.user_data['age'],
        phone=context.user_data['phone'],
        level=context.user_data['level'],
        country=context.user_data['country'],
        chat_id=update.message.chat_id,
        username=update.message.from_user.username
    )
    update.message.reply_html(text="<b>Ma'lumotlar saqlandi</b>")
    return st.menu
