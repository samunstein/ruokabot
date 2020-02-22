from statics import FOOD_STORAGE


def kirjoita(viikot, kansio=FOOD_STORAGE):
    for viikko in viikot:
        pvm, ruoat = viikko
        with open("{}/{}_{}".format(kansio, pvm.year, pvm.isocalendar()[1]), "w", encoding="UTF-8") as f:
            for ruoka in ruoat:
                f.write("{}\t{}\n".format(ruoka.nimi, ruoka.ainekset))
