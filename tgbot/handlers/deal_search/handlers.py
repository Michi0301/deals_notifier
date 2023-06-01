from telegram import Update
from telegram.ext import CallbackContext
import deal_search.modules.deals_client.client as client
from tgbot.handlers.deal_search import static_text
from tgbot.handlers.deal_search.keyboards import make_keyboard_for_product_select_command, make_keyboard_for_register_search_command, make_keyboard_for_search_request_deletion
from tgbot.handlers.deal_search.manage_data import PRODUCT_SEARCH, PRODUCT_SEARCH_REQUEST

import re

from users.models import User
from deal_search.models import DealSearchRequest

def command_product_select(update: Update, context: CallbackContext) -> None:
    mm = client.Provider('MM')
    query = client.DealsQuery({"text": " ".join(context.args)})
    search = client.DealSearch(mm, query)

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
    provider = client.Provider('MM')
    
    callback_data = update.callback_query["data"]
    exp = re.compile(f"{PRODUCT_SEARCH}:(.*)")
    pim_id = re.findall(exp, callback_data)[0]

    query_params = {"text": pim_id}
    query = client.DealsQuery(query_params)
    search = client.DealSearch(provider, query)

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

    u = User.get_user(update, context)
    
    provider_instance = client.Provider(provider) 
    name = client.DealSearch.fetch_product_name(provider_instance, pim_id)

    DealSearchRequest.objects.create(user=u, name=name, provider=provider, product_id=pim_id, price=price)

    text = static_text.notification_created
    update.effective_message.reply_text(text=text)

def command_list_search_requests(update: Update, context: CallbackContext):
    u = User.get_user(update, context)
    search_requests = DealSearchRequest.objects.filter(user=u)
    if search_requests.exists():
        for search_request in search_requests:
            text = static_text.search_request.format(name=search_request.name, price=search_request.price)
            update.effective_message.reply_text(text=text,
                                                reply_markup=make_keyboard_for_search_request_deletion(search_request.id),
                                                parse_mode="HTML")
    else:
        update.effective_message.reply_text(text="You don't have any notifications setup.")
