import argparse
from .scanners import http_info, ports, subdomains, xss_reflect

def main():
    parser = argparse.ArgumentParser(
        prog="webhawk",
        description="Modern, modular web recon & light vuln scanner."
    )

    subparsers = parser.add_subparsers(dest="command")

    # http-info
    p_http = subparsers.add_parser("http-info", help="Fetch HTTP info & security headers.")
    p_http.add_argument("url", help="Target URL (e.g. https://example.com)")

    # ports
    p_ports = subparsers.add_parser("ports", help="Scan ports on a host.")
    p_ports.add_argument("host", help="Target host (domain or IP)")
    p_ports.add_argument("--start", type=int, default=1)
    p_ports.add_argument("--end", type=int, default=1024)

    # subdomains
    p_sub = subparsers.add_parser("subdomains", help="Enumerate subdomains from wordlist.")
    p_sub.add_argument("domain", help="Base domain (e.g. example.com)")
    p_sub.add_argument("--wordlist", default="wordlists/subdomains.txt")

    # xss-reflect
    p_xss = subparsers.add_parser("xss", help="Check for simple reflected XSS.")
    p_xss.add_argument("url", help="Target URL with parameter, e.g. https://site.com/search?q=")
    p_xss.add_argument("--param", default="q", help="Parameter name (default: q)")

    args = parser.parse_args()

    if args.command == "http-info":
        http_info.run(args.url)
    elif args.command == "ports":
        ports.run(args.host, args.start, args.end)
    elif args.command == "subdomains":
        subdomains.run(args.domain, args.wordlist)
    elif args.command == "xss":
        xss_reflect.run(args.url, args.param)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
