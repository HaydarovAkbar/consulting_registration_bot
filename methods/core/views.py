from telegram import Update
from telegram.ext import CallbackContext
from states import States as st
from db.models import User
from asgiref.sync import async_to_sync


async def start(update: Update, context: CallbackContext):
    await User.objects.get_or_create(chat_id=update.message.chat_id)
    await update.message.reply_html(text="<b>Ism Familiyangizni kiriting:</b>")
    return st.get_fullname


async def get_fullname(update: Update, context: CallbackContext):
    context.user_data['fullname'] = update.message.text
    await update.message.reply_html(text="<b>Yoshingizni kiriting:</b>")
    return st.get_age


async def get_age(update: Update, context: CallbackContext):
    context.user_data['age'] = update.message.text
    await update.message.reply_html(text="<b>Telefon raqamingizni kiriting:</b>")
    return st.get_phone


async def get_phone(update: Update, context: CallbackContext):
    context.user_data['phone'] = update.message.text
    await update.message.reply_html(text="<b>Qaysi darajadasiz kiriting:</b>")
    return st.get_level


async def get_level(update: Update, context: CallbackContext):
    context.user_data['level'] = update.message.text
    await update.message.reply_html(text="<b>Mamlakatingizni kiriting:</b>")
    return st.get_country


async def get_country(update: Update, context: CallbackContext):
    context.user_data['country'] = update.message.text
    await update.message.reply_html(text="<b>Ma'lumotlar saqlandi</b>")
    return st.menu


sync_start = async_to_sync(start)


def start_sync(update, context):
    return sync_start(update, context)
