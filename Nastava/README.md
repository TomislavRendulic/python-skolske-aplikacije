# StudyOS - Interaktivna Aplikacija za Učenje i Testiranje

**StudyOS** je desktop aplikacija razvijena u Python-u sa Tkinter GUI interfejsom, namenjena vođenom učenju, savladavanju gradiva i samostalnoj proveri znanja kroz interaktivne testove.

Aplikacija je dizajnirana sa potpunim fokusom na učenje i pratećim modulima za praćenje napretka.

---

## 🚀 Funkcionalnosti

- **Podrška za više predmeta:**
  - `CS100` – Uvod u programiranje
  - `MA120` – Linearna algebra
  - `NT110` – Poslovna komunikacija
  - `NT111` – Engleski 1
  - `SE101` – Inženjerstvo Softvera

- **Raznovrsni tipovi testova i lekcija:**
  - **Teorijsko gradivo:** Pregled lekcija sa strukturisanim tekstom, podvučenim i boldovanim stavkama.
  - **Pitanja sa višestrukim izborom (Multi-choice):** Trenutna evaluacija tačnosti odgovora.
  - **Pitanja Tačno/Netačno:** Brza provera razumevanja koncepata.
  - **Pitanja sa dopunjavanjem:** Interaktivna polja za unos rešenja.
  - **Povezivanje pojmova:** Uparivanje leve i desne kolone odgovora.
  - **Kategorizacija i Sortiranje:** Razvrstavanje pojmova po odgovarajućim kategorijama.
  - **Redosled koraka:** Poredak procesa i logičkih celina.

- **Dodatne mogućnosti:**
  - **Automatsko čuvanje napretka:** Pamćenje poslednje pređene strane/lekcije po predmetu u `study_os_data.json`.
  - **Dinamičko učitavanje sadržaja:** Sva pitanja i lekcije se učitavaju eksternom JSON strukturom (`lekcije.json`).
  - **Anti-Distraction Mehanizam:** Motivaciona ekran-kazna sa potvrdom izlaska kucanjem teksta.

---

## 🛠️ Tehnologije

- **Python 3.x**
- **Tkinter** (GUI interfejs)
- **Pillow (PIL)** (Obrada i prilagođavanje slika)

---

## 📦 Instalacija i Pokretanje

Pokrenite sledeće komande u terminalu:

```bash
git clone https://github.com/TomislavRendulic/python-skolske-aplikacije.git
cd python-skolske-aplikacije/Nastava
pip install Pillow
python Nastava5.py
