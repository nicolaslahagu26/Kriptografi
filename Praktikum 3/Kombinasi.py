def faktorial(x):
    if x == 0 or x == 1:
        return 1
    hasil = 1
    for i in range(2, x + 1):
        hasil *= i
    return hasil

def kombinasi(n, r):
    if r > n:
        return 0
    return faktorial(n) // (faktorial(r) * faktorial(n - r))

def main():
    n = int(input("Masukkan jumlah total objek (n): "))
    r = int(input("Masukkan jumlah objek yang dipilih (r): "))
    hasil = kombinasi(n, r)
    print(f"\nJumlah kombinasi C({n}, {r}) adalah: {hasil}")

main()
