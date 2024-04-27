import sys

class Bank:
    def __init__(self, id, muenzen, registrierungsprozess, muenzenprotag, muenzentypen):
        self.id = id
        self.muenzen = muenzen
        self.registrierungsprozess = registrierungsprozess
        self.muenzenprotag = muenzenprotag
        self.muenzentypen = muenzentypen
        self.muenzen_sortiert = []
        self.bank_wert = 0


muenzenanzahl = 0
anzahl_banken = 0
tage = 0

wertigkeiten = []
banken = []

with open(f"in/{sys.argv[1]}", "r") as f:
    muenzenanzahl, anzahl_banken, tage = [int(i) for i in f.readline().split()]
    wertigkeiten = [int(i) for i in f.readline().split()]

    for i in range(anzahl_banken):
        banken.append(Bank(i,
                           *[int(i) for i in f.readline().split()],
                           [int(i) for i in f.readline().split()]
                           ))

print("Münzen: ", muenzenanzahl)
print("Banken: ", banken[1].muenzentypen)
print("Tage: ", tage)
print("Wertigkeiten: ", wertigkeiten)

####

unregistrierte_banken = [b for b in banken]
registriert_banken = []
gescannte_muenzen = []


def beste_bank(aktuelle_banken, tage_uebrig):
    for bank in aktuelle_banken:
        for muenze in bank.muenzentypen:
            if muenze not in gescannte_muenzen:
                bank.muenzen_sortiert.append(muenze)
        muenz_werte = []
        for muenze in bank.muenzen_sortiert:
            muenz_werte.append(wertigkeiten[muenze])
        bank.muenzen_sortiert = sorted(bank.muenzen_sortiert, key=lambda x: wertigkeiten[x], reverse=True)

        zeit_zum_scannen = tage_uebrig - bank.registrierungsprozess
        anz_muenzen_scanbar = zeit_zum_scannen * bank.muenzenprotag
        bank.muenzen_sortiert = bank.muenzen_sortiert[0: min(len(bank.muenzen_sortiert) - 1, anz_muenzen_scanbar)]
        bank.bank_wert = sum([wertigkeiten[muenze] for muenze in bank.muenzen_sortiert]) / bank.registrierungsprozess

    aktuelle_banken = sorted(aktuelle_banken, key=lambda x: x.bank_wert, reverse=True)

    return aktuelle_banken[0]


zeit_registrierung = 0
for tag in range(tage):
    if zeit_registrierung == 0:
        if len(unregistrierte_banken) == 0:
            break
        bank_registrieren = beste_bank(unregistrierte_banken, tage - tag)
        unregistrierte_banken.remove(bank_registrieren)
        registriert_banken.append(bank_registrieren)
        zeit_registrierung = bank_registrieren.registrierungsprozess
    zeit_registrierung -= 1
    print("Tag: ", tag, "/", tage)

ausgabe_text = str(len(registriert_banken)) + "\n"
for bank in registriert_banken:
    ausgabe_text += str(bank.id) + " " + str(len(bank.muenzen_sortiert)) + "\n"
    for muenze in bank.muenzen_sortiert:
        ausgabe_text += str(muenze) + " "
    ausgabe_text += "\n"

with open(f"out/{sys.argv[1]}", "w") as f:
    f.truncate(0)
    f.write(ausgabe_text)