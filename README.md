<!-- omit in toc -->
# finger-counter
Projekt na przedmiot "Przetwarzanie obrazu w Pythonie", Wydział Mechatroniki, 2021/22. Członkowie zespołu: [Mateusz Stryjek](https://github.com/mstryjek), [Maciej Klimek](https://github.com/MKlimek00), [Kamil Florek](https://github.com/phlorek).

<!-- omit in toc -->
## Spis treści
- [1. Założenia projektowe](#1-założenia-projektowe)
- [2. TODO](#2-todo)
- [3. Moduły](#3-moduły)
  - [a. main.py](#a-mainpy)
  - [b. imio.py](#b-imiopy)
  - [c. config.py](#c-configpy)
  - [d. visualizer.py](#d-visualizerpy)
- [4. Wizualizacje](#4-wizualizacje)

## 1. Założenia projektowe
Celem projektu jest utworzenie programu wyświetlającego na ekranie liczby palców u dłoni pokazywanych przez użytkownika. 
Ponadto projekt zakłada:
- Działanie na nagraniu lub obrazie z kamery ("na żywo")
- Wykorzystanie metod klasycznych przetwarzania obrazu do realizacji projektu
- Wykrywanie i separację dłoni (wraz z palcami) użytkownika
- Separację palców od dłoni oraz zliczanie ich liczby
- Wyświetlanie informacji użytkownikowi na ekranie, w tym liczbę palców oraz ich pozycje
- Prostotę dostosowania przez użytkownika programu do własnych potrzeb (jeden plik konfiguracyjny)
- Utworzenie wizualizacji każdego kroku działania programu, zarówno w celach demonstracyjnych jak diagnostycznych

## 2. TODO
- [ ] Nagrania testowe, min. 3x30s, najlepiej w różnych oświetleniach (MK)
- [X] Separacja obszarów odpowiadających skórze ludzkiej (MK/KF)
- [ ] Separacja dłoni z palcami od innych obszarów (np. twarzy) (MK/KF)
- [ ] Separacja palców od dłoni (KF/MK)
- [ ] Zliczanie palców (KF/MK)
- [ ] Wyznaczenie pozycji palców (KF/MK)
- [ ] Wyświetlanie informacji użytkownikowi (MS/MK)
- [ ] Dokumentacja projektu (na bieżąco) (MS)
- [ ] Wizualizacje końcowe (MS)
- [ ] Dodanie nazw do kroków wizualizacji (MS)
- [ ] Wizualizacje w README (MS)
- [X] Wizualizacje pośrednie (MS)
- [X] Ustalenie struktury modułów projektu (MS)
- [X] Plik konfiguracyjny + parser (MS)


## 3. Moduły
### a. [main.py](src/main.py)
Główny plik projektu. Uruchomienie programu odbywa się poprzez uruchomienie tego pliku:
```shell
python src/main.py
```

### b. [imio.py](src/imio.py)
Moduł odpowiadający za wczytywanie obrazów z kamery lub nagrania, a także za zapisywanie ich w postaci nagrania lub osobnych obrazów.

### c. [config.py](src/config.py)
Moduł odpowiadający za wczytywanie pliku konfiguracyjnego projektu do postaci używalnej przez klasy zdefiniowane w poszczególnych modułach. Pozwala na dostęp do elementów jak do pól.

### d. [visualizer.py](src/visualizer.py)
Moduł służący do wizualizacji pośrednich, w szczególności przy pracy nad projektem. Obecnie nie posiada metod do wizualizacji końcowej.


## 4. Wizualizacje
TODO
