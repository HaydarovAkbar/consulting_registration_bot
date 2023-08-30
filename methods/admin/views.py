from telegram import Update
from telegram.ext import CallbackContext
from states import States as st
from db.models import User, Admin, Message, Country, Reklama


def admin(update: Update, context: CallbackContext):
    print(Admin.objects.filter(chat_id=update.message.chat_id).exists())
    if Admin.objects.filter(chat_id=update.message.chat_id).exists():
        update.message.reply_html(text="<code>Admin xush kelibsiz!</code>")
        return st.admin_menu
    else:
        update.message.reply_html(text="<code>Admin xush kelibsiz!</code>")
        return st.admin_menu


