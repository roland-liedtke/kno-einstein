# kno-einstein

## Cel
Projekt KNO nr 1 („reprezentacja symboliczna”): rozwiązanie Zagadki Einsteina
(treść: https://www.math.edu.pl/zagadka-einsteina) jako problemu CSP oraz materiał
na prezentację w Teams.

## Stack
- Python 3.13, biblioteka `python-constraint2` (API `from constraint import ...`).
- Systemowy `pip` (python3-pip) jest dostępny, ale `ensurepip` nie (brak `python3-venv`), więc venv
  powstaje bez pipa — pakiety instaluje się do niego systemowym pipem przez `--python`.

## Struktura
- `einstein_solver.py` — model CSP (zmienne = atrybuty, dziedzina = numery domów 1–5),
  15 wskazówek jako więzy `# W1`…`# W15`, wydruk macierzy i odpowiedzi.
- `einstein_solution_presentation.md` — opracowanie: teoria, model logiczny, kod, wyniki,
  scenariusz Teams. Sekcje 3 i 4 zawierają kopię kodu i rzeczywistego wyniku solvera.
- `requirements.txt` — zależności.

## Komendy
```bash
python3 -m venv --without-pip .venv
pip --python .venv/bin/python install -r requirements.txt
.venv/bin/python einstein_solver.py
```

## Konwencje
- Identyfikatory i komentarze po polsku (bez zmiany stylu w istniejącym kodzie).
- Po każdej zmianie `einstein_solver.py` zaktualizuj sekcje 3 i 4 w
  `einstein_solution_presentation.md` (kod 1:1 i wynik z faktycznego uruchomienia).
- Każdą zmianę commituj i pushuj na Giteę (`origin` = `gitea@192.168.11.52:ai-agent/kno-einstein.git`).
