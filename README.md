# Pacman Reinforcement Learning
## Opis projektu
Ten projekt to implementacja gry Pacman z wykorzystaniem uczenia ze wzmocnieniem (Reinforcement Learning). Celem projektu jest nauczenie Pacmana poruszania się po planszy i unikania duchów.
## Instalacja i uruchomienie
1. Sklonuj repozytorium: `git clone https:                                                                       
2. Zainstaluj wymagane biblioteki: `pip install pygame`
3. Uruchom trening: `python -m train.train`
## Trening
Trening Pacmana odbywa się w kilku etapach:
* Początkowo Pacman uczy się poruszania po planszy bez duchów.
* Następnie Pacman uczy się unikania jednego ducha.
## Wyniki
Oto przykład działania Pacmana po treningu:
<img src="https://github.com/user-attachments/assets/35a35ea0-caf7-4460-9a5b-767eabe92253" width="200" height="300">
## Uwagi
* Projekt jest w trakcie rozwoju i może być podatny na błędy.
* Na razie najlepszy z modeli `pacman_ai_ep2600.keras` z folderu `models4` działa najlpiej ale jest on w stanie przejść tylko jeden raz całą planszę, potem się myli 
## Licencja
Projekt jest udostępniony na licencji MIT.
