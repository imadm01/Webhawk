from colorama import Fore, Style, init

init(autoreset=True)  # makes colors reset automatically

def info(text):
    print(Fore.CYAN + "[*] " + Style.RESET_ALL + text)

def success(text):
    print(Fore.GREEN + "[+] " + Style.RESET_ALL + text)

def warn(text):
    print(Fore.YELLOW + "[!] " + Style.RESET_ALL + text)

def error(text):
    print(Fore.RED + "[X] " + Style.RESET_ALL + text)

def title(text):
    print(Fore.MAGENTA + Style.BRIGHT + f"\n=== {text} ===\n" + Style.RESET_ALL)
