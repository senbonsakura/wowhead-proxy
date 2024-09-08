import http.server
import socketserver
import requests
from fp.fp import FreeProxy
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Shared flag to indicate when a successful proxy is found
success_flag = threading.Event()

# 1. Get a free proxy using free-proxy and strip protocol
def get_free_proxy():
    proxy = FreeProxy(timeout=1, rand=False).get()
    clean_proxy = proxy.replace("http://", "").replace("https://", "")
    print(f"Proxy fetched and cleaned: {clean_proxy}")
    return clean_proxy

# 2. Generate a PAC file for wowhead.com and zamimg.com
def generate_pac_file(proxy):
    pac_content = f"""
    function FindProxyForURL(url, host) {{
            if (shExpMatch(host, "*.wowhead.com") || shExpMatch(host, "wowhead.com") ||
                shExpMatch(host, "*.zamimg.com") || shExpMatch(host, "zamimg.com")) {{
            return "PROXY {proxy}";
        }}
        return "DIRECT";
    }}
    """
    with open("proxy.pac", "w") as pac_file:
        pac_file.write(pac_content)
    print("PAC file generated at proxy.pac.")

# 3. Serve the PAC file using built-in HTTP server
class PACRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/proxy.pac':
            self.send_response(200)
            self.send_header('Content-type', 'application/x-ns-proxy-autoconfig')
            self.end_headers()
            with open('proxy.pac', 'r') as pac_file:
                self.wfile.write(pac_file.read().encode())
            print("Served PAC file at /proxy.pac")
        else:
            self.send_error(404, "File Not Found")

def serve_pac_file():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), PACRequestHandler) as httpd:
        print(f"Serving PAC file locally at http://localhost:{PORT}/proxy.pac")
        httpd.serve_forever()

# 4. Check if the proxy works and can access wowhead.com
def check_proxy(proxy):
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    try:
        response = requests.get("https://www.wowhead.com", proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"Proxy works! Accessed wowhead.com successfully with {proxy}.")
            success_flag.set()  # Signal success
            return proxy
        else:
            print(f"Failed to access wowhead.com with proxy {proxy}. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error accessing wowhead.com with proxy {proxy}: {e}")
        return None

# 5. Try fetching multiple proxies concurrently
def fetch_and_check_proxies_concurrently():
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_free_proxy): i for i in range(10)}

        while not success_flag.is_set():
            for future in as_completed(futures):
                proxy = future.result()
                if proxy and check_proxy(proxy):
                    return proxy

            # Fetch new proxies if none work
            futures = {executor.submit(get_free_proxy): i for i in range(10)}

if __name__ == "__main__":
    # Step 1: Fetch multiple proxies concurrently and find one that works
    proxy = fetch_and_check_proxies_concurrently()

    # Step 2: Create PAC file to redirect traffic for wowhead.com and zamimg.com
    generate_pac_file(proxy)

    # Step 3: Serve PAC file locally (run in a separate thread or process for serving continuously)
    from threading import Thread
    server_thread = Thread(target=serve_pac_file)
    server_thread.start()