from generointi.vuodenaika import Vuodenaika

class Ruoka:
    def __init__(self, rivi):
        nimi, tyyppi, proteiini, sesongit, ainekset = rivi.split("\t")

        self.nimi = nimi
        self.tyyppi = tyyppi
        self.proteiini = proteiini
        self.sesongit = \
            Vuodenaika.kaikki() if sesongit.strip() == "" else list(map(Vuodenaika.tekstista, sesongit.split(",")))
        self.ainekset = ainekset.strip()

    def sopiva_sesonkiin(self, vuodenaika: Vuodenaika):
        return vuodenaika in self.sesongit