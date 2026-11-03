# NOW

## Zrobione
- 2026-10-28: Założono repozytorium i `.venv` z `python-constraint2==2.9.0`.
- 2026-10-28: `einstein_solver.py` — model CSP, 15 więzów, sprawdzenie jednoznaczności; wynik: 1 rozwiązanie, rybki hoduje Niemiec (dom 4).
- 2026-10-28: Repozytorium wypchnięte na Giteę (`ai-agent/kno-einstein`).
- 2026-10-28: `einstein_solution_presentation.md` — sekcje 1–5 (teoria, model logiczny, kod, macierz wyników, scenariusz Teams).
- 2026-10-28: W systemie jest już `pip` 25.1.1 — instrukcje instalacji przestawione z `get-pip.py` na `pip --python .venv/bin/python` (`ensurepip` nadal brak).
- 2026-10-28: Doinstalowano `python3-venv` — `python3 -m venv` tworzy venv z pipem; instrukcje wrócone do standardowego `python3 -m venv .venv` + `.venv/bin/pip install`.
- 2026-10-28: Opracowanie, sekcja 3.1 — porównanie `python-constraint` (nierozwijany, ostatnio 1.4.0 z 2018) i `python-constraint2` (rozwijany przez społeczność, 2.9.0).
- 2026-10-30: Wprowadzono GitHub flow z PR-ami przez AGit: `CONTRIBUTING.md`, sekcja Git w `CLAUDE.md` (PR `docs/zasady-galezi`).
- 2026-11-01: Repozytorium przeniesione do organizacji `konfiguracje.online` (`konfiguracje.online/kno-einstein`); zaktualizowane ścieżki w `CLAUDE.md`.
- 2026-11-02: Identyfikatory w `einstein_solver.py` przemianowane na angielskie (np. `ten_sam_dom` → `same_house`, `KATEGORIE` → `CATEGORIES`); wynik solvera bez zmian, sekcja 3 opracowania zaktualizowana.
- 2026-11-03: Więzy unarne W1 i W8 jako nazwane funkcje `in_first_house` i `in_middle_house` zamiast lambd; wynik bez zmian, sekcja 3 opracowania (kod i tabela 3.2) zaktualizowana.

## W toku
- (brak)

## Dalej
- Ewentualnie: slajdy na podstawie sekcji 5, wariant solvera w z3 lub Prologu do porównania.
