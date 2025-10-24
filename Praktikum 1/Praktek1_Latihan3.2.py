import tkinter as tk
from tkinter import ttk, messagebox

# ========== Fungsi Hover Effect ==========
def on_enter(e):
    e.widget['background'] = "#4a90e2"   # warna hover
    e.widget['foreground'] = "white"

def on_leave(e):
    e.widget['background'] = "#ffffff"   # warna normal
    e.widget['foreground'] = "#333333"

# ========== LATIHAN 1 ==========
def latihan1():
    win = tk.Toplevel(root)
    win.title("Latihan 1 - Aritmatika")
    win.geometry("400x300")
    win.configure(bg="#f9f9f9")

    def hitung():
        try:
            a = float(entry1.get())
            b = float(entry2.get())
            hasil = f"""
            Penjumlahan: {a+b}
            Pengurangan: {a-b}
            Perkalian  : {a*b}
            Pembagian  : {a/b if b!=0 else "Error"}
            """
            messagebox.showinfo("Hasil Perhitungan", hasil)
        except:
            messagebox.showerror("Error", "Masukkan angka yang benar!")

    tk.Label(win, text="Latihan 1 - Aritmatika", bg="#f9f9f9",
             font=("Segoe UI", 14, "bold")).pack(pady=10)

    frame = tk.Frame(win, bg="#f9f9f9")
    frame.pack(pady=20)

    tk.Label(frame, text="Angka 1:", bg="#f9f9f9").grid(row=0, column=0, pady=5, sticky="e")
    entry1 = tk.Entry(frame, width=15)
    entry1.grid(row=0, column=1)

    tk.Label(frame, text="Angka 2:", bg="#f9f9f9").grid(row=1, column=0, pady=5, sticky="e")
    entry2 = tk.Entry(frame, width=15)
    entry2.grid(row=1, column=1)

    ttk.Button(win, text="Hitung", command=hitung).pack(pady=10)

# ========== LATIHAN 2 ==========
def latihan2():
    win = tk.Toplevel(root)
    win.title("Latihan 2 - Kalkulator")
    win.geometry("400x300")
    win.configure(bg="#f0f8ff")

    def kalkulator():
        try:
            a = float(entry1.get())
            b = float(entry2.get())
            op = operator.get()
            if op == '+': hasil = a+b
            elif op == '-': hasil = a-b
            elif op == '*': hasil = a*b
            elif op == '/': hasil = "Error (bagi 0)" if b==0 else a/b
            else: hasil = "Salah operator"
            lbl_hasil.config(text=f"Hasil: {hasil}")
        except:
            lbl_hasil.config(text="Input salah!")

    tk.Label(win, text="Latihan 2 - Kalkulator", bg="#f0f8ff",
             font=("Segoe UI", 14, "bold")).pack(pady=10)

    frame = tk.Frame(win, bg="#f0f8ff")
    frame.pack(pady=20)

    tk.Label(frame, text="Angka 1:", bg="#f0f8ff").grid(row=0, column=0, pady=5, sticky="e")
    entry1 = tk.Entry(frame, width=10); entry1.grid(row=0, column=1)

    tk.Label(frame, text="Angka 2:", bg="#f0f8ff").grid(row=1, column=0, pady=5, sticky="e")
    entry2 = tk.Entry(frame, width=10); entry2.grid(row=1, column=1)

    tk.Label(frame, text="Operator:", bg="#f0f8ff").grid(row=2, column=0, pady=5, sticky="e")
    operator = ttk.Combobox(frame, values=["+", "-", "*", "/"], width=7)
    operator.grid(row=2, column=1); operator.current(0)

    ttk.Button(win, text="Hitung", command=kalkulator).pack(pady=10)
    lbl_hasil = tk.Label(win, text="Hasil: -", bg="#f0f8ff", font=("Segoe UI", 12, "bold"))
    lbl_hasil.pack(pady=10)

