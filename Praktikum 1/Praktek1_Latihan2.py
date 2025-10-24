def kalkulator(): 
    """Program kalkulator sederhana dengan input data.""" 
    print("Selamat datang di kalkulator sederhana!") 
    while True: 
        try: 
            angka1 = float(input("Masukkan angka pertama: ")) 
            angka2 = float(input("Masukkan angka kedua: ")) 
            operator = input("Masukkan operator (+, -, *, /): ") 
 
            if operator == '+': 
                hasil = angka1 + angka2 
            elif operator == '-': 
                hasil = angka1 - angka2 
            elif operator == '*': 
                hasil = angka1 * angka2 
            elif operator == '/': 
                if angka2 == 0: 
                    print("Error: Pembagian dengan nol tidak diizinkan.") 
                    continue 
                hasil = angka1 / angka2 
            else: 
                print("Operator tidak valid.") 
                continue 
                
            print("Hasil:", hasil) 
            break   

        except ValueError: 
            print("Input tidak valid. Masukkan angka.") 
 
if __name__ == "__main__": 
    kalkulator()
