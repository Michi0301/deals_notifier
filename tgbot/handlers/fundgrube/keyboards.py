from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.fundgrube.static_text import search_button_text, register_search_button_text
from tgbot.handlers.fundgrube.manage_data import PRODUCT_SEARCH
from tgbot.handlers.fundgrube.manage_data import PRODUCT_SEARCH_REQUEST
import urllib



def make_keyboard_for_product_select_command(pim_id) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(search_button_text, callback_data=f'{PRODUCT_SEARCH}:{pim_id}')
    ]]

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_register_search_command(provider,pim_id, price) -> InlineKeyboardMarkup:
    callback_data = f'{PRODUCT_SEARCH_REQUEST}:{provider}:{pim_id}:{price}'
    buttons = [[
        InlineKeyboardButton(register_search_button_text, callback_data=callback_data)
    ]]

    return InlineKeyboardMarkup(buttons)
