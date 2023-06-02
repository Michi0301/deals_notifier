from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.deal_search.static_text import search_button_text, create_search_button_text, delete_search_button, add_branch, delete_branch
from tgbot.handlers.deal_search.manage_data import PRODUCT_SEARCH, PRODUCT_SEARCH_REQUEST, PRODUCT_SEARCH_REQUEST_DELETE, ADD_BRANCH, DELETE_BRANCH

def make_keyboard_for_product_select_command(pim_id) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(search_button_text, callback_data=f'{PRODUCT_SEARCH}:{pim_id}')
    ]]

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_register_search_command(pim_id, price) -> InlineKeyboardMarkup:
    callback_data = f'{PRODUCT_SEARCH_REQUEST}:{pim_id}:{price}'
    buttons = [[
        InlineKeyboardButton(create_search_button_text, callback_data=callback_data)
    ]]

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_search_request_deletion(search_request_id):
    callback_data = f'{PRODUCT_SEARCH_REQUEST_DELETE}:{search_request_id}'
    buttons = [[
        InlineKeyboardButton(delete_search_button, callback_data=callback_data)
    ]]

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_branch_selection(branch_id, branch_name):
    callback_data = f'{ADD_BRANCH}:{branch_id}:{branch_name}'
    buttons = [[
        InlineKeyboardButton(add_branch, callback_data=callback_data)
    ]]
    
    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_branch_delete(branch_id):
    callback_data = f'{DELETE_BRANCH}:{branch_id}'
    buttons = [[
        InlineKeyboardButton(delete_branch, callback_data=callback_data)
    ]]
    
    return InlineKeyboardMarkup(buttons)
