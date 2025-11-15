import tkinter as tk
from tkinter import scrolledtext, messagebox

# ==============================
#       DES TABLES
# ==============================

IP = [
58, 50, 42, 34, 26, 18, 10, 2,
60, 52, 44, 36, 28, 20, 12, 4,
62, 54, 46, 38, 30, 22, 14, 6,
64, 56, 48, 40, 32, 24, 16, 8,
57, 49, 41, 33, 25, 17, 9, 1,
59, 51, 43, 35, 27, 19, 11, 3,
61, 53, 45, 37, 29, 21, 13, 5,
63, 55, 47, 39, 31, 23, 15, 7
]

FP = [
40, 8, 48, 16, 56, 24, 64, 32,
39, 7, 47, 15, 55, 23, 63, 31,
38, 6, 46, 14, 54, 22, 62, 30,
37, 5, 45, 13, 53, 21, 61, 29,
36, 4, 44, 12, 52, 20, 60, 28,
35, 3, 43, 11, 51, 19, 59, 27,
34, 2, 42, 10, 50, 18, 58, 26,
33, 1, 41, 9, 49, 17, 57, 25
]

PC1 = [
57, 49, 41, 33, 25, 17, 9,
1, 58, 50, 42, 34, 26, 18,
10, 2, 59, 51, 43, 35, 27,
19, 11, 3, 60, 52, 44, 36,
63, 55, 47, 39, 31, 23, 15,
7, 62, 54, 46, 38, 30, 22,
14, 6, 61, 53, 45, 37, 29,
21, 13, 5, 28, 20, 12, 4
]

PC2 = [
14, 17, 11, 24, 1, 5,
3, 28, 15, 6, 21, 10,
23, 19, 12, 4, 26, 8,
16, 7, 27, 20, 13, 2,
41, 52, 31, 37, 47, 55,
30, 40, 51, 45, 33, 48,
44, 49, 39, 56, 34, 53,
46, 42, 50, 36, 29, 32
]

E = [
32, 1, 2, 3, 4, 5,
4, 5, 6, 7, 8, 9,
8, 9, 10, 11, 12, 13,
12, 13, 14, 15, 16, 17,
16, 17, 18, 19, 20, 21,
20, 21, 22, 23, 24, 25,
24, 25, 26, 27, 28, 29,
28, 29, 30, 31, 32, 1
]

P = [
16, 7, 20, 21, 29, 12, 28, 17,
1, 15, 23, 26, 5, 18, 31, 10,
2, 8, 24, 14, 32, 27, 3, 9,
19, 13, 30, 6, 22, 11, 4, 25
]

SBOX = [
    # S1
    [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
    ],
    # S2
    [
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],
    ],
    # S3
    [
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12],
    ],
    # S4
    [
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14],
    ],
    # S5
    [
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3],
    ],
    # S6
    [
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13],
    ],
    # S7
    [
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12],
    ],
    # S8
    [
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11],
    ],
]


# ======================================================
#         HELPER FUNCTIONS + LOGGING
# ======================================================

def permute(block, table, log_title=None, logger=None):
    result = "".join(block[i - 1] for i in table)
    if logger is not None and log_title:
        logger.append(f"{log_title}:\n{result}\n")
    return result


def shift_left(bits, n):
    return bits[n:] + bits[:n]


def xor(a, b):
    return "".join("1" if i != j else "0" for i, j in zip(a, b))


def sbox_substitution(bits, logger=None):
    result = ""
    if logger is not None:
        logger.append("\n=== S-BOX Substitution ===")

    for i in range(8):
        block = bits[i*6:(i+1)*6]
        row = int(block[0] + block[5], 2)
        col = int(block[1:5], 2)
        out = f"{SBOX[i][row][col]:04b}"
        result += out

        if logger is not None:
            logger.append(
                f"SBOX-{i+1}: input={block}, row={row}, col={col}, output={out}"
            )

    if logger is not None:
        logger.append(f"SBOX Output Total: {result}\n")
    return result


