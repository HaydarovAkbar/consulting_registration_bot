import sys

sys.dont_write_bytecode = True
# Django specific settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django

django.setup()
from decouple import config
# Import your models for use in your script
import logging

TOKEN = config('TOKEN')
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from methods.core.views import start, get_fullname, get_age, get_phone, get_level, get_country
from methods.admin.views import admin, add_admin, add_admin_succesfuly, del_admin, del_admin_confirm, back, message, \
    message_text, message_text_confirm, message_photo, message_photo_confirm, message_location, message_location_confirm, \
    add_country, add_country_icon, add_country_confirm, reklama
from states import States as st
from methods.dictionary import AdminKeyboardMessage as adm_msg

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
            CommandHandler('admin', admin),
            CallbackQueryHandler(get_country)],
        st.admin_menu: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^' + adm_msg.base[0] + '$'), add_admin),
            MessageHandler(Filters.regex('^' + adm_msg.base[1] + '$'), del_admin),
            MessageHandler(Filters.regex('^' + adm_msg.base[2] + '$'), message),
            MessageHandler(Filters.regex('^' + adm_msg.base[3] + '$'), reklama),
            MessageHandler(Filters.regex('^' + adm_msg.base[4] + '$'), add_country),

            MessageHandler(Filters.regex('^' + adm_msg.back[0] + '$'), back),
        ],

        st.add_admin: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^' + adm_msg.back[0] + '$'), back),
            MessageHandler(Filters.text, add_admin_succesfuly),
        ],

        st.del_admin: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^' + adm_msg.back[0] + '$'), back),
            MessageHandler(Filters.text, del_admin_confirm),
        ],

        st.message: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^' + adm_msg.message[0] + '$'), message_text),
            MessageHandler(Filters.regex('^' + adm_msg.message[1] + '$'), message_photo),
            MessageHandler(Filters.regex('^' + adm_msg.message[2] + '$'), message_location),
            MessageHandler(Filters.regex('^' + adm_msg.message[3] + '$'), back),
        ],

        st.message_text: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^' + adm_msg.back[0] + '$'), back),
            MessageHandler(Filters.text, message_text_confirm),
        ],
        st.message_photo: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^' + adm_msg.back[0] + '$'), back),
            MessageHandler(Filters.photo, message_photo_confirm),
        ],
        st.message_location: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^' + adm_msg.back[0] + '$'), back),
            MessageHandler(Filters.location, message_location_confirm),
        ],

        st.add_country: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^' + adm_msg.back[0] + '$'), back),
            MessageHandler(Filters.text, add_country_icon),
        ],
        st.add_country_icon: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^' + adm_msg.back[0] + '$'), back),
            MessageHandler(Filters.text, add_country_confirm),
        ],
    },
    fallbacks=[CommandHandler('start', start),
               CommandHandler('admin', admin), ]
)

app.add_handler(handler=handler)

update.start_polling()
print('started polling')
update.idle()
