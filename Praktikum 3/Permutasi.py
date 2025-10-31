import itertools

def permutasi_menyeluruh():
    data = input("Masukkan elemen (pisahkan dengan spasi): ").split()
    hasil = list(itertools.permutations(data))
    print("\n=== Permutasi Menyeluruh ===")
    for p in hasil:
        print(p)
    print(f"\nTotal Permutasi: {len(hasil)}")

permutasi_menyeluruh()
