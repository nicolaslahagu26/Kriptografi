import tkinter as tk
from tkinter import ttk, messagebox
import itertools, math

BG, PRIMARY, ACCENT, WHITE, TEXT = "#f0fff4", "#006d77", "#83c5be", "#ffffff", "#1a1a1a"

def hitung():
    try:
        jenis = combo.get()
        hasil.delete(1.0, tk.END)

        if jenis == "Hitung Jumlah Kombinasi C(n, r)":
            n = int(entry_n.get())
            r = int(entry_r.get())
            hasil.insert(tk.END, f"Jumlah Kombinasi C({n},{r}) = {math.comb(n, r)}")
        elif jenis == "Tampilkan Kombinasi Huruf":
            huruf = entry_huruf.get().split()
            r = int(entry_r.get())
            out = list(itertools.combinations(huruf, r))
            hasil.insert(tk.END, f"Total Kombinasi: {len(out)}\n\n")
            for h in out:
                hasil.insert(tk.END, f"{h}\n")
        else:
            messagebox.showwarning("Peringatan", "Pilih jenis kombinasi!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear():
    entry_n.delete(0, tk.END)
    entry_n.insert(0, "Masukkan n...")
    entry_r.delete(0, tk.END)
    entry_r.insert(0, "Masukkan r...")
    entry_huruf.delete(0, tk.END)
    entry_huruf.insert(0, "Masukkan huruf (pisah spasi)...")
    hasil.delete(1.0, tk.END)
    for e in (entry_n, entry_r, entry_huruf):
        e.config(fg="gray")

def on_entry_click(e):
    e.widget.delete(0, tk.END)
    e.widget.config(fg=TEXT)

def on_focusout(e):
    if not e.widget.get():
        if e.widget == entry_n:
            e.widget.insert(0, "Masukkan n...")
        elif e.widget == entry_r:
            e.widget.insert(0, "Masukkan r...")
        else:
            e.widget.insert(0, "Masukkan huruf (pisah spasi)...")
        e.widget.config(fg="gray")

root = tk.Tk()
root.title("🎲 Bab III – Kombinasi")
root.geometry("560x460")
root.config(bg=BG)

tk.Label(root, text="KOMBINASI", font=("Arial Rounded MT Bold", 18),
         fg=PRIMARY, bg=BG).pack(pady=15)

combo = ttk.Combobox(root, values=[
    "Hitung Jumlah Kombinasi C(n, r)",
    "Tampilkan Kombinasi Huruf"
])
combo.set("Pilih jenis kombinasi")
combo.pack(fill="x", padx=40, pady=5)

entry_n = tk.Entry(root, font=("Consolas", 12), fg="gray", justify="center", relief="solid")
entry_n.insert(0, "Masukkan n...")
entry_n.bind("<FocusIn>", on_entry_click)
entry_n.bind("<FocusOut>", on_focusout)
entry_n.pack(fill="x", padx=40, pady=5, ipady=5)

entry_r = tk.Entry(root, font=("Consolas", 12), fg="gray", justify="center", relief="solid")
entry_r.insert(0, "Masukkan r...")
entry_r.bind("<FocusIn>", on_entry_click)
entry_r.bind("<FocusOut>", on_focusout)
entry_r.pack(fill="x", padx=40, pady=5, ipady=5)

entry_huruf = tk.Entry(root, font=("Consolas", 12), fg="gray", justify="center", relief="solid")
entry_huruf.insert(0, "Masukkan huruf (pisah spasi)...")
entry_huruf.bind("<FocusIn>", on_entry_click)
entry_huruf.bind("<FocusOut>", on_focusout)
entry_huruf.pack(fill="x", padx=40, pady=5, ipady=5)

btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Hitung", command=hitung, bg=ACCENT, fg=WHITE,
          font=("Arial", 10, "bold"), relief="flat", width=12, cursor="hand2").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Clear", command=clear, bg="#ef476f", fg=WHITE,
          font=("Arial", 10, "bold"), relief="flat", width=12, cursor="hand2").grid(row=0, column=1, padx=5)

hasil = tk.Text(root, font=("Consolas", 11), bg=WHITE, fg=TEXT, wrap="word", relief="solid", bd=1)
hasil.pack(fill="both", padx=40, pady=10, expand=True)

root.mainloop()
