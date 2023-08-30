import sys

sys.dont_write_bytecode = True
# Django specific settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django

django.setup()
from decouple import config
# Import your models for use in your script
from db.models import *
import logging

TOKEN = config('TOKEN')
from telegram import Update, ForceReply, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters, ConversationHandler
from methods.core.views import start, get_fullname, get_age, get_phone, get_level, get_country
from methods.admin.views import admin
from states import States as st

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# app = ApplicationBuilder().token(TOKEN).build()
update = Updater(token=TOKEN, use_context=True, workers=500)
app = update.dispatcher

handler = ConversationHandler(
    entry_points=[CommandHandler('start', start),
                  CommandHandler('admin', admin)
                  ],
    states={
        st.get_fullname: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.text, get_fullname)],
        st.get_age: [
            CommandHandler('start', start),
            CommandHandler('admin', admin), MessageHandler(Filters.text, get_age)],
        st.get_phone: [
            CommandHandler('start', start),
            CommandHandler('admin', admin), MessageHandler(Filters.text, get_phone)],
        st.get_level: [
            CommandHandler('start', start),
            CommandHandler('admin', admin), MessageHandler(Filters.text, get_level)],
        st.get_country: [
            CommandHandler('start', start),
            CommandHandler('admin', admin), MessageHandler(Filters.text, get_country)],
    },
    fallbacks=[CommandHandler('start', start),
               CommandHandler('admin', admin), ]
)

app.add_handler(handler=handler)

update.start_polling()
update.idle()
print('started polling')
