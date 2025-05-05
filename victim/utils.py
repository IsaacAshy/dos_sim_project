# victim/utils.py
import platform
import subprocess
import time
import os

blocked_ips = {}
unblock_duration = 600  # 10 minutes

def block_ip(ip):
    if ip in blocked_ips:
        return  # Already blocked

    print(f"[!] Attempting to block IP: {ip}")
    if platform.system() != "Linux":
        print(f"[!] Blocking not supported on {platform.system()} — only available on Linux.")
        return

    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        blocked_ips[ip] = time.time()
        print(f"[+] Successfully blocked {ip}")
    except FileNotFoundError:
        print("[!] 'iptables' command not found. Are you running this on Linux?")
    except PermissionError:
        print("[!] Permission denied. Run this script with sudo/root privileges.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to block {ip}. iptables returned an error: {e}")
    except Exception as e:
        print(f"[!] Unexpected error blocking {ip}: {e}")

def unblock_ips():
    if platform.system() != "Linux":
        return

    current_time = time.time()
    to_unblock = [ip for ip, block_time in blocked_ips.items()
                  if current_time - block_time > unblock_duration]

    for ip in to_unblock:
        try:
            subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"], check=True)
            del blocked_ips[ip]
            print(f"[-] Unblocked IP: {ip}")
        except subprocess.CalledProcessError as e:
            print(f"[!] Failed to unblock {ip}: {e}")
        except Exception as e:
            print(f"[!] Unexpected error unblocking {ip}: {e}")
