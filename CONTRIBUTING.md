# Zasady pracy z repozytorium

Zasady dotyczą **wszystkich plików i katalogów w repozytorium** — kodu, skryptów, konfiguracji,
CI i dokumentacji (`README.md`, `CLAUDE.md`, `NOW.md`, ten plik). Nie ma wyjątków dla „drobnych”
zmian ani dla samej dokumentacji.

## Najważniejsze

1. **Nie commituj i nie pushuj bezpośrednio do `main`.**
2. Każda zmiana powstaje na **nowej gałęzi** odgałęzionej od aktualnego `main`.
3. Do `main` zmiana trafia wyłącznie przez **Pull Request** na Gitei. PR recenzuje tester
   (`ai-tester`), a scala wyłącznie właściciel repozytorium (Roland Liedtke) — po zatwierdzeniu
   przez testera. Agenci AI nie scalają PR-ów.
4. Jeśli repo ma CI — PR scalamy tylko przy **zielonym CI**.

`main` jest jedyną gałęzią stałą i zawsze jest w stanie gotowym do wdrożenia.

## Jak zacząć zmianę

```bash
git switch main
git pull --ff-only
git switch -c feat/krotki-opis    # prefiks wg tabeli niżej
# … zmiany …
.venv/bin/python einstein_solver.py   # solver musi zwrócić 1 rozwiązanie
git commit -m "Dodaj …"
```

Pull Request tworzymy pushem AGit — gałąź robocza nie trafia na serwer, Gitea zakłada z pusha PR:

```bash
T=$(printf '%s' "Tytuł PR" | base64 -w0)
D=$(printf '%s\n' "Opis PR (markdown)" | base64 -w0)
git push origin HEAD:refs/for/main -o topic=feat/krotki-opis \
  -o "title={base64}$T" -o "description={base64}$D"
```

Kolejny push z tym samym `topic` dodaje commity do istniejącego PR (tytułu i opisu nie zmienia).
Można też pracować ręcznie:
`git push -u origin <gałąź>` i otworzyć PR w WWW Gitei.

## Nazwy gałęzi

Format: `<typ>/<krótki-opis>` — opis po polsku, małymi literami, słowa rozdzielone `-`,
**bez polskich znaków**.

| Prefiks     | Kiedy                                            | Przykład                 |
| ----------- | ------------------------------------------------ | ------------------------ |
| `feat/`     | nowa funkcja                                     | `feat/eksport-csv`       |
| `fix/`      | poprawka błędu                                   | `fix/pusty-formularz`    |
| `docs/`     | dokumentacja: README, CLAUDE.md, NOW.md, ten plik | `docs/opis-wdrozenia`   |
| `chore/`    | zależności, konfiguracja narzędzi, porządki      | `chore/aktualizacja-zaleznosci` |
| `refactor/` | przebudowa kodu bez zmian zachowania             | `refactor/podzial-modulu`|
| `test/`     | same testy, bez zmian zachowania                 | `test/przypadki-brzegowe`|

## Podział pracy na gałęzie

- **Jedna gałąź = jedna logiczna zmiana = jeden PR.**
- **Gałęzie są krótkie** — od kilku godzin do kilku dni; długo żyjące gałęzie (`develop`) nie są potrzebne.
- **Aktualizacje zależności major** — każda w osobnym `chore/` PR.
- **Gałęzie zależne:** jeśli PR wymaga innego, niescalonego PR-a, napisz to w opisie
  („scalać po #N”) albo poczekaj na scalenie poprzedniego.
- **Po scaleniu** usuń gałąź lokalnie (`git branch -d <gałąź>`); gałąź wypchniętą ręcznie usuń też na serwerze.
- **Wersje** oznaczamy tagami na `main` (`v1.0.0`), nie gałęziami.

## Commity i Pull Requesty

- Opisy commitów po polsku, w trybie rozkazującym: „Dodaj…”, „Popraw…”, „Usuń…”.
- Tytuł PR jak tytuł commita; w opisie: co i dlaczego, jak sprawdzono, na co zwrócić uwagę.
- Przed wypchnięciem: `.venv/bin/python einstein_solver.py`; po zmianie solvera zaktualizuj sekcje 3 i 4 w `einstein_solution_presentation.md`.
