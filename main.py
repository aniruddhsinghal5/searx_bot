#!/usr/bin/env python3

from telegram import ParseMode, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from telegram.error import BadRequest, TimedOut
import logging
import requests
import json
from random import randint
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


def request_(query):
    response = requests.post(
        INSTANCE_URL,
        data={"q": " ".join(query), "language": "en-US", "format": "json"},
    )
    query_link = response.url + "?" + response.request.body.replace("&format=json", "")

    return response, query_link


def result_message(title, pretty_url, query_link, content, engines):
    return f"""
*{title}*
[direct link]({pretty_url}) | [query link]({query_link})
\n{content}\n
`from: {", ".join(engines)}`"""


def searx(update, context):
    try:
        if int(context.args[0]) > 10:
            results_number = 10
        else:
            results_number = int(context.args[0])
        del context.args[0]
    except ValueError:
        results_number = 1

    response, query_link = request_(context.args)

    for i in range(results_number):
        try:
            result = json.loads(response.text)["results"][i]

            title, pretty_url, engines = (
                result["title"],
                result["pretty_url"],
                result["engines"],
            )
            try:
                content = result["content"]
            except KeyError:
                content = ""

            try:
                update.message.reply_text(
                    result_message(title, pretty_url, query_link, content, engines),
                    parse_mode=ParseMode.MARKDOWN,
                )
            except BadRequest:
                update.message.reply_text("Exception: BadRequest")
                print("Exception: BadRequest")
            except TimedOut:
                update.message.reply_text("Exception: TimedOut")
                print("Exception: TimedOut")

        except IndexError:
            update.message.reply_text("No results.")


def inline(update, context):
    answers = []
    query = list(str(update.inline_query.query).split(" "))
    if not query:
        return
    response, query_link = request_(query)
    for i in range(15):
        try:
            result = json.loads(response.text)["results"][i]
        except IndexError:
            continue

        title, pretty_url, engines = (
            result["title"],
            result["pretty_url"],
            result["engines"],
        )
        try:
            content = result["content"]
        except KeyError:
            content = ""

            answers.append(
                InlineQueryResultArticle(
                    id=randint(0, 10000),
                    title=title[:32] + (title[29:] and "..."),
                    description=content[:32] + (content[29:] and "..."),
                    input_message_content=InputTextMessageContent(
                        result_message(title, pretty_url, query_link, content, engines),
                        parse_mode=ParseMode.MARKDOWN,
                    ),
                )
            )
    try:
        context.bot.answer_inline_query(update.inline_query.id, answers)
    except BadRequest:
        answers.append(
            InlineQueryResultArticle(id="Bad request", title="Bad request")
        )
        print("Exception: BadRequest")


def main():
    global updater
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("searx", searx))
    dispatcher.add_handler(InlineQueryHandler(inline))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
