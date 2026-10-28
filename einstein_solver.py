"""Solver Zagadki Einsteina jako problem spełniania więzów (CSP).

Reprezentacja symboliczna:
    * Uniwersum pozycji: D = {1, 2, 3, 4, 5} (numery domów, od lewej).
    * Każda wartość atrybutu (np. "Norweg", "Czerwony", "Rybki") jest zmienną,
      której dziedziną jest D. Wartość zmiennej = numer domu, w którym dany
      atrybut występuje, czyli zmienna X reprezentuje poz(X).
    * W obrębie jednej kategorii (narodowość, kolor, ...) wszystkie zmienne
      muszą mieć różne wartości (więz AllDifferent) - każdy dom ma dokładnie
      jeden kolor, jednego mieszkańca itd.
    * 15 wskazówek z treści zagadki to dodatkowe więzy na tych zmiennych.

Źródło treści: https://www.math.edu.pl/zagadka-einsteina
Uruchomienie: python einstein_solver.py   (wymaga pakietu python-constraint2)
"""

from constraint import AllDifferentConstraint, Problem

# --- Uniwersum: domy i kategorie atrybutów ----------------------------------

DOMY = [1, 2, 3, 4, 5]

KATEGORIE = {
    "Narodowość": ["Norweg", "Anglik", "Duńczyk", "Niemiec", "Szwed"],
    "Kolor": ["Czerwony", "Zielony", "Biały", "Żółty", "Niebieski"],
    "Napój": ["Herbata", "Mleko", "Woda", "Piwo", "Kawa"],
    "Papierosy": ["Rothmans", "Dunhill", "Marlboro", "Pall Mall", "Philip Morris"],
    "Zwierzę": ["Koty", "Ptaki", "Psy", "Konie", "Rybki"],
}


# --- Relacje przestrzenne (predykaty) ---------------------------------------

def obok(a, b):
    """Obok(a, b) <=> |poz(a) - poz(b)| = 1."""
    return abs(a - b) == 1


def na_lewo(a, b):
    """NaLewo(a, b) <=> poz(a) = poz(b) - 1 (a stoi bezpośrednio na lewo od b)."""
    return a == b - 1


def ten_sam_dom(a, b):
    """TenSamDom(a, b) <=> poz(a) = poz(b)."""
    return a == b


def zbuduj_problem():
    """Tworzy model CSP: zmienne, dziedziny i wszystkie więzy."""
    problem = Problem()

    # Zmienne i dziedziny: poz(X) ∈ D dla każdej wartości atrybutu X.
    for wartosci in KATEGORIE.values():
        problem.addVariables(wartosci, DOMY)
        # Więz strukturalny: w kategorii każda wartość w innym domu.
        problem.addConstraint(AllDifferentConstraint(), wartosci)

    # 15 wskazówek z treści zagadki.
    # W1: Norweg mieszka w pierwszym domu.
    problem.addConstraint(lambda n: n == 1, ["Norweg"])
    # W2: Anglik mieszka w czerwonym domu.
    problem.addConstraint(ten_sam_dom, ["Anglik", "Czerwony"])
    # W3: Zielony dom stoi bezpośrednio po lewej stronie białego.
    problem.addConstraint(na_lewo, ["Zielony", "Biały"])
    # W4: Duńczyk pija herbatę.
    problem.addConstraint(ten_sam_dom, ["Duńczyk", "Herbata"])
    # W5: Palacz Rothmansów mieszka obok hodowcy kotów.
    problem.addConstraint(obok, ["Rothmans", "Koty"])
    # W6: Mieszkaniec żółtego domu pali Dunhille.
    problem.addConstraint(ten_sam_dom, ["Żółty", "Dunhill"])
    # W7: Niemiec pali Marlboro.
    problem.addConstraint(ten_sam_dom, ["Niemiec", "Marlboro"])
    # W8: Mieszkaniec środkowego domu pija mleko.
    problem.addConstraint(lambda m: m == 3, ["Mleko"])
    # W9: Palacz Rothmansów ma sąsiada, który pija wodę.
    problem.addConstraint(obok, ["Rothmans", "Woda"])
    # W10: Palacz Pall Malli hoduje ptaki.
    problem.addConstraint(ten_sam_dom, ["Pall Mall", "Ptaki"])
    # W11: Szwed hoduje psy.
    problem.addConstraint(ten_sam_dom, ["Szwed", "Psy"])
    # W12: Norweg mieszka obok niebieskiego domu.
    problem.addConstraint(obok, ["Norweg", "Niebieski"])
    # W13: Hodowca koni mieszka obok żółtego domu.
    problem.addConstraint(obok, ["Konie", "Żółty"])
    # W14: Palacz Philip Morrisów pija piwo.
    problem.addConstraint(ten_sam_dom, ["Philip Morris", "Piwo"])
    # W15: W zielonym domu pija się kawę.
    problem.addConstraint(ten_sam_dom, ["Zielony", "Kawa"])

    return problem


def odwroc(rozwiazanie):
    """Zamienia przypisanie {atrybut: dom} na macierz {dom: {kategoria: atrybut}}."""
    macierz = {dom: {} for dom in DOMY}
    for kategoria, wartosci in KATEGORIE.items():
        for wartosc in wartosci:
            macierz[rozwiazanie[wartosc]][kategoria] = wartosc
    return macierz


def tabela_markdown(macierz):
    """Formatuje macierz rozwiązania jako tabelę Markdown."""
    naglowek = ["Dom", *KATEGORIE]
    wiersze = [
        "| " + " | ".join(naglowek) + " |",
        "|" + "|".join(["---"] * len(naglowek)) + "|",
    ]
    for dom in DOMY:
        komorki = [str(dom), *(macierz[dom][k] for k in KATEGORIE)]
        wiersze.append("| " + " | ".join(komorki) + " |")
    return "\n".join(wiersze)


def main():
    rozwiazania = zbuduj_problem().getSolutions()
    print(f"Liczba rozwiązań: {len(rozwiazania)}")
    if len(rozwiazania) != 1:
        raise SystemExit("Zagadka nie ma jednoznacznego rozwiązania.")

    macierz = odwroc(rozwiazania[0])
    print()
    print(tabela_markdown(macierz))

    dom_rybek = rozwiazania[0]["Rybki"]
    print()
    print(f"Kto hoduje rybki? {macierz[dom_rybek]['Narodowość']} (dom nr {dom_rybek}).")


if __name__ == "__main__":
    main()
