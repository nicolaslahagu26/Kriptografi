def hitung_nilai_akhir(Sikap, Tugas, UTS, UAS):
    total = (Sikap * 0.10)+(Tugas * 0.30)+(UTS * 0.25)+(UAS*0.35)
    return total

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

def main():
    print("Menghitung Nilai Akhir Akademik")
    Sikap = float(input("Masukkan nilai Sikap/Kehadiran: "))
    Tugas = float(input("Masukkan nilai Tugas: "))
    UTS = float(input("Masukkan nilai UTS: "))
    UAS = float(input("Masukkan nilai UAS: "))

    total = hitung_nilai_akhir(Sikap, Tugas, UTS, UAS)
    huruf, bobot = konversi_nilai(total)

    print("\n Hasil Akhir ")
    print(f"Total Nilai Akhir: {total:.2f}")
    print(f"Konversi Nilai: {huruf} (Bobot: {bobot})")

    if total >= 56:
        print("Keterangan: Lulus")
    else:
        print("Keterangan: Tidak Lulus")

if __name__ == "__main__":
    main()
    
