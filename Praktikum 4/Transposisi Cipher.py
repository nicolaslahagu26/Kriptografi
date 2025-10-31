def transposisi_cipher(plaintext):
    part_length = len(plaintext) // 4
    parts = [plaintext[i:i + part_length] for i in range(0, len(plaintext), part_length)]
    ciphertext = ""
    for col in range(4):
        for part in parts:
            if col < len(part):
                ciphertext += part[col]
    return ciphertext

plaintext = input("Masukkan plaintext: ").upper()
ciphertext = transposisi_cipher(plaintext)

print(f"Plaintext  : {plaintext}")
print(f"Ciphertext : {ciphertext}")
