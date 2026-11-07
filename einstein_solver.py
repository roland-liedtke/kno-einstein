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

HOUSES = [1, 2, 3, 4, 5]

CATEGORIES = {
    "Narodowość": ["Norweg", "Anglik", "Duńczyk", "Niemiec", "Szwed"],
    "Kolor": ["Czerwony", "Zielony", "Biały", "Żółty", "Niebieski"],
    "Napój": ["Herbata", "Mleko", "Woda", "Piwo", "Kawa"],
    "Papierosy": ["Rothmans", "Dunhill", "Marlboro", "Pall Mall", "Philip Morris"],
    "Zwierzę": ["Koty", "Ptaki", "Psy", "Konie", "Rybki"],
}


# --- Relacje przestrzenne (predykaty) ---------------------------------------

def next_to(a, b):
    """Obok(a, b) <=> |poz(a) - poz(b)| = 1."""
    return abs(a - b) == 1


def left_of(a, b):
    """NaLewo(a, b) <=> poz(a) = poz(b) - 1 (a stoi bezpośrednio na lewo od b)."""
    return a == b - 1


def same_house(a, b):
    """TenSamDom(a, b) <=> poz(a) = poz(b)."""
    return a == b


def in_first_house(a):
    """poz(a) = 1 (a mieszka w pierwszym domu)."""
    return a == 1


def in_middle_house(a):
    """poz(a) = 3 (a mieszka w środkowym domu)."""
    return a == 3


def build_problem():
    """Tworzy model CSP: zmienne, dziedziny i wszystkie więzy."""
    problem = Problem()

    # Zmienne i dziedziny: poz(X) ∈ D dla każdej wartości atrybutu X.
    for values in CATEGORIES.values():
        problem.addVariables(values, HOUSES)
        # Więz strukturalny: w kategorii każda wartość w innym domu.
        problem.addConstraint(AllDifferentConstraint(), values)

    # 15 wskazówek z treści zagadki.
    # W1: Norweg mieszka w pierwszym domu.
    problem.addConstraint(in_first_house, ["Norweg"])
    # W2: Anglik mieszka w czerwonym domu.
    problem.addConstraint(same_house, ["Anglik", "Czerwony"])
    # W3: Zielony dom stoi bezpośrednio po lewej stronie białego.
    problem.addConstraint(left_of, ["Zielony", "Biały"])
    # W4: Duńczyk pija herbatę.
    problem.addConstraint(same_house, ["Duńczyk", "Herbata"])
    # W5: Palacz Rothmansów mieszka obok hodowcy kotów.
    problem.addConstraint(next_to, ["Rothmans", "Koty"])
    # W6: Mieszkaniec żółtego domu pali Dunhille.
    problem.addConstraint(same_house, ["Żółty", "Dunhill"])
    # W7: Niemiec pali Marlboro.
    problem.addConstraint(same_house, ["Niemiec", "Marlboro"])
    # W8: Mieszkaniec środkowego domu pija mleko.
    problem.addConstraint(in_middle_house, ["Mleko"])
    # W9: Palacz Rothmansów ma sąsiada, który pija wodę.
    problem.addConstraint(next_to, ["Rothmans", "Woda"])
    # W10: Palacz Pall Malli hoduje ptaki.
    problem.addConstraint(same_house, ["Pall Mall", "Ptaki"])
    # W11: Szwed hoduje psy.
    problem.addConstraint(same_house, ["Szwed", "Psy"])
    # W12: Norweg mieszka obok niebieskiego domu.
    problem.addConstraint(next_to, ["Norweg", "Niebieski"])
    # W13: Hodowca koni mieszka obok żółtego domu.
    problem.addConstraint(next_to, ["Konie", "Żółty"])
    # W14: Palacz Philip Morrisów pija piwo.
    problem.addConstraint(same_house, ["Philip Morris", "Piwo"])
    # W15: W zielonym domu pija się kawę.
    problem.addConstraint(same_house, ["Zielony", "Kawa"])

    return problem


def invert(solution):
    """Zamienia przypisanie {atrybut: dom} na macierz {dom: {kategoria: atrybut}}."""
    matrix = {house: {} for house in HOUSES}
    for category, values in CATEGORIES.items():
        for value in values:
            matrix[solution[value]][category] = value
    return matrix


def terminal_table(matrix):
    """Formatuje macierz rozwiązania jako tabelę z ramką do wydruku w terminalu.

    Szerokość każdej kolumny = najdłuższy tekst w kolumnie (nagłówek lub
    wartość), więc kolumny są wyrównane niezależnie od długości nazw.
    """
    header = ["Dom", *CATEGORIES]
    rows = [
        [str(house), *(matrix[house][cat] for cat in CATEGORIES)]
        for house in HOUSES
    ]
    widths = [max(len(row[i]) for row in [header, *rows]) for i in range(len(header))]

    def border(left, middle, right):
        return left + middle.join("─" * (w + 2) for w in widths) + right

    def line(cells):
        padded = [
            cell.center(w) if i == 0 else cell.ljust(w)
            for i, (cell, w) in enumerate(zip(cells, widths))
        ]
        return "│ " + " │ ".join(padded) + " │"

    return "\n".join([
        border("┌", "┬", "┐"),
        line(header),
        border("├", "┼", "┤"),
        *(line(row) for row in rows),
        border("└", "┴", "┘"),
    ])


def main():
    solutions = build_problem().getSolutions()
    print(f"Liczba rozwiązań: {len(solutions)}")
    if len(solutions) != 1:
        raise SystemExit("Zagadka nie ma jednoznacznego rozwiązania.")

    matrix = invert(solutions[0])
    print()
    print(terminal_table(matrix))

    fish_house = solutions[0]["Rybki"]
    print()
    print(f"Kto hoduje rybki? {matrix[fish_house]['Narodowość']} (dom nr {fish_house}).")


if __name__ == "__main__":
    main()
