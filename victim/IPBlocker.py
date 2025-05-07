"""
Original Code by Isaac Ashworth.
Modified by Tom Davis to meet OOP Standards of encapsulation and avoid globals being relied upon.
Last Modified: 07/05/2025
"""

import platform
import subprocess
import time


class IPBlocker:
    def __init__(self):
        self._blocked_ips = {}
        self._block_duration = 600

        # Check if the platform is correct. This system is only built for Linux Devices.
        if platform.system() != "Linux":
            print(f"[!] Blocking not supported on {platform.system()} — only available on Linux.")
            return

    def block_ip(self, ip: str) -> None:
        """
        Block an IP on the system level.

        :param ip: String. Which IP you wish to block.
        :returns: None
        """

        # Ensure the IP is not already blocked.
        if ip in self._blocked_ips:
            return

        # Attempt to block the IP. Catch possible exceptions to provide error handling.
        print(f"[!] Attempting to block IP: {ip}")

        try:
            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
            self._blocked_ips[ip] = time.time()
            print(f"[+] Successfully blocked {ip}")
        except FileNotFoundError:
            print("[!] 'iptables' command not found. Are you running this on Linux?")
        except PermissionError:
            print("[!] Permission denied. Run this script with sudo/root privileges.")
        except subprocess.CalledProcessError as e:
            print(f"[!] Failed to block {ip}. iptables returned an error: {e}")
        except Exception as e:
            print(f"[!] Unexpected error blocking {ip}: {e}")

    def unblock_cycle(self):
        """
        A cycle to unblock all expired IP Blocks.

        :return: None
        """
        # Grab the current time and form a list of ips to unblock.
        current_time = time.time()
        to_unblock = [unblock_ip for unblock_ip, block_time in self._blocked_ips.items() if current_time - block_time > self._block_duration]

        for ip in to_unblock:
            try:
                subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"], check=True)
                del self._blocked_ips[ip]
                print(f"[-] Unblocked IP: {ip}")
            except subprocess.CalledProcessError as e:
                print(f"[!] Failed to unblock {ip}: {e}")
            except Exception as e:
                print(f"[!] Unexpected error unblocking {ip}: {e}")
