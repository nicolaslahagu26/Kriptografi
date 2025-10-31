import tkinter as tk
from tkinter import ttk, messagebox

def transposisi_cipher(plaintext):
    if len(plaintext) < 4:
        messagebox.showerror("❌ Error", "Teks terlalu pendek! Minimal 4 karakter.")
        return "", []
    part_length = len(plaintext) // 4
    parts = [plaintext[i:i + part_length] for i in range(0, len(plaintext), part_length)]
    
    ciphertext = ""
    for col in range(4):
        for part in parts:
            if col < len(part):
                ciphertext += part[col]
    return ciphertext, parts

def enkripsi():
    plaintext = entry_plaintext.get().upper().strip()
    if plaintext in ("MASUKKAN PLAINTEXT...", ""):
        messagebox.showwarning("⚠️ Peringatan", "Masukkan teks terlebih dahulu!")
        return

    ciphertext, parts = transposisi_cipher(plaintext)
    entry_ciphertext.config(state='normal')
    entry_ciphertext.delete(0, tk.END)
    entry_ciphertext.insert(0, ciphertext)
    entry_ciphertext.config(state='readonly')

    text_detail.config(state='normal')
    text_detail.delete(1.0, tk.END)
    text_detail.insert(tk.END, "🔹 PEMBENTUKAN BLOK:\n", "judul")
    for i, part in enumerate(parts):
        text_detail.insert(tk.END, f"   Bagian {i+1}: {part}\n", "isi")
    text_detail.insert(tk.END, "\n🔹 HASIL ENKRIPSI:\n", "judul")
    text_detail.insert(tk.END, f"   {ciphertext}", "hasil")
    text_detail.config(state='disabled')

def clear():
    entry_plaintext.config(foreground="gray")
    entry_plaintext.delete(0, tk.END)
    entry_plaintext.insert(0, "Masukkan plaintext...")
    entry_ciphertext.config(state='normal')
    entry_ciphertext.delete(0, tk.END)
    entry_ciphertext.config(state='readonly')
    text_detail.config(state='normal')
    text_detail.delete(1.0, tk.END)
    text_detail.config(state='disabled')

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
root.title("🔄 Transposisi Cipher")
root.geometry("640x450")
root.resizable(False, False)
root.configure(bg="#e9f0ff")

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
    text="🔄 Transposisi Cipher",
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

btn_frame = tk.Frame(main_frame, bg="white")
btn_frame.grid(row=1, column=0, columnspan=2, pady=10)

btn_enkripsi = ttk.Button(btn_frame, text="🔐 Enkripsi", command=enkripsi)
btn_enkripsi.grid(row=0, column=0, padx=10)

btn_clear = ttk.Button(btn_frame, text="🧹 Clear", command=clear)
btn_clear.grid(row=0, column=1, padx=10)

lbl_cipher = tk.Label(main_frame, text="Hasil Ciphertext:", bg="white", font=("Segoe UI", 10))
lbl_cipher.grid(row=2, column=0, padx=10, pady=8, sticky="w")

entry_ciphertext = ttk.Entry(main_frame, width=50, state='readonly', foreground="blue")
entry_ciphertext.grid(row=2, column=1, padx=10, pady=8)

lbl_detail = tk.Label(main_frame, text="Detail Proses:", bg="white", font=("Segoe UI", 10))
lbl_detail.grid(row=3, column=0, padx=10, pady=8, sticky="nw")

text_detail = tk.Text(main_frame, width=50, height=8, bg="#f1f5fb", fg="#222", state='disabled', font=("Consolas", 10))
text_detail.grid(row=3, column=1, padx=10, pady=8)
text_detail.tag_config("judul", font=("Segoe UI", 10, "bold"), foreground="#005a9e")
text_detail.tag_config("isi", font=("Consolas", 10))
text_detail.tag_config("hasil", font=("Consolas", 10, "bold"), foreground="blue")

root.mainloop()
