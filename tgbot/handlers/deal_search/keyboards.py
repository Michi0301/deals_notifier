from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.deal_search.static_text import search_button_text_local, search_button_text_cheapest, create_search_button_text_local, delete_search_button, add_branch, delete_branch
from tgbot.handlers.deal_search.manage_data import PRODUCT_SEARCH, PRODUCT_SEARCH_REQUEST, PRODUCT_SEARCH_REQUEST_DELETE, ADD_BRANCH, DELETE_BRANCH

from deal_search.models import Notification

def make_keyboard_for_product_search_command(pim_id) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(search_button_text_local, callback_data=f'{PRODUCT_SEARCH}:{pim_id}:LOCAL'),
        InlineKeyboardButton(search_button_text_cheapest, callback_data=f'{PRODUCT_SEARCH}:{pim_id}:CHEAPEST')
    ]]

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_create_notification_command(pim_id) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(create_search_button_text_local, callback_data=f'{PRODUCT_SEARCH_REQUEST}:{pim_id}:LOCAL')
    ]]

    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_notification_deletion(notification_id):
    callback_data = f'{PRODUCT_SEARCH_REQUEST_DELETE}:{notification_id}'
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
