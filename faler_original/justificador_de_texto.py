import itertools


def justificar(texto, largo):  # LA BELLA
    lista_de_palabras = texto.split(" ")
    linea = ""
    for palabra in lista_de_palabras:
        if len(linea + palabra + " ") <= largo:
            linea += palabra + " "
        elif len(linea + palabra) <= largo:
            linea += palabra
            print(linea)
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
            print(linea)
            linea = palabra + " "


def run_test():
    """
    Correr tests para la funcion justificar
    """

    textos = [
        "You think water moves fast? You should see ice. It moves like it has a mind. Like it knows it killed the world once and got a taste for murder. After the avalanche, it took us a week to climb out. Now, I don't know exactly when we turned on each other, but I know that seven of us survived the slide... and only five made it out. Now we took an oath, that I'm breaking now. We said we'd say it was the snow that killed the other two, but it wasn't. Nature is lethal but it doesn't hold a candle to man.",
        "Do you see any Teletubbies in here? Do you see a slender plastic tag clipped to my shirt with my name printed on it? Do you see a little Asian child with a blank expression on his face sitting outside on a mechanical helicopter that shakes when you put quarters in it? No? Well, that's what you see at a toy store. And you must think you're in a toy store, because you're here shopping for an infant named Jeb.",
        "Look, just because I don't be givin' no man a foot massage don't make it right for Marsellus to throw Antwone into a glass motherfuckin' house, fuckin' up the way the nigger talks. Motherfucker do that shit to me, he better paralyze my ass, 'cause I'll kill the motherfucker, know what I'm sayin'?",
        "Now that we know who you are, I know who I am. I'm not a mistake! It all makes sense! In a comic, you know how you can tell who the arch-villain's going to be? He's the exact opposite of the hero. And most times they're friends, like you and me! I should've known way back when... You know why, David? Because of the kids. They called me Mr Glass.",
        "The path of the righteous man is beset on all sides by the iniquities of the selfish and the tyranny of evil men. Blessed is he who, in the name of charity and good will, shepherds the weak through the valley of darkness, for he is truly his brother's keeper and the finder of lost children. And I will strike down upon thee with great vengeance and furious anger those who would attempt to poison and destroy My brothers. And you will know My name is the Lord when I lay My vengeance upon thee.",
    ]
    largos = [12, 15, 20, 30, 50]

    for elemento in itertools.product(textos, largos):
        print("\n\n Largo {} \n\n".format(elemento[1]))

        justificar(elemento[0], elemento[1])

        print("\n\n -------------------------- \n\n")


if __name__ == "__main__":
    run_test()
# ------------------------------------------------------------------------

