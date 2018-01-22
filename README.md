

# Dokumentacja użytkowa projektu sound-visualizer
Wizualizacja muzyki w czasie rzeczywistym przy wykorzystaniu Raspberry Pi i Pythona

![sound-visualizer](https://github.com/jasieksz/sound-visualizer/blob/master/resources/example_gif.gif)

# Wymagania sprzętowe i technologiczne
## Sprzęt
- [Raspberry Pi 3](https://www.raspberrypi.org/products/)
- Źródło zasilania 5V
- Odpowiednie urządzenia peryferyjne (monitor, klawiatura, etc.)
- Interfejs dźwiękowy
- Mikrofon

## Oprogramowanie
- System operacyjny  [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)
- Python 3.5 lub nowszy
- Git (opcjonalne)

# Instalacja oprogramowania
## Instalacja programu
1. Stwórz folder do którego ściągniesz program
2. W terminalu wykonaj komendę  ``` git clone https://github.com/jasieksz/sound-visualizer.git ```
3.  Alternatywnie pobierz [archiwum programu](https://github.com/jasieksz/sound-visualizer)

## Instalacja dodatkowych modułów dla Raspberry Pi
- [Alsa](http://blog.scphillips.com/posts/2013/01/sound-configuration-on-raspberry-pi-with-alsa/)  (zainstalowane domyślnie z systemem)

W terminalu wykonaj komendę :
```
sudo apt-get install alsa-utils
```

## Instalacja dodatkowych bibliotek pythona
W terminalu wykonaj komendy :
```
sudo apt-get update
sudo apt-get install python-numpy python-scipy python-pyaudio
sudo apt-get install python-pyqtgraph
```
# Konfiguracja i test sprzętu
## Konfiguracja urządzenia dźwiękowego
1. Menu start
2. Audio settings
3. Należy z listy wybrać podłączone urządzenie (mikrofon) i zaznaczyć jako domyślne
4. Jeżeli powyższe kroki nie przyniosły oczekiwanego rezultatu
[alternatywna konfiguracja urządzenia dźwiękowego](https://www.linuxcircle.com/2013/05/08/raspberry-pi-microphone-setup-with-usb-sound-card/)

## Test urządzenia dźwiękowego
- Korzystając z interfejsu graficznego
	1. Uruchom program audacity
	2. Wybierz podłączone urządzenie z listy
	3. Spróbuj nagrać próbkę dźwięku
- Korzystając z terminala
	1. W terminalu uruchom ```$ arecord -D plughw:1,0 -f cd test.wav```
	2. Następnie sprawdź nagranie ``` $ aplay test.wav```
	
# Obsługa aplikacji
Kiedy poprawnie skonfigurujesz sprzęt i system. 
1. Odtwórz swoją ulubioną płytę
2. Uruchom wizualizację
## Uruchomienie wizualizacji
Uruchom program [visualizer.py](https://github.com/jasieksz/sound-visualizer/blob/master/visualizer.py) wykonując w terminalu komendę :

```python visualizer.py```

Otworzy się okno aplikacji, w dalszych krokach możesz ustawić dodatkowe opcje
## Ustawienia i zmiana trybu wizualizacji
Podaj odpowiednie opcje

``` python visualizer.py -visualiztionId=1 -time=100 -signal=True -spectrum=True```

time jest to okres czasu działania programu w sekundach

### Dostępne tryby wizualizacji
- należy wybrać opcję signal=True

![sygnał](https://github.com/jasieksz/sound-visualizer/blob/master/resources/signal_example.PNG)

- należy wybrać opcję spectrum=True

![spektrum](https://github.com/jasieksz/sound-visualizer/blob/master/resources/specturm_example.PNG)

- należy wybrać opcję visualizationId=1 

![wizualizacja 1](https://github.com/jasieksz/sound-visualizer/blob/master/resources/vis1_example.PNG)

- należy wybrać opcję visualizationId=2 

![wizualizacja 2](https://github.com/jasieksz/sound-visualizer/blob/master/resources/vis2_example.PNG)

# Podsumowanie
Jeżeli napotkasz problemy z sprzętem lub oprogramowaniem [otwórz nowy issue](https://github.com/jasieksz/sound-visualizer/issues).
