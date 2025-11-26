import socket

def run(domain: str, wordlist_path: str):
    print(f"[+] Enumerating subdomains for: {domain}")
    print(f"[*] Using wordlist: {wordlist_path}")

    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            words = [w.strip() for w in f if w.strip()]
    except FileNotFoundError:
        print(f"[!] Wordlist not found: {wordlist_path}")
        return

    found = []

    for word in words:
        sub = f"{word}.{domain}"
        try:
            ip = socket.gethostbyname(sub)
            print(f"    [FOUND] {sub} -> {ip}")
            found.append((sub, ip))
        except socket.gaierror:
            # Not resolved. Skip silently.
            continue

    if not found:
        print("[*] No subdomains found with this wordlist.")
    else:
        print(f"\n[+] Total valid subdomains found: {len(found)}")
