from telegram import Update
from telegram.ext import CallbackContext
import utils.fundgrube_client as fundgrube
from tgbot.handlers.fundgrube import static_text
from tgbot.handlers.fundgrube.keyboards import make_keyboard_for_product_select_command
from tgbot.handlers.fundgrube.manage_data import PRODUCT_SELECT_SEARCH_BUTTON

import re


def command_search(update: Update, context: CallbackContext) -> None:
    
    mm = fundgrube.Provider('MM')
    query = fundgrube.Query({"text": " ".join(context.args)})
    search = fundgrube.FundgrubeSearch(mm, query)

    cheapest_products = search.cheapest(3)

    if len(cheapest_products) > 0:
        for product in cheapest_products:
            text = static_text.result.format(name=product.name, price=product.price, url=product.fundgrube_url())
            update.message.reply_text(text=text, parse_mode="HTML")
    else:
        text = static_text.none_found
        update.message.reply_text(text=text)

def command_product_select(update: Update, context: CallbackContext) -> None:
    mm = fundgrube.Provider('MM')
    query = fundgrube.Query({"text": " ".join(context.args)})
    search = fundgrube.FundgrubeSearch(mm, query)

    products = search.unique_pim_ids_with_name()

    if len(products) > 0:
        for id, name in products.items():
            text = static_text.product.format(name=name)
            update.message.reply_text(text=text,
                                      reply_markup=make_keyboard_for_product_select_command(id),
                                      parse_mode="HTML")
    else:
        text = static_text.none_found
        update.message.reply_text(text=text)

def command_search_offers_for_product_id(update: Update, context: CallbackContext) -> None:
    mm = fundgrube.Provider('MM')
    
    callback_data = update.callback_query["data"]
    exp = re.compile(f"{PRODUCT_SELECT_SEARCH_BUTTON}:(.*)")
    pim_id = re.findall(exp, callback_data)[0]

    query = fundgrube.Query({"text": pim_id})
    search = fundgrube.FundgrubeSearch(mm, query)

    cheapest_products = search.cheapest(3)

    if len(cheapest_products) > 0:
        for product in cheapest_products:
            text = static_text.result.format(name=product.name, price=product.price, url=product.fundgrube_url())
            update.effective_message.reply_text(text=text, parse_mode="HTML")
    else:
        text = static_text.none_found
        update.effective_message.reply_text(text=text)
