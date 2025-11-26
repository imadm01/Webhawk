# WebHawk – Modern Web Recon & Light Vulnerability Scanner

WebHawk is a Python 3 based command-line tool that automates common reconnaissance and basic vulnerability checks for web targets.  
It is designed to help red teamers, bug bounty hunters, and security enthusiasts quickly gather information and identify low-hanging weaknesses.

> **Disclaimer:** For educational use and authorized testing only. Do not use this tool against systems you do not have permission to test.

---

## Features

- HTTP information and security header analysis.
- Port scanning for a given host (configurable range).
- Subdomain enumeration using a wordlist.
- Simple reflected XSS detection using a test payload.

Planned features.

- Basic SQL injection error pattern detection.
- Sensitive file and backup file discovery.
- Simple HTML or JSON reporting.

---

## Installation

```bash
git clone https://github.com/<your-username>/webhawk.git
cd webhawk
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
