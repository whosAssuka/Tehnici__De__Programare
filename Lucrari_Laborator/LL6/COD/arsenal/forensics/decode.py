import re
import base64
import hashlib
import argparse
import json
from urllib.parse import unquote

# A2. recunoasterea stratului dupa forma
def ghici_strat(s):
    # Verifică URL (% urmat de 2 caractere hex)
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"
    if len(s) % 2 == 0 and re.fullmatch(r"[0-9a-fA-F]+", s):
        return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return "base64"
    return "necunoscut"

# A3. desfacerea stratului identificat
def desfa(s):
    strat = ghici_strat(s)
    try:
        if strat == "base64":
            return strat, base64.b64decode(s)
        elif strat == "hex":
            return strat, bytes.fromhex(s)
        elif strat == "url":
            return strat, unquote(s).encode()
    except Exception:
        pass
    return "necunoscut", s.encode()

# A4. Text citibil 
def citibil(b):
    # Un text e citibil dacă toți octeții săi sunt în intervalul ASCII vizibil (32-126)
    if not b: return False
    return all(32 <= c < 127 for c in b)

# A5. spargerea xor cu cheia de un octet
def sparge_xor():
    date = open("probe/xor.bin", "rb").read()
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if citibil(clar):
            print(f"[+] XOR Spart! Cheia: {k} | Mesaj: {clar.decode()}")
            break

# A6. sparg hash-ul cu ajutorului dictionarului
def sparge_hash():
    tinta = open("probe/hashuri.txt").readline().strip()
    lungime = len(tinta)
    print(f"[*] Hash țintă are lungimea {lungime} (Algoritm MD5)")
    
    for cuv in open("probe/wordlist.txt", encoding="latin1"):
        cuv = cuv.strip()
        if hashlib.md5(cuv.encode()).hexdigest() == tinta:
            print(f"[+] Hash Spart! Parola este: {cuv}")
            break

# A7. Legarea uneltei (CLI) și salvarea JSON 
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("intrare") 
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()

    if a.fisier:
        val = open(a.intrare, "r").read().strip()
    else:
        val = a.intrare

    straturi_gasite = []
    rezultat_final = None

    print("\n--- DECODARE STRATURI ---")
    for i in range(8):
        strat, b = desfa(val)
        straturi_gasite.append(strat)
        
        if citibil(b):
            rezultat_final = b.decode()
            print(f"[+] Mesaj ascuns găsit: {rezultat_final}")
            break
            
        try:
            val = b.decode()
        except:
            break

    with open("arsenal/forensics/fisa.json", "w") as f:
        json.dump({"straturi": straturi_gasite, "rezultat": rezultat_final}, f, indent=4)
    print("[+] Fișa JSON a fost salvată în arsenal/forensics/fisa.json")

    print("\n--- SPARGERE XOR ---")
    sparge_xor()

    print("\n--- SPARGERE HASH ---")
    sparge_hash()