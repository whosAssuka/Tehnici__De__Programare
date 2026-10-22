# Laborator: funcții, metode și importuri pe web
# Student: Tîltu Daniel

import time
import requests
import urllib.request

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# ==========================================
# Exercițiul 1: Primul import
# ==========================================
print("Ex 1: Versiune requests:", requests.__version__)
# EXPLICAȚIE: `requests` a avut nevoie de `pip install` pentru că este o bibliotecă externă (third-party),
# dezvoltată de comunitate, în timp ce `urllib` face parte din biblioteca standard Python (vine preinstalat).

# ==========================================
# Exercițiul 2: Două stiluri de import
# ==========================================
response_1 = requests.get(BASE_URL, timeout=TIMEOUT)
print(f"Ex 2 (requests.get): Cod de stare {response_1.status_code}")

from requests import get
response_2 = get(BASE_URL, timeout=TIMEOUT)
print(f"Ex 2 (import get): Cod de stare {response_2.status_code}")
# EXPLICAȚIE: 
# Avantaj `import requests`: Evită coliziunile de nume (știm clar că `get` e din `requests`).
# Avantaj `from requests import get`: Codul devine mai scurt și mai rapid de scris dacă folosim funcția des.

time.sleep(1) # Pauză obligatorie conform regulilor

# ==========================================
# Exercițiul 3: Alias-uri
# ==========================================
import requests as rq
response_3 = rq.get(BASE_URL, timeout=TIMEOUT)
print(f"Ex 3: Cod de stare prin alias {response_3.status_code}")
# EXPLICAȚIE: Un alias face codul mai ușor de citit când numele modulului este foarte lung (ex: `import matplotlib.pyplot as plt`).
# Îl face mai greu de citit dacă alias-ul este obscur sau neconvențional, derutând alți programatori.

time.sleep(1)

# ==========================================
# Exercițiul 4: Doar biblioteca standard
# ==========================================
response_urllib = urllib.request.urlopen(BASE_URL, timeout=TIMEOUT)
print(f"Ex 4: Status urllib: {response_urllib.status}")
corp_pagina = response_urllib.read().decode("utf-8")
print(f"Ex 4: Primele 200 caractere:\n{corp_pagina[:200]}\n")
# EXPLICAȚIE: .read() aduce datele brute (bytes). .decode("utf-8") le traduce în text citibil, folosind standardul de codare web.

time.sleep(1)

# ==========================================
# Exercițiul 5: Priviți în interiorul unui modul
# ==========================================
# print(dir(requests)) # Decomentează pentru a vedea toată lista
# EXPLICAȚIE PENTRU 3 NUME DIN LISTĂ:
# 1. 'get' - este o funcție (metodă ajutătoare pentru cereri GET).
# 2. 'Session' - este o clasă (permite menținerea persistenței datelor, cum ar fi cookie-urile).
# 3. 'exceptions' - este un modul (conține tipurile de erori specifice requests, ex: Timeout).

# ==========================================
# Exercițiul 6: Citiți documentația
# ==========================================
# help(requests.get) # Decomentează pentru a citi manualul funcției
# EXPLICAȚIE: Am folosit deja parametrul `timeout=TIMEOUT` în cererile de mai sus, exact cum cere documentația pentru a preveni blocajele.

# ==========================================
# Exercițiul 7: Cronometrarea unei cereri
# ==========================================
start_time = time.perf_counter()
response_chrono = requests.get(BASE_URL, timeout=TIMEOUT)
end_time = time.perf_counter()

timp_masurat = end_time - start_time
timp_raportat = response_chrono.elapsed.total_seconds()

print(f"Ex 7: Timp măsurat manual: {timp_masurat:.4f} secunde")
print(f"Ex 7: Timp raportat de requests: {timp_raportat:.4f} secunde")
# EXPLICAȚIE: time.perf_counter() măsoară tot timpul de execuție al scriptului pentru acea linie (inclusiv procesarea Python), 
# pe când response.elapsed măsoară strict timpul din momentul trimiterii cererii HTTP până la primirea primilor octeți.

# ==========================================
# Exercițiul 8: Când un import eșuează
# ==========================================
try:
    import bs4
    print("Ex 8: bs4 este instalat!")
except ImportError:
    print("Ex 8: Instalați modulul cu: pip install beautifulsoup4")
# EXPLICAȚIE DIFERENȚE:
# - Modul: Un singur fișier .py.
# - Pachet: Un folder cu mai multe module (fișiere .py) și un fișier __init__.py.
# - Bibliotecă: Un termen generic pentru o colecție de pachete/module complexe menite să rezolve un domeniu larg (ex: requests).