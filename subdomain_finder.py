import socket
import threading
import argparse

print_lock = threading.Lock()
found_subdomains = []

def scan_subdomain(domain, subdomain):
    url = f"{subdomain}.{domain}"
    try:
        ip = socket.gethostbyname(url)
        with print_lock:
            print(f"[+] Found: {url} → {ip}")
            found_subdomains.append((url, ip))
    except socket.gaierror:
        pass

def main():
    parser = argparse.ArgumentParser(description="Fast Subdomain Enumerator (Python)")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g. example.com)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist file")
    parser.add_argument("-o", "--output", help="Output file to save results (optional)")
    args = parser.parse_args()

    try:
        with open(args.wordlist, "r") as file:
            subdomains = file.read().splitlines()

        print(f"\n🔍 Scanning subdomains for: {args.domain}\n")

        threads = []
        for sub in subdomains:
            t = threading.Thread(target=scan_subdomain, args=(args.domain, sub))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

        print(f"\n✅ Scan Complete. Found {len(found_subdomains)} subdomains.")

        if args.output:
            with open(args.output, "w") as f:
                for sub, ip in found_subdomains:
                    f.write(f"{sub} → {ip}\n")
            print(f"📁 Results saved to: {args.output}")

    except FileNotFoundError:
        print("❌ Wordlist file not found.")

if __name__ == "__main__":
    main()
