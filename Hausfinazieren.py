"""
Dieses Skript berechnet die Zahlen für eine Immobilieninvestition in Deutschland.
Es brechnet die Nebenkosten, die monatliche Rate, die Dauer des Kredits, und den Cashflow jedes Jahres.
Allgemeine Annahmen sowie Grunderwebsteuer, Maklerprovision, Notarkosten sind für Hessen. Einkommensteuer ist der Spitzensteuersatz in Deutschland.
Alle Daten spezielle zur Immobile in Frage sind in der main Funktion einzutragen.
"""
__author__ = "Yuanyuan Mao"
__version__ = "1.0"

STEUER = 0.06 # Grunderwerbsteuer in Hessen
MARKLER = 0.0357 # Normaler Maklerprovision in Hessen
NOTAR = 0.015 # Durchschnittliche Notarkosten in Hessen
EINKOMMENSTEUER = 0.42 # Spitzensteuersatz in Deutschland

def nebenkosten(kaufpreis):
    return kaufpreis * (STEUER + MARKLER + NOTAR)

def gesamtkosten(kaufpreis):
    return kaufpreis + nebenkosten(kaufpreis)

def monatliche_rate(kredit, zins, tilgung):
    return kredit * (zins + tilgung) / 12

def abschreibung(kaufpreis, baujahr):
    # info von der Webseite des Finanzamts NRW 
    if 1924 < baujahr < 2023:
        return kaufpreis / 100 * 2
    if baujahr < 1925:
        return kaufpreis / 100 * 2.5
    if baujahr > 2022:
        return kaufpreis / 100 * 3
    
def cashflow(kredit, miete, monatliche_rate, zins, abschreibung):
    jahr = 1
    monatlicher_zins = (1 + zins)**(1/12) - 1 
    monatliche_abschreibung = abschreibung / 12
    while True: # Endlosschleife, bis Kredit abbezahlt ist
        # Initialisierung für jedes Jahr
        netto_miete = 0
        steuerersparnis = 0
        zinsen_bezahlt = 0
        tilgung_bezahlt = 0
        # Der Kredit wird jeden Monat abbezahlt, dabei werden Zinsen und Tilgung berechnet
        for monate in range(1, 13):
            zinsen = kredit * monatlicher_zins # Zinsen für den Monat
            zinsen_bezahlt += zinsen
            tilgung = monatliche_rate - zinsen # Tilgung für den Monat
            tilgung_bezahlt += tilgung
            kredit = kredit - tilgung          # Restkredit
            if kredit <= 0: # Wenn Kredit abbezahlt ist, beenden die Schleife und geben die Dauer aus
                print(f"Kredit abbezahlt, insgesamt dauert: {jahr-1} Jahre {monate} Monate")
                return
            netto_miete += miete * (1 - STEUER)
            steuerersparnis += (monatliche_abschreibung + zinsen) * EINKOMMENSTEUER
        cashflow = netto_miete - monatliche_rate * 12 + steuerersparnis
        print(f"Ende Jahr: {jahr} kredit: {kredit}, Cashflow: {cashflow}, davon Zinsen: {zinsen_bezahlt}, Tilgung: {tilgung_bezahlt}, Steuerersparnis: {steuerersparnis}")
        jahr += 1

def main():
    kaufpreis = 830000
    eigenkapital = 100000
    zins = 0.0327
    tilgung = 0.03
    kaltmiete = 3000
    baujar = 1900
    haus = True # True für Haus, False für Wohnung
    hausgeld = 0 # Nur für Wohnung
    if haus:
        kaltmiete = kaltmiete
    else:
        kaltmiete = kaltmiete - hausgeld
    kredit = gesamtkosten(kaufpreis) - eigenkapital

    print("Der Kreditbetrag beträgt: ", kredit)
    print("Die monatliche Rate beträgt: ", monatliche_rate(kredit, zins, tilgung))
    print("Die monatliche Miete beträgt: ", kaltmiete)
    print("Die jährige Abschreibung beträgt: ", abschreibung(kaufpreis, baujar))
    print("------------------------------------------------")
    cashflow(kredit, kaltmiete, monatliche_rate(kredit, zins, tilgung), zins, abschreibung(kaufpreis, baujar))

if __name__ == "__main__":
    main()