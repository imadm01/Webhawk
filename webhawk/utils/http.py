import requests

def fetch(url: str, timeout: int = 10):
    """Send a GET request with common headers and return the response object."""
    headers = {
        "User-Agent": "WebHawk/1.0 (+github.com/yourusername)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=timeout, verify=True)
        return response
    except requests.exceptions.RequestException as e:
        print(f"[!] Request failed: {e}")
        return None
