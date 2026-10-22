# Laborator: funcții, metode și importuri pe web
# Student: Tîltu Daniel

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # Prevenirea blocajelor infinite la nivel de socket (ex. 27)

# Executarea unei cereri unice pentru optimizarea numărului de request-uri către server
response = requests.get(BASE_URL, timeout=TIMEOUT)
time.sleep(1) # Pauză conform bunelor practici (ex. 10)

# ==========================================
# Exercițiul 9: Elementele de bază ale răspunsului
# ==========================================
print("--- Exercițiul 9 ---")
# Diferența esențială: acestea sunt atribute de date, nu metode invocabile
print("Status code:", response.status_code) # Returnează un int
print("Este OK?:", response.ok)             # Returnează un bool (True pentru status 200-399)
print("URL:", response.url)                 # Returnează un string (URL final)
print("Encoding:", response.encoding)       # Returnează un string (ex. utf-8)

# ==========================================
# Exercițiul 10: Tratarea erorilor cu o metodă
# ==========================================
print("\n--- Exercițiul 10 ---")
# Nu va face nimic pe o pagină validă
response.raise_for_status() 

try:
    bad_response = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    # Metoda raise_for_status() aruncă o excepție dacă codul HTTP este 4xx sau 5xx
    bad_response.raise_for_status() 
except requests.HTTPError:
    print("Pagina nu a fost găsită (Eroare HTTP).")

time.sleep(1)

# ==========================================
# Exercițiul 11: Toate antetele
# ==========================================
print("\n--- Exercițiul 11 ---")
# response.headers este un obiect dict-like special definit de requests
for nume, valoare in response.headers.items():
    print(f"{nume}: {valoare}")

# ==========================================
# Exercițiul 12: Metode de dicționar
# ==========================================
print("\n--- Exercițiul 12 ---")
print("Server:", response.headers.get("Server", "lipsește"))
print("Content-Type:", response.headers.get("Content-Type", "lipsește"))
print("content-type (litere mici):", response.headers.get("content-type", "lipsește"))
# EXPLICAȚIE (cerință laborator): Dict-ul response.headers ignoră case-ul (este case-insensitive)
# conform RFC-urilor HTTP unde antetele sunt case-insensitive.

# ==========================================
# Exercițiul 13: Înlănțuirea metodelor de șir
# ==========================================
print("\n--- Exercițiul 13 ---")
aparitii_cyber = response.text.lower().count("cyber")
print(f"Cuvântul 'cyber' apare de: {aparitii_cyber} ori")
# EXPLICAȚIE (cerință laborator): Înlănțuirea (chaining) este posibilă pentru că `lower()` 
# returnează un nou obiect string, pe care se poate apela imediat metoda `count()`.

# ==========================================
# Exercițiul 14: Găsirea titlului
# ==========================================
print("\n--- Exercițiul 14 ---")
html = response.text
# Parsare simplă prin calcul de indici, fără expresii regulate sau BeautifulSoup
start = html.find("<title>") + len("<title>")
end = html.find("</title>")
titlu = html[start:end].strip()
print("Titlul paginii este:", titlu)

# ==========================================
# Exercițiul 15: Numărarea liniilor
# ==========================================
print("\n--- Exercițiul 15 ---")
# splitlines() împarte un șir multilinie într-o listă de șiruri
linii = html.splitlines()
print("Numărul total de linii HTML:", len(linii))
# Folosim funcția built-in `max` furnizând `len` drept funcție cheie de evaluare
cea_mai_lunga = max(linii, key=len)
print("Lungimea celei mai lungi linii:", len(cea_mai_lunga))

# ==========================================
# Exercițiul 16: Verificarea HTTPS
# ==========================================
print("\n--- Exercițiul 16 ---")
if response.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")

# ==========================================
# Exercițiul 17: Urmărirea redirecționărilor
# ==========================================
print("\n--- Exercițiul 17 ---")
response_http = requests.get("http://cybercor.org", timeout=TIMEOUT)
# Istoricul reține obiecte Response pentru cererile intermediare
for resp in response_http.history:
    print(f"Redirecționare: {resp.status_code} -> {resp.url}")
print("URL-ul final după redirecționare:", response_http.url)

time.sleep(1)

# ==========================================
# Exercițiul 18: HEAD versus GET
# ==========================================
print("\n--- Exercițiul 18 ---")
response_head = requests.head(BASE_URL, timeout=TIMEOUT)
time.sleep(1)
response_get = requests.get(BASE_URL, timeout=TIMEOUT)

print("Lungime conținut HEAD:", len(response_head.content))
print("Lungime conținut GET:", len(response_get.content))
# EXPLICAȚIE (cerință laborator): Metoda HEAD solicită strict metadatele (headers), 
# rezultând un body gol (0 bytes). GET cere datele complete (inclusiv body-ul).

time.sleep(1)

# ==========================================
# Exercițiul 19: Cookie-uri
# ==========================================
print("\n--- Exercițiul 19 ---")
# Obiectul response.cookies conține instanțe de Cookie
if response.cookies:
    for cookie in response.cookies:
        print(f"Cookie nume: {cookie.name}, Secure: {cookie.secure}")
else:
    print("Niciun cookie setat")

# ==========================================
# Exercițiul 20: Sesiuni
# ==========================================
print("\n--- Exercițiul 20 ---")
# Menținerea stării (stateful) spre deosebire de cererile statice de mai sus
sesiune = requests.Session()
sesiune.headers.update({"User-Agent": "WebLab-Tîltu_Daniel"})

response_sesiune = sesiune.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print("Rezultat de la ECHO_URL:\n", response_sesiune.text)

# RĂSPUNS VERIFICAȚI-VĂ:
# `response.text` este un atribut static descărcat de la început, reprezentând textul brut.
# `response.json()` este o metodă (necesită paranteze) deoarece declanșează execuția 
# logică a unui parser intern care citește și mapează string-ul într-un dicționar valid.