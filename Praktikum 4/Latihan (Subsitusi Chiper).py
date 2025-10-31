import tkinter as tk
from tkinter import ttk, messagebox

def substitusi_cipher(plaintext, aturan):
    ciphertext = ''
    for char in plaintext.upper():
        if char in aturan:
            ciphertext += aturan[char]
        else:
            ciphertext += char
    return ciphertext

def enkripsi():
    plaintext = entry_plaintext.get().upper().strip()
    aturan_input = entry_aturan.get().upper().strip()

    if plaintext in ("MASUKKAN PLAINTEXT...", "") or aturan_input in ("MASUKKAN ATURAN SUBSTITUSI...", ""):
        messagebox.showwarning("⚠️ Peringatan", "Mohon isi plaintext dan aturan substitusi!")
        return

    aturan = {}
    try:
        for pair in aturan_input.split(','):
            k, v = pair.split(':')
            aturan[k.strip()] = v.strip()
    except:
        messagebox.showerror("❌ Error", "Format aturan salah!\nGunakan format: U:K,N:N,I:I,K:K,A:B")
        return

    ciphertext = substitusi_cipher(plaintext, aturan)
    entry_ciphertext.config(state='normal')
    entry_ciphertext.delete(0, tk.END)
    entry_ciphertext.insert(0, ciphertext)
    entry_ciphertext.config(state='readonly')

def clear():
    for e, placeholder in [(entry_plaintext, "Masukkan plaintext..."),
                           (entry_aturan, "Masukkan aturan substitusi...")]:
        e.config(foreground="gray")
        e.delete(0, tk.END)
        e.insert(0, placeholder)
    entry_ciphertext.config(state='normal')
    entry_ciphertext.delete(0, tk.END)
    entry_ciphertext.config(state='readonly')

def set_placeholder(entry, text):
    entry.insert(0, text)
    entry.config(foreground="gray")

    def on_focus_in(event):
        if entry.get() == text:
            entry.delete(0, tk.END)
            entry.config(foreground="black")

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, text)
            entry.config(foreground="gray")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

root = tk.Tk()
root.title("🔐 Substitusi Cipher")
root.geometry("580x400")
root.resizable(False, False)
root.configure(bg="#e8f0fe")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton",
                font=("Segoe UI", 10, "bold"),
                padding=8,
                background="#0078D7",
                foreground="white")
style.map("TButton",
          background=[("active", "#005a9e")])

header_frame = tk.Frame(root, bg="#0078D7")
header_frame.pack(fill="x")

header_label = tk.Label(
    header_frame,
    text="🔐 Substitusi Cipher",
    font=("Segoe UI", 16, "bold"),
    bg="#0078D7",
    fg="white",
    pady=10
)
header_label.pack()

main_frame = tk.Frame(root, bg="white", bd=0, relief="ridge")
main_frame.pack(padx=25, pady=25, fill="both", expand=True)

lbl_plaintext = tk.Label(main_frame, text="Masukkan Plaintext:", bg="white", font=("Segoe UI", 10))
lbl_plaintext.grid(row=0, column=0, padx=10, pady=10, sticky="w")

entry_plaintext = ttk.Entry(main_frame, width=50)
entry_plaintext.grid(row=0, column=1, padx=10, pady=10)
set_placeholder(entry_plaintext, "Masukkan plaintext...")

lbl_aturan = tk.Label(main_frame, text="Aturan Substitusi:", bg="white", font=("Segoe UI", 10))
lbl_aturan.grid(row=1, column=0, padx=10, pady=10, sticky="w")

entry_aturan = ttk.Entry(main_frame, width=50)
entry_aturan.grid(row=1, column=1, padx=10, pady=10)
set_placeholder(entry_aturan, "Masukkan aturan substitusi... (contoh: U:K,N:N,I:I,K:K,A:B)")

btn_frame = tk.Frame(main_frame, bg="white")
btn_frame.grid(row=2, column=0, columnspan=2, pady=15)

btn_enkripsi = ttk.Button(btn_frame, text="🔒 Enkripsi", command=enkripsi)
btn_enkripsi.grid(row=0, column=0, padx=10)

btn_clear = ttk.Button(btn_frame, text="🧹 Clear", command=clear)
btn_clear.grid(row=0, column=1, padx=10)

lbl_cipher = tk.Label(main_frame, text="Hasil Ciphertext:", bg="white", font=("Segoe UI", 10))
lbl_cipher.grid(row=3, column=0, padx=10, pady=10, sticky="w")

entry_ciphertext = ttk.Entry(main_frame, width=50, state='readonly', foreground="blue")
entry_ciphertext.grid(row=3, column=1, padx=10, pady=10)

root.mainloop()
