# -*- coding: utf-8 -*-
import os
import logging
import argparse
import requests as rq
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv

from models import WebSite
from db import Base, Session, engine


class CommandManager:
    def __init__(self, updater):
        self.jobs = updater.job_queue
        self.website_checker_job = None

        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("add_website", self.add_website))
        dispatcher.add_handler(CommandHandler("drop_websites", self.drop_websites))
        dispatcher.add_handler(CommandHandler("start_tracking", self.start_traking))
        dispatcher.add_handler(CommandHandler("stop_tracking", self.stop_tracking))

    def start(self, update, context):
        update.message.reply_text("Ping... 1 2 3")

    def add_website(self, update, context):
        if not context.args:
            update.message.reply_text(text="Send me an argument snowman")
        website_url = context.args[0]
        response = rq.get(website_url, verify=False)
        if response.ok:
            site = WebSite(url=website_url, content=response.text)
            with Session() as session:
                session.add(site)
                session.commit()

            update.message.reply_text(text="Added website to tracking list")
        else:
            update.message.reply_text(text="Status code for website is not OK")

    def drop_websites(self, update, context):
        with Session() as session:
            session.query(WebSite).delete()
        update.message.reply_text(text="Droped website table :S")

    def check_changes(self, context):
        chat_id = context.job.context
        with Session() as session:
            websites = session.query(WebSite).all()
            for site in websites:
                response = rq.get(site.url, verify=False)
                if response.ok:
                    if site.is_same_content(response.text):
                        context.bot.send_message(
                            chat_id=chat_id,
                            text=f"[+] No changes on {site.url}",
                        )
                    else:
                        site.update_content(response.text)
                        session.add(site)
                        session.commit()
                        context.bot.send_message(
                            chat_id=chat_id,
                            text=f"[!] Found changes on {site.url}",
                        )
                else:
                    context.bot.send_message(
                        chat_id=chat_id,
                        text=f"[X] Status code for {site.url} is not OK",
                    )

    def start_traking(self, update, context):
        self.website_checker_job = self.jobs.run_repeating(
            self.check_changes, interval=60, first=1, context=update.message.chat_id
        )
        update.message.reply_text(text="Started job")

    def stop_tracking(self, update, context):
        self.website_checker_job.schedule_removal()
        update.message.reply_text(text="Removed job")


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

    Base.metadata.create_all(engine)

    bot = Faler(os.getenv("BOT_KEY"))
    if args.local:
        logging.info("Running bot in LOCAL mode")
        bot.start_polling()
    else:
        bot.start_webhook()
