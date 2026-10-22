# Laborator: funcții, metode și importuri pe web
# Student: Tîltu Daniel

import time
import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

# ==========================================
# Exercițiile 21 & 23: Prima funcție și parametri impliciți
# ==========================================
# Folosim `timeout=10` ca argument implicit. Dacă funcția este apelată doar cu URL, 
# va aștepta maxim 10 secunde. Această valoare poate fi suprascrisă la apelare.
def fetch(url, timeout=10):
    """Returnează obiectul răspuns pentru URL-ul dat."""
    return requests.get(url, timeout=timeout)

print("--- Exercițiile 21 & 23 ---")
print("Status Ex 21:", fetch(BASE_URL).status_code)
time.sleep(1)
print("Status Ex 23 (implicit):", fetch(BASE_URL).status_code)
time.sleep(1)
print("Status Ex 23 (timeout=3):", fetch(BASE_URL, timeout=3).status_code)
time.sleep(1)

# ==========================================
# Exercițiile 22 & 26: Funcții simple și adnotări de tip
# ==========================================
# Adnotările `url: str` și `-> int` (Type Hints) nu forțează tipul la rulare în Python, 
# ci servesc ca documentație pentru programator și pentru mediul de dezvoltare (IDE).
def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = fetch(url)
    return response.status_code

print("\n--- Exercițiul 22 ---")
for path in ["", "/robots.txt", "/sitemap.xml"]:
    print(f"Status pentru {path}:", get_status(BASE_URL + path))
    time.sleep(1)

print("\n--- Exercițiul 26 ---")
try:
    get_status(123)
except Exception as e:
    print("Eroare la apelarea cu 123:", type(e).__name__)
# EXPLICAȚIE (cerință laborator): Deoarece Python are tipizare dinamică, adnotările nu opresc
# execuția. Eroarea `MissingSchema` apare abia în interiorul modulului `requests`, care 
# așteaptă un șir de caractere valid (cu "http://"), nu un număr întreg.

# ==========================================
# Exercițiile 24 & 25: Extragere titlu și Docstring-uri
# ==========================================
def get_title(html: str) -> str:
    """Extrage titlul dintr-un document HTML."""
    start = html.find("<title>")
    if start == -1:
        return "Fără titlu"
    start += len("<title>")
    end = html.find("</title>")
    return html[start:end].strip()

print("\n--- Exercițiile 24 & 25 ---")
html_test = fetch(BASE_URL).text
print("Titlu:", get_title(html_test))
# Funcția built-in help() citește primul șir de caractere (docstring) din definiția funcției.
help(get_title)  
time.sleep(1)

