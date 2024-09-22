
---

# Wowhead Proxy

This Python script helps bypass geographic blocks on Wowhead by routing traffic through a proxy. It fetches free proxies, generates a PAC (Proxy Auto-Config) file, and serves it locally.

## Features

- **Fetches Free Proxies:** Retrieves free proxy servers using the `free-proxy` library.
- **Generates PAC File:** Creates a PAC file to route traffic for `wowhead.com` and `zamimg.com` through the chosen proxy.
- **Local HTTP Server:** Serves the PAC file at `http://localhost:8000/proxy.pac`.
- **Concurrent Proxy Checking:** Tests up to 10 proxies simultaneously.

## Purpose

**Wowhead Proxy** allows users to bypass geographic restrictions imposed by Wowhead by using a proxy server.

## Requirements

- Python 3.x
- `requests` library
- `fp` library (`free-proxy`)

If you have a `requirements.txt` file, you can install the required libraries with:

```bash
pip install -r requirements.txt
```

## Usage

1. **Run the Script:**

   ```bash
   python wowhead_proxy.py
   ```

   The script will:
   - Fetch and test proxies.
   - Generate a PAC file named `proxy.pac`.
   - Serve the PAC file at `http://localhost:8000/proxy.pac`.

2. **Configure Your Browser:**

   - Open **Internet Options** (`inetcpl.cpl`).
   - Go to the **Connections** tab and click **LAN settings**.
   - Check **Use automatic configuration script**.
   - Enter the PAC file URL: `http://localhost:8000/proxy.pac`.
   - Click **OK** to apply.

## Notes

- Ensure port `8000` is free.
- The script may take time to find a working proxy.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Free Proxy](https://pypi.org/project/free-proxy/) for the proxy library.

---

Feel free to customize or expand upon this as needed!
