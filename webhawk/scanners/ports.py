import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

from webhawk.utils.output import info, success, warn, error, title


def _scan_single_port(host: str, port: int, timeout: float = 1.0):
    """
    Try to connect to a single TCP port.
    Returns (port, is_open, banner_str or "").
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect((host, port))
            # Try to grab a simple banner (if any)
            try:
                banner = s.recv(1024).decode(errors="ignore").strip()
            except Exception:
                banner = ""
            return port, True, banner
        except (socket.timeout, ConnectionRefusedError, OSError):
            return port, False, ""


def run(host: str, start: int, end: int):
    title("TCP Port Scan")
    info(f"Target host: {host}")
    info(f"Port range: {start}-{end}")

    # Resolve hostname to IP
    try:
        ip = socket.gethostbyname(host)
        success(f"Resolved {host} -> {ip}")
    except socket.gaierror as e:
        error(f"Could not resolve host: {e}")
        return

    if start < 1 or end > 65535 or start > end:
        error("Invalid port range. Valid range is 1-65535 and start <= end.")
        return

    open_ports = []

    info("Scanning ports... (this may take a moment)")
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {
            executor.submit(_scan_single_port, ip, port): port
            for port in range(start, end + 1)
        }

        for fut in as_completed(futures):
            port, is_open, banner = fut.result()
            if is_open:
                open_ports.append((port, banner))
                if banner:
                    success(f"Port {port} OPEN  |  Banner: {banner}")
                else:
                    success(f"Port {port} OPEN")

    print()
    if not open_ports:
        warn("No open ports found in the specified range.")
    else:
        success(f"Found {len(open_ports)} open ports in range {start}-{end}.")
