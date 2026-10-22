# Laborator: funcții, metode și importuri pe web
# Student: <Tîltu Daniel>

import argparse
import csv
from datetime import datetime

# Exercițiul 45: Importarea anumitor nume
from webtools import DEFAULT_HEADERS, check_paths, site_report

# EXPLICAȚIE EX 45: Dacă main.py ar avea propria funcție numită `get_title`, 
# și am face un import global (import webtools), ar fi coliziune/suprascriere. 
# De aceea e mai sigur să folosim "from ... import ...".

# EXPLICAȚIE EX 46: Autotestul din webtools.py rulează doar cu `python webtools.py` deoarece 
# variabila specială __name__ este "__main__" doar când acel fișier este rulat direct. 
# Când e importat aici, __name__ devine "webtools", așadar blocul `if` nu se execută.

print(f"Constanta importată (Ex 47): {DEFAULT_HEADERS}\n")

# Exercițiul 48: Argumente din linia de comandă
parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL-ul de analizat")
args = parser.parse_args()

url_tinta = args.url

# Exercițiul 49: Un raport CSV
print("Verificăm căile pentru a genera report.csv...")
cai_test = ["/", "/robots.txt", "/sitemap.xml"]
rezultate = check_paths(url_tinta, cai_test)

with open("report.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["path", "status", "checked_at"])
    for path, status in rezultate.items():
        writer.writerow([path, status, datetime.now().isoformat()])
print("Fișierul report.csv a fost creat.")

# Exercițiul 50: Proiect final: raportul site-ului
site_report(url_tinta)