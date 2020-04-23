from statics import FOOD_STORAGE
from os import path, makedirs


def kirjoita(offset, viikot, kansio=FOOD_STORAGE):
    if not path.exists(kansio):
        makedirs(kansio)

    for viikko in viikot[offset:]:
        pvm, ruoat = viikko
        with open("{}/{}_{}".format(kansio, pvm.year, pvm.isocalendar()[1]), "w", encoding="UTF-8") as f:
            for ruoka in ruoat:
                f.write("{}\n".format(ruoka.nimi))
