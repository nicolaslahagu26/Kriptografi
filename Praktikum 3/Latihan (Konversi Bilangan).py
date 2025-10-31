import tkinter as tk
from tkinter import ttk, messagebox

BG, PRIMARY, ACCENT, WHITE, TEXT = "#e7f0ff", "#264653", "#2a9d8f", "#ffffff", "#1a1a1a"

def konversi():
    try:
        jenis = combo.get()
        nilai = entry.get().strip()
        if not nilai or nilai == entry.placeholder:
            messagebox.showwarning("Peringatan", "Masukkan nilai terlebih dahulu!")
            return
        hasil.delete(1.0, tk.END)

        if jenis == "Desimal ke Biner, Oktal, Heksadesimal":
            d = int(nilai)
            hasil.insert(tk.END, f"Desimal      : {d}\nBiner        : {bin(d)[2:]}\n"
                                 f"Oktal        : {oct(d)[2:]}\nHeksadesimal : {hex(d)[2:].upper()}")
        elif jenis == "Biner ke Desimal dan Heksadesimal":
            d = int(nilai, 2)
            hasil.insert(tk.END, f"Biner : {nilai}\nDesimal : {d}\nHeksadesimal : {hex(d)[2:].upper()}")
        elif jenis == "Oktal ke Desimal, Biner, dan Heksadesimal":
            d = int(nilai, 8)
            hasil.insert(tk.END, f"Oktal : {nilai}\nDesimal : {d}\nBiner : {bin(d)[2:]}\nHeksadesimal : {hex(d)[2:].upper()}")
        elif jenis == "Heksadesimal ke Desimal, Biner, dan Oktal":
            d = int(nilai, 16)
            hasil.insert(tk.END, f"Heksadesimal : {nilai.upper()}\nDesimal : {d}\nBiner : {bin(d)[2:]}\nOktal : {oct(d)[2:]}")
        else:
            messagebox.showwarning("Peringatan", "Pilih jenis konversi!")
    except ValueError:
        messagebox.showerror("Error", "Masukkan angka yang valid!")

def clear():
    entry.delete(0, tk.END)
    entry.insert(0, entry.placeholder)
    entry.config(fg="gray")
    hasil.delete(1.0, tk.END)

def on_focus_in(event):
    if entry.get() == entry.placeholder:
        entry.delete(0, tk.END)
        entry.config(fg=TEXT)

def on_focus_out(event):
    if not entry.get():
        entry.insert(0, entry.placeholder)
        entry.config(fg="gray")

root = tk.Tk()
root.title("🔢 Bab I – Konversi Bilangan")
root.geometry("520x420")
root.config(bg=BG)

tk.Label(root, text="KONVERSI BILANGAN", font=("Arial Rounded MT Bold", 18),
         fg=PRIMARY, bg=BG).pack(pady=15)

combo = ttk.Combobox(root, values=[
    "Desimal ke Biner, Oktal, Heksadesimal",
    "Biner ke Desimal dan Heksadesimal",
    "Oktal ke Desimal, Biner, dan Heksadesimal",
    "Heksadesimal ke Desimal, Biner, dan Oktal"
])
combo.set("Pilih jenis konversi")
combo.pack(fill="x", padx=40, pady=5)

entry = tk.Entry(root, font=("Consolas", 12), fg="gray", justify="center", relief="solid")
entry.placeholder = "Masukkan nilai bilangan..."
entry.insert(0, entry.placeholder)
entry.bind("<FocusIn>", on_focus_in)
entry.bind("<FocusOut>", on_focus_out)
entry.pack(fill="x", padx=40, pady=10, ipady=5)

btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Konversi", command=konversi, bg=ACCENT, fg=WHITE,
          font=("Arial", 10, "bold"), relief="flat", width=12, cursor="hand2").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Clear", command=clear, bg="#ef476f", fg=WHITE,
          font=("Arial", 10, "bold"), relief="flat", width=12, cursor="hand2").grid(row=0, column=1, padx=5)

hasil = tk.Text(root, height=10, font=("Consolas", 11), bg=WHITE, fg=TEXT, wrap="word", relief="solid", bd=1)
hasil.pack(fill="both", padx=40, pady=15, expand=True)

root.mainloop()
