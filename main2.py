import sys
import heapq

class Bank:
    def __init__(self, id, muenzen, registrierungsprozess, muenzenprotag, muenzentypen):
        self.id = id
        self.muenzen = muenzen
        self.registrierungsprozess = registrierungsprozess
        self.muenzenprotag = muenzenprotag
        self.muenzentypen = tuple(muenzentypen)  # Verwenden Sie ein Tupel für Effizienz
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

unregistrierte_banken = set(banken)  # Verwenden Sie ein Set für Effizienz
registrierte_banken = []
gescannte_muenzen = set()  # Verwenden Sie ein Set für Effizienz

def beste_bank(aktuelle_banken, tage_uebrig, gesammelte_muenzen):
    for bank in aktuelle_banken:
        gesammelte_muenzen |= set(bank.muenzentypen)  # Update des Sets mit neuen Münzen
        if not bank.muenzen_sortiert:
            bank.muenzen_sortiert = heapq.nlargest(min(tage_uebrig * bank.muenzenprotag, len(bank.muenzentypen)),
                                                  key=lambda muenze: wertigkeiten[muenze],
                                                  iterable=bank.muenzentypen)
        bank.bank_wert = sum(wertigkeiten[muenze] for muenze in bank.muenzen_sortiert) / bank.registrierungsprozess

    beste_bank = max(aktuelle_banken, key=lambda x: x.bank_wert, default=None)
    return beste_bank

zeit_registrierung = 0
for tag in range(tage):
    if zeit_registrierung == 0:
        if not unregistrierte_banken:
            break
        bank_registrieren = beste_bank(unregistrierte_banken, tage - tag, gescannte_muenzen)
        unregistrierte_banken.remove(bank_registrieren)
        registrierte_banken.append(bank_registrieren)
        zeit_registrierung = bank_registrieren.registrierungsprozess
    zeit_registrierung -= 1
    print("Tag: ", tag, "/", tage)

ausgabe_text = f"{len(registrierte_banken)}\n"
for bank in registrierte_banken:
    ausgabe_text += f"{bank.id} {len(bank.muenzen_sortiert)}\n"
    ausgabe_text += " ".join(str(muenze) for muenze in bank.muenzen_sortiert) + "\n"

with open(f"out/{sys.argv[1]}", "w") as f:
    f.truncate(0)
    f.write(ausgabe_text)
