
# Dokumentacja użytkowa projektu sound-visualizer
Wizualizacja muzyki w czasie rzeczywistym przy wykorzystaniu Raspberry Pi i Pythona
TO JEST SUPER WSTĘP XD

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
 ```
sudo apt-get install alsa-utils
```

## Instalacja dodatkowych bibliotek pythona
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
2. Rozluźnij się xD
3. Uruchom wizualizację
## Uruchomienie wizualizacji
Uruchom program [visualizer.py](https://github.com/jasieksz/sound-visualizer/blob/master/visualizer.py) wykonując w terminalu komendę :
 ```python visualizer.py```
Otworzy się okno aplikacji .... i coś fajnego się stanie
## Ustawienia i zmiana trybu wizualizacji
nanananananan podaj odpowiednie opcje
``` python visualizer.py -visualiztionId=1 -time=100```

# Podsumowanie
Jeżeli napotkasz problemy z sprzętem lub oprogramowaniem [otwórz nowy issue](https://github.com/jasieksz/sound-visualizer/issues).