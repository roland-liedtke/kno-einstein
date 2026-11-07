# NOW — stan projektu
*Ostatnia aktualizacja: 2026-11-07 13:29*

## Stan
- `einstein_solver.py` działa: model CSP z 15 więzami, sprawdza jednoznaczność; wynik — 1 rozwiązanie, rybki hoduje Niemiec (dom 4).
- Macierz wypisywana jako tabela z ramką (znaki `┌─┬│`) z wyrównanymi kolumnami (PR feat/czytelny-wydruk-macierzy); testy w `test_einstein_solver.py` (6, przechodzą).
- `einstein_solution_presentation.md` — sekcje 1–5 gotowe (teoria, model logiczny, kod, macierz wyników, scenariusz Teams); sekcje 3 i 4 zgodne z kodem i wynikiem (ostatnio po PR feat/czytelny-wydruk-macierzy).
- `.venv` z `python-constraint2==2.9.0`; `python3 -m venv` tworzy venv z pipem.

## W toku
- (brak)

## Dalej
1. Ewentualnie: slajdy na podstawie sekcji 5 opracowania.
2. Ewentualnie: wariant solvera w z3 lub Prologu do porównania.

## Decyzje
- 2026-10-28: `python-constraint2` zamiast `python-constraint` — stary pakiet nierozwijany (1.4.0 z 2018), nowy rozwijany (2.9.0); porównanie w sekcji 3.1 opracowania.
- 2026-11-02: Identyfikatory w kodzie po angielsku, komentarze i wydruki po polsku, wartości atrybutów zagadki po polsku (PR #3).
- 2026-11-03: Więzy jako nazwane funkcje, bez lambd — W1 i W8 używają `in_first_house` i `in_middle_house` (prośba właściciela, PR #4).
- 2026-11-07: Wydruk macierzy w terminalu jako tabela z ramką zamiast surowej tabeli Markdown — czytelna przy demonstracji na żywo w Teams; tabela Markdown zostaje w sekcji 4 opracowania (prośba właściciela).

## Otwarte problemy
- (brak)