# ==========================================
# Exercițiul 27: Fără opriri neașteptate
# ==========================================
def page_exists(url: str) -> bool:
    """Verifică dacă o pagină poate fi descărcată fără erori."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return True
    # Prindem excepția generală RequestException pentru a acoperi timeout-uri, erori DNS etc.
    except requests.RequestException:
        return False

print("\n--- Exercițiul 27 ---")
print("Există pagina validă?:", page_exists(BASE_URL))
time.sleep(1)
print("Există pagina invalidă?:", page_exists("https://this-domain-does-not-exist.invalid"))

# ==========================================
# Exercițiul 28: Returnarea unui dicționar
# ==========================================
def check_paths(base: str, paths: list) -> dict:
    """Verifică o listă de căi și returnează un dicționar cu codurile de stare."""
    rezultate = {}
    for path in paths:
        # Folosim dicționarul pentru a mapa fiecare cale (cheia) la codul ei HTTP (valoarea)
        rezultate[path] = get_status(base + path)
        time.sleep(1)
    return rezultate

print("\n--- Exercițiul 28 ---")
print("Căi verificate:", check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

# ==========================================
# Exercițiul 29: Argumente cu nume
# ==========================================
def get_header(url: str, name: str, default: str = "lipsește") -> str:
    """Afișează valoarea unui singur antet HTTP."""
    resp = fetch(url)
    return resp.headers.get(name, default)

print("\n--- Exercițiul 29 ---")
print("Server:", get_header(BASE_URL, name="Server"))
time.sleep(1)

# ==========================================
# Exercițiile 30 & 31: Antete de securitate și funcții înlănțuite
# ==========================================
def security_headers(url: str) -> dict:
    """Verifică prezența a 5 antete de securitate importante."""
    antete_cautate = [
        "Strict-Transport-Security", "Content-Security-Policy",
        "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"
    ]
    resp = fetch(url)
    # Folosim o expresie de verificare directă: `antet in resp.headers` care returnează boolean
    return {antet: (antet in resp.headers) for antet in antete_cautate}

def score_headers(results: dict) -> str:
    """Calculează un scor de tip '3/5' pe baza antetelor găsite."""
    # În Python, True este echivalent cu 1 matematic. Astfel, funcția sum() adună valorile True.
    gasite = sum(results.values())
    total = len(results)
    return f"{gasite}/{total}"

print("\n--- Exercițiile 30 & 31 ---")
rezultat_securitate = security_headers(BASE_URL)
print("Analiză securitate:", rezultat_securitate)
print("Scor final:", score_headers(rezultat_securitate))
time.sleep(1)

# ==========================================
# Exercițiul 32: Două funcții, o sarcină
# ==========================================
# Este o bună practică de programare (Separation of Concerns) să nu amestecăm 
# descărcarea datelor (I/O) cu procesarea lor (parsare).
def fetch_robots(base: str):
    """Descarcă și returnează textul din /robots.txt."""
    resp = requests.get(base + "/robots.txt", timeout=TIMEOUT)
    return resp.text if resp.status_code == 200 else None

def disallowed_paths(robots_text: str) -> list:
    """Extrage căile interzise din conținutul fișierului robots.txt."""
    if not robots_text:
        return []
    
    interzise = []
    for linie in robots_text.splitlines():
        if linie.startswith("Disallow:"):
            # Împărțim linia strict de la primul separator ":" găsit
            cale = linie.split(":", 1)[1].strip()
            interzise.append(cale)
    return interzise

print("\n--- Exercițiul 32 ---")
text_robots = fetch_robots(BASE_URL)
print("Căi blocate găsite:", disallowed_paths(text_robots))
time.sleep(1)

# ==========================================
# Exercițiul 33: Oricâte argumente (*args)
# ==========================================
def response_times(*urls):
    """Returnează un dicționar cu timpul de răspuns pentru mai multe URL-uri."""
    timpi = {}
    # Operatorul * colectează toate argumentele poziționale oferite într-un tuplu numit `urls`
    for url in urls:
        start = time.perf_counter()
        requests.get(url, timeout=TIMEOUT)
        timpi[url] = round(time.perf_counter() - start, 4)
        time.sleep(1)
    return timpi

print("\n--- Exercițiul 33 ---")
print("Timpi de răspuns:", response_times(BASE_URL, "https://cybercor.org/robots.txt"))

# ==========================================
# Exercițiul 34: Argumente cu nume colectate (**kwargs)
# ==========================================
def log(message, **details):
    """Afișează un mesaj însoțit de detalii suplimentare."""
    rezultat = message
    # Operatorul ** ambalează argumentele keyword suplimentare într-un dicționar
    for cheie, valoare in details.items():
        rezultat += f" | {cheie}={valoare}"
    print(rezultat)

print("\n--- Exercițiul 34 ---")
log("verificat", url=BASE_URL, status=200)

# RĂSPUNS VERIFICAȚI-VĂ (Partea 3):
# print() direcționează o valoare strict către standard output (ecran), fiind invizibilă pentru restul programului.
# return finalizează execuția funcției și trimite o valoare înapoi în cod, permițând salvarea în variabile și evaluări matematice/logice viitoare.