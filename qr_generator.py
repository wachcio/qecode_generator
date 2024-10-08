import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.ttk as ttk
import qrcode
from PIL import Image, ImageTk
import io

qr_window = None  # Global variable to hold the QR window instance

def generate_qr():
    current_tab = notebook.index(notebook.select())
    if current_tab == 0:  # Text tab
        text = text_entry.get()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text")
            return None
        qr = qrcode.make(text)
        qr_info = f"Text: {text}"
    elif current_tab == 1:  # WiFi tab
        ssid = ssid_entry.get()
        hide = hide_var.get()
        security = security_var.get()
        password = password_entry.get()
        if not ssid:
            messagebox.showwarning("Warning", "Please enter SSID")
            return None
        if security == "nopass":
            qr = qrcode.make(f"WIFI:T:{security};S:{ssid};H:{'true' if hide else 'false'};;")
            qr_info = f"WiFi SSID: {ssid}, Security: {security}, Hidden: {hide}"
        else:
            qr = qrcode.make(f"WIFI:T:{security};S:{ssid};P:{password};H:{'true' if hide else 'false'};;")
            qr_info = f"WiFi SSID: {ssid}, Password: {password}, Security: {security}, Hidden: {hide}"
    elif current_tab == 2:  # Contact tab
        contact_name = contact_entry.get()
        contact_surname = surname_entry.get()
        company = company_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        birthday = birthday_entry.get()
        address = address_entry.get()
        if not contact_name or not contact_surname:
            messagebox.showwarning("Warning", "Please enter contact name and surname")
            return None
        qr = qrcode.make(f"BEGIN:VCARD\nFN:{contact_name} {contact_surname}\nORG:{company}\nTEL:{phone}\nEMAIL:{email}\nBDAY:{birthday}\nADR:{address}\nEND:VCARD")
        qr_info = f"Contact: {contact_name} {contact_surname}, Phone: {phone}, Email: {email}"

    show_qr_window(qr, qr_info)  # Show QR code in a new window

def show_qr_window(qr, qr_info):
    global qr_window
    if qr_window is None or not qr_window.winfo_exists():
        qr_window = tk.Toplevel(app)
        qr_window.title("Generated QR Code")

        qr_image = ImageTk.PhotoImage(qr)
        qr_label = tk.Label(qr_window, image=qr_image)
        qr_label.image = qr_image
        qr_label.pack(padx=10, pady=10)

        info_label = tk.Label(qr_window, text=qr_info)
        info_label.pack(pady=5)

        save_button = tk.Button(qr_window, text="Save QR Code", command=lambda: save_qr(qr))
        save_button.pack(pady=10)

        # Zakomentowane wywołanie funkcji kopiowania i przycisk
        # copy_button = tk.Button(qr_window, text="Copy to Clipboard", command=lambda: copy_to_clipboard(qr))
        # copy_button.pack(pady=10)

        qr_window.protocol("WM_DELETE_WINDOW", on_close)  # Handle window close event
    else:
        qr_label = qr_window.children['!label']
        qr_image = ImageTk.PhotoImage(qr)
        qr_label.config(image=qr_image)
        qr_label.image = qr_image
        info_label = qr_window.children['!label2']
        info_label.config(text=qr_info)

def save_qr(qr):
    if qr is None:
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        qr.save(file_path)
        messagebox.showinfo("Saved", f"QR code saved as {file_path}")

def copy_to_clipboard(qr):
    if qr is None:
        return
    with io.BytesIO() as output:
        qr.save(output, format="PNG")
        data = output.getvalue()

    # Copy image to clipboard
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        root.clipboard_clear()  # Clear the clipboard
        image = Image.open(io.BytesIO(data))
        
        # Save as BMP for clipboard compatibility
        with io.BytesIO() as bmp_output:
            image.save(bmp_output, format="BMP")
            bmp_data = bmp_output.getvalue()
        
        root.clipboard_append(bmp_data)  # Append the image data to the clipboard
        root.update()  # Keep the clipboard updated
        messagebox.showinfo("Copied", "QR code copied to clipboard")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy image to clipboard: {e}")

def on_close():
    global qr_window  # Declare qr_window as global
    qr_window.destroy()  # Close the QR window
    qr_window = None  # Reset the global variable

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
    security_var = tk.StringVar(value="WPA2")
    security_options = ["WPA", "WPA2", "WPA3", "WEP", "nopass"]
    security_menu = tk.OptionMenu(wifi_tab, security_var, *security_options)

    password_label = tk.Label(wifi_tab, text="Password:")
    password_entry = tk.Entry(wifi_tab, show="*", width=40)

    def toggle_password_field(*args):
        if security_var.get() == "nopass":
            password_entry.pack_forget()
            password_label.pack_forget()
        else:
            password_label.pack(anchor=tk.W)
            password_entry.pack(anchor=tk.W, padx=5)

    security_var.trace("w", toggle_password_field)
    security_menu.pack(anchor=tk.W)
    toggle_password_field()

    # Contact Tab
    contact_tab = ttk.Frame(notebook)
    notebook.add(contact_tab, text='Contact')

    contact_label = tk.Label(contact_tab, text="Contact Name:")
    contact_label.pack(anchor=tk.W)
    contact_entry = tk.Entry(contact_tab, width=40)
    contact_entry.pack(anchor=tk.W, padx=5)

    surname_label = tk.Label(contact_tab, text="Surname:")
    surname_label.pack(anchor=tk.W)
    surname_entry = tk.Entry(contact_tab, width=40)
    surname_entry.pack(anchor=tk.W, padx=5)

    company_label = tk.Label(contact_tab, text="Company:")
    company_label.pack(anchor=tk.W)
    company_entry = tk.Entry(contact_tab, width=40)
    company_entry.pack(anchor=tk.W, padx=5)

    phone_label = tk.Label(contact_tab, text="Phone:")
    phone_label.pack(anchor=tk.W)
    phone_entry = tk.Entry(contact_tab, width=40)
    phone_entry.pack(anchor=tk.W, padx=5)

    email_label = tk.Label(contact_tab, text="Email:")
    email_label.pack(anchor=tk.W)
    email_entry = tk.Entry(contact_tab, width=40)
    email_entry.pack(anchor=tk.W, padx=5)

    birthday_label = tk.Label(contact_tab, text="Birthday (YYYY-MM-DD):")
    birthday_label.pack(anchor=tk.W)
    birthday_entry = tk.Entry(contact_tab, width=40)
    birthday_entry.pack(anchor=tk.W, padx=5)

    address_label = tk.Label(contact_tab, text="Address:")
    address_label.pack(anchor=tk.W)
    address_entry = tk.Entry(contact_tab, width=40)
    address_entry.pack(anchor=tk.W, padx=5)

    generate_button = tk.Button(app, text="Generate", command=generate_qr)
    generate_button.pack(pady=10)

    app.mainloop()
