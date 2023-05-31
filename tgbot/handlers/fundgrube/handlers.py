from telegram import Update
from telegram.ext import CallbackContext
import utils.fundgrube_client as fundgrube
from tgbot.handlers.fundgrube import static_text

def command_search(update: Update, context: CallbackContext) -> None:
    
    mm = fundgrube.Provider('MM')
    query = fundgrube.Query({"text": " ".join(context.args)})
    search = fundgrube.FundgrubeSearch(mm, query)

    cheapest_products = search.cheapest(5)

    if len(cheapest_products) > 0:
        for product in cheapest_products:
            text = static_text.result.format(name=product.name, price=product.price, url=product.fundgrube_url())
            update.message.reply_text(text=text, parse_mode="HTML")
    else:
        text = static_text.none_found
        update.message.reply_text(text=text)

