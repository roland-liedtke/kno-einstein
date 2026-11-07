# kno-einstein

## Cel
Projekt KNO nr 1 („reprezentacja symboliczna”): rozwiązanie Zagadki Einsteina
(treść: https://www.math.edu.pl/zagadka-einsteina) jako problemu CSP oraz materiał
na prezentację w Teams.

## Stack
- Python 3.13, biblioteka `python-constraint2` (API `from constraint import ...`).
- Zależności instaluj tylko w `.venv` (w systemie są `python3-pip` i `python3-venv`, venv ma własny pip).

## Struktura
- `einstein_solver.py` — model CSP (zmienne = atrybuty, dziedzina = numery domów 1–5),
  15 wskazówek jako więzy `# W1`…`# W15`, wydruk macierzy (tabela z ramką do terminala) i odpowiedzi.
- `test_einstein_solver.py` — testy `unittest`: jednoznaczność rozwiązania, odpowiedź, układ tabeli.
- `einstein_solution_presentation.md` — opracowanie: teoria, model logiczny, kod, wyniki,
  scenariusz Teams. Sekcje 3 i 4 zawierają kopię kodu i rzeczywistego wyniku solvera.
- `requirements.txt` — zależności.

## Komendy
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python einstein_solver.py
.venv/bin/python -m unittest -v    # testy
```

## Konwencje
- Identyfikatory (zmienne, funkcje, stałe) po angielsku; komentarze, docstringi i teksty
  wypisywane przez solver po polsku (opracowanie jest po polsku). Wartości atrybutów
  (np. `"Norweg"`, `"Rybki"`) to dane zagadki — zostają po polsku.
- Po każdej zmianie `einstein_solver.py` zaktualizuj sekcje 3 i 4 w
  `einstein_solution_presentation.md` (kod 1:1 i wynik z faktycznego uruchomienia).

## Git
- Remote: `gitea@192.168.11.52:konfiguracje.online/kno-einstein.git` (organizacja `konfiguracje.online`).
- Gałąź główna: `main` — nie commituj do niej bezpośrednio.
- **Zasady gałęzi i PR-ów są w `CONTRIBUTING.md`**: nowa gałąź od aktualnego `main`, nazwa `<typ>/<opis-bez-diakrytykow>`, jedna logiczna zmiana na PR.
- Każdą zmianę commituj i otwieraj Pull Request do `main` przez AGit flow (bez tokenu). PR-y recenzuje tester (`ai-tester`), a scala wyłącznie właściciel — agent ich nie scala.
```bash
T=$(printf '%s' "Tytuł PR" | base64 -w0)
D=$(printf '%s\n' "Opis PR (markdown)" | base64 -w0)
git push origin HEAD:refs/for/main -o topic=<nazwa-gałęzi> \
  -o "title={base64}$T" -o "description={base64}$D"
```
- Otwarte PR-y: `curl -s "http://192.168.11.52:3000/api/v1/repos/konfiguracje.online/kno-einstein/pulls?state=open"`.

## Stan projektu
@NOW.md