def generate_subkeys(key_64, logger):
    logger.append("\n===== GENERATE SUBKEY (K1 - K16) =====")
    logger.append("Key (64-bit):\n" + key_64 + "\n")

    # PC-1
    key_56 = permute(key_64, PC1, "PC-1 (56-bit)", logger)
    C = key_56[:28]
    D = key_56[28:]

    logger.append(f"C0 = {C}")
    logger.append(f"D0 = {D}\n")

    shifts = [1, 1, 2, 2, 2, 2, 2, 2,
              1, 2, 2, 2, 2, 2, 2, 1]

    subkeys = []

    for i in range(16):
        logger.append(f"\n===== ROUND PEMBENTUKAN SUBKEY {i+1} =====")
        logger.append(f"Shift = {shifts[i]} kali")

        # Rotasi kiri sesuai tabel shift
        C = shift_left(C, shifts[i])
        D = shift_left(D, shifts[i])

        logger.append(f"C{i+1}: {C}")
        logger.append(f"D{i+1}: {D}")

        # PC-2 → menghasilkan subkey
        subkey = permute(C + D, PC2, f"Subkey K{i+1} (48-bit)", logger)

        logger.append(f"Hasil K{i+1}: {subkey}\n")

        subkeys.append(subkey)

    return subkeys



def feistel(right, subkey, round_num, logger):
    logger.append(f"\n=== FEISTEL FUNCTION ROUND {round_num} ===")

    expanded = permute(right, E, "E-Expansion", logger)
    logger.append(f"XOR dengan subkey K{round_num}")

    x = xor(expanded, subkey)
    logger.append("Hasil XOR:\n" + x)

    sbox_out = sbox_substitution(x, logger)
    p_out = permute(sbox_out, P, "P-Permutation", logger)

    return p_out


def des_encrypt_block(block_64, subkeys, logger):
    logger.append("\n===== ENKRIPSI BLOCK 64-bit =====")
    logger.append("Input Block:\n" + block_64)

    block = permute(block_64, IP, "Initial Permutation (IP)", logger)

    L = block[:32]
    R = block[32:]

    logger.append(f"L0 = {L}")
    logger.append(f"R0 = {R}\n")

    for i in range(16):
        logger.append(f"\n===== ROUND {i+1} =====")

        f_out = feistel(R, subkeys[i], i+1, logger)

        newR = xor(L, f_out)

        logger.append(f"L{i+1}: {R}")
        logger.append(f"R{i+1}: {newR}")

        L, R = R, newR

    final = permute(R + L, FP, "Final Permutation (IP^-1)", logger)
    logger.append("\n===== CIPHERTEXT BLOCK (64-bit) =====")
    logger.append(final)

    return final


def text_to_bin(text):
    return "".join(f"{ord(c):08b}" for c in text)


def pad_text(text):
    while len(text) % 8 != 0:
        text += " "
    return text


# ======================================================
#               MAIN DES PROCESS
# ======================================================

def run_des():
    plaintext = entry_plain.get()
    key_input = entry_key.get()

    if len(key_input) > 8:
        messagebox.showerror("Error", "Key maksimal 8 karakter!")
        return

    plaintext = pad_text(plaintext)
    key_input = pad_text(key_input)

    logger = []
    logger.append("===== KONVERSI AWAL =====")

    pt_bin = text_to_bin(plaintext)
    key_bin = text_to_bin(key_input)

    logger.append(f"Plaintext (biner):\n{pt_bin}\n")
    logger.append(f"Key (64-bit):\n{key_bin}\n")

    subkeys = generate_subkeys(key_bin, logger)

    logger.append("\n===== MULAI ENKRIPSI =====")

    result_bin = ""
    for i in range(0, len(pt_bin), 64):
        block = pt_bin[i:i+64]
        result_bin += des_encrypt_block(block, subkeys, logger)

    result_hex = hex(int(result_bin, 2))[2:].upper()

    logger.append("\n===== HASIL AKHIR =====")
    logger.append("Ciphertext (biner):")
    logger.append(result_bin)
    logger.append("\nCiphertext (hex):")
    logger.append(result_hex)

    # Tampilkan di GUI
    text_output.delete(1.0, tk.END)
    for line in logger:
        text_output.insert(tk.END, line + "\n")


# ======================================================
#                      GUI
# ======================================================

root = tk.Tk()
root.title("DES Encryption - Full Process")

tk.Label(root, text="Plaintext:").grid(row=0, column=0, sticky="w")
entry_plain = tk.Entry(root, width=40)
entry_plain.grid(row=0, column=1)

tk.Label(root, text="Key (maks 8 char):").grid(row=1, column=0, sticky="w")
entry_key = tk.Entry(root, width=40)
entry_key.grid(row=1, column=1)

btn = tk.Button(root, text="Encrypt", command=run_des)
btn.grid(row=2, column=1, pady=10)

text_output = scrolledtext.ScrolledText(root, width=110, height=40)
text_output.grid(row=3, column=0, columnspan=2)

root.mainloop()