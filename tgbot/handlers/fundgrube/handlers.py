from telegram import Update
from telegram.ext import CallbackContext
import utils.fundgrube_client as fundgrube
from tgbot.handlers.fundgrube import static_text
from tgbot.handlers.fundgrube.keyboards import make_keyboard_for_product_select_command
from tgbot.handlers.fundgrube.keyboards import make_keyboard_for_register_search_command
from tgbot.handlers.fundgrube.manage_data import PRODUCT_SEARCH, PRODUCT_SEARCH_REQUEST
import json

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
    provider = fundgrube.Provider('MM')
    
    callback_data = update.callback_query["data"]
    exp = re.compile(f"{PRODUCT_SEARCH}:(.*)")
    pim_id = re.findall(exp, callback_data)[0]

    query_params = {"text": pim_id}
    query = fundgrube.Query(query_params)
    search = fundgrube.FundgrubeSearch(provider, query)

    cheapest_products = search.cheapest(3)

    cheapest_price = cheapest_products[0].price

    if len(cheapest_products) > 0:
        product_name = cheapest_products[0].name
        header = static_text.result_header.format(product_name=product_name)
        update.effective_message.reply_text(text=header)
        for product in cheapest_products:
            text = static_text.result.format(name=product.name, price=product.price, url=product.fundgrube_url())
            update.effective_message.reply_text(text=text, parse_mode="HTML")
        update.effective_message.reply_text(text=static_text.register_search,
                                            reply_markup=make_keyboard_for_register_search_command(provider.identifier, product.pim_id, cheapest_price),
                                            parse_mode="HTML")
    else:
        text = static_text.none_found
        update.effective_message.reply_text(text=text)

def command_register_search(update: Update, context: CallbackContext) -> None:
    callback_data = update.callback_query["data"]
    exp = re.compile(f"{PRODUCT_SEARCH_REQUEST}:(.*):(.*):(.*)")
    provider, pim_id, price = re.findall(exp, callback_data)[0]
    print(provider)
    print(pim_id)
    print(price)
