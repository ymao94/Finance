"""
Dieses Skript berechnet die Zahlen für eine Immobilieninvestition in Deutschland.
Es brechnet die Nebenkosten, die monatliche Rate, die Dauer des Kredits, und den Cashflow jedes Jahres.
Allgemeine Annahmen sowie Grunderwebsteuer, Maklerprovision, Notarkosten sind für Hessen. Einkommensteuer ist der Spitzensteuersatz in Deutschland.
Alle Daten spezielle zur Immobile in Frage sind in der main Funktion einzutragen.
"""
__author__ = "Yuanyuan Mao"
__version__ = "1.0"

STEUER = 0.065 # Grunderwerbsteuer in Hessen
MARKLER = 0.0357 # Normaler Maklerprovision in Hessen
NOTAR = 0.015 # Durchschnittliche Notarkosten in Hessen

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
    
def einkommensteuer(zu_versteuerndes_einkommen):
    if zu_versteuerndes_einkommen <= 12096:
        return 0.0    
    elif zu_versteuerndes_einkommen <= 17443:
        y = (zu_versteuerndes_einkommen - 12096) / 10000
        return (932.3 * y + 1400) * y
    elif zu_versteuerndes_einkommen <= 68480:
        y = (zu_versteuerndes_einkommen - 17443) / 10000
        return (176.64 * y + 2397) * y + 1015.13
    elif zu_versteuerndes_einkommen <= 277825:
        return 0.42 * zu_versteuerndes_einkommen - 10911.92
    else:
        return 0.45 * zu_versteuerndes_einkommen - 19246.67
    
def steuer2(zu_versteuerndes_einkommen):
    steuer = 0
    if zu_versteuerndes_einkommen <= 12096:
        return steuer
    if zu_versteuerndes_einkommen <= 17443-12906:
        y = (zu_versteuerndes_einkommen - 12096) / 10000
        return (932.3 * y + 1400) * y
    steuer += (17443 - 12096) / 10000 * (932.3 * (17443 - 12096) / 10000 + 1400)
    if zu_versteuerndes_einkommen <= 68480:
        y = (zu_versteuerndes_einkommen - 17443) / 10000
        return steuer + (176.64 * y + 2397) * y + 1015.13
    if zu_versteuerndes_einkommen <= 277825:
        return 0.42 * zu_versteuerndes_einkommen - 10911.92
    else:
        return 0.45 * zu_versteuerndes_einkommen - 19246.67
    
def cashflow(kredit, miete, monatliche_rate, zins, abschreibung, gehaltA, gehaltB):
    """
    Berechnet den jährlichen Cashflow und die Steuerersparnis während der Rückzahlung eines Kredits für eine Immobilie.

    Die Funktion simuliert die Rückzahlung eines Kredits über monatliche Ratenzahlungen, berechnet dabei die jährlich gezahlten Zinsen und Tilgungen,
    sowie die Steuerersparnis durch abzugsfähige Kosten (Zinsen und Abschreibung). Sie gibt jährlich eine Zusammenfassung des verbleibenden Kredits,
    des Cashflows, der gezahlten Zinsen und Tilgungen sowie der Steuerersparnis aus. Die Simulation läuft, bis der Kredit vollständig abbezahlt ist.

    Args:
        kredit (float): Anfangsbetrag des Kredits.
        miete (float): Monatliche Mieteinnahmen.
        monatliche_rate (float): Monatliche Kreditrate (Zins + Tilgung).
        zins (float): Effektiver Jahreszinssatz (z.B. 0.03 für 3%).
        abschreibung (float): Jährlicher Abschreibungsbetrag.
        gehaltA (float): Zu versteuerndes Jahreseinkommen der ersten Person.
        gehaltB (float): Zu versteuerndes Jahreseinkommen der zweiten Person.

    Returns:
        None: Gibt jährlich Informationen zum Cashflow und zur Steuerersparnis aus und beendet sich, wenn der Kredit abbezahlt ist.
    """
    jahr = 1
    monatlicher_zins = (1 + zins)**(1/12) - 1 
    while True: # Endlosschleife, bis Kredit abbezahlt ist
        # Initialisierung für jedes Jahr
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
        einkommen_aendern_pro_kopf = (miete*12 - zinsen_bezahlt - abschreibung) / 2
        soll_steuer = einkommensteuer(gehaltA) + einkommensteuer(gehaltB)
        echt_steuer = einkommensteuer(gehaltA + einkommen_aendern_pro_kopf) + einkommensteuer(gehaltB + einkommen_aendern_pro_kopf)
        steuerersparnis = soll_steuer - echt_steuer
        cashflow = miete * 12 - monatliche_rate * 12 + steuerersparnis
        print(f"Ende Jahr: {jahr} kredit: {kredit:.1f}, Cashflow: {cashflow:.1f}, davon Miete: {miete*12:.1f}, Zinsen: {-zinsen_bezahlt:.1f}, Tilgung: {-tilgung_bezahlt:.1f}, Steuerersparnis: {steuerersparnis:.1f}")
        jahr += 1

def main():
    kaufpreis = 239000
    eigenkapital = 30000
    zins = 0.0327
    tilgung = 0.02
    kaltmiete = 826
    baujahr =2001
    haus = False # True für Haus, False für Wohnung
    hausgeld = 164 # Nur für Wohnung
    if haus:
        kaltmiete = kaltmiete
    else:
        kaltmiete = kaltmiete - hausgeld
    kredit = gesamtkosten(kaufpreis) - eigenkapital
    ehemann_gehalt = 75000
    ehefrau_gehalt = 70000

    print("Der Kreditbetrag beträgt: ", kredit)
    print("Die monatliche Rate beträgt: ", monatliche_rate(kredit, zins, tilgung))
    print("Die monatliche Miete beträgt: ", kaltmiete)
    print("Die jährige Abschreibung beträgt: ", abschreibung(kaufpreis, baujahr))
    print("------------------------------------------------")
    cashflow(kredit, kaltmiete, monatliche_rate(kredit, zins, tilgung), zins, abschreibung(kaufpreis, baujahr), ehemann_gehalt, ehefrau_gehalt)

if __name__ == "__main__":
    main()