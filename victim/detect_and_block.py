# victim/detect_and_block.py
from scapy.sendrecv import sniff
from scapy.layers.inet import IP
from collections import defaultdict
from IPBlocker import IPBlocker
from VictimPopup import Alert
import time
import platform
import os

packet_count = defaultdict(int)
threshold = 200  # ICMP packets per 5 seconds
ip_blocker = IPBlocker()
debug = False


def monitor(pkt: dict) -> None:
    """
    Monitor how many packets are coming from a source.

    :param pkt: A packet of information.
    :return: None
    """
    if IP in pkt:
        src_ip = pkt[IP].src

        if debug:
            print(f"[DEBUG] ICMP packet from {src_ip}")

        packet_count[src_ip] += 1


def is_root() -> bool:
    """
    Check if the root is being used.
    :return: None
    """
    return os.geteuid() == 0 if platform.system() == "Linux" else True


def main():
    print("========================================")
    print("[*] DoS Detection System Started")
    print(f"[*] Threshold: {threshold} packets / 5 seconds")
    print(f"[*] OS: {platform.system()}")
    print("[*] Blocking enabled:", platform.system() == "Linux")
    print("[*] Requires sudo/root on Linux")
    print("========================================\n")

    if not is_root():
        print("[!] WARNING: This script must be run with sudo on Linux.")
        return

    alert_screen = Alert()


    try:
        while True:
            ip_blocker.unblock_cycle()
            packet_count.clear()

            print("[*] Sniffing ICMP packets for 5 seconds...")
            try:
                sniff(filter="icmp", prn=monitor, timeout=5, store=0)
            except PermissionError:
                print("[!] Permission denied. Try running with sudo.")
                time.sleep(5)
                continue
            except Exception as e:
                print(f"[!] Error during sniffing: {e}")
                time.sleep(5)
                continue

            print("[*] Checking packet counts...")
            for ip, count in packet_count.items():
                print(f"[DEBUG] Packet count for {ip}: {count}")
                if count > threshold:
                    print(f"[!] DoS detected from {ip} — {count} packets")
                    ip_blocker.block_ip(ip)
                    alert_screen.send_alert(ip, count)
    except KeyboardInterrupt:
        print("\n[*] Detection stopped by user.")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")


if __name__ == "__main__":
    main()
