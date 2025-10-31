def substitusi_cipher(plaintext, aturan):
    ciphertext = ''
    for char in plaintext.upper():
        if char in aturan:
            ciphertext += aturan[char]
        else:
            ciphertext += char
    return ciphertext

aturan_substitusi = {
    'U': 'K',
    'N': 'N',
    'I': 'I',
    'K': 'K',
    'A': 'B'
}

plaintext = input("Masukkan plaintext: ").upper()
ciphertext = substitusi_cipher(plaintext, aturan_substitusi)

print(f"Plaintext : {plaintext}")
print(f"Ciphertext: {ciphertext}")
