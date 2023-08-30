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
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, filters, ConversationHandler, \
    ApplicationBuilder
from methods.core.views import start_sync, get_fullname, get_age, get_phone, get_level, get_country
from states import States as st

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

app = ApplicationBuilder().token(TOKEN).build()

handler = ConversationHandler(
    entry_points=[CommandHandler('start', start_sync)],
    states={
        st.get_fullname: [
            CommandHandler('start', start_sync),
            MessageHandler(filters.TEXT, get_fullname)],
        st.get_age: [
            CommandHandler('start', start_sync), MessageHandler(filters.TEXT, get_age)],
        st.get_phone: [
            CommandHandler('start', start_sync), MessageHandler(filters.TEXT, get_phone)],
        st.get_level: [
            CommandHandler('start', start_sync), MessageHandler(filters.TEXT, get_level)],
        st.get_country: [
            CommandHandler('start', start_sync), MessageHandler(filters.TEXT, get_country)],
    },
    fallbacks=[CommandHandler('start', start_sync)]
)

app.add_handler(handler=handler)

app.run_polling()
print('started polling')
