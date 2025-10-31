def konversi_bilangan():
    desimal = int(input("Masukkan bilangan desimal: "))

    biner = bin(desimal)[2:]
    oktal = oct(desimal)[2:]
    heksa = hex(desimal)[2:].upper()

    print(f"\nBilangan desimal: {desimal}")
    print(f"Biner: {biner}")
    print(f"Oktal: {oktal}")
    print(f"Heksadesimal: {heksa}")

konversi_bilangan()
