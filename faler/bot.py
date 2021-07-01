# -*- coding: utf-8 -*-
import os
import logging
import argparse
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv


class CommandManager:
    def __init__(self, updater):
        self.jobs = updater.job_queue
        self.dota_spam_job = None

        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", self.start))
        # dispatcher.add_handler(CommandHandler("dota_on", self.faler_dota_on))
        # dispatcher.add_handler(CommandHandler("dota_off", self.faler_dota_off))

    def start(self, update, context):
        update.message.reply_text("Hola, que tal")

    # def spam_msg(self, context):
    #     context.bot.send_message(chat_id=context.job.context,
    #                              text="Vienen a la dota?")

    # def faler_dota_on(self, update, context):
    #     self.dota_spam_job = self.jobs.run_repeating(
    #         self.spam_msg, interval=2, context=update.message.chat_id
    #     )

    # def faler_dota_off(self, update, context):
    #     self.dota_spam_job.schedule_removal()


class Faler:
    def __init__(self, token):
        self.updater = Updater(token)
        self.token = token
        CommandManager(self.updater)

    def start_polling(self):
        self.updater.start_polling()
        self.updater.idle()

    def start_webhook(self):
        PORT = int(os.getenv("PORT", "8443"))
        self.updater.start_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=self.token,
            webhook_url=f"https://faler.herokuapp.com/{self.token}",
        )
        self.updater.idle()


if __name__ == "__main__":
    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-l",
        "--local",
        help="Excecute the bot in local mode for testing purposes",
        action="store_true",
    )
    args = argparser.parse_args()

    bot = Faler(os.getenv("BOT_KEY"))
    if args.local:
        logging.info("Running bot in LOCAL mode")
        bot.start_polling()
    else:
        bot.start_webhook()
