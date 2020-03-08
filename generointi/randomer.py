from statics import TYPE_COOLDOWN, PROTEIN_COOLDOWN, EXTRA_PER_WEEK, FOOD_PER_WEEK, FOOD_COOLDOWN
from generointi.vuodenaika import Vuodenaika
from generointi.reader import lue
from datetime import date, timedelta
from random import shuffle
from generointi.saver import kirjoita


def ruoka_ominaisuudet(viikot, ominaisuus):
    kaikki = []
    for vko in viikot:
        kaikki.extend(vko[1])
    return set(map(ominaisuus, kaikki))


def ruoka_filter(ei_proteiinit, ei_tyypit, ei_ruoka, kuukausi):
    return lambda ruoka: \
        ruoka.proteiini not in ei_proteiinit and \
        ruoka.tyyppi not in ei_tyypit and \
        ruoka.nimi not in ei_ruoka and \
        (ruoka.sopiva_sesonkiin(Vuodenaika.kuukaudesta(kuukausi)) if kuukausi is not None else True)


def viikon_ruoat(tarjolla):
    ruoat = []

    shuffle(tarjolla)
    ruoka = tarjolla[0]
    ruoat.append(ruoka)

    for j in range(EXTRA_PER_WEEK + FOOD_PER_WEEK - 1):
        tarjolla = list(filter(ruoka_filter([ruoka.proteiini], [ruoka.tyyppi], [], None), tarjolla))

        shuffle(tarjolla)
        ruoka = tarjolla[0]
        ruoat.append(ruoka)

    return ruoat


def main():
    tanaan = date.today()
    ruoat = lue()

    viikot = []

    for i in range(5):
        delta = timedelta(weeks=i)
        vko = tanaan + delta
        kuukausi = vko.month

        proteiini_i = max(0, len(viikot) - PROTEIN_COOLDOWN)
        tyyppi_i = max(0, len(viikot) - TYPE_COOLDOWN)
        ruoka_i = max(0, len(viikot) - FOOD_COOLDOWN)

        ei_proteiineja = ruoka_ominaisuudet(viikot[proteiini_i:], lambda r: r.proteiini)
        ei_tyyppeja = ruoka_ominaisuudet(viikot[tyyppi_i:], lambda r: r.tyyppi)
        ei_ruokaa = ruoka_ominaisuudet(viikot[ruoka_i:], lambda r: r.nimi)

        tarjolla = list(filter(ruoka_filter(ei_proteiineja, ei_tyyppeja, ei_ruokaa, kuukausi), ruoat))

        vko_ruoat = viikon_ruoat(tarjolla)
        viikot.append([vko, vko_ruoat])

    kirjoita(viikot)


if __name__ == "__main__":
    main()
