from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from ..dictionary import AdminKeyboardMessage as adm_key


class AdminKeyboards:
    @staticmethod
    def base():
        msg = adm_key.base
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [msg[0], msg[1]],
                [msg[2], msg[3]],
                [msg[4]],
            ],
            resize_keyboard=True
        )
        return keyboard

    @staticmethod
    def back():
        msg = adm_key.back
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [msg[0]],
            ],
            resize_keyboard=True
        )
        return keyboard

    @staticmethod
    def message():
        msg = adm_key.message
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [msg[0]],
                [msg[1]],
                [msg[2]],
                [msg[3]],
            ],
            resize_keyboard=True
        )
        return keyboard