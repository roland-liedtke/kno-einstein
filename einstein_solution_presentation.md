# Zagadka Einsteina — reprezentacja symboliczna i automatyczne wnioskowanie

Projekt KNO nr 1 · temat: **reprezentacja symboliczna** · treść zagadki: [math.edu.pl/zagadka-einsteina](https://www.math.edu.pl/zagadka-einsteina)

> **Treść w skrócie.** Pięć domów w pięciu kolorach stoi w rzędzie. W każdym mieszka osoba innej narodowości; każda pije inny napój, pali inną markę papierosów i hoduje inne zwierzę. Na podstawie 15 wskazówek należy ustalić, **kto hoduje rybki**.

---

## 1. Odpowiedź na pytanie główne

> **Jak przejść od opisu problemu w języku naturalnym do formalnej reprezentacji, na podstawie której można wywnioskować rozwiązanie?**

Przejście odbywa się w czterech krokach. Każdy z nich usuwa część niejednoznaczności języka naturalnego, aż zostaje obiekt matematyczny, na którym da się mechanicznie wnioskować.

```
 tekst w języku naturalnym
        │  (1) identyfikacja pojęć → zmienne i dziedziny
        ▼
 uniwersum: obiekty, właściwości, relacje
        │  (2) formalizacja zdań → predykaty / więzy / klauzule
        ▼
 model formalny (CSP / formuła logiki pierwszego rzędu)
        │  (3) wnioskowanie: propagacja więzów + przeszukiwanie
        ▼
 przypisanie spełniające wszystkie więzy
        │  (4) interpretacja z powrotem w języku naturalnym
        ▼
 „Rybki hoduje Niemiec”
```

### 1.1. Mapowanie pojęć języka naturalnego na zmienne i dziedziny

Najpierw wyodrębniamy z tekstu **rzeczowniki** i **cechy**, które w nim występują, i grupujemy je w kategorie: „Norweg”, „Anglik”… to wartości kategorii *Narodowość*; „czerwony”, „zielony”… to wartości kategorii *Kolor* itd. Trzeba też wskazać, **co jest nieznane**. Tu niewiadomą jest przyporządkowanie: który atrybut należy do którego domu.

Można to zakodować na dwa równoważne sposoby:

| Wariant | Zmienne | Dziedzina | Liczba zmiennych |
|---|---|---|---|
| A — „dom → atrybut” | $\text{Kolor}(d)$, $\text{Narodowość}(d)$, … dla $d \in D$ | zbiór wartości kategorii | 25 |
| B — „atrybut → dom” | $\text{poz}(x)$ dla każdej wartości $x$ (np. $\text{poz}(\text{Norweg})$) | $D=\{1,\dots,5\}$ | 25 |

Wybieramy **wariant B**. Wszystkie zmienne mają wtedy tę samą dziedzinę liczbową, więc relacje przestrzenne („obok”, „na lewo”) stają się zwykłą arytmetyką na numerach domów.

### 1.2. Definiowanie uniwersum

Uniwersum to wszystko, o czym model może cokolwiek orzec:

* **obiekty**: domy $D=\{1,2,3,4,5\}$ uporządkowane liniowo (od lewej do prawej);
* **właściwości**: 25 wartości atrybutów w 5 rozłącznych kategoriach. Każdemu domowi przysługuje dokładnie jedna wartość z każdej kategorii;
* **relacje**: *ten sam dom* ($=$), *bezpośrednio na lewo* ($\text{poz}(a)=\text{poz}(b)-1$), *obok* ($|\text{poz}(a)-\text{poz}(b)|=1$).

Część wiedzy jest w tekście **niejawna**, a w modelu musi być zapisana jawnie: „każdy pije **inny** napój” oznacza, że przyporządkowanie jest bijekcją, czyli działa więz *all-different*. Człowiek uzupełnia to zdrowym rozsądkiem, maszyna potrzebuje osobnej reguły.

### 1.3. Formalizacja zdań

Każde zdanie przekładamy na **więz**, czyli relację, którą muszą spełniać wartości wskazanych zmiennych. Zdania w tej zagadce mają tylko kilka wzorców składniowych:

| Wzorzec w języku naturalnym | Predykat | Formuła |
|---|---|---|
| „X mieszka w domu nr k” | stała | $\text{poz}(X)=k$ |
| „X [ma / pije / pali / hoduje] Y” | $\text{TenSamDom}(X,Y)$ | $\text{poz}(X)=\text{poz}(Y)$ |
| „X stoi bezpośrednio na lewo od Y” | $\text{NaLewo}(X,Y)$ | $\text{poz}(X)=\text{poz}(Y)-1$ |
| „X mieszka obok Y” / „X ma sąsiada Y” | $\text{Obok}(X,Y)$ | $\lvert\text{poz}(X)-\text{poz}(Y)\rvert=1$ |

Ten sam model można zapisać w kilku równoważnych formalizmach:

* **CSP** (*Constraint Satisfaction Problem*): trójka $\langle X, \mathcal{D}, C\rangle$, czyli zmienne, dziedziny i więzy. Ten formalizm wykorzystuje nasz solver.
* **Logika pierwszego rzędu**: np. $\forall d\,(\text{Ma}(d,\text{Zielony}) \rightarrow \text{Ma}(d+1,\text{Biały}))$.
* **Programowanie w logice** (Prolog): fakty i reguły, a rozwiązanie wyznacza unifikacja z nawrotami.
* **SAT**: zmienne boolowskie $x_{\text{Norweg},1}, x_{\text{Norweg},2},\dots$ (125 zmiennych) i klauzule CNF.

### 1.4. Wnioskowanie jako przeszukiwanie przestrzeni stanów

* **Stan** to częściowe przypisanie wartości zmiennym. **Cel** to pełne przypisanie, które spełnia wszystkie więzy.
* Przestrzeń pełnych przypisań zgodnych z *all-different* ma $(5!)^5 \approx 2{,}5\cdot 10^{10}$ elementów. Przegląd zupełny jest możliwy, ale nieefektywny.
* **Propagacja więzów** (np. *forward checking*, spójność łukowa) usuwa z dziedzin wartości, które nie mogą należeć do żadnego rozwiązania. Wskazówki 1 i 8 od razu ustalają $\text{poz}(\text{Norweg})=1$ i $\text{poz}(\text{Mleko})=3$.
* **Przeszukiwanie z nawrotami** (*backtracking*) przypisuje kolejne zmienne. Gdy dziedzina którejś zmiennej się opróżni, solver cofa ostatnią decyzję.
* Ta sama procedura **dowodzi jednoznaczności**: solver wylicza wszystkie rozwiązania i znajduje dokładnie jedno. Odpowiedź jest więc logiczną konsekwencją wskazówek, a nie jednym z możliwych wariantów.

---

## 2. Reprezentacja Symboliczna (Model Logiczny)

### 2.1. Zbiory (dziedziny)

$$
\begin{aligned}
D   &= \{1,2,3,4,5\} && \text{(domy, numerowane od lewej)}\\
N   &= \{\text{Norweg},\ \text{Anglik},\ \text{Duńczyk},\ \text{Niemiec},\ \text{Szwed}\} && \text{(narodowości)}\\
K   &= \{\text{Czerwony},\ \text{Zielony},\ \text{Biały},\ \text{Żółty},\ \text{Niebieski}\} && \text{(kolory)}\\
Nap &= \{\text{Herbata},\ \text{Mleko},\ \text{Woda},\ \text{Piwo},\ \text{Kawa}\} && \text{(napoje)}\\
P   &= \{\text{Rothmans},\ \text{Dunhill},\ \text{Marlboro},\ \text{Pall Mall},\ \text{Philip Morris}\} && \text{(papierosy)}\\
Z   &= \{\text{Koty},\ \text{Ptaki},\ \text{Psy},\ \text{Konie},\ \text{Rybki}\} && \text{(zwierzęta)}
\end{aligned}
$$

Zbiór wszystkich atrybutów: $A = N \cup K \cup Nap \cup P \cup Z$, $|A| = 25$.

### 2.2. Zmienne

Szukamy funkcji
$$
\text{poz} : A \to D,
$$
gdzie $\text{poz}(x)$ to numer domu, w którym występuje atrybut $x$. Każda wartość $\text{poz}(x)$ jest zmienną CSP o dziedzinie $D$.

### 2.3. Więzy strukturalne (wiedza niejawna)

Dla każdej kategorii $S \in \{N, K, Nap, P, Z\}$:
$$
\text{AllDifferent}(S):\quad \forall x,y \in S:\ x \neq y \rightarrow \text{poz}(x) \neq \text{poz}(y).
$$
Ponieważ $|S| = |D| = 5$, funkcja $\text{poz}$ obcięta do $S$ jest bijekcją, czyli każdy dom ma dokładnie jedną wartość każdej kategorii.

### 2.4. Predykaty pomocnicze

$$
\begin{aligned}
\text{TenSamDom}(x,y) &\iff \text{poz}(x) = \text{poz}(y)\\
\text{NaLewo}(x,y)    &\iff \text{poz}(x) = \text{poz}(y) - 1\\
\text{Obok}(x,y)      &\iff \lvert \text{poz}(x) - \text{poz}(y) \rvert = 1
\end{aligned}
$$

### 2.5. Piętnaście wskazówek jako formuły

| Nr | Język naturalny | Formuła |
|---:|---|---|
| W1 | Norweg mieszka w pierwszym domu. | $\text{poz}(\text{Norweg}) = 1$ |
| W2 | Anglik mieszka w czerwonym domu. | $\text{poz}(\text{Anglik}) = \text{poz}(\text{Czerwony})$ |
| W3 | Zielony dom stoi bezpośrednio na lewo od białego. | $\text{poz}(\text{Zielony}) = \text{poz}(\text{Biały}) - 1$ |
| W4 | Duńczyk pije herbatę. | $\text{poz}(\text{Duńczyk}) = \text{poz}(\text{Herbata})$ |
| W5 | Palacz Rothmansów mieszka obok hodowcy kotów. | $\lvert\text{poz}(\text{Rothmans}) - \text{poz}(\text{Koty})\rvert = 1$ |
| W6 | Mieszkaniec żółtego domu pali Dunhille. | $\text{poz}(\text{Żółty}) = \text{poz}(\text{Dunhill})$ |
| W7 | Niemiec pali Marlboro. | $\text{poz}(\text{Niemiec}) = \text{poz}(\text{Marlboro})$ |
| W8 | Mieszkaniec środkowego domu pije mleko. | $\text{poz}(\text{Mleko}) = 3$ |
| W9 | Palacz Rothmansów ma sąsiada, który pije wodę. | $\lvert\text{poz}(\text{Rothmans}) - \text{poz}(\text{Woda})\rvert = 1$ |
| W10 | Palacz Pall Malli hoduje ptaki. | $\text{poz}(\text{Pall Mall}) = \text{poz}(\text{Ptaki})$ |
| W11 | Szwed hoduje psy. | $\text{poz}(\text{Szwed}) = \text{poz}(\text{Psy})$ |
| W12 | Norweg mieszka obok niebieskiego domu. | $\lvert\text{poz}(\text{Norweg}) - \text{poz}(\text{Niebieski})\rvert = 1$ |
| W13 | Hodowca koni mieszka obok żółtego domu. | $\lvert\text{poz}(\text{Konie}) - \text{poz}(\text{Żółty})\rvert = 1$ |
| W14 | Palacz Philip Morrisów pije piwo. | $\text{poz}(\text{Philip Morris}) = \text{poz}(\text{Piwo})$ |
| W15 | W zielonym domu pije się kawę. | $\text{poz}(\text{Zielony}) = \text{poz}(\text{Kawa})$ |

### 2.6. Ten sam model w logice pierwszego rzędu (wariant A)

Dla porównania, w wariancie „dom → atrybut” z predykatem $\text{Ma}(d, x)$ („dom $d$ ma atrybut $x$”):

$$
\begin{aligned}
\text{W1:}\ & \text{Ma}(1, \text{Norweg})\\
\text{W3:}\ & \forall d \in D:\ \text{Ma}(d,\text{Zielony}) \leftrightarrow (d < 5 \wedge \text{Ma}(d+1,\text{Biały}))\\
\text{W5:}\ & \forall d \in D:\ \text{Ma}(d,\text{Rothmans}) \rightarrow \exists e \in D:\ |d-e|=1 \wedge \text{Ma}(e,\text{Koty})\\
\text{Unikalność:}\ & \forall S\ \forall d\ \exists!\,x \in S:\ \text{Ma}(d,x) \quad\wedge\quad \forall S\ \forall x \in S\ \exists!\,d:\ \text{Ma}(d,x)
\end{aligned}
$$

**Zapytanie:** $\exists n \in N\ \exists d \in D:\ \text{Ma}(d, n) \wedge \text{Ma}(d, \text{Rybki})$. Szukamy takiego $n$.

### 2.7. Rozmiar problemu

* 25 zmiennych, każda o dziedzinie 5-elementowej, daje $5^{25} \approx 3\cdot 10^{17}$ przypisań.
* Po uwzględnieniu *all-different* zostaje $(5!)^5 = 120^5 \approx 2{,}49\cdot 10^{10}$ kandydatów.
* Po nałożeniu 15 wskazówek zostaje **dokładnie 1** rozwiązanie.

---

## 3. Kod źródłowy w Pythonie (Solver)

Solver korzysta z biblioteki [`python-constraint2`](https://pypi.org/project/python-constraint2/), utrzymywanej kontynuacji `python-constraint` o tym samym API (`from constraint import ...`).

### 3.1. `python-constraint` a `python-constraint2`

Na PyPI istnieją dwa pakiety o tej samej nazwie modułu (`constraint`), więc nie należy ich instalować jednocześnie:

| | [`python-constraint`](https://pypi.org/project/python-constraint/) | [`python-constraint2`](https://pypi.org/project/python-constraint2/) |
|---|---|---|
| Status | **nierozwijany** — ostatnie wydanie 1.4.0 z 5.11.2018 | **rozwijany przez społeczność** — wydania 2.x od 2025 r., ostatnie 2.9.0 z 27.10.2026 |
| Autor / opiekun | Gustavo Niemeyer (autor oryginału) | Floris-Jan Willemsen i kontrybutorzy organizacji [`python-constraint`](https://github.com/python-constraint/python-constraint) na GitHubie |
| Python | wersje z epoki Pythona 2/3.x, bez wsparcia nowych wydań | Python ≥ 3.11 (do 3.15) |
| Implementacja | czysty Python | kod kompilowany Cythonem do C — wyraźnie szybszy |
| API | `Problem`, `addVariable(s)`, `addConstraint`, `getSolution(s)`, podstawowe więzy (`AllDifferent`, `ExactSum`, `InSet` …) | to samo API (kompatybilne wstecz) **plus** nowe więzy (np. `ExactProdConstraint`, `MaxProdConstraint`, `Variable*SumConstraint`), więzy zapisywane jako napisy (`"a + b == 5"`), solvery `OptimizedBacktrackingSolver` (domyślny) i `ParallelSolver` |

Dla naszego modelu oba pakiety dałyby ten sam wynik — używamy wyłącznie `Problem`, `AllDifferentConstraint` i więzów-funkcji. Wybraliśmy `python-constraint2`, bo jest aktywnie utrzymywany, działa z Pythonem 3.13 i jest szybszy.

### 3.2. Struktura kodu

Struktura kodu odpowiada modelowi z sekcji 2:

| Model (sekcja 2) | Kod |
|---|---|
| zbiory $N, K, Nap, P, Z$ | słownik `CATEGORIES` |
| zmienne $\text{poz}(x) \in D$ | `problem.addVariables(values, HOUSES)` |
| $\text{AllDifferent}(S)$ | `AllDifferentConstraint()` |
| predykaty $\text{TenSamDom}$, $\text{NaLewo}$, $\text{Obok}$ | funkcje `same_house`, `left_of`, `next_to` |
| wskazówki W1–W15 | 15 wywołań `addConstraint` z komentarzem `# Wn:` |

**Uruchomienie:**

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt     # python-constraint2==2.9.0
.venv/bin/python einstein_solver.py
```

**`einstein_solver.py`:**

```python
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
    problem.addConstraint(lambda pos: pos == 1, ["Norweg"])
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
    problem.addConstraint(lambda pos: pos == 3, ["Mleko"])
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


def markdown_table(matrix):
    """Formatuje macierz rozwiązania jako tabelę Markdown."""
    header = ["Dom", *CATEGORIES]
    rows = [
        "| " + " | ".join(header) + " |",
        "|" + "|".join(["---"] * len(header)) + "|",
    ]
    for house in HOUSES:
        cells = [str(house), *(matrix[house][cat] for cat in CATEGORIES)]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join(rows)


def main():
    solutions = build_problem().getSolutions()
    print(f"Liczba rozwiązań: {len(solutions)}")
    if len(solutions) != 1:
        raise SystemExit("Zagadka nie ma jednoznacznego rozwiązania.")

    matrix = invert(solutions[0])
    print()
    print(markdown_table(matrix))

    fish_house = solutions[0]["Rybki"]
    print()
    print(f"Kto hoduje rybki? {matrix[fish_house]['Narodowość']} (dom nr {fish_house}).")


if __name__ == "__main__":
    main()
```

---

## 4. Wyniki i Macierz Rozwiązania

Wynik uruchomienia `einstein_solver.py` (czas ok. 0,2 s):

```text
Liczba rozwiązań: 1

| Dom | Narodowość | Kolor | Napój | Papierosy | Zwierzę |
|---|---|---|---|---|---|
| 1 | Norweg | Żółty | Woda | Dunhill | Koty |
| 2 | Duńczyk | Niebieski | Herbata | Rothmans | Konie |
| 3 | Anglik | Czerwony | Mleko | Pall Mall | Ptaki |
| 4 | Niemiec | Zielony | Kawa | Marlboro | Rybki |
| 5 | Szwed | Biały | Piwo | Philip Morris | Psy |

Kto hoduje rybki? Niemiec (dom nr 4).
```

### Macierz rozwiązania

| Dom | Narodowość | Kolor | Napój | Papierosy | Zwierzę |
|---|---|---|---|---|---|
| 1 | Norweg | Żółty | Woda | Dunhill | Koty |
| 2 | Duńczyk | Niebieski | Herbata | Rothmans | Konie |
| 3 | Anglik | Czerwony | Mleko | Pall Mall | Ptaki |
| 4 | Niemiec | Zielony | Kawa | Marlboro | Rybki |
| 5 | Szwed | Biały | Piwo | Philip Morris | Psy |

> ### Odpowiedź: **rybki hoduje Niemiec**, który mieszka w zielonym domu nr 4, pije kawę i pali Marlboro.

### Jak wnioskuje solver: pierwsze kroki prześledzone ręcznie

Poniższe kroki pokazują, jak propagacja więzów zawęża dziedziny. Solver wykonuje to samo mechanicznie.

1. **W1** daje $\text{poz}(\text{Norweg}) = 1$, a **W8** daje $\text{poz}(\text{Mleko}) = 3$. To więzy unarne, więc dziedziny tych zmiennych od razu redukują się do jednej wartości.
2. **W12**: Norweg (dom 1) ma sąsiada w niebieskim domu, a dom 1 ma tylko jednego sąsiada. Stąd $\text{poz}(\text{Niebieski}) = 2$.
3. **W3**: para (Zielony, Biały) to sąsiednie domy $(d, d+1)$. Dom 2 jest niebieski, więc zostają pary $(3,4)$ i $(4,5)$. **W15**: w zielonym domu pije się kawę, a w domu 3 pije się mleko. Zatem $\text{poz}(\text{Zielony}) = 4$ i $\text{poz}(\text{Biały}) = 5$.
4. Wolne kolory dla domów 1 i 3 to czerwony i żółty. **W2**: w czerwonym domu mieszka Anglik, a dom 1 należy do Norwega. Zatem dom 3 jest czerwony, a dom 1 żółty.
5. **W6** daje Dunhill w domu 1. **W13**: konie są obok żółtego domu, więc w domu 2.
6. Dalej podobnie: napoje (W4, W14), papierosy (W9, W5, W7, W10), narodowości (W11). Na końcu dla rybek zostaje tylko dom 4, w którym mieszka Niemiec.

Solver nie potrzebuje tej „sprytnej” kolejności kroków. Wystarczą mu reguły z sekcji 2 i ogólny algorytm.

---

## 5. Scenariusz Prezentacji na Teams

**Czas łączny:** ok. 12–15 min + pytania. **Na ekranie:** ten plik (podgląd Markdown), terminal z gotowym `.venv` i edytor z `einstein_solver.py`.

**Przed spotkaniem (checklista):**
- [ ] Sprawdź, czy `.venv/bin/python einstein_solver.py` działa, i zostaw terminal otwarty w katalogu projektu.
- [ ] Ustaw większą czcionkę w terminalu i edytorze (min. 16–18 pt), bo na udostępnionym ekranie mały tekst jest nieczytelny.
- [ ] Udostępniaj **okno**, a nie cały pulpit. Wyłącz powiadomienia.
- [ ] Miej pod ręką zrzut ekranu wyniku na wypadek problemów z uruchomieniem.

### Blok 1 — Wstęp teoretyczny (ok. 3 min) · *na ekranie: sekcja 1, diagram z czterema krokami*

- Przedstaw temat: „Pokażę, jak zagadkę logiczną zapisaną zwykłym językiem zamienić na model, który komputer rozwiązuje sam”.
- Postaw pytanie główne i odpowiedz na nie **czterema krokami** z diagramu: pojęcia → uniwersum → więzy → wnioskowanie.
- Zaznacz kluczową decyzję modelowania: **zmienną jest numer domu danego atrybutu**. Dzięki temu „obok” i „na lewo” to zwykła arytmetyka.
- Wspomnij o wiedzy niejawnej: „każdy pije **inny** napój” trzeba zapisać jako osobny więz *AllDifferent*.

### Blok 2 — Demonstracja reprezentacji symbolicznej (ok. 4 min) · *na ekranie: sekcja 2.5, tabela wskazówek*

- Pokaż zbiory z sekcji 2.1: 5 domów i 5 kategorii po 5 wartości, czyli 25 zmiennych.
- Omów **trzy wzorce** zdań (tabela w 1.3) i na każdy podaj przykład z tabeli 2.5:
  - stała: W1 „Norweg w pierwszym domu” → $\text{poz}(\text{Norweg})=1$;
  - ten sam dom: W2 „Anglik w czerwonym” → $\text{poz}(\text{Anglik})=\text{poz}(\text{Czerwony})$;
  - relacja przestrzenna: W3 „zielony na lewo od białego” → $\text{poz}(\text{Zielony})=\text{poz}(\text{Biały})-1$ oraz W12 „obok” → wartość bezwzględna różnicy równa 1.
- Puenta: „Wszystkie 15 zdań da się wyrazić tymi trzema wzorcami. Język naturalny jest bogaty, ale treść logiczna tej zagadki jest bardzo prosta”.
- (Opcjonalnie, 30 s) Sekcja 2.6: ten sam model w logice pierwszego rzędu. Reprezentacja nie zależy od narzędzia.

### Blok 3 — Kod i wynik (ok. 4 min) · *na ekranie: edytor, potem terminal*

- Pokaż w kodzie **odpowiedniki modelu** według tabeli z sekcji 3: `CATEGORIES` → `addVariables` → `AllDifferentConstraint` → 15 komentarzy `# W1…# W15`.
- Zwróć uwagę, że każda wskazówka to **jedna linijka**, a komentarz nad nią to dosłowne zdanie z zagadki. To czytelny ślad od tekstu do formuły.
- Uruchom na żywo: `.venv/bin/python einstein_solver.py`.
- Omów wynik:
  - „Liczba rozwiązań: 1”, czyli wskazówki wyznaczają rozwiązanie jednoznacznie;
  - macierz 5×5 (sekcja 4);
  - odpowiedź: **rybki hoduje Niemiec (dom 4)**.
- (Jeśli zostanie czas) Przejdź szybko przez 2–3 pierwsze kroki ręcznego wnioskowania z sekcji 4, żeby pokazać, czym jest propagacja więzów.

### Blok 4 — Wnioski (ok. 2 min) · *na ekranie: sekcja 2.7 lub ostatni slajd*

- **Rozdzielenie „co” od „jak”**: opisujemy *co* musi być prawdą (więzy), a ogólny algorytm sam ustala, *jak* to znaleźć. Nie trzeba wymyślać sprytnej kolejności rozumowania.
- **Skala**: z ok. $2{,}5\cdot 10^{10}$ kandydatów propagacja i nawroty zostawiają 1 rozwiązanie w ułamku sekundy.
- **Weryfikowalność**: każdą regułę da się porównać ze zdaniem źródłowym. Solver dodatkowo sprawdza, że rozwiązanie jest jedyne.
- **Przenośność**: zmiana zagadki (inne wskazówki, więcej domów) wymaga zmiany danych i reguł, a algorytmu nie trzeba ruszać. Ten sam model da się zapisać w Prologu, SAT czy SMT.
- Zakończenie: „Najtrudniejsze było przełożenie tekstu na formuły. Samo rozwiązanie znalazł już algorytm”.

### Pytania, których można się spodziewać

| Pytanie | Krótka odpowiedź |
|---|---|
| Czemu zmiennymi są atrybuty, a nie domy? | Wspólna dziedzina liczbowa $\{1..5\}$ sprawia, że relacje „obok” i „na lewo” są arytmetyką. Wariant „dom → atrybut” też działa, ale te relacje są w nim bardziej rozwlekłe (patrz 2.6). |
| Skąd pewność, że rozwiązanie jest jedyne? | `getSolutions()` wylicza **wszystkie** rozwiązania, a program sprawdza, że jest dokładnie jedno. |
| Jak by to wyglądało w Prologu lub z3? | Te same więzy: w Prologu jako `member/2` i `nextto/3` z nawrotami, w z3 jako `Distinct(...)` i `Abs(a-b) == 1`. Model się nie zmienia, zmienia się tylko składnia. |
| Co, gdyby usunąć jedną wskazówkę? | Rozwiązań może być więcej. `getSolutions()` zwróci wszystkie, program wypisze ich liczbę i zgłosi brak jednoznaczności, więc łatwo sprawdzić, które wskazówki są niezbędne. |
| Czy to naprawdę wymyślił Einstein? | Brak na to dowodów, to raczej legenda. Ten typ łamigłówki to tzw. *zebra puzzle*. |
