# Edukativna Vežbaonica - Brojni Sistemi (RADIX)

Interaktivna desktop aplikacija razvijena u Python-u sa grafičkim korisničkim interfejsom (GUI) namenjena vežbanju i učenju konverzija između različitih brojnih sistema. Aplikacija ne traži samo konačno rešenje, već vodi korisnika kroz kompletan postupak i korak-po-korak radnu tabelu (sukcesivno deljenje, sabiranje stepena baze, grupisanje bitova).

## Funkcionalnosti

Aplikacija pokriva sledeće konverzije i formate:
- **Dekadni u Binarni** (korak-po-korak sukcesivno deljenje sa 2, unosi se količnik i ostatak)
- **Binarni u Dekadni** (izračunavanje vrednosti svakog bita i sumiranje)
- **Binarni u Oktalni** (grupisanje bitova u trijade)
- **Binarni u Heksadekadni** (grupisanje bitova u tetrade)
- **Pakovani BCD format** (konverzija cifara u 4-bitne BCD kodove)
- **Raspakovani BCD format** (konverzija cifara u 8-bitne BCD kodove)
- **Opšta RADIX konverzija** (nasumični zadaci za konverziju između baze 10 i bilo koje druge baze od 3 do 16 u oba smera)

## Tehnologije i Biblioteke

- **Python 3.x**
- **Tkinter / ttk** (ugrađena biblioteka za izradu grafičkog interfejsa)

## Kako pokrenuti aplikaciju

1. Uverite se da imate instaliran Python (verzija 3.6 ili novija).
2. Preuzmite repozitorijum ili fajl `kviz_brojni_sistemi2.py`.
3. Pokrenite aplikaciju iz terminala / komandne linije:
   ```bash
   python kviz_brojni_sistemi2.py

# Napredne Računarske Reprezentacije i IEEE 754 Standard

Interaktivna desktop aplikacija razvijena u Python-u za vežbanje i savladavanje tema iz oblasti računarskih sistema i digitalne elektronike. Aplikacija pruža dinamičke zadatke sa validacijom svakog koraka u radnom postupku u realnom vremenu.

## Moduli i Funkcionalnosti

Aplikacija obuhvata sledeće oblasti:
- **Raspakovani BCD format sa predznakom** (konverzija označenih brojeva u 8-bitne raspakovane BCD zapise sa definisanim zonama za predznak)
- **Prvi Komplement (1's Complement)** (inverzija bitova u zadatom binarnom nizu)
- **Drugi Komplement (2's Complement)** (korak-po-korak postupak: nalazak prvog komplementa i sukcesivno sabiranje sa +1 uz praćenje prenosa/carry bitova zdesna ulevo)
- **Predstavljanje sa Pomerajem (Offset Binary / Excess-K)** (izračunavanje pomeraja/bias-a $2^{m-1}$, računanje pomerene dekadne vrednosti i konverzija sukcesivnim deljenjem sa 2)
- **IEEE 754 Standardni Format (32-bitni Single Precision)** (kompletan postupak: određivanje bita znaka, konverzija celog i razlomljenog dela, izračunavanje i binarizacija pomerenog eksponenta, kao i formiranje normalizovane mantise)
- **IEEE 754 Specijalne Vrednosti** (konstruisanje specijanih bitovskih konfiguracija za nulu, pozitivnu beskonačnost i NaN - Not a Number)

## Tehnologije i Biblioteke

- **Python 3.x**
- **Tkinter / ttk** (grafički interfejs sa prilagođenim stilovima i scrollable platnom za kompleksne tabele)

## Kako pokrenuti aplikaciju

1. Uverite se da imate instaliran Python (verzija 3.6 ili novija).
2. Preuzmite repozitorijum ili fajl `CS120 2.py`.
3. Pokrenite aplikaciju iz terminala / komandne linije:
   ```bash
   python "CS120 2.py"

# Logička Minimizacija i BCD Sistemi

Desktop aplikacija razvijena u Python-u kao alat za brzu proveru i vežbanje osnovnih zadataka iz logičke minimizacije, Karnoovih mapa i BCD kodiranja.

## Moduli i Funkcionalnosti

Aplikacija pokriva tri tipična tipa zadataka sa prve lekcije:
- **Tip 1: Indeksi P skupa** (generisanje tablice istinitosti na osnovu datog P skupa minterma, prenos u Karnoovu mapu i minimizacija u DNF i KNF oblike)
- **Tip 2: PDNF u Tablicu i Minimizacija** (prevođenje savršene DNF forme u dekadne indekse na osnovu težina promenljivih A=8, B=4, C=2, D=1 i popunjavanje tablice/mape)
- **Tip 3: BCD Pakovani Sistem** (konverzija četvorocifrenih brojeva u 4-bitni BCD kod i minimizacija funkcije izlaza)

### Dodatne funkcije:
- **Validacija ulaza u realnom vremenu**: Provera tačnosti unosa tablice, BCD kodova i Karnoove mape sa vizuelnim obeležavanjem grešaka (zeleno/crveno).
- **Automatski vodič**: Mogućnost generisanja korak-po-korak objašnjenja i automatskog popunjavanja tačnih rešenja.

## Tehnologije

- **Python 3.x**
- **Tkinter** (GUI sa interaktivnom tabelom, Karnoovom mapom i prilagođenom temom)

## Kako pokrenuti aplikaciju

1. Uverite se da imate instaliran Python (3.6 ili noviji).
2. Pokrenite fajl `CS120 3.py` iz terminala ili komandne linije:
   ```bash
   python "CS120 3.py"
