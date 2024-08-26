import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk

def generate_qr():
    qr_type = qr_type_var.get()
    text = entry.get() if qr_type != "wifi" else ssid_entry.get()
    broadcast = broadcast_var.get()
    security = security_var.get()
    password = password_entry.get()
    if not text:
        messagebox.showwarning("Warning", "Please enter some text")
        return

    if qr_type == "text":
        qr = qrcode.make(text)
    elif qr_type == "wifi":
        qr = qrcode.make(f"WIFI:T:{security};S:{text};P:{password};H:{'true' if broadcast else 'false'};;")
    elif qr_type == "contact":
        qr = qrcode.make(f"BEGIN:VCARD\nFN:{text}\nEND:VCARD")
    else:
        messagebox.showwarning("Warning", "Please select a QR code type")
        return
    qr_image = ImageTk.PhotoImage(qr)

    qr_label.config(image=qr_image)
    qr_label.image = qr_image

if __name__ == "__main__":
    app = tk.Tk()
    app.title("QR Code Generator")

    qr_type_var = tk.StringVar(value="text")

    frame = tk.Frame(app)
    frame.pack(padx=10, pady=10)

    ssid_label = tk.Label(app, text="SSID:")
    ssid_label.pack(anchor=tk.W)
    ssid_entry = tk.Entry(app, width=40)
    ssid_entry.pack(anchor=tk.W, padx=5)

    broadcast_var = tk.BooleanVar()
    broadcast_check = tk.Checkbutton(app, text="Broadcast SSID", variable=broadcast_var)
    broadcast_check.pack(anchor=tk.W)

    security_label = tk.Label(app, text="Security Type:")
    security_label.pack(anchor=tk.W)
    security_var = tk.StringVar(value="WPA")
    security_options = ["WPA", "WEP", "nopass"]
    security_menu = tk.OptionMenu(app, security_var, *security_options)
    security_menu.pack(anchor=tk.W)

    password_label = tk.Label(app, text="Password:")
    password_label.pack(anchor=tk.W)
    password_entry = tk.Entry(app, show="*", width=40)
    password_entry.pack(anchor=tk.W, padx=5)

    entry = tk.Entry(frame, width=40)
    entry.pack(side=tk.LEFT, padx=5)

    text_radio = tk.Radiobutton(app, text="Text", variable=qr_type_var, value="text")
    text_radio.pack(anchor=tk.W)

    wifi_radio = tk.Radiobutton(app, text="WiFi", variable=qr_type_var, value="wifi")
    wifi_radio.pack(anchor=tk.W)

    contact_radio = tk.Radiobutton(app, text="Contact", variable=qr_type_var, value="contact")
    contact_radio.pack(anchor=tk.W)

    generate_button = tk.Button(frame, text="Generate", command=generate_qr)
    generate_button.pack(side=tk.LEFT, padx=5)

    qr_label = tk.Label(app)
    qr_label.pack(pady=10)

    app.mainloop()
