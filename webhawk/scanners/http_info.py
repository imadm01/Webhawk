import ssl
from urllib.parse import urlparse

from webhawk.utils.http import fetch
from webhawk.utils.output import info, success, warn, error, title

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
]


def _get_scheme_host_port(url: str):
    parsed = urlparse(url)
    scheme = parsed.scheme or "http"
    host = parsed.hostname
    port = parsed.port
    if port is None:
        port = 443 if scheme == "https" else 80
    return scheme, host, port


def run(url: str):
    title("HTTP Information & Security Header Analysis")
    info(f"Target: {url}")

    resp = fetch(url)
    if resp is None:
        error("Failed to retrieve response from target.")
        return

    # Basic info
    success(f"Status: {resp.status_code}")

    server = resp.headers.get("Server", "Unknown")
    powered = resp.headers.get("X-Powered-By", "Unknown")
    success(f"Server: {server}")
    info(f"X-Powered-By: {powered}")

    # TLS info (best-effort)
    scheme, host, port = _get_scheme_host_port(url)
    if scheme == "https":
        try:
            import socket

            ctx = ssl.create_default_context()
            with socket.create_connection((host, port), timeout=5) as sock:
                with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    subject = dict(x[0] for x in cert.get("subject", []))
                    issued_to = subject.get("commonName", "Unknown")
                    issuer = dict(x[0] for x in cert.get("issuer", []))
                    issued_by = issuer.get("commonName", "Unknown")
                    info(f"TLS: Issued to {issued_to}, Issued by {issued_by}")
        except Exception as e:
            warn(f"Could not fetch TLS certificate details: {e}")

    # All headers
    info("Response headers:")
    for k, v in resp.headers.items():
        print(f"    {k}: {v}")

    # Security header check
    print()
    title("Security Headers Check")

    present = 0
    for header in SECURITY_HEADERS:
        if header in resp.headers:
            present += 1
            success(f"{header} present")
        else:
            warn(f"{header} missing")

    score = int((present / len(SECURITY_HEADERS)) * 100)
    print()
    if score == 100:
        success(f"Security header score: {score}/100 (Excellent)")
    elif score >= 60:
        warn(f"Security header score: {score}/100 (Partially configured)")
    else:
        error(f"Security header score: {score}/100 (Weak configuration)")
