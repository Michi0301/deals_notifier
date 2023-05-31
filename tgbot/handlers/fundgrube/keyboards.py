from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.fundgrube.static_text import search_button_text
from tgbot.handlers.fundgrube.manage_data import PRODUCT_SELECT_SEARCH_BUTTON


def make_keyboard_for_product_select_command(product_id) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(search_button_text, callback_data=f'{PRODUCT_SELECT_SEARCH_BUTTON}:{product_id}')
    ]]

    return InlineKeyboardMarkup(buttons)
