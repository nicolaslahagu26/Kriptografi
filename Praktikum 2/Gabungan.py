import tkinter as tk
from tkinter import ttk, messagebox

# === Fungsi Latihan 1: Pengulangan Perhitungan ===
def hitung_pengulangan():
    try:
        a = float(entry_a1.get())
        b = float(entry_b1.get())
        c = a + b
        label_hasil1.config(text=f"Hasil: {c}")
    except ValueError:
        messagebox.showerror("Error", "Masukkan angka yang valid!")

def reset_lat1():
    entry_a1.delete(0, tk.END)
    entry_b1.delete(0, tk.END)
    label_hasil1.config(text="Hasil:")

# === Fungsi Latihan 2: Kalkulator Sederhana ===
def hitung_kalkulator():
    try:
        a = float(entry_a2.get())
        b = float(entry_b2.get())
        op = entry_op.get().strip()
        if op == "+":
            hasil = a + b
        elif op == "-":
            hasil = a - b
        elif op == "*":
            hasil = a * b
        elif op == "/":
            hasil = "Error: Pembagian dengan nol!" if b == 0 else a / b
        else:
            hasil = "Operator tidak valid!"
        label_hasil2.config(text=f"Hasil: {hasil}")
    except ValueError:
        messagebox.showerror("Error", "Masukkan angka yang valid!")

def reset_lat2():
    entry_a2.delete(0, tk.END)
    entry_b2.delete(0, tk.END)
    entry_op.delete(0, tk.END)
    label_hasil2.config(text="Hasil:")

# === Fungsi Latihan 3: If Logika Kombinasi ===
def cek_logika():
    try:
        x = int(entry_x.get())
        y = int(entry_y.get())
        z = int(entry_z.get())

        hasil = []
        hasil.append("x berada di antara 18 dan 30" if 18 <= x <= 30 else "x tidak berada di antara 18 dan 30")
        hasil.append("y berada di luar rentang 10 hingga 20" if y < 10 or y > 20 else "y berada di dalam rentang 10 hingga 20")
        hasil.append("z sama dengan 5" if z == 5 else "z tidak sama dengan 5")
        hasil.append("x tidak sama dengan y" if x != y else "x sama dengan y")
        hasil.append("x lebih besar dari y" if x > y else "x tidak lebih besar dari y")
        hasil.append("z lebih kecil dari y" if z < y else "z tidak lebih kecil dari y")
        if y >= 15 and z <= 5:
            hasil.append("y lebih besar atau sama dengan 15, dan z lebih kecil atau sama dengan 5")

        text_hasil3.config(state="normal")
        text_hasil3.delete("1.0", tk.END)
        text_hasil3.insert(tk.END, "\n".join(hasil))
        text_hasil3.config(state="disabled")
    except ValueError:
        messagebox.showerror("Error", "Masukkan angka yang valid!")

def reset_lat3():
    entry_x.delete(0, tk.END)
    entry_y.delete(0, tk.END)
    entry_z.delete(0, tk.END)
    text_hasil3.config(state="normal")
    text_hasil3.delete("1.0", tk.END)
    text_hasil3.config(state="disabled")

# === GUI Utama ===
root = tk.Tk()
root.title("Praktikum 2 - Operator, If, dan Perulangan")
root.geometry("700x600")
root.config(bg="#e9edf5")

# Judul
judul = tk.Label(root, text="PRAKTIKUM 2 - OPERATOR, IF, DAN PERULANGAN",
                 font=("Segoe UI", 14, "bold"), bg="#e9edf5", fg="#2c3e50")
judul.pack(pady=15)

# Notebook (Tab)
style = ttk.Style()
style.configure("TNotebook.Tab", padding=[15, 8], font=("Segoe UI", 10))
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=15, pady=10)

# === LATIHAN 1 ===
frame1 = tk.Frame(notebook, bg="#ffffff")
notebook.add(frame1, text="Latihan 1 - Pengulangan")

tk.Label(frame1, text="Masukkan Nilai A:", bg="#ffffff", font=("Segoe UI", 11)).pack(pady=8)
entry_a1 = tk.Entry(frame1, font=("Segoe UI", 11), width=20, justify="center")
entry_a1.pack()

