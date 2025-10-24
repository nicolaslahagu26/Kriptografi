import tkinter as tk
from tkinter import ttk, messagebox

def konversi():
    try:
        jenis = combo_jenis.get()
        nilai = entry_input.get().strip()

        if not nilai:
            messagebox.showwarning("Peringatan", "Masukkan nilai terlebih dahulu!")
            return

        if jenis == "Biner":
            desimal = int(nilai, 2)
        elif jenis == "Oktal":
            desimal = int(nilai, 8)
        elif jenis == "Desimal":
            desimal = int(nilai)
        elif jenis == "Heksadesimal":
            desimal = int(nilai, 16)
        else:
            messagebox.showerror("Error", "Pilih jenis bilangan terlebih dahulu!")
            return

        biner = bin(desimal)[2:]
        oktal = oct(desimal)[2:]
        heksa = hex(desimal)[2:].upper()

        entry_desimal.delete(0, tk.END)
        entry_desimal.insert(0, str(desimal))

        entry_biner.delete(0, tk.END)
        entry_biner.insert(0, biner)

        entry_oktal.delete(0, tk.END)
        entry_oktal.insert(0, oktal)

        entry_heksa.delete(0, tk.END)
        entry_heksa.insert(0, heksa)

    except ValueError:
        messagebox.showerror("Error", "Input tidak valid untuk jenis bilangan yang dipilih!")


def hapus():
    entry_input.delete(0, tk.END)
    entry_desimal.delete(0, tk.END)
    entry_biner.delete(0, tk.END)
    entry_oktal.delete(0, tk.END)
    entry_heksa.delete(0, tk.END)
    combo_jenis.set("")


root = tk.Tk()
root.title("Konversi Bilangan")
root.geometry("420x400")
root.configure(bg="#F9F9F9")

judul = tk.Label(root, text="🧮 KONVERSI BILANGAN", font=("Arial", 16, "bold"), bg="#F9F9F9", fg="#333")
judul.pack(pady=10)

frame = tk.Frame(root, bg="#F9F9F9")
frame.pack(pady=10)

tk.Label(frame, text="Jenis Bilangan:", font=("Arial", 11), bg="#F9F9F9").grid(row=0, column=0, sticky="w", pady=5)
combo_jenis = ttk.Combobox(frame, values=["Biner", "Oktal", "Desimal", "Heksadesimal"], width=18)
combo_jenis.grid(row=0, column=1, pady=5, padx=5)

tk.Label(frame, text="Masukkan Nilai:", font=("Arial", 11), bg="#F9F9F9").grid(row=1, column=0, sticky="w", pady=5)
entry_input = tk.Entry(frame, width=22, font=("Arial", 11))
entry_input.grid(row=1, column=1, pady=5, padx=5)

frame_btn = tk.Frame(root, bg="#F9F9F9")
frame_btn.pack(pady=5)
btn_konversi = tk.Button(frame_btn, text="Konversi", font=("Arial", 11, "bold"), bg="#007BFF", fg="white",
                         width=12, command=konversi)
btn_konversi.grid(row=0, column=0, padx=10)
btn_hapus = tk.Button(frame_btn, text="Hapus", font=("Arial", 11, "bold"), bg="#DC3545", fg="white",
                      width=12, command=hapus)
btn_hapus.grid(row=0, column=1, padx=10)

frame_hasil = tk.Frame(root, bg="#F9F9F9")
frame_hasil.pack(pady=10)

tk.Label(frame_hasil, text="Desimal:", font=("Arial", 11), bg="#F9F9F9").grid(row=0, column=0, sticky="w", pady=3)
entry_desimal = tk.Entry(frame_hasil, width=25, font=("Arial", 11))
entry_desimal.grid(row=0, column=1, pady=3, padx=5)

tk.Label(frame_hasil, text="Biner:", font=("Arial", 11), bg="#F9F9F9").grid(row=1, column=0, sticky="w", pady=3)
entry_biner = tk.Entry(frame_hasil, width=25, font=("Arial", 11))
entry_biner.grid(row=1, column=1, pady=3, padx=5)

tk.Label(frame_hasil, text="Oktal:", font=("Arial", 11), bg="#F9F9F9").grid(row=2, column=0, sticky="w", pady=3)
entry_oktal = tk.Entry(frame_hasil, width=25, font=("Arial", 11))
entry_oktal.grid(row=2, column=1, pady=3, padx=5)

tk.Label(frame_hasil, text="Heksadesimal:", font=("Arial", 11), bg="#F9F9F9").grid(row=3, column=0, sticky="w", pady=3)
entry_heksa = tk.Entry(frame_hasil, width=25, font=("Arial", 11))
entry_heksa.grid(row=3, column=1, pady=3, padx=5)

tk.Label(root, text="© 2025 Program Konversi Bilangan - Python", bg="#F9F9F9", fg="#777", font=("Arial", 9)).pack(side="bottom", pady=10)

root.mainloop()
