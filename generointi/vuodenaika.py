import enum

class Vuodenaika(enum.Enum):
    TALVI = 0
    KEVAT = 1
    KESA = 2
    SYKSY = 3

    @staticmethod
    def tekstit():
        return {
            "kevät": Vuodenaika.KEVAT,
            "kevat": Vuodenaika.KEVAT,
            "talvi": Vuodenaika.TALVI,
            "syksy": Vuodenaika.SYKSY,
            "kesä": Vuodenaika.KESA,
            "kesa": Vuodenaika.KESA
        }

    @staticmethod
    def kuukaudesta(kuukausi: int):
        return Vuodenaika((kuukausi % 12) // 3)

    @staticmethod
    def tekstista(teksti: str):
        return Vuodenaika.tekstit()[teksti.strip().lower()]

    @staticmethod
    def kaikki():
        return [Vuodenaika.TALVI, Vuodenaika.KESA, Vuodenaika.SYKSY, Vuodenaika.KEVAT]