tk.Label(frame1, text="Masukkan Nilai B:", bg="#ffffff", font=("Segoe UI", 11)).pack(pady=8)
entry_b1 = tk.Entry(frame1, font=("Segoe UI", 11), width=20, justify="center")
entry_b1.pack()

frame1_btn = tk.Frame(frame1, bg="#ffffff")
frame1_btn.pack(pady=15)
tk.Button(frame1_btn, text="Hitung", command=hitung_pengulangan, bg="#4CAF50", fg="white",
          font=("Segoe UI", 10, "bold"), width=12).grid(row=0, column=0, padx=5)
tk.Button(frame1_btn, text="Reset", command=reset_lat1, bg="#E74C3C", fg="white",
          font=("Segoe UI", 10, "bold"), width=12).grid(row=0, column=1, padx=5)

label_hasil1 = tk.Label(frame1, text="Hasil:", bg="#ffffff", font=("Segoe UI", 12, "bold"), fg="#2c3e50")
label_hasil1.pack(pady=15)

# === LATIHAN 2 ===
frame2 = tk.Frame(notebook, bg="#ffffff")
notebook.add(frame2, text="Latihan 2 - Kalkulator")

tk.Label(frame2, text="Masukkan Nilai A:", bg="#ffffff", font=("Segoe UI", 11)).pack(pady=8)
entry_a2 = tk.Entry(frame2, font=("Segoe UI", 11), width=20, justify="center")
entry_a2.pack()

tk.Label(frame2, text="Masukkan Nilai B:", bg="#ffffff", font=("Segoe UI", 11)).pack(pady=8)
entry_b2 = tk.Entry(frame2, font=("Segoe UI", 11), width=20, justify="center")
entry_b2.pack()

tk.Label(frame2, text="Masukkan Operator (+, -, *, /):", bg="#ffffff", font=("Segoe UI", 11)).pack(pady=8)
entry_op = tk.Entry(frame2, font=("Segoe UI", 11), width=10, justify="center")
entry_op.pack()

frame2_btn = tk.Frame(frame2, bg="#ffffff")
frame2_btn.pack(pady=15)
tk.Button(frame2_btn, text="Hitung", command=hitung_kalkulator, bg="#2196F3", fg="white",
          font=("Segoe UI", 10, "bold"), width=12).grid(row=0, column=0, padx=5)
tk.Button(frame2_btn, text="Reset", command=reset_lat2, bg="#E74C3C", fg="white",
          font=("Segoe UI", 10, "bold"), width=12).grid(row=0, column=1, padx=5)

label_hasil2 = tk.Label(frame2, text="Hasil:", bg="#ffffff", font=("Segoe UI", 12, "bold"), fg="#2c3e50")
label_hasil2.pack(pady=15)

# === LATIHAN 3 ===
frame3 = tk.Frame(notebook, bg="#ffffff")
notebook.add(frame3, text="Latihan 3 - Logika If")

for label_text, var_name in [("Masukkan Nilai X:", "entry_x"),
                             ("Masukkan Nilai Y:", "entry_y"),
                             ("Masukkan Nilai Z:", "entry_z")]:
    tk.Label(frame3, text=label_text, bg="#ffffff", font=("Segoe UI", 11)).pack(pady=5)
    globals()[var_name] = tk.Entry(frame3, font=("Segoe UI", 11), width=20, justify="center")
    globals()[var_name].pack()

frame3_btn = tk.Frame(frame3, bg="#ffffff")
frame3_btn.pack(pady=15)
tk.Button(frame3_btn, text="Cek Logika", command=cek_logika, bg="#FF9800", fg="white",
          font=("Segoe UI", 10, "bold"), width=12).grid(row=0, column=0, padx=5)
tk.Button(frame3_btn, text="Reset", command=reset_lat3, bg="#E74C3C", fg="white",
          font=("Segoe UI", 10, "bold"), width=12).grid(row=0, column=1, padx=5)

text_hasil3 = tk.Text(frame3, height=10, width=70, font=("Consolas", 10))
text_hasil3.pack(pady=10)
text_hasil3.config(state="disabled", bg="#f4f6f7")

# Tombol keluar di bawah
tk.Button(root, text="Keluar Program", command=root.destroy, bg="#2c3e50", fg="white",
          font=("Segoe UI", 11, "bold"), width=20, relief="raised").pack(pady=15)

root.mainloop()