# ========== LATIHAN 3 ==========
def latihan3():
    win = tk.Toplevel(root)
    win.title("Latihan 3 - Nilai Akhir")
    win.geometry("420x400")
    win.configure(bg="#f5fff5")

    def hitung_nilai_akhir(sikap, tugas, uts, uas):
        return (sikap*0.10)+(tugas*0.30)+(uts*0.25)+(uas*0.35)

    def konversi_nilai(nilai):
        if 81 <= nilai <= 100: return "A", 4
        elif 76 <= nilai <= 80: return "B+", 3.5
        elif 71 <= nilai <= 75: return "B", 3
        elif 66 <= nilai <= 70: return "C+", 2.5
        elif 56 <= nilai <= 65: return "C", 2
        elif 46 <= nilai <= 55: return "D", 1
        else: return "E", 0

    def proses_hitung():
        try:
            sikap = float(entry_sikap.get())
            tugas = float(entry_tugas.get())
            uts = float(entry_uts.get())
            uas = float(entry_uas.get())
            total = hitung_nilai_akhir(sikap, tugas, uts, uas)
            huruf, bobot = konversi_nilai(total)
            ket = "Lulus" if total>=56 else "Tidak Lulus"
            lbl_total.config(text=f"Total: {total:.2f}")
            lbl_huruf.config(text=f"Huruf: {huruf}")
            lbl_bobot.config(text=f"Bobot: {bobot}")
            lbl_ket.config(text=f"Keterangan: {ket}", fg="green" if ket=="Lulus" else "red")
        except:
            lbl_total.config(text="Total: -")
            lbl_ket.config(text="Error input!", fg="red")

    tk.Label(win, text="Latihan 3 - Form Nilai Akhir", bg="#f5fff5",
             font=("Segoe UI", 14, "bold")).pack(pady=10)

    frame = tk.Frame(win, bg="#f5fff5")
    frame.pack(pady=20)

    tk.Label(frame, text="Sikap (10%)", bg="#f5fff5").grid(row=0, column=0, pady=5, sticky="w")
    entry_sikap = tk.Entry(frame, width=10); entry_sikap.grid(row=0, column=1)

    tk.Label(frame, text="Tugas (30%)", bg="#f5fff5").grid(row=1, column=0, pady=5, sticky="w")
    entry_tugas = tk.Entry(frame, width=10); entry_tugas.grid(row=1, column=1)

    tk.Label(frame, text="UTS (25%)", bg="#f5fff5").grid(row=2, column=0, pady=5, sticky="w")
    entry_uts = tk.Entry(frame, width=10); entry_uts.grid(row=2, column=1)

    tk.Label(frame, text="UAS (35%)", bg="#f5fff5").grid(row=3, column=0, pady=5, sticky="w")
    entry_uas = tk.Entry(frame, width=10); entry_uas.grid(row=3, column=1)

    ttk.Button(win, text="Hitung Nilai", command=proses_hitung).pack(pady=10)

    lbl_total = tk.Label(win, text="Total: -", bg="#f5fff5", font=("Segoe UI", 11, "bold")); lbl_total.pack()
    lbl_huruf = tk.Label(win, text="Huruf: -", bg="#f5fff5", font=("Segoe UI", 11, "bold")); lbl_huruf.pack()
    lbl_bobot = tk.Label(win, text="Bobot: -", bg="#f5fff5", font=("Segoe UI", 11, "bold")); lbl_bobot.pack()
    lbl_ket = tk.Label(win, text="Keterangan: -", bg="#f5fff5", font=("Segoe UI", 11, "bold")); lbl_ket.pack()

# ========== MENU UTAMA ==========
root = tk.Tk()
root.title("Menu Utama - Latihan Python")
root.geometry("450x450")
root.configure(bg="#ddeeff")

tk.Label(root, text="PROGRAM LATIHAN PYTHON", font=("Segoe UI", 18, "bold"),
         bg="#ddeeff", fg="#333").pack(pady=30)

# Style tombol custom
def buat_tombol(teks, perintah):
    btn = tk.Button(root, text=teks, font=("Segoe UI", 12, "bold"),
                    bg="white", fg="#333333", relief="raised", bd=2,
                    command=perintah, cursor="hand2")
    btn.pack(pady=12, ipadx=10, ipady=5, fill="x", padx=80)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

buat_tombol("Latihan 1 - Aritmatika", latihan1)
buat_tombol("Latihan 2 - Kalkulator", latihan2)
buat_tombol("Latihan 3 - Form Nilai", latihan3)
buat_tombol("Keluar", root.quit)

root.mainloop()
