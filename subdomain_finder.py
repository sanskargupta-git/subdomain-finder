import socket
import threading

print_lock = threading.Lock()  # To prevent print conflicts
found_subdomains = []

# Function to resolve subdomain
def scan_subdomain(domain, subdomain):
    url = f"{subdomain}.{domain}"
    try:
        ip = socket.gethostbyname(url)
        with print_lock:
            print(f"[+] Found: {url} → {ip}")
            found_subdomains.append((url, ip))
    except socket.gaierror:
        pass  # Ignore if subdomain doesn't resolve

# Main function
def main():
    domain = input("Enter target domain (e.g. example.com): ")
    wordlist_file = input("Enter path to wordlist file (e.g. wordlist.txt): ")

    try:
        with open(wordlist_file, "r") as f:
            subdomains = f.read().splitlines()

        print(f"\n🔍 Starting Subdomain Scan for: {domain}\n")

        threads = []
        for sub in subdomains:
            t = threading.Thread(target=scan_subdomain, args=(domain, sub))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

        print("\n✅ Scan Complete.")
        print(f"Total found: {len(found_subdomains)}")

    except FileNotFoundError:
        print("❌ Wordlist file not found.")

if __name__ == "__main__":
    main()
