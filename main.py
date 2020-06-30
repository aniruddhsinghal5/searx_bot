#!/usr/bin/env python3

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram.error import BadRequest, TimedOut
import logging
import requests
import json
import time
from settings import TOKEN, INSTANCE_URL

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)
updater = None


def start(update, context):
    update.message.reply_text(
        """
    Available commands:

    /searx <num*> <phrase> -  search in Searx

    *num  -  number of results (max 10)"""
    )


def searx(update, context):
    try:
        if int(context.args[0]) > 10:
            results_number = 10
        else:
            results_number = int(context.args[0])
        del context.args[0]
    except ValueError:
        results_number = 1

    response = json.loads(
        requests.post(
            INSTANCE_URL,
            data={"q": json.dumps(context.args), "language": "en-US", "format": "json"},
        ).text
    )

    for i in range(results_number):
        if results_number > 5:
            time.sleep(1)

        try:
            result = response["results"][i]

            try:
                update.message.reply_text(
                    f"""
*{result['title']}*
[direct link]({result['pretty_url']})

{result['content']}

`from: {result['engines']}`""",
                    parse_mode=ParseMode.MARKDOWN,
                )
            except KeyError:
                pass
            except BadRequest:
                update.message.reply_text("Exception: BadRequest")
                print("Exception: BadRequest")
            except TimedOut:
                update.message.reply_text("Exception: TimedOut")
                print("Exception: TimedOut")

        except IndexError:
            update.message.reply_text("No results.")


def main():
    global updater
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("searx", searx))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
