# Pacman Reinforcement Learning
## Opis projektu
Ten projekt to implementacja gry Pacman z wykorzystaniem uczenia ze wzmocnieniem (Reinforcement Learning). Celem projektu jest nauczenie Pacmana poruszania się po planszy i unikania duchów.
## Instalacja i uruchomienie
1. Sklonuj repozytorium: `git clone`
```bash
git clone git@github.com:Nicram123/pacman_Reinforcement_Learning.git
```                                                                      
3. Zainstaluj wymagane biblioteki:
```bash
pip install pygame
```
5. Uruchom trening:
```bash
python -m train.train
```
lub skorzystaj z gotowych modeli w folderze `model4`
7. Uruchom program z poziomu `main.py`
```bash
python main.py
```
## Trening
Trening Pacmana odbywa się w kilku etapach:
* Początkowo Pacman uczy się poruszania po planszy bez duchów.
* Następnie Pacman uczy się unikania jednego ducha.
## Wyniki po treningu 
![pacman3](https://github.com/user-attachments/assets/e68fb6af-75e8-4df3-90ab-b17b12ffea26)
## Uwagi
* Projekt jest w trakcie rozwoju i może być podatny na błędy.
* Na razie najlepszy z modeli `pacman_ai_ep2600.keras` z folderu `models4` działa najlpiej ale jest on w stanie przejść tylko jeden raz całą planszę, potem się myli 

