import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import qrcode
from PIL import Image, ImageTk

def generate_qr():
    current_tab = notebook.index(notebook.select())
    if current_tab == 0:  # Text tab
        text = text_entry.get()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text")
            return
        qr = qrcode.make(text)
    elif current_tab == 1:  # WiFi tab
        ssid = ssid_entry.get()
        hide = hide_var.get()
        security = security_var.get()
        password = password_entry.get()
        if not ssid:
            messagebox.showwarning("Warning", "Please enter SSID")
            return
        if security == "nopass":
            qr = qrcode.make(f"WIFI:T:{security};S:{ssid};H:{'true' if hide else 'false'};;")
        else:
            qr = qrcode.make(f"WIFI:T:{security};S:{ssid};P:{password};H:{'true' if hide else 'false'};;")
    elif current_tab == 2:  # Contact tab
        contact_name = contact_entry.get()
        if not contact_name:
            messagebox.showwarning("Warning", "Please enter contact name")
            return
        qr = qrcode.make(f"BEGIN:VCARD\nFN:{contact_name}\nEND:VCARD")
    qr_image = ImageTk.PhotoImage(qr)

    qr_label.config(image=qr_image)
    qr_label.image = qr_image

if __name__ == "__main__":
    app = tk.Tk()
    app.title("QR Code Generator")

    notebook = ttk.Notebook(app)
    notebook.pack(padx=10, pady=10, fill='both', expand=True)

    # Text Tab
    text_tab = ttk.Frame(notebook)
    notebook.add(text_tab, text='Text')

    text_label = tk.Label(text_tab, text="Text:")
    text_label.pack(anchor=tk.W)
    text_entry = tk.Entry(text_tab, width=40)
    text_entry.pack(anchor=tk.W, padx=5)

    # WiFi Tab
    wifi_tab = ttk.Frame(notebook)
    notebook.add(wifi_tab, text='WiFi')

    ssid_label = tk.Label(wifi_tab, text="SSID:")
    ssid_label.pack(anchor=tk.W)
    ssid_entry = tk.Entry(wifi_tab, width=40)
    ssid_entry.pack(anchor=tk.W, padx=5)

    hide_var = tk.BooleanVar()
    hide_check = tk.Checkbutton(wifi_tab, text="Hide SSID", variable=hide_var)
    hide_check.pack(anchor=tk.W)

    security_label = tk.Label(wifi_tab, text="Security Type:")
    security_label.pack(anchor=tk.W)
    security_var = tk.StringVar(value="WPA")
    security_options = ["WPA", "WPA2", "WPA3", "WEP", "nopass"]
    security_menu = tk.OptionMenu(wifi_tab, security_var, *security_options)
    def toggle_password_field(*args):
        if security_var.get() == "nopass":
            password_entry.pack_forget()
            password_label.pack_forget()
        else:
            password_label.pack(anchor=tk.W)
            password_entry.pack(anchor=tk.W, padx=5)

    password_label = tk.Label(wifi_tab, text="Password:")
    password_label.pack(anchor=tk.W)
    password_entry = tk.Entry(wifi_tab, show="*", width=40)
    password_entry.pack(anchor=tk.W, padx=5)

    security_var.trace("w", toggle_password_field)
    security_menu.pack(anchor=tk.W)
    toggle_password_field()

    password_label = tk.Label(wifi_tab, text="Password:")
    password_label.pack(anchor=tk.W)
    password_entry = tk.Entry(wifi_tab, show="*", width=40)
    password_entry.pack(anchor=tk.W, padx=5)

    # Contact Tab
    contact_tab = ttk.Frame(notebook)
    notebook.add(contact_tab, text='Contact')

    contact_label = tk.Label(contact_tab, text="Contact Name:")
    contact_label.pack(anchor=tk.W)
    contact_entry = tk.Entry(contact_tab, width=40)
    contact_entry.pack(anchor=tk.W, padx=5)

    generate_button = tk.Button(app, text="Generate", command=generate_qr)
    generate_button.pack(pady=10)

    qr_label = tk.Label(app)
    qr_label.pack(pady=10)

    app.mainloop()
