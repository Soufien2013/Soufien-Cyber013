import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import time
import requests


def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)


def run_tool_thread(command):
    def task():
        target = entry.get().strip()
        if not target:
            messagebox.showerror("Error", "Please enter a domain or IP address")
            return
        output_box.insert(tk.END, f"\n🔍 Running: {command}\n")
        output_box.see(tk.END)
        output = run_command(command)
        output_box.insert(tk.END, output + "\n")
        output_box.see(tk.END)
    threading.Thread(target=task).start()


def ddos_attack():
    target = entry.get().strip()
    if not target:
        messagebox.showerror("Error", "Please enter a domain or IP address")
        return
    messagebox.showinfo("Warning", "DDoS Attack simulation started.\nThis is for learning only and must be done on authorized targets!")
    def attack():
        try:
            for i in range(100):  
                response = requests.get(f"http://{target}")
                output_box.insert(tk.END, f"Request {i+1} sent, status code: {response.status_code}\n")
                output_box.see(tk.END)
                time.sleep(0.1)  
            output_box.insert(tk.END, "\nDDoS simulation finished.\n")
            output_box.see(tk.END)
        except Exception as e:
            output_box.insert(tk.END, f"Error during DDoS simulation: {e}\n")
            output_box.see(tk.END)
    threading.Thread(target=attack).start()

def clear_output():
    output_box.delete('1.0', tk.END)

window = tk.Tk()
window.title("🧠 Soufien Cyber Amri013 - Info Gathering & DDoS Tool")
window.geometry("1000x700")
window.configure(bg="#121212")

window.rowconfigure(2, weight=1)
window.columnconfigure(0, weight=1)

title = tk.Label(window, text="🧠 Soufien Cyber Amri013 🎩", font=("Helvetica", 22, "bold"), bg="#121212", fg="#00ffcc")
title.pack(pady=5)

subtitle = tk.Label(window, text="Information Gathering & DDoS Simulation | For legal testing only", font=("Arial", 12), bg="#121212", fg="gray")
subtitle.pack()

entry = tk.Entry(window, font=("Arial", 14), width=60)
entry.pack(pady=10)

frame = tk.Frame(window, bg="#121212")
frame.pack()

btn_params = {
    "font": ("Arial", 11),
    "bg": "#333",
    "fg": "white",
    "width": 16,
    "padx": 5,
    "pady": 5
}


tk.Button(frame, text="Whois", command=lambda: run_tool_thread(f"whois {entry.get().strip()}"), **btn_params).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame, text="Dig", command=lambda: run_tool_thread(f"dig {entry.get().strip()}"), **btn_params).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame, text="Nslookup", command=lambda: run_tool_thread(f"nslookup {entry.get().strip()}"), **btn_params).grid(row=0, column=2, padx=5, pady=5)
tk.Button(frame, text="theHarvester", command=lambda: run_tool_thread(f"theHarvester -d {entry.get().strip()} -b google"), **btn_params).grid(row=0, column=3, padx=5, pady=5)
tk.Button(frame, text="Dnsenum", command=lambda: run_tool_thread(f"dnsenum {entry.get().strip()}"), **btn_params).grid(row=0, column=4, padx=5, pady=5)
tk.Button(frame, text="Sublist3r", command=lambda: run_tool_thread(f"sublist3r -d {entry.get().strip()}"), **btn_params).grid(row=0, column=5, padx=5, pady=5)
tk.Button(frame, text="Amass", command=lambda: run_tool_thread(f"amass enum -d {entry.get().strip()}"), **btn_params).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame, text="WhatWeb", command=lambda: run_tool_thread(f"whatweb {entry.get().strip()}"), **btn_params).grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame, text="Curl", command=lambda: run_tool_thread(f"curl -s {entry.get().strip()}"), **btn_params).grid(row=1, column=2, padx=5, pady=5)
tk.Button(frame, text="Nmap", command=lambda: run_tool_thread(f"nmap -A -T4 {entry.get().strip()}"), **btn_params).grid(row=1, column=3, padx=5, pady=5)
tk.Button(frame, text="SQLMap", command=lambda: run_tool_thread(f"sqlmap -u {entry.get().strip()} --batch --level=5 --risk=3"), **btn_params).grid(row=1, column=4, padx=5, pady=5)
tk.Button(frame, text="Ping", command=lambda: run_tool_thread(f"ping -c 4 {entry.get().strip()}"), **btn_params).grid(row=1, column=5, padx=5, pady=5)


tk.Button(window, text="Run DDoS Simulation", command=ddos_attack, bg="#aa0000", fg="white", font=("Arial", 13, "bold"), width=30, pady=10).pack(pady=15)


output_box = scrolledtext.ScrolledText(window, font=("Fira Code", 14), bg="black", fg="white")
output_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

window.mainloop()
