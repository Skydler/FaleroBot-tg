# -*- coding: utf-8 -*-
import requests
import json
import time
import random
import itertools
from threading import Thread

from server import init


class Bot(object):
    def __init__(self, token):
        self.api_url = "https://api.telegram.org/bot" + token + "/"
        self.last_message = None
        self.msgs = init()
        self.get_updates()

    def make_request(self, command, args={}):
        response = requests.get("{}{}".format(self.api_url, command), args)
        if response.status_code == 200:
            return response
        else:
            raise Exception(response.content)

    def send_message(self, text, chat):
        values = {"text": text, "chat_id": chat}
        self.make_request("sendMessage", values)

    def get_updates(self):
        while True:
            try:
                msg = self.msgs.get()
                text = msg["message"]["text"]
                chat = msg["message"]["chat"]["id"]
                first_name = msg["message"]["from"]["first_name"]
                self.reacts(text, chat, first_name)
            except Exception:
                pass

    def reacts(self, text, chat, first_name):
        self.faler_calls(text, chat, first_name)
        if "faler no entiendo" in text.lower():
            self.justify(text, chat)
        elif "faler on" == text.lower():
            self.faler_dota_on = True
            self.invitacion = Thread(target=self.invitation, args=(chat,))
            self.invitacion.start()
        elif "faler off" == text.lower():
            self.faler_dota_on = False

    # --------------- RESPUESTAS DE FALER -------------------------------------

    def faler_calls(self, text, chat, first_name):
        if "xd" in text.lower():
            self.send_message("xdxdxdxd", chat)

        elif text.lower() == "falero vt":
            self.send_message("Adiós mundo cruel", chat)

        elif "ste faler" == text.lower():
            self.send_message("Ste " + first_name, chat)

        elif ":v" in text.lower():
            self.send_message("Ste men", chat)

        elif text.lower() == ("dota?") or text.lower() == ("dota ?"):
            self.send_message("Si son más de tres no entro porq se hace dificil", chat)

        elif text.lower() == "inteligente":
            self.send_message("Akzo eres 100tifiko?", chat)

        elif (text.lower() == ("nadie habla")) or (text.lower() == ("que silencio")):
            self.send_message("El grupo muere lentamente....", chat)

        elif ("rubia" in text.lower()) or (
            "amor" in text.lower() and "faler" in text.lower()
        ):
            self.send_message("No me interesa más la rubia", chat)

        elif "flaco sch" in text.lower():
            quotes = [
                "Que grande que es el flaco",
                "Ídolo!!",
                "Genio!!",
                "Crack!!",
                "Master!",
                "Capo!",
            ]
            self.send_message(random.choice(quotes), chat)

        elif "cara de" in text.lower():
            quotes = [
                "Pepino de mar",
                "poste de luz",
                "langosta",
                "pulpo",
                "nebulosa cosmica",
                "boludo",
                "zapato sucio",
                "sapo",
                "tortilla",
                "pescado frito",
                "zoquete sucio",
                "perejil",
                "trapo sucio",
                "zapallo podrido",
                "culo",
                "negro resentido",
                "piojo resucitado",
                "gil atómico",
            ]
            self.send_message(random.choice(quotes), chat)

        elif "me insulto" in text.lower():
            self.send_message("si, te insulté y que vas a hacer al respecto? >:v", chat)
        elif "oe si" in text.lower():
            self.send_message(">:>", chat)

        elif "oe no" in text.lower():
            self.send_message(":<", chat)

        elif ("<.<" in text.lower()) or (">.>" in text.lower()):
            if first_name == "Ariel":
                self.send_message("Callate nacho", chat)

        elif "no" in text.lower() and "dota" in text.lower() and "jue" in text.lower():
            quotes = [
                "Yi ni jigui diti",
                "Tingui qui istidiar",
                "Ni jigui pirqui si pinin i hiblir di itris cisis",
            ]
            self.send_message(random.choice(quotes), chat)
        elif "callate nacho" in text.lower():
            self.send_message("Bien dicho", chat)

        elif "/hola@falero_bot" in text.lower() or "/hola" in text.lower():
            if first_name == "Andrés":
                self.send_message("Oh, buenas", chat)
            else:
                self.send_message("silencio... van a invocar a pastor", chat)

    # ----------------------------- FUNCIONES DE FALER ----------------------------

    def justify(self, texto, chat, largo=15):  # LA BELLA
        lista_de_palabras = texto.split(" ")
        linea = ""
        for palabra in lista_de_palabras:
            if len(linea + palabra + " ") <= largo:
                linea += palabra + " "
            elif len(linea + palabra) <= largo:
                linea += palabra
                self.send_message(linea, chat)
                linea = ""
            else:
                linea = linea[:-1]
                espacios = largo - len(linea)
                try:
                    times, remainder = divmod(espacios, len(linea.split()) - 1)
                except Exception:
                    pass
                linea = linea.replace(" ", " " + " " * (times))
                linea = linea.replace(" ", "  ", remainder)
                self.send_message(linea, chat)
                linea = palabra + " "

    def invitation(self, chat):
        while self.faler_dota_on:
            print(self.faler_dota_on)
            self.send_message("Vienen a la dota?", chat)
            time.sleep(1)


if __name__ == "__main__":
    bot = Bot("467923481:AAFSNxWjgofFkWCxKRMoAGH2SS4Gj6PET0I")


"""
git add .
git commit -m "Algo descriptivo aca"
git push heroku master


heroku logs --tail"""
