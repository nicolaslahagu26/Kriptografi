import tkinter as tk
from tkinter import ttk

# Fungsi hitung nilai akhir
def hitung_nilai_akhir(sikap, tugas, uts, uas):
    return (sikap * 0.10) + (tugas * 0.30) + (uts * 0.25) + (uas * 0.35)

# Fungsi konversi nilai ke huruf & bobot
def konversi_nilai(nilai):
    if 81 <= nilai <= 100:
        return "A", 4
    elif 76 <= nilai <= 80:
        return "B+", 3.5
    elif 71 <= nilai <= 75:
        return "B", 3
    elif 66 <= nilai <= 70:
        return "C+", 2.5
    elif 56 <= nilai <= 65:
        return "C", 2
    elif 46 <= nilai <= 55:
        return "D", 1
    else:
        return "E", 0

# Fungsi tombol hitung
def proses_hitung():
    try:
        sikap = float(entry_sikap.get())
        tugas = float(entry_tugas.get())
        uts = float(entry_uts.get())
        uas = float(entry_uas.get())

        total = hitung_nilai_akhir(sikap, tugas, uts, uas)
        huruf, bobot = konversi_nilai(total)
        keterangan = "Lulus" if total >= 56 else "Tidak Lulus"

        lbl_total.config(text=f"{total:.2f}")
        lbl_huruf.config(text=huruf)
        lbl_bobot.config(text=bobot)
        lbl_keterangan.config(text=keterangan, fg="green" if keterangan == "Lulus" else "red")

    except ValueError:
        lbl_total.config(text="-")
        lbl_huruf.config(text="-")
        lbl_bobot.config(text="-")
        lbl_keterangan.config(text="Input tidak valid!", fg="red")

# ==== GUI TKINTER ====
root = tk.Tk()
root.title("Form Nilai Akhir Akademik")
root.geometry("420x350")
root.resizable(False, False)

# Frame utama
frame = ttk.Frame(root, padding="20")
frame.pack(fill="both", expand=True)

# Input data
ttk.Label(frame, text="Nilai Sikap/Kehadiran (10%)").grid(row=0, column=0, sticky="w", pady=5)
entry_sikap = ttk.Entry(frame, width=10)
entry_sikap.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Nilai Tugas (30%)").grid(row=1, column=0, sticky="w", pady=5)
entry_tugas = ttk.Entry(frame, width=10)
entry_tugas.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Nilai UTS (25%)").grid(row=2, column=0, sticky="w", pady=5)
entry_uts = ttk.Entry(frame, width=10)
entry_uts.grid(row=2, column=1, pady=5)

ttk.Label(frame, text="Nilai UAS (35%)").grid(row=3, column=0, sticky="w", pady=5)
entry_uas = ttk.Entry(frame, width=10)
entry_uas.grid(row=3, column=1, pady=5)

# Tombol hitung
btn_hitung = ttk.Button(frame, text="Hitung Nilai Akhir", command=proses_hitung)
btn_hitung.grid(row=4, column=0, columnspan=2, pady=15)

# Hasil
ttk.Label(frame, text="Total Nilai Akhir:").grid(row=5, column=0, sticky="w", pady=5)
lbl_total = tk.Label(frame, text="-", font=("Arial", 10, "bold"))
lbl_total.grid(row=5, column=1, sticky="w", pady=5)

ttk.Label(frame, text="Nilai Huruf:").grid(row=6, column=0, sticky="w", pady=5)
lbl_huruf = tk.Label(frame, text="-", font=("Arial", 10, "bold"))
lbl_huruf.grid(row=6, column=1, sticky="w", pady=5)

ttk.Label(frame, text="Bobot:").grid(row=7, column=0, sticky="w", pady=5)
lbl_bobot = tk.Label(frame, text="-", font=("Arial", 10, "bold"))
lbl_bobot.grid(row=7, column=1, sticky="w", pady=5)

ttk.Label(frame, text="Keterangan:").grid(row=8, column=0, sticky="w", pady=5)
lbl_keterangan = tk.Label(frame, text="-", font=("Arial", 10, "bold"))
lbl_keterangan.grid(row=8, column=1, sticky="w", pady=5)

root.mainloop()
