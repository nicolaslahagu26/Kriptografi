while True:
    a = float(input("Masukkan nilai a: "))
    b = float(input("Masukkan nilai b: "))
    c = a + b
    print("Hasil dari Nilai C adalah:", c)

    ulang = input("Apakah Anda ingin menghitung lagi? (Y/T): ").upper()
    if ulang != "Y":
        print("Program selesai. Terima kasih!")
        break
