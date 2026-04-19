import subprocess

def solve():
    # 1. Extract required fields using tshark
    cmd = [
        "tshark", "-r", "flag_tcp_nightmare (1).pcap",
        "-T", "fields",
        "-e", "tcp.srcport",
        "-e", "tcp.dstport",
        "-e", "tcp.window_size_value",
        "-e", "tcp.seq_raw"
    ]
    
    print("[*] Running tshark to extract fields...")
    out = subprocess.check_output(cmd).decode('utf-8')
    
    flag = ""
    packets_found = 0
    
    print("[*] Processing packets...")
    for line in out.strip().split('\n'):
        parts = line.strip().split()
        if len(parts) >= 4:
            sp = int(parts[0])
            dp = int(parts[1])
            ws = int(parts[2])
            seq = int(parts[3])
            
            # 2. Filter using Window Size and Ports relationship
            if sp ^ dp == ws:
                packets_found += 1
                
                # 3. Decode character from Raw Sequence
                # We discovered that the LSB of Raw Sequence XORed with 0x42 (66) gives the flag char
                char = chr((seq & 0xFF) ^ 0x42)
                flag += char
                
    print(f"[+] Found {packets_found} matching packets")
    print(f"[+] Flag: {flag}")

if __name__ == "__main__":
    solve()
