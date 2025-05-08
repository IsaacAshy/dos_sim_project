import os
from time import sleep
from tkinter import *


class Alert:
    def __init__(self) -> None:
        self._base_window = Tk()
        self._base_window.geometry("750x270")
        self._base_text = Label(
            self._base_window,
            text="PROGRAM IS LISTENING FOR ATTACKS",
            font=('Arial Bold', 25),
            bg='#e3a909',
            fg='#ffffff',
            justify='center',
            wraplength=900,
            height=270,
            width=1000,
            )
        self._base_window.title('Attack Listener')
        self._base_window.config(bg='#e3a909')
        self._base_text.pack(pady=100)
        self.update()

    def send_alert(self, attacker_ip: str, packet_count: int) -> None:
        top_level = Toplevel()
        top_level.title("Attack Detected")
        top_level.geometry("1000x270")
        top_level.config(bg='#e30931')
        attack_label = Label(
            top_level,
            text=f"ATTACK DETECTED FROM {attacker_ip}. IP Blocked at {packet_count} packets",
            font=('Arial Bold', 25),
            fg='#ffffff',
            bg='#e30931',
            justify='center',
            wraplength=900,
            height=270,
            width=1000,
        )

        attack_label.pack(pady=100)

        # Play an alert sound.
        os.system(f'play -nq -t alsa synth {5} sine {40}')

        # Push the UI to the users screen.
        self.update()

    def update(self):
        self._base_window.update()


if __name__ == '__main__':
    alert_window = Alert()
    sleep(1)
    alert_window.send_alert('1', 100)
    sleep(10)

