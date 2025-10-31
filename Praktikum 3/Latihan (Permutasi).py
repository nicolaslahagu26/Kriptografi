import tkinter as tk
from tkinter import ttk, messagebox
import itertools

BG, PRIMARY, ACCENT, WHITE, TEXT = "#f9f0ff", "#5a189a", "#9d4edd", "#ffffff", "#1a1a1a"

def hitung():
    try:
        jenis = combo.get()
        data = entry_data.get().split()
        if not data or data == [entry_data.placeholder]:
            messagebox.showwarning("Peringatan", "Masukkan data terlebih dahulu!")
            return
        hasil.delete(1.0, tk.END)

        if jenis == "Permutasi Menyeluruh":
            out = list(itertools.permutations(data))
        elif jenis == "Permutasi Sebagian":
            k = int(entry_k.get())
            out = list(itertools.permutations(data, k))
        elif jenis == "Permutasi Keliling":
            pertama = data[0]
            out = [[pertama] + list(p) for p in itertools.permutations(data[1:])]
        elif jenis == "Mengatur n buku di r bagian rak":
            n, r = map(int, data)
            hasil.insert(tk.END, f"Jumlah cara = {r ** n}")
            return
        else:
            messagebox.showwarning("Peringatan", "Pilih jenis permutasi!")
            return

        hasil.insert(tk.END, f"Total Permutasi: {len(out)}\n\n")
        for h in out:
            hasil.insert(tk.END, f"{h}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear():
    entry_data.delete(0, tk.END)
    entry_data.insert(0, entry_data.placeholder)
    entry_data.config(fg="gray")
    entry_k.delete(0, tk.END)
    entry_k.insert(0, "Masukkan k (jika perlu)")
    entry_k.config(fg="gray")
    hasil.delete(1.0, tk.END)

def on_entry_click(e):
    if e.widget.get() in (e.widget.placeholder, "Masukkan k (jika perlu)"):
        e.widget.delete(0, tk.END)
        e.widget.config(fg=TEXT)

def on_focusout(e):
    if not e.widget.get():
        ph = e.widget.placeholder if hasattr(e.widget, "placeholder") else "Masukkan k (jika perlu)"
        e.widget.insert(0, ph)
        e.widget.config(fg="gray")

root = tk.Tk()
root.title("🔄 Bab II – Permutasi")
root.geometry("600x470")
root.config(bg=BG)

tk.Label(root, text="PERMUTASI", font=("Arial Rounded MT Bold", 18),
         fg=PRIMARY, bg=BG).pack(pady=15)

combo = ttk.Combobox(root, values=[
    "Permutasi Menyeluruh",
    "Permutasi Sebagian",
    "Permutasi Keliling",
    "Mengatur n buku di r bagian rak"
])
combo.set("Pilih jenis permutasi")
combo.pack(fill="x", padx=40, pady=5)

entry_data = tk.Entry(root, font=("Consolas", 12), fg="gray", justify="center", relief="solid")
entry_data.placeholder = "Masukkan elemen (pisah spasi) atau n r..."
entry_data.insert(0, entry_data.placeholder)
entry_data.bind("<FocusIn>", on_entry_click)
entry_data.bind("<FocusOut>", on_focusout)
entry_data.pack(fill="x", padx=40, pady=5, ipady=5)

entry_k = tk.Entry(root, font=("Consolas", 12), fg="gray", justify="center", relief="solid")
entry_k.insert(0, "Masukkan k (jika perlu)")
entry_k.bind("<FocusIn>", on_entry_click)
entry_k.bind("<FocusOut>", on_focusout)
entry_k.pack(fill="x", padx=40, pady=5, ipady=5)

btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Hitung", command=hitung, bg=ACCENT, fg=WHITE,
          font=("Arial", 10, "bold"), relief="flat", width=12, cursor="hand2").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Clear", command=clear, bg="#ef476f", fg=WHITE,
          font=("Arial", 10, "bold"), relief="flat", width=12, cursor="hand2").grid(row=0, column=1, padx=5)

hasil = tk.Text(root, font=("Consolas", 11), bg=WHITE, fg=TEXT, wrap="word", relief="solid", bd=1)
hasil.pack(fill="both", padx=40, pady=10, expand=True)

root.mainloop()
