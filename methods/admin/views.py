from telegram import Update
from telegram.ext import CallbackContext
from states import States as st
from db.models import User, Admin, Message, Country, Reklama
from methods.admin.keyboards import AdminKeyboards as adm_key


def admin(update: Update, context: CallbackContext):
    if Admin.objects.filter(chat_id=update.message.chat_id).exists():
        update.message.reply_html(text="<code>Admin xush kelibsiz!</code>",
                                  reply_markup=adm_key.base())
        return st.admin_menu


def back(update: Update, context: CallbackContext):
    if Admin.objects.filter(chat_id=update.message.chat_id).exists():
        update.message.reply_html(text="<code>Admin xush kelibsiz!</code>",
                                  reply_markup=adm_key.base())
        return st.admin_menu


def add_admin(update: Update, context: CallbackContext):
    update.message.reply_html(text="<b>Yangi adminni telegram id-sini kiriting:</b>", reply_markup=adm_key.back())
    return st.add_admin


def add_admin_succesfuly(update: Update, context: CallbackContext):
    admin_id = update.message.text
    if admin_id.isdigit():
        Admin.objects.create(
            chat_id=admin_id,
            username=admin_id
        )
        update.message.reply_html(text="<b>Admin muvaffaqiyatli qo'shildi!</b>", reply_markup=adm_key.base())
        return st.admin_menu
    else:
        error_msg = f"<u>{update.message.text}</u> telegram id raqam emas! Iltimos qaytadan kiriting! (Ma'lumot uchun telegram id faqat raqamlardan iborat bo'ladi)"
        update.message.reply_html(text=error_msg, reply_markup=adm_key.back())


def del_admin(update: Update, context: CallbackContext):
    admins = Admin.objects.all()
    adm_msg = f"<b>Adminlar ro'yxati:</b>\n\n"
    for i in range(len(admins)):
        adm_msg += f"{i + 1}. {admins[i].username}    [<code>{admins[i].chat_id}</code>]\n"
    update.message.reply_html(text=adm_msg)
    update.message.reply_html(text="<b>O'chiriladigan adminni telegram id-sini kiriting:</b>",
                              reply_markup=adm_key.back())
    return st.del_admin


def del_admin_confirm(update: Update, context: CallbackContext):
    admin_id = update.message.text
    if admin_id.isdigit():
        if Admin.objects.filter(chat_id=admin_id).exists():
            Admin.objects.filter(chat_id=admin_id).delete()
            update.message.reply_html(text="<b>Admin muvaffaqiyatli o'chirildi!</b>", reply_markup=adm_key.base())
        else:
            update.message.reply_html(text="<b>Bunday admin topilmadi!</b>", reply_markup=adm_key.base())
        return st.admin_menu
    else:
        error_msg = f"<u>{update.message.text}</u> telegram id raqam emas! Iltimos qaytadan kiriting! (Ma'lumot uchun telegram id faqat raqamlardan iborat bo'ladi)"
        update.message.reply_html(text=error_msg, reply_markup=adm_key.back())


def message(update: Update, context: CallbackContext):
    update.message.reply_html(text="<b>Xabarni qaysi malumotini o'zgartirmoqchisiz tanlang</b>",
                              reply_markup=adm_key.message())
    return st.message


def message_text(update: Update, context: CallbackContext):
    old_msg = Message.objects.last()
    if old_msg:
        update.message.reply_html(text=f"<b>Eski xabar:</b>\n\n{old_msg.text}")
    update.message.reply_html(text="<b>Yangi xabarni kiriting:</b>", reply_markup=adm_key.back())
    return st.message_text


def message_text_confirm(update: Update, context: CallbackContext):
    text = update.message.text
    last_msg = Message.objects.last()
    if last_msg:
        last_msg.text = text
        last_msg.save()
    else:
        Message.objects.create(text=text)
    update.message.reply_html(text="<b>Xabar texti muvaffaqiyatli o'zgartirildi!</b>", reply_markup=adm_key.base())
    return st.admin_menu


def message_photo(update: Update, context: CallbackContext):
    old_msg = Message.objects.last()
    if old_msg.photo:
        update.message.reply_photo(caption=f"<b>Eski rasm:</b>", photo=old_msg.photo, parse_mode="HTML")
    update.message.reply_html(text="<b>Yangi rasmda yuboring:</b>", reply_markup=adm_key.back())
    return st.message_photo


def message_photo_confirm(update: Update, context: CallbackContext):
    photo = update.message.photo[-1].file_id
    last_msg = Message.objects.last()
    if last_msg:
        last_msg.photo = photo
        last_msg.save()
    else:
        Message.objects.create(photo=photo)
    update.message.reply_html(text="<b>Xabar rasmi muvaffaqiyatli o'zgartirildi!</b>", reply_markup=adm_key.base())
    return st.admin_menu


def message_location(update: Update, context: CallbackContext):
    old_msg = Message.objects.last()
    if old_msg.longitude:
        update.message.reply_location(latitude=old_msg.latitude, longitude=old_msg.longitude)
    update.message.reply_html(text="<b>Yangi joylashuvni yuboring:</b>", reply_markup=adm_key.back())
    return st.message_location


def message_location_confirm(update: Update, context: CallbackContext):
    location = update.message.location
    last_msg = Message.objects.last()
    if last_msg:
        last_msg.latitude = location.latitude
        last_msg.longitude = location.longitude
        last_msg.save()
    else:
        Message.objects.create(latitude=location.latitude, longitude=location.longitude)
    update.message.reply_html(text="<b>Xabar joylashuvi muvaffaqiyatli o'zgartirildi!</b>", reply_markup=adm_key.base())
    return st.admin_menu


def add_country(update: Update, context: CallbackContext):
    all_country = Country.objects.all()
    msg = f"<b>Davlatlar ro'yxati:</b>\n\n"
    for i in range(len(all_country)):
        msg += f"{i + 1}. {all_country[i].icon} {all_country[i].name}\n"
    update.message.reply_html(text=msg)
    update.message.reply_html(text="<b>Qo'shiladigan davlat nomini kiriting:</b>", reply_markup=adm_key.back())
    return st.add_country


def add_country_icon(update: Update, context: CallbackContext):
    country_name = update.message.text
    if Country.objects.filter(name=country_name).exists():
        update.message.reply_html(text="<b>Bunday davlat ro'yxatda mavjud!</b>", reply_markup=adm_key.base())
        return st.admin_menu
    context.user_data['country_name'] = country_name
    update.message.reply_html(text="<b>Davlat bayrog'ini yuboring:</b>", reply_markup=adm_key.back())
    return st.add_country_icon


def add_country_confirm(update: Update, context: CallbackContext):
    country_icon = update.message.text
    country_name = context.user_data['country_name']
    Country.objects.create(
        name=country_name,
        icon=country_icon
    )
    update.message.reply_html(text="<b>Davlat muvaffaqiyatli qo'shildi!</b>", reply_markup=adm_key.base())
    return st.admin_menu


def reklama(update: Update, context: CallbackContext):
    update.message.reply_html(text="<b>Reklama xabarini yuboring:</b>", reply_markup=adm_key.back())
    return st.reklama


def send_rek_all_users(update: Update, context: CallbackContext):
    counter = 0
    for user in User.objects.all():
        update.message.copy(chat_id=user.chat_id)
        counter += 1
    all_user_count = User.objects.all().count()
    update.message.reply_html(
        text=f"<b>Reklama muvaffaqiyatli yuborildi! </b>    Aktivlar soni: {counter}, Barchasi: {all_user_count}",
        reply_markup=adm_key.base())
    return st.admin_menu
