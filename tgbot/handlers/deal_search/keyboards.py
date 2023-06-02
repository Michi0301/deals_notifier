from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.deal_search.static_text import search_button_text, create_search_button_text, delete_search_button_text, add_branch
from tgbot.handlers.deal_search.manage_data import PRODUCT_SEARCH, PRODUCT_SEARCH_REQUEST, PRODUCT_SEARCH_REQUEST_DELETE, BRANCH_SELECT




def make_keyboard_for_product_select_command(pim_id) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(search_button_text, callback_data=f'{PRODUCT_SEARCH}:{pim_id}')
    ]]

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_register_search_command(provider,pim_id, price) -> InlineKeyboardMarkup:
    callback_data = f'{PRODUCT_SEARCH_REQUEST}:{provider}:{pim_id}:{price}'
    buttons = [[
        InlineKeyboardButton(create_search_button_text, callback_data=callback_data)
    ]]

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_search_request_deletion(search_request_id):
    callback_data = f'{PRODUCT_SEARCH_REQUEST_DELETE}:{search_request_id}'
    buttons = [[
        InlineKeyboardButton(delete_search_button_text, callback_data=callback_data)
    ]]

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_branch_selection(provider, branch_id):
    callback_data = f'{BRANCH_SELECT}:{provider}:{branch_id}'
    buttons = [[
        InlineKeyboardButton(add_branch, callback_data=callback_data)
    ]]
    
    return InlineKeyboardMarkup(buttons)
