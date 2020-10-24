from generointi.vuodenaika import Vuodenaika

class Ruoka:
    def __init__(self, rivi):
        if len(rivi) == 6:
            nimi, tyyppi, proteiini, sesongit, annokset, ainekset = rivi
            linkki = None
        elif len(rivi) == 7:
            nimi, tyyppi, proteiini, sesongit, annokset, ainekset, linkki = rivi
        else:
            raise ValueError("Rivissä {} on jotain vikaa".format(rivi))

        self.nimi = nimi
        self.tyyppi = tyyppi
        self.proteiini = proteiini
        self.sesongit = \
            Vuodenaika.kaikki() if sesongit.strip() == "" else list(map(Vuodenaika.tekstista, sesongit.split(",")))
        self.ainekset = ainekset.strip()
        self.annokset = annokset
        self.linkki = linkki

    def sopiva_sesonkiin(self, vuodenaika: Vuodenaika):
        return vuodenaika in self.sesongit

    def __repr__(self):
        return "Ruoka({} : {} : {} : {} : {} : {} : {})".format(self.nimi, self.tyyppi, self.proteiini, self.sesongit, self.annokset, self.ainekset, self.linkki)

    @staticmethod
    def ei_loydy(nimi):
        return Ruoka([nimi, "", "", "", "En tiedä mikä tämä ruoka on. Onko tiedostoihin jäänyt vanha ruoka jota ei ole enää listalla?"])
