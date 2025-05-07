from time import sleep
from tkinter import *
from tkinter import ttk


class Alert:
    def __init__(self) -> None:
        self._base_window = Tk()
        self._base_window.geometry("750x270")
        self._base_text = Label(
            self._base_window,
            text="Program is listening for attacks",
            font=('Arial', 25)
            )

        self._base_text.pack()
        self.update()

    def send_alert(self, attacker_ip: str, packet_count: int) -> None:
        top_level = Toplevel()
        top_level.title("Attack Detected")
        top_level.geometry("750x270")
        attack_label = Label(
            top_level,
            text=f"Attack detected from {attacker_ip}. IP Blocked at {packet_count} packets",
            font=('Arial', 25)
        )

        attack_label.pack(pady=10)
        print('alert sent')
        self.update()

    def update(self):
        self._base_window.update()


if __name__ == '__main__':
    alert_window = Alert()
    sleep(1)
    alert_window.send_alert('1', 100)

