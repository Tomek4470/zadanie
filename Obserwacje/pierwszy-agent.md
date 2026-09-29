# Mój pierwszy agent — karta obserwacji

- Narzędzie i model: Anti gravity / Claude Sonnet 4.6

- Moje zadanie (2–3 zdania): Generator haseł 

- Pierwsza wiadomość (wklejona co do znaku): 

Stwórz aplikację (nie html) która będzie generatorem haseł. 
Aplikacja ma pobierać od użytkownika ilość znaków które z których potem wygeneruje hasło. 
Po wygenerowaniu hasła ma pojawić się hasło z możliwością jego skopiowaniem oraz napisem " Twoje hasło to ..." 
Pracuj tylko w utworzonym katalogu 
Stwórz tyle plików ile będzie to konieczne 
Pod koniec stwórz plik README który zawiera informacje jak uruchomić aplikację


- Co agent zrobił najpierw: 
Najpierw sprawdził struktue katalogu roboczego
- O co pytał — i co zostało zatwierdzone bez czytania: 
Pytał o zatwierdzenie tylko przy run_command — czyli przy każdym uruchomieniu komendy w terminalu
Bez potrzeby potwierdzenia przeglądał folder, czytał pliki oraz przeszukiwał sieć.


- Pierwszy błąd i co agent z nim zrobił: 
Na początku agent niepoprawnie zrobił generator i nic nie działało jak powinno. Później zidentyfikował problemy i je poprawił
- Stan po 25 minutach: działa / częściowo / nie działa / nie wiem

Częściowo działa - robi główne zadanie, czyli generuje hasło (problemy wyłącznie wyglądowe)

- Skąd wiem, że aplikacja działa (co zostało sprawdzone): …
Uruchomiłem aplikację i kliknąłem przycisk "Generuj hasło". Aplikacja wygenerowała losowe hasło o wybranej przez mnie długości.

- Rzeczy, które agent zrobił, a których nie rozumiem: 
Nie rozumiem w pełni kodu pythona ale resztę działań jakie wykonał rozumiem.

- Jak mi się wydawało, że poszło (jedno zdanie): 
Okej.