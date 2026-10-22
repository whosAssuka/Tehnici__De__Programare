# Laborator: funcții, metode și importuri pe web
# Student: <Tîltu Daniel>

import requests
import urllib.parse
import socket
import ssl
import time
import json
import re

TIMEOUT = 10
# Exercițiul 47: Constante de modul
DEFAULT_HEADERS = {"User-Agent": "WebLab-Tîltu Daniel"}

def fetch(url, timeout=TIMEOUT):
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)

def get_status(url):
    return fetch(url).status_code

def get_title(html):
    start = html.find("<title>")
    if start == -1: return "Fără titlu"
    start += len("<title>")
    end = html.find("</title>")
    return html[start:end].strip()

def security_headers(url):
    antete_cautate = [
        "Strict-Transport-Security", "Content-Security-Policy",
        "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"
    ]
    resp = fetch(url)
    return {antet: (antet in resp.headers) for antet in antete_cautate}

def score_headers(results):
    gasite = sum(results.values())
    return f"{gasite}/{len(results)}"

def check_paths(base, paths):
    rezultate = {}
    for path in paths:
        full_url = urllib.parse.urljoin(base, path)
        rezultate[path] = get_status(full_url)
        time.sleep(1)
    return rezultate

def extract_links(html_content):
    gasite = re.findall(r'href="([^"]+)"', html_content)
    return list(set(gasite))

def split_links(links, domain):
    interne, externe = [], []
    for link in links:
        full_url = urllib.parse.urljoin("https://" + domain, link)
        if urllib.parse.urlparse(full_url).netloc == domain:
            interne.append(full_url)
        else:
            externe.append(full_url)
    return interne, externe

def resolve(hostname):
    return socket.gethostbyname(hostname)

def cert_days_left(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expire_seconds = ssl.cert_time_to_seconds(cert["notAfter"])
            return int((expire_seconds - time.time()) / (24 * 3600))

def fetch_robots(base):
    resp = fetch(urllib.parse.urljoin(base, "/robots.txt"))
    return resp.text if resp.status_code == 200 else None

def disallowed_paths(robots_text):
    if not robots_text: return []
    interzise = []
    for linie in robots_text.splitlines():
        if linie.startswith("Disallow:"):
            interzise.append(linie.split(":", 1)[1].strip())
    return interzise

# Exercițiul 50: Proiect final
def site_report(url):
    print(f"\n=== Raport site: {url} ===")
    
    resp = fetch(url)
    print(f"Cod de stare:      {resp.status_code}")
    
    titlu = get_title(resp.text)
    print(f"Titlu:             {titlu}")
    
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.netloc
    
    ip = resolve(hostname)
    print(f"Adresă IP:         {ip}")
    
    resp_http = requests.get(url.replace("https", "http"), headers=DEFAULT_HEADERS, timeout=TIMEOUT)
    redir_list = []
    for r in resp_http.history:
        redir_list.append(f"{r.status_code} -> {r.url}")
    redirs = ", ".join(redir_list) if redir_list else "Niciuna"
    print(f"Redirecționări:    {redirs}")
    
    scor_sec = score_headers(security_headers(url))
    print(f"Scor securitate:   {scor_sec}")
    
    zile = cert_days_left(hostname)
    print(f"Certificat:        {zile} de zile rămase")
    
    toate_legaturile = extract_links(resp.text)
    int_links, ext_links = split_links(toate_legaturile, hostname)
    print(f"Legături:          {len(int_links)} interne, {len(ext_links)} externe")
    
    robots_text = fetch_robots(url)
    cai_interzise = disallowed_paths(robots_text)
    interzise_str = ", ".join(cai_interzise) if cai_interzise else "Niciuna"
    print(f"Căi interzise:     {interzise_str}")

    date_json = {
        "status_code": resp.status_code,
        "title": titlu,
        "ip": ip,
        "redirects": redir_list,
        "security_score": scor_sec,
        "cert_days_left": zile,
        "links": {"internal": len(int_links), "external": len(ext_links)},
        "disallowed_paths": cai_interzise
    }
    with open("report.json", "w", encoding="utf-8") as file:
        json.dump(date_json, file, indent=2)
    print("Salvat în report.json")

# Exercițiul 46: Blocul main
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))