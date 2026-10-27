import re
from PIL import Image
from PIL.ExifTags import TAGS

# B1.
print("\n[+] B1. MAGIC BYTES")
def tip_real(cale):
    cap = open(cale, "rb").read(8)
    if cap.startswith(b"%PDF"): return "pdf"
    if cap.startswith(b"\x89PNG"): return "png"
    if cap.startswith(b"\xff\xd8"): return "jpeg"
    if cap.startswith(b"PK\x03\x04"): return "zip/docx"
    return cap.hex()

print("Tipul real al foto.jpg este:", tip_real("probe/foto.jpg"))
print("Tipul real al ascuns.png este:", tip_real("probe/ascuns.png"))

# --- B2.
print("\n[+] B2. STRINGS (Căutare text în fișier binar)")
date_ascuns = open("probe/ascuns.png", "rb").read()
for m in re.findall(rb"[ -~]{4,}", date_ascuns):
    text = m.decode()
    if "FLAG" in text or ".txt" in text:
        print("Indiciu găsit:", text)

# B3.
print("\n[+] B3. METADATE EXIF ȘI GPS")
exif = Image.open("probe/foto.jpg")._getexif() or {}
for id_tag, val in exif.items():
    nume_tag = TAGS.get(id_tag, id_tag)
    if nume_tag in ["Make", "Model", "DateTime"]:
        print(f"{nume_tag} : {val}")
    
    if nume_tag == "GPSInfo":
        lat = val[2][0] + val[2][1]/60 + val[2][2]/3600
        lon = val[4][0] + val[4][1]/60 + val[4][2]/3600
        print(f"Coordonate GPS: {lat:.4f} {val[1]}, {lon:.4f} {val[3]}")
        print(f"Link Maps: https://maps.google.com/?q={lat},{lon}")

#B4.
print("\n[+] B4. FILE CARVING")
i = date_ascuns.find(b"PK\x03\x04")
if i != -1:
    open("gasit.zip", "wb").write(date_ascuns[i:])
    print(f"Arhivă extrasă cu succes la octetul {i} (salvată ca 'gasit.zip')")

#  B5. 
print("\n[+] B5. ASCUNDERE MESAJ (Steganografie LSB)")
img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())

mesaj = b"FLAG{ascuns_in_pixeli}\x00" 
biti_mesaj = "".join(f"{x:08b}" for x in mesaj)

px_nou = []
idx_bit = 0

for r, g, b in px:
    if idx_bit < len(biti_mesaj):
        r = (r & ~1) | int(biti_mesaj[idx_bit]); idx_bit += 1
    if idx_bit < len(biti_mesaj):
        g = (g & ~1) | int(biti_mesaj[idx_bit]); idx_bit += 1
    if idx_bit < len(biti_mesaj):
        b = (b & ~1) | int(biti_mesaj[idx_bit]); idx_bit += 1
    px_nou.append((r, g, b))

img.putdata(px_nou)
img.save("stego.png")
print("Mesajul a fost ascuns cu succes în 'stego.png'")

# B6.
print("\n[+] B6. DEZVĂLUIRE MESAJ LSB")
px_stego = list(Image.open("stego.png").convert("RGB").getdata())
biti_extrasi = ""

for r, g, b in px_stego:
    biti_extrasi += str(r & 1)
    biti_extrasi += str(g & 1)
    biti_extrasi += str(b & 1)

mesaj_decodat = bytearray()
for i in range(0, len(biti_extrasi), 8):
    octet_binar = biti_extrasi[i:i+8]
    if len(octet_binar) == 8:
        valoare_ascii = int(octet_binar, 2)
        if valoare_ascii == 0:
            break
        mesaj_decodat.append(valoare_ascii)

print("Mesajul dezvăluit este:", mesaj_decodat.decode(errors="ignore"))