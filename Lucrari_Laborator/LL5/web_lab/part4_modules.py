# Laborator: funcții, metode și importuri pe web
# Student: Tîltu Daniel

import time
import requests
import urllib.parse
import re
from html.parser import HTMLParser
import hashlib
import json
import socket
import ssl
from datetime import datetime

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

# Descărcăm HTML-ul o singură dată pentru exercițiile următoare (optimizare I/O)
response = requests.get(BASE_URL, timeout=TIMEOUT)
html = response.text
time.sleep(1)

# ==========================================
# Exercițiul 35: Descompunerea unui URL
# ==========================================
print("--- Exercițiul 35 ---")
url_test = "https://cybercor.org/path?x=1#top"
# urlparse descompune URL-ul respectând standardele RFC, fiind mult mai sigur 
# decât o partiționare manuală cu .split()
parsed = urllib.parse.urlparse(url_test)
print(f"Scheme: {parsed.scheme}")
print(f"Netloc: {parsed.netloc}")
print(f"Path: {parsed.path}")
print(f"Query: {parsed.query}")
print(f"Fragment: {parsed.fragment}")

# ==========================================
# Exercițiul 36: Compunerea URL-urilor
# ==========================================
print("\n--- Exercițiul 36 ---")
# urljoin rezolvă inteligent căile relative (inclusiv ".." pentru directorul părinte)
print("Absolut pentru /about:", urllib.parse.urljoin(BASE_URL, "/about"))
print("Absolut pentru contact.html:", urllib.parse.urljoin(BASE_URL, "contact.html"))
print("Absolut pentru ../index.html:", urllib.parse.urljoin(BASE_URL, "../index.html"))

# ==========================================
# Exercițiul 37: Extragerea legăturilor
# ==========================================
def extract_links(html_content: str) -> list:
    """Extrage toate legăturile (href) dintr-un document HTML, fără duplicate."""
    # Expresia regulată [^"]+ captează orice secvență de caractere care nu este ghilimea
    gasite = re.findall(r'href="([^"]+)"', html_content)
    # Convertirea listei în set (mulțime) elimină automat duplicatele (complexitate O(1) la căutare), 
    # apoi reconvertim în listă
    return list(set(gasite)) 

print("\n--- Exercițiul 37 ---")
toate_legaturile = extract_links(html)
print(f"S-au găsit {len(toate_legaturile)} legături unice. Primele 3: {toate_legaturile[:3]}")

# ==========================================
# Exercițiul 38: Interne sau externe?
# ==========================================
def split_links(links: list, domain: str) -> tuple:
    """Împarte lista de legături în interne (același domeniu) și externe."""
    interne, externe = [], []
    for link in links:
        # Standardizăm URL-ul pentru a evita compararea greșită a căilor relative
        full_url = urllib.parse.urljoin("https://" + domain, link)
        netloc = urllib.parse.urlparse(full_url).netloc
        
        # Clasificăm pe baza domeniului principal (netloc)
        if netloc == domain:
            interne.append(full_url)
        else:
            externe.append(full_url)
            
    return interne, externe

print("\n--- Exercițiul 38 ---")
linkuri_interne, linkuri_externe = split_links(toate_legaturile, "cybercor.org")
print(f"Legături interne: {len(linkuri_interne)}")
print(f"Legături externe: {len(linkuri_externe)}")

# ==========================================
# Exercițiul 39: Propriile metode (Parser HTML)
# ==========================================
print("\n--- Exercițiul 39 ---")
# OOP: Clasa ImageFinder moștenește clasa de bază HTMLParser din biblioteca standard
class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__() # Apelăm constructorul părintelui
        self.images = []
 
    # Suprascriem (override) metoda handle_starttag
    def handle_starttag(self, tag, attrs):
        if tag == "img":
            # attrs vine sub formă de listă de tupluri [(cheie, valoare)], îl facem dict pentru acces facil
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)

test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""
 
finder = ImageFinder()
finder.feed(test_html) # feed() declanșează parsarea
assert finder.images == [
    "/logo.png",                            
    "poza.jpg",                             
    "https://cdn.example.com/banner.webp",  
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul de validare a parserului a trecut cu succes!")

finder_real = ImageFinder()
finder_real.feed(html)
print(f"Pe site-ul real au fost găsite {len(finder_real.images)} imagini.")

# ==========================================
# Exercițiul 40: Amprenta paginii
# ==========================================
def page_fingerprint(url: str) -> str:
    """Returnează hash-ul (amprenta digitală) a conținutului paginii."""
    resp = requests.get(url, timeout=TIMEOUT)
    # SHA-256 creează o semnătură unică; orice modificare minoră în HTML va schimba complet hash-ul
    return hashlib.sha256(resp.content).hexdigest()

print("\n--- Exercițiul 40 ---")
hash1 = page_fingerprint(BASE_URL)
time.sleep(1)
hash2 = page_fingerprint(BASE_URL)
print(f"Sunt hash-urile identice? {hash1 == hash2}")

# ==========================================
# Exercițiul 41: Salvarea în JSON
# ==========================================
print("\n--- Exercițiul 41 ---")
# Serializare: Transformăm dicționarul Python într-un string formatat JSON și îl scriem pe disc
with open("headers.json", "w", encoding="utf-8") as file:
    json.dump(dict(response.headers), file, indent=2)

# Deserializare: Citim string-ul JSON de pe disc și îl reconstruim ca dicționar Python
with open("headers.json", "r", encoding="utf-8") as file:
    headers_incarcate = json.load(file)
    print(f"Antetul 'Content-Type' citit din JSON: {headers_incarcate.get('Content-Type')}")

# ==========================================
# Exercițiul 42: Interogare DNS
# ==========================================
def resolve(hostname: str) -> str:
    """Returnează adresa IP a unui hostname."""
    # Interoghează rezolvitorul DNS al sistemului de operare
    return socket.gethostbyname(hostname)

print("\n--- Exercițiul 42 ---")
print(f"Adresa IP pentru cybercor.org este: {resolve('cybercor.org')}")

# ==========================================
# Exercițiul 43: Expirarea certificatului
# ==========================================
def cert_days_left(hostname: str) -> int:
    """Se conectează la portul 443 și returnează zilele până la expirarea SSL."""
    context = ssl.create_default_context()
    # Stabilim o conexiune raw (socket) TCP pe portul 443, apoi o securizăm (wrap) cu SSL/TLS
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expire_date_str = cert["notAfter"]
            
            expire_seconds = ssl.cert_time_to_seconds(expire_date_str)
            current_seconds = time.time()
            zile = (expire_seconds - current_seconds) / (24 * 3600)
            return int(zile)

print("\n--- Exercițiul 43 ---")
print(f"Certificatul cybercor.org mai este valabil {cert_days_left('cybercor.org')} zile.")

# RĂSPUNS VERIFICAȚI-VĂ (Partea 4):
# Metoda `handle_starttag()` este un "callback". Nu o apelăm noi manual, ci 
# metoda `feed()` din clasa de bază HTMLParser scanează textul și, 
# ori de câte ori dă peste un tag HTML de deschidere (precum <img> sau <a>), 
# declanșează/apelează automat această metodă internă.