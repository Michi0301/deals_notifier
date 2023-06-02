from telegram import Update
from telegram.ext import CallbackContext
import deal_search.modules.deals_client.client as client
from tgbot.handlers.deal_search import static_text
from tgbot.handlers.deal_search.keyboards import make_keyboard_for_product_search_command, make_keyboard_for_create_search_request_command, make_keyboard_for_search_request_deletion, make_keyboard_for_branch_selection, make_keyboard_for_branch_delete
from tgbot.handlers.deal_search.manage_data import PRODUCT_SEARCH, PRODUCT_SEARCH_REQUEST, ADD_BRANCH, DELETE_BRANCH

import re

from users.models import User, Location
from deal_search.models import Branch, SearchRequest

PROVIDER = 'MM'

# Search products
def command_product_select(update: Update, context: CallbackContext) -> None:
    mm = client.Provider(PROVIDER)
    query = client.DealsQuery({"text": " ".join(context.args)})
    search = client.DealSearch(mm, query)

    products = search.unique_pim_ids_with_name()

    if len(products) > 0:
        for id, name in products.items():
            text = static_text.product.format(name=name)
            update.message.reply_text(text=text,
                                      reply_markup=make_keyboard_for_product_search_command(id),
                                      parse_mode="HTML")
    else:
        text = static_text.none_found
        update.message.reply_text(text=text)

# Search offers for a given product, offer keyboard to create search request
def command_search_offers_for_product_id(update: Update, context: CallbackContext) -> None:
    provider = client.Provider(PROVIDER)
    
    pim_id, search_type = extract_callback_data(update, f"{PRODUCT_SEARCH}:(.*):(.*)")

    query_params = {"text": pim_id}
    if search_type == "LOCAL":
        user = User.get_user(update, context)
        query_params["outletIds"] = ','.join(map(lambda x: str(x), user.branch_set.values_list('branch_id', flat=True)))        

    query = client.DealsQuery(query_params)
    search = client.DealSearch(provider, query)

    cheapest_products = search.cheapest(5)

    if len(cheapest_products) > 0:
        product_name = cheapest_products[0].name
        header = static_text.result_header.format(product_name=product_name)
        update.effective_message.reply_text(text=header)
        for product in cheapest_products:
            text = static_text.result.format(name=product.name, price=product.price, branch_name=product.outlet_name, url=product.fundgrube_url())
            update.effective_message.reply_text(text=text, parse_mode="HTML")
    else:
        update.effective_message.reply_text(text=static_text.none_found, parse_mode="HTML")
    
    if search_type == 'LOCAL':
        update.effective_message.reply_text(text=static_text.ask_for_notification_local,
                                            reply_markup=make_keyboard_for_create_search_request_command(pim_id),
                                            parse_mode="HTML")

# Create search request from keyboard callback
def command_create_search_request(update: Update, context: CallbackContext) -> None:
    pim_id, search_type = extract_callback_data(update, f"{PRODUCT_SEARCH_REQUEST}:(.*):(.*)")

    user = User.get_user(update, context)
    
    provider_instance = client.Provider(PROVIDER) 
    name = client.DealSearch.fetch_product_name(provider_instance, pim_id)

    if not user.branch_set.exists():
        update.effective_message.reply_text(text=static_text.no_branches)
        return      

    SearchRequest.objects.get_or_create(user=user, name=name, provider=PROVIDER, product_id=pim_id, search_type=search_type)
    update.effective_message.reply_text(text=static_text.notification_created)
    
## List persisted search requests
def command_list_search_requests(update: Update, context: CallbackContext):
    u = User.get_user(update, context)
    search_requests = SearchRequest.objects.filter(user=u)
    if search_requests.exists():
        for search_request in search_requests:
            text = static_text.search_request_local.format(name=search_request.name)
            update.effective_message.reply_text(text=text,
                                                reply_markup=make_keyboard_for_search_request_deletion(search_request.id),
                                                parse_mode="HTML")
    else:
        update.effective_message.reply_text(text=static_text.no_searches)

## Branches
def command_search_branches(update: Update, context: CallbackContext):
    u = User.get_user(update, context)
    location_str = " ".join(context.args)
    location_not_empty = bool(location_str.strip())
    last_location = Location.objects.filter(user=u).last()

    if location_not_empty:
        branches = fetch_branches_via_identifier(location_str)
    
    elif last_location:
        branches = fetch_branches_via_coordinates({"lat": last_location.latitude, "lng": last_location.longitude})
    
    else:
        branches = []

    if len(branches) > 0:
        for branch in branches:
            text = branch["displayName"]
            update.message.reply_text(text=text,
                                        reply_markup=make_keyboard_for_branch_selection(branch['id'], branch["displayNameShort"]),
                                        parse_mode="HTML")
    else:
        update.message.reply_text(text=static_text.no_location)

def fetch_branches_via_identifier(identifier):
    return client.BranchSearch(provider=client.Provider(PROVIDER), zip_or_city=identifier).fetch_branches()

def fetch_branches_via_coordinates(coordinates):
    return client.BranchSearch(provider=client.Provider(PROVIDER), coordinates=coordinates).fetch_branches()

def command_add_branch(update: Update, context: CallbackContext):
    user = User.get_user(update, context)

    branch_id, branch_name = extract_callback_data(update, f"{ADD_BRANCH}:(.*):(.*)")

    Branch.objects.get_or_create(user=user, provider=PROVIDER, branch_id=branch_id, name=branch_name)
    update.effective_message.edit_reply_markup(reply_markup=make_keyboard_for_branch_delete(branch_id))

def command_list_branches(update: Update, context: CallbackContext):
    user = User.get_user(update, context)

    branches = Branch.objects.filter(user=user)
    update.effective_message.reply_text(text=static_text.list_branches)
    if branches.exists():
        for branch in branches:
            text = static_text.branch.format(name=branch.name)
            update.effective_message.reply_text(text=text,
                                                reply_markup=make_keyboard_for_branch_delete(branch.id),
                                                parse_mode="HTML")
    else:
        update.effective_message.reply_text(text=static_text.no_branches)

def command_delete_branch(update: Update, context: CallbackContext):
    user = User.get_user(update, context)

    branch_id = extract_callback_data(update, f"{DELETE_BRANCH}:(.*)")


    branches = Branch.objects.filter(user=user, id=branch_id)
    foreign_branch_id = branches.last().branch_id
    branch_name = branches.last().name
    branches.delete()
    
    update.effective_message.edit_reply_markup(reply_markup=make_keyboard_for_branch_selection(foreign_branch_id, branch_name))

# Utils
def extract_callback_data(update, matcher):
    callback_data = update.callback_query["data"]
    exp = re.compile(matcher)
    
    return re.findall(exp, callback_data)[0]