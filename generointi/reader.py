from generointi.ruoka import Ruoka

def lue(tiedosto="sheet.csv"):
    headeri = "Nimi\tTyyppi\tProteiini\tSesonki\tAinekset"
    with open(tiedosto, encoding="UTF-8") as f:
        lines = filter(lambda rivi: rivi.strip() != "" and rivi.strip() != headeri, f.readlines())
        ruoat = list(map(Ruoka, lines))
    return ruoat

if __name__ == "__main__":
    print(lue())
