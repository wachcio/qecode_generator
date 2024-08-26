import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk

def generate_qr():
    text = entry.get()
    if not text:
        messagebox.showwarning("Warning", "Please enter some text")
        return

    qr = qrcode.make(text)
    qr_image = ImageTk.PhotoImage(qr)

    qr_label.config(image=qr_image)
    qr_label.image = qr_image

if __name__ == "__main__":
    app = tk.Tk()
    app.title("QR Code Generator")

    frame = tk.Frame(app)
    frame.pack(padx=10, pady=10)

    entry = tk.Entry(frame, width=40)
    entry.pack(side=tk.LEFT, padx=5)

    generate_button = tk.Button(frame, text="Generate", command=generate_qr)
    generate_button.pack(side=tk.LEFT, padx=5)

    qr_label = tk.Label(app)
    qr_label.pack(pady=10)

    app.mainloop()
