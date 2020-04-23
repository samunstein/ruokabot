from statics import TYPE_COOLDOWN, PROTEIN_COOLDOWN, EXTRA_PER_WEEK, FOOD_PER_WEEK, FOOD_COOLDOWN, FOOD_STORAGE
from generointi.vuodenaika import Vuodenaika
from generointi.reader import read
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


def lue_aikaisemmat(offset, ruoat):
    alku = date.today() + timedelta(weeks=offset)
    viikkoja = max(PROTEIN_COOLDOWN, TYPE_COOLDOWN, FOOD_COOLDOWN)
    aikaisemmat_ruoat = []
    for vko in range(viikkoja):
        tama = alku - timedelta(weeks=viikkoja - vko)
        tiedosto = "{}/{}_{}".format(FOOD_STORAGE, tama.year, tama.isocalendar()[1])
        try:
            with open(tiedosto, encoding="UTF-8") as f:
                nimet = [a.strip() for a in f.readlines()]
        except FileNotFoundError:
            nimet = []

        vko_ruoat = []
        for nimi in nimet:
            if nimi in ruoat:
                vko_ruoat.append(ruoat[nimi])
        aikaisemmat_ruoat.append([tama, vko_ruoat])
    return aikaisemmat_ruoat


def generate(offset):
    tanaan = date.today()
    ruoat = read()

    viikot = lue_aikaisemmat(offset, ruoat)

    for i in range(100):
        delta = timedelta(weeks=i + offset)
        vko = tanaan + delta
        kuukausi = vko.month

        proteiini_i = max(0, len(viikot) - PROTEIN_COOLDOWN)
        tyyppi_i = max(0, len(viikot) - TYPE_COOLDOWN)
        ruoka_i = max(0, len(viikot) - FOOD_COOLDOWN)

        ei_proteiineja = ruoka_ominaisuudet(viikot[proteiini_i:], lambda r: r.proteiini)
        ei_tyyppeja = ruoka_ominaisuudet(viikot[tyyppi_i:], lambda r: r.tyyppi)
        ei_ruokaa = ruoka_ominaisuudet(viikot[ruoka_i:], lambda r: r.nimi)

        tarjolla = list(filter(ruoka_filter(ei_proteiineja, ei_tyyppeja, ei_ruokaa, kuukausi), ruoat.values()))

        vko_ruoat = viikon_ruoat(tarjolla)
        viikot.append([vko, vko_ruoat])

    kirjoita(offset, viikot)
    return ruoat


if __name__ == "__main__":
    generate(0)
