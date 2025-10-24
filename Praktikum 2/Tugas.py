import tkinter as tk
from tkinter import messagebox

# Fungsi untuk menghitung ekspresi
def hitung():
    ekspresi = entry.get().strip()
    if not ekspresi:
        messagebox.showwarning("Peringatan", "Silakan masukkan ekspresi terlebih dahulu!")
        return
    
    try:
        hasil = eval(ekspresi)
        proses_label.config(text=f"Ekspresi yang dihitung: {ekspresi}")
        output_label.config(text=f"Output > {hasil}")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

# Membuat jendela utama
root = tk.Tk()
root.title("Kalkulator Hybrid")
root.geometry("400x350")
root.config(bg="#F9F9F9")

# Judul
judul = tk.Label(root, text="Tugas Pratikum 2", font=("Helvetica", 14, "bold"), bg="#F9F9F9")
judul.pack(pady=10)

subjudul = tk.Label(root, text="Kalkulator Hybrid", font=("Helvetica", 11), bg="#F9F9F9")
subjudul.pack(pady=2)

separator = tk.Label(root, text="─" * 50, fg="gray", bg="#F9F9F9")
separator.pack(pady=5)

# Input
label_input = tk.Label(root, text="Input (Ekspresi):", font=("Helvetica", 10, "bold"), bg="#F9F9F9")
label_input.pack(pady=(10, 0))

entry = tk.Entry(root, width=30, font=("Consolas", 12))
entry.pack(pady=5)

# Tombol Hitung
btn_hitung = tk.Button(root, text="Hitung", font=("Helvetica", 10, "bold"), bg="#4CAF50", fg="white", padx=15, pady=5, command=hitung)
btn_hitung.pack(pady=10)

# Hasil diproses
label_proses = tk.Label(root, text="Hasil Diproses:", font=("Helvetica", 10, "bold"), bg="#F9F9F9")
label_proses.pack(pady=(10, 0))

proses_label = tk.Label(root, text="(Ekspresi akan muncul di sini)", font=("Consolas", 10), bg="#F9F9F9", fg="gray")
proses_label.pack(pady=3)

# Output (Hasil)
label_output = tk.Label(root, text="Output (Hasil):", font=("Helvetica", 10, "bold"), bg="#F9F9F9")
label_output.pack(pady=(10, 0))

output_label = tk.Label(root, text="(Hasil akan muncul di sini)", font=("Consolas", 11), bg="#F9F9F9", fg="#333")
output_label.pack(pady=3)

separator2 = tk.Label(root, text="─" * 50, fg="gray", bg="#F9F9F9")
separator2.pack(pady=10)

# Contoh input
contoh_label = tk.Label(root, text="Contoh Input:", font=("Helvetica", 10, "bold"), bg="#F9F9F9")
contoh_label.pack(pady=(5, 0))

contoh_text = tk.Label(root, text="4+4-3  → Output > 5\n5 - 3 * 4  → Output > -7", font=("Consolas", 10), bg="#F9F9F9")
contoh_text.pack()

# Jalankan aplikasi
root.mainloop()
