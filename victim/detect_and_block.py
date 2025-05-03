from scapy.sendrecv import sniff
from scapy.layers.inet import IP
import subprocess
from collections import defaultdict
import time

packet_count = defaultdict(int)
threshold = 1000  # packets per 5 seconds
blocked_ips = {} # empty dict
unblock_duration = 600

def monitor(pkt):
    if IP in pkt:
        src_ip = pkt[IP].src
        packet_count[src_ip] += 1

def block_ip(ip):
    if ip not in blocked_ips:
        print(f"[!] Blocking IP: {ip}")
        try:
            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
            blocked_ips[ip] = time.time()
        except subprocess.CalledProcessError as e:
            print(f"[!] Error blocking IP {ip} with iptables: {e}")


def main():
    print("[*] Starting packet monitor...")
    while True:
        packet_count.clear()
        sniff(filter="icmp", prn=monitor, timeout=5)
        for ip, count in packet_count.items():
            if count > threshold:
                print(f"[!] DoS detected from {ip} - {count} packets")
                block_ip(ip)

if __name__ == "__main__":
    main()