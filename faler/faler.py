# -*- coding: utf-8 -*-
import os
import re
import logging
import argparse
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class MessageManager:
    def __init__(self, updater):
        dispatcher = updater.dispatcher

        dispatcher.add_handler(
            MessageHandler(self._re_ignorecase(r"xd"), self.xd_reply)
        )
        dispatcher.add_handler(
            MessageHandler(self._re_ignorecase(r"ste faler"), self.ste_faler_reply)
        )
        dispatcher.add_handler(
            MessageHandler(self._re_ignorecase(r":v"), self.pacman_reply)
        )
        dispatcher.add_handler(
            MessageHandler(
                self._re_ignorecase(r"nadie habla")
                | self._re_ignorecase(r"que silencio"),
                self.nadie_habla_reply,
            )
        )
        dispatcher.add_handler(
            MessageHandler(self._re_ignorecase(r"oe si"), self.oe_si_reply)
        )
        dispatcher.add_handler(
            MessageHandler(self._re_ignorecase(r"oe no"), self.oe_no_reply)
        )
        dispatcher.add_handler(
            MessageHandler(
                self._re_ignorecase(r"<.<") | self._re_ignorecase(r">.>"),
                self.nacho_reply,
            )
        )
        dispatcher.add_handler(
            MessageHandler(
                self._re_ignorecase(r"callate nacho"), self.callate_nacho_reply
            )
        )

    def _re_ignorecase(self, word):
        return Filters.regex(re.compile(word, re.IGNORECASE))

    def xd_reply(self, bot, update):
        bot.send_message(update.message.chat_id, "xdxdxdxd")

    def ste_faler_reply(self, bot, update):
        text = "Ste {}".format(update.message.from_user.first_name)
        bot.send_message(update.message.chat_id, text)

    def pacman_reply(self, bot, update):
        update.message.reply_text("Ste men")

    def nadie_habla_reply(self, bot, update):
        text = "El grupo muere lentamente...."
        bot.send_message(update.message.chat_id, text)

    def oe_si_reply(self, bot, update):
        text = ">:>"
        bot.send_message(update.message.chat_id, text)

    def oe_no_reply(self, bot, update):
        text = ":<"
        bot.send_message(update.message.chat_id, text)

    def nacho_reply(self, bot, update):
        if update.message.from_user.first_name == "Ariel":
            bot.send_message(update.message.chat_id, "Callate nacho")
        else:
            bot.send_message(
                update.message.chat_id, "Callate nacho, uh perdón la costumbre"
            )

    def callate_nacho_reply(self, bot, update):
        bot.send_message(update.message.chat_id, "Bien dicho")


class CommandManager:
    def __init__(self, updater):
        self.job_queue = updater.job_queue
        self.dota_spam_job = None

        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("dota_on", self.faler_dota_on))
        dispatcher.add_handler(CommandHandler("dota_off", self.faler_dota_off))

    def start(self, bot, update):
        if update.message.from_user.first_name == "Andrés":
            bot.send_message(update.message.chat_id, "Buenas, sale dota?")
        else:
            bot.send_message(
                update.message.chat_id, "Silencio... van a invocar a pastor"
            )

    def spam_msg(self, bot, job):
        bot.send_message(chat_id=job.context, text="Vienen a la dota?")

    def faler_dota_on(self, bot, update):
        self.dota_spam_job = self.job_queue.run_repeating(
            self.spam_msg, interval=2, first=0, context=update.message.chat_id
        )

    def faler_dota_off(self, bot, update):
        self.dota_spam_job.schedule_removal()


class Bot:
    def __init__(self, token, name):
        self.updater = Updater(token)
        self.token = token
        self.name = name
        CommandManager(self.updater)
        MessageManager(self.updater)

        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )

    def start_polling(self):
        self.updater.start_polling()

    def start_webhook(self):
        PORT = os.environ.get("PORT")
        self.updater.start_webhook(
            listen="0.0.0.0", port=int(PORT), url_path=self.token
        )
        self.updater.bot.setWebhook(
            "https://{}.herokuapp.com/{}".format(self.name, self.token)
        )
        self.updater.idle()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-o",
        "--offline",
        help="Excecute the bot in offline mode for testing purposes",
        action="store_true",
    )
    args = argparser.parse_args()
    if args.offline:
        print("Running offline...")
        bot = Bot("467923481:AAFSNxWjgofFkWCxKRMoAGH2SS4Gj6PET0I", "faler")
        bot.start_polling()
    else:
        bot = Bot(os.getenv("bot_key"), "faler")
        bot.start_webhook()
