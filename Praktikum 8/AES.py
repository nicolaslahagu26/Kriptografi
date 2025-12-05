# AES.py
# Perbaikan: GUI CustomTkinter + AES-128 (ECB educational)
# Align with "Pertemuan 8 dan 9.pdf" steps and results:
# - State is column-major (fill by columns)
# - SBOX HEX used from PDF
# - Key schedule uses words (columns) W0..W43 and logs RotWord/SubWord/RCON
# - MixColumns logs intermediate 02/03/01/01 multiplications with binary and hex
# - Detailed per-round steps shown (SubBytes, ShiftRows, MixColumns, AddRoundKey)
# - ENCRYPT ALL builds step states; Next/Prev shows 4x4 matrices in table view

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import textwrap

# ---------- SBOX & RCON (HEX as in PDF) ----------
SBOX = [
0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76,
0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0,
0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15,
0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75,
0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84,
0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF,
0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8,
0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2,
0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73,
0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB,
0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79,
0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08,
0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A,
0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E,
0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF,
0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16
]
RCON = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]

# ---------- utilities ----------
def hexstr(b): return f"{b:02X}"
def bytes_to_hex(b): return ' '.join(f"{x:02X}" for x in b)
def pad_pkcs7_bytes_from_text(text: str) -> list:
    arr=[ord(c) for c in text]
    pad_len = 16 - (len(arr) % 16)
    if pad_len == 0: pad_len = 16
    return arr + [pad_len]*pad_len
def unpad_pkcs7_bytes(arr):
    if not arr: return []
    p=arr[-1]
    if p<1 or p>16: return arr
    return arr[:-p]

# Important: AES state is column-major (bytes are filled column by column)
def bytes_to_state_column_major(bs16):
    # bs16: list of 16 bytes in order from input (ASCII hex order)
    # fill by columns: state[row][col]
    state = [[0]*4 for _ in range(4)]
    for i in range(16):
        row = i % 4
        col = i // 4
        state[row][col] = bs16[i]
    return state

def state_to_bytes_column_major(state):
    out=[]
    for col in range(4):
        for row in range(4):
            out.append(state[row][col])
    return out

# ---------- GF helpers & MixColumns with verbose steps ----------
def xtime(a): return ((a<<1)^0x1B)&0xFF if (a&0x80) else ((a<<1)&0xFF)
def mul(a,b):
    # multiply in GF(2^8)
    r=0
    for _ in range(8):
        if b & 1: r ^= a
        h = a & 0x80
        a = (a<<1) & 0xFF
        if h: a ^= 0x1B
        b >>= 1
    return r

def mix_column_verbose(col, log_lines, col_index):
    # col: list of 4 bytes (column)
    # returns new column and logs each intermediate multiplication and binary steps like PDF
    a = col
    # compute 02*a and 03*a per element (02 = xtime, 03 = xtime xor original)
    mul2 = [xtime(x) for x in a]
    mul3 = [mul2[i]^a[i] for i in range(4)]
    # compute final according to MixColumns matrix:
    # c0 = (02*a0) ^ (03*a1) ^ (01*a2) ^ (01*a3)
    c0 = mul2[0] ^ mul3[1] ^ a[2] ^ a[3]
    c1 = mul2[1] ^ mul3[2] ^ a[3] ^ a[0]
    c2 = mul2[2] ^ mul3[3] ^ a[0] ^ a[1]
    c3 = mul2[3] ^ mul3[0] ^ a[1] ^ a[2]
    # log details
    log_lines.append(f"--- MixColumns col{col_index} input: " + ' '.join(f"{x:02X}" for x in a))
    for i in range(4):
        log_lines.append(f"  byte[{i}]: {a[i]:02X}")
        log_lines.append(f"    02*{a[i]:02X} -> {mul2[i]:02X} (bin {format(mul2[i],'08b')})")
        log_lines.append(f"    03*{a[i]:02X} -> {mul3[i]:02X} (02 xor original)")
    log_lines.append(f"  column result: {c0:02X} {c1:02X} {c2:02X} {c3:02X}")
    return [c0,c1,c2,c3]

def mix_columns_verbose(state, log_lines):
    # state is 4x4 rows; columns are tuples zip(*state)
    cols = list(zip(*state))
    newcols=[]
    for i,c in enumerate(cols):
        nc = mix_column_verbose(list(c), log_lines, i)
        newcols.append(nc)
    # reconstruct rows
    new_state = [ [ newcols[col][row] for col in range(4) ] for row in range(4) ]
    return new_state

def inv_mix_columns_verbose(state, log_lines):
    cols = list(zip(*state))
    newcols=[]
    for i,c in enumerate(cols):
        a=list(c)
        # compute with mul using constants 14,11,13,9
        r0 = mul(a[0],14)^mul(a[1],11)^mul(a[2],13)^mul(a[3],9)
        r1 = mul(a[0],9)^mul(a[1],14)^mul(a[2],11)^mul(a[3],13)
        r2 = mul(a[0],13)^mul(a[1],9)^mul(a[2],14)^mul(a[3],11)
        r3 = mul(a[0],11)^mul(a[1],13)^mul(a[2],9)^mul(a[3],14)
        log_lines.append(f"--- InvMixColumns col{i} input: " + ' '.join(f"{x:02X}" for x in a))
        log_lines.append(f"  result: {r0:02X} {r1:02X} {r2:02X} {r3:02X}")
        newcols.append([r0,r1,r2,r3])
    new_state = [ [ newcols[col][row] for col in range(4) ] for row in range(4) ]
    return new_state

# ---------- SubBytes / ShiftRows / AddRoundKey helpers ----------
def sub_bytes(state, log_lines, roundnum):
    log_lines.append(f"-- ROUND {roundnum} SUBBYTES (byte->SBOX)")
    new=[[0]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            b = state[r][c]
            sb = SBOX[b]
            log_lines.append(f"   [{r},{c}] {b:02X} -> {sb:02X}")
            new[r][c] = sb
    return new

def inv_sub_bytes(state, log_lines, roundnum):
    inv=[0]*256
    for i,v in enumerate(SBOX): inv[v]=i
    log_lines.append(f"-- ROUND {roundnum} INV-SUBBYTES (byte->INV_SBOX)")
    new=[[0]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            b=state[r][c]
            sb=inv[b]
            log_lines.append(f"   [{r},{c}] {b:02X} -> {sb:02X}")
            new[r][c]=sb
    return new

def shift_rows(state, log_lines):
    res = [
        state[0],
        state[1][1:]+state[1][:1],
        state[2][2:]+state[2][:2],
        state[3][3:]+state[3][:3],
    ]
    log_lines.append("-- SHIFTROWS result:")
    for i,row in enumerate(res):
        log_lines.append("   " + ' '.join(f"{x:02X}" for x in row))
    return res

def inv_shift_rows(state, log_lines):
    res = [
        state[0],
        state[1][-1:]+state[1][:-1],
        state[2][-2:]+state[2][:-2],
        state[3][-3:]+state[3][:-3],
    ]
    log_lines.append("-- INV-SHIFTROWS result:")
    for i,row in enumerate(res):
        log_lines.append("   " + ' '.join(f"{x:02X}" for x in row))
    return res

def add_round_key(state, roundkey, log_lines):
    # both are 4x4 matrices (rows)
    res = [[0]*4 for _ in range(4)]
    log_lines.append("-- ADDROUNDKEY (state XOR roundkey)")
    for r in range(4):
        for c in range(4):
            s = state[r][c]
            k = roundkey[r][c]
            v = s ^ k
            log_lines.append(f"   [{r},{c}] {s:02X} XOR {k:02X} -> {v:02X}")
            res[r][c] = v
    return res

# ---------- Key expansion (words are columns, as AES) ----------
def key_expansion_with_log(key_bytes):
    # key_bytes: 16 bytes (text converted)
    logs=[]
    # Build initial words W0..W3 from key_bytes column-major
    # AES standard: words = 4-byte words; with key bytes ordered as key[0..15] -> first word = key[0..3]
    # To align with PDF column-major display we will also keep words as lists of 4 bytes
    w = [ key_bytes[i:i+4] for i in range(0,16,4) ]  # w0..w3
    logs.append("Initial W0..W3:")
    for i in range(4):
        logs.append(f" W{i}: " + ' '.join(f"{x:02X}" for x in w[i]))
    for i in range(4,44):
        t = w[i-1].copy()
        if i % 4 == 0:
            logs.append(f"\n-- i={i}: RotWord(W{i-1})")
            t = t[1:]+t[:1]
            logs.append("   RotWord -> " + ' '.join(f"{x:02X}" for x in t))
            t = [SBOX[x] for x in t]
            logs.append("   SubWord -> " + ' '.join(f"{x:02X}" for x in t))
            rc = RCON[(i//4)-1]
            logs.append(f"   XOR RCON {rc:02X} to first byte")
            t[0] ^= rc
            logs.append("   After RCON -> " + ' '.join(f"{x:02X}" for x in t))
        neww = [ (t[j] ^ w[i-4][j]) & 0xFF for j in range(4) ]
        w.append(neww)
        logs.append(f" W{i}: " + ' '.join(f"{x:02X}" for x in neww))
    # group into round keys: each round key uses 4 words; represent roundkey as 4x4 rows where row r contains the r-th byte of each word
    round_keys=[]
    for r in range(0,44,4):
        words = w[r:r+4]  # words = [w_r, w_r+1, w_r+2, w_r+3]
        # Build roundkey matrix rows: row0 = [w_r[0], w_r+1[0], w_r+2[0], w_r+3[0]]
        rk = [ [ words[col][row] for col in range(4) ] for row in range(4) ]
        round_keys.append(rk)
    return round_keys, '\n'.join(logs)

# ---------- Per-block encryption / decryption with logs ----------
def aes_encrypt_block_detailed(block_bytes, round_keys, block_index=0):
    logs=[]
    logs.append(f"=== BLOCK {block_index} INPUT (bytes col-major order) ===")
    logs.append(bytes_to_hex(block_bytes))
    state = bytes_to_state_column_major(block_bytes)  # column-major fill
    logs.append("-- Initial State (column-major rows shown):")
    for row in state: logs.append(' '.join(f"{x:02X}" for x in row))
    # Round 0
    logs.append("\n-- ROUND 0 AddRoundKey")
    state = add_round_key(state, round_keys[0], logs)
    logs.append("State after Round 0:")
    for row in state: logs.append(' '.join(f"{x:02X}" for x in row))
    # Rounds 1..9
    for r in range(1,10):
        logs.append(f"\n=== ROUND {r} ===")
        state = sub_bytes(state, logs, r)
        logs.append("After SubBytes:")
        for row in state: logs.append(' '.join(f"{x:02X}" for x in row))
        state = shift_rows(state, logs)
        state = mix_columns_verbose(state, logs)
        logs.append("After MixColumns:")
        for row in state: logs.append(' '.join(f"{x:02X}" for x in row))
        state = add_round_key(state, round_keys[r], logs)
        logs.append("After AddRoundKey:")
        for row in state: logs.append(' '.join(f"{x:02X}" for x in row))
    # Round 10
    logs.append("\n=== ROUND 10 (FINAL) ===")
    state = sub_bytes(state, logs, 10)
    logs.append("After SubBytes:")
    for row in state: logs.append(' '.join(f"{x:02X}" for x in row))
    state = shift_rows(state, logs)
    state = add_round_key(state, round_keys[10], logs)
    logs.append("After AddRoundKey (FINAL):")
    for row in state: logs.append(' '.join(f"{x:02X}" for x in row))
    # output cipher bytes in column-major order
    cipher_bytes = state_to_bytes_column_major(state)
    return cipher_bytes, '\n'.join(logs)

def aes_decrypt_block_detailed(cipher_bytes, round_keys, block_index=0):
    logs=[]
    logs.append(f"=== DECRYPT BLOCK {block_index} INPUT ===")
    logs.append(bytes_to_hex(cipher_bytes))
    state = bytes_to_state_column_major(cipher_bytes)
    logs.append("-- Initial State (column-major rows):")
    for row in state: logs.append(' '.join(f"{x:02X}" for x in row))
    # Round 10 start: AddRoundKey K10, InvShiftRows, InvSubBytes
    logs.append("\n-- ROUND 10 start: AddRoundKey with K10")
    state = add_round_key(state, round_keys[10], logs)
    logs.append("State:")
    for row in state: logs.append(' '.join(f"{x:02X}" for x in row))
    state = inv_shift_rows(state, logs)
    state = inv_sub_bytes(state, logs, 10)
    logs.append("After InvSubBytes:")
    for row in state: logs.append(' '.join(f"{x:02X}" for x in row))
    # rounds 9..1 inverse
    for r in range(9,0,-1):
        logs.append(f"\n=== ROUND {r} inverse ===")
        state = add_round_key(state, round_keys[r], logs)
        logs.append("After AddRoundKey with K{}:".format(r))
        for row in state: logs.append(' '.join(f"{x:02X}" for x in row))
        state = inv_mix_columns_verbose(state, logs)
        logs.append("After InvMixColumns:")
        for row in state: logs.append(' '.join(f"{x:02X}" for x in row))
        state = inv_shift_rows(state, logs)
        state = inv_sub_bytes(state, logs, r)
        logs.append("After InvSubBytes:")
        for row in state: logs.append(' '.join(f"{x:02X}" for x in row))
    # final round 0
    state = add_round_key(state, round_keys[0], logs)
    logs.append("\n-- ROUND 0 final AddRoundKey (K0)")
    for row in state: logs.append(' '.join(f"{x:02X}" for x in row))
    plain_bytes = state_to_bytes_column_major(state)
    return plain_bytes, '\n'.join(logs)

# ---------- High-level message handlers (ECB) ----------
def encrypt_message_all_detail(plaintext, key_text):
    padded = pad_pkcs7_bytes_from_text(plaintext)
    key_bytes = ([ord(c) for c in key_text] + [0]*16)[:16]
    round_keys, keylog = key_expansion_with_log(key_bytes)
    logs = []
    logs.append("=== KEY EXPANSION ===\n" + keylog)
    cipher=[]
    for i in range(0,len(padded),16):
        block = padded[i:i+16]
        cb, blocklog = aes_encrypt_block_detailed(block, round_keys, block_index=i//16)
        logs.append(blocklog)
        cipher += cb
    return cipher, logs, round_keys

def decrypt_message_all_detail(cipher_hex, key_text):
    # accepts cipher_hex (spaced or not)
    s = ''.join(cipher_hex.split())
    if len(s)%2 != 0:
        raise ValueError("Cipher hex length must be even")
    cb = [int(s[i:i+2],16) for i in range(0,len(s),2)]
    if len(cb)%16 != 0:
        raise ValueError("Cipher must be multiple of 16 bytes")
    key_bytes = ([ord(c) for c in key_text] + [0]*16)[:16]
    round_keys, keylog = key_expansion_with_log(key_bytes)
    logs = []
    logs.append("=== KEY EXPANSION ===\n" + keylog)
    plain=[]
    for i in range(0,len(cb),16):
        cblk = cb[i:i+16]
        pblk, blocklog = aes_decrypt_block_detailed(cblk, round_keys, block_index=i//16)
        logs.append(blocklog)
        plain += pblk
    try:
        up = unpad_pkcs7_bytes(plain)
    except:
        up = plain
    return up, logs, round_keys

# ---------- GUI (CustomTkinter) ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.title("AES (aligned with Pertemuan 8&9 PDF) - CustomTkinter")
app.geometry("1200x820")

# Header
hdr = ctk.CTkFrame(app); hdr.pack(fill="x", padx=12, pady=8)
ctk.CTkLabel(hdr, text="AES-128 (ECB) — Steps aligned to PDF (column-major state)", font=("Segoe UI",16,"bold")).pack(side="left", padx=8)

# Main frames
main = ctk.CTkFrame(app); main.pack(fill="both", expand=True, padx=12, pady=6)
left = ctk.CTkFrame(main, width=420); left.pack(side="left", fill="y", padx=8, pady=8)
center = ctk.CTkFrame(main); center.pack(side="left", fill="both", expand=True, padx=8, pady=8)
right = ctk.CTkFrame(main, width=380); right.pack(side="right", fill="y", padx=8, pady=8)

# Left controls
ctk.CTkLabel(left, text="Plaintext:").pack(anchor="w", pady=(6,2))
txt_plain = ctk.CTkTextbox(left, width=380, height=6); txt_plain.pack(pady=(0,8))
txt_plain.insert("0.0","PASKAMARTOHASUGI")
ctk.CTkLabel(left, text="Key (16 chars):").pack(anchor="w", pady=(6,2))
entry_key = ctk.CTkEntry(left, width=380); entry_key.pack(pady=(0,8))
entry_key.insert(0, "UNIKASANTOTHOMAS")
ctk.CTkLabel(left, text="Cipher (HEX) for decrypt:").pack(anchor="w", pady=(6,2))
entry_cipher = ctk.CTkEntry(left, width=380); entry_cipher.pack(pady=(0,8))

btnframe = ctk.CTkFrame(left); btnframe.pack(pady=6)
def on_encrypt_all():
    pt = txt_plain.get("1.0","end").strip()
    key = entry_key.get().strip()
    if not key:
        messagebox.showerror("Key required","Please enter key")
        return
    try:
        cipher, logs, round_keys = encrypt_message_all_detail(pt, key)
    except Exception as e:
        messagebox.showerror("Encrypt error", str(e)); return
    entry_cipher.delete(0,'end'); entry_cipher.insert(0, ''.join(f"{x:02X}" for x in cipher))
    text_log.delete("1.0","end"); text_log.insert("end", '\n\n'.join(logs))
    populate_key_tree(round_keys)
    build_step_states(pt, key, round_keys)
    show_step(0)

def on_decrypt_all():
    key = entry_key.get().strip()
    ch = entry_cipher.get().strip()
    if not key:
        messagebox.showerror("Key required","Please enter key"); return
    if not ch:
        messagebox.showerror("Cipher required","Please enter cipher hex"); return
    try:
        plain, logs, round_keys = decrypt_message_all_detail(ch, key)
    except Exception as e:
        messagebox.showerror("Decrypt error", str(e)); return
    try:
        txt_plain.delete("1.0","end"); txt_plain.insert("0.0", ''.join(chr(x) for x in plain))
    except:
        txt_plain.delete("1.0","end"); txt_plain.insert("0.0", bytes_to_hex(plain))
    text_log.delete("1.0","end"); text_log.insert("end", '\n\n'.join(logs))
    populate_key_tree(round_keys)
    build_step_states_from_cipher(ch, key, round_keys)
    show_step(0)

ctk.CTkButton(btnframe, text="ENCRYPT ALL (detailed)", command=on_encrypt_all).grid(row=0,column=0,padx=6)
ctk.CTkButton(btnframe, text="DECRYPT ALL (detailed)", command=on_decrypt_all).grid(row=0,column=1,padx=6)
ctk.CTkButton(left, text="Save Log to TXT", command=lambda: save_log(text_log)).pack(pady=(6,8))

# Center: matrix display + controls
matrix_frame = ctk.CTkFrame(center); matrix_frame.pack(pady=6)
state_table = ctk.CTkFrame(matrix_frame); state_table.grid(row=0,column=0,padx=6,pady=6)
key_table = ctk.CTkFrame(matrix_frame); key_table.grid(row=1,column=0,padx=6,pady=6)

ctrl_frame = ctk.CTkFrame(center); ctrl_frame.pack(fill="x", pady=6)
lbl_step = ctk.CTkLabel(ctrl_frame, text="Step: 0"); lbl_step.pack(side="left", padx=8)
btn_prev = ctk.CTkButton(ctrl_frame, text="<< Prev", command=lambda: show_step(CURRENT_STEP-1)); btn_prev.pack(side="left", padx=6)
btn_next = ctk.CTkButton(ctrl_frame, text="Next >>", command=lambda: show_step(CURRENT_STEP+1)); btn_next.pack(side="left", padx=6)

# Right: log + key expansion tree
ctk.CTkLabel(right, text="Detailed Log:").pack(anchor="w", pady=(6,2))
text_log = ctk.CTkTextbox(right, width=360, height=520); text_log.pack(padx=6,pady=6)
ctk.CTkLabel(right, text="Key Expansion (round keys rows):").pack(anchor="w", pady=(6,2))
tree_frame = ctk.CTkFrame(right); tree_frame.pack(fill="x", padx=6)
cols=("W0","W1","W2","W3"); tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=8)
for c in cols: tree.heading(c,text=c); tree.column(c,width=80,anchor="center")
tree.pack(fill="x")

# helper save
def save_log(textbox):
    txt = textbox.get("1.0","end")
    if not txt.strip(): messagebox.showinfo("Info","No log"); return
    path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text file","*.txt")])
    if path:
        with open(path,"w",encoding="utf-8") as f: f.write(txt)
        messagebox.showinfo("Saved", f"Saved to {path}")

# Step states data & helpers
STEP_STATES = []
CURRENT_STEP = 0

def show_matrix(parent, matrix, title="Matrix"):
    for w in parent.winfo_children(): w.destroy()
    lbl = ctk.CTkLabel(parent, text=title, font=("Segoe UI",11,"bold")); lbl.grid(row=0,column=0,columnspan=4,sticky="w", pady=(0,4))
    for r in range(4):
        for c in range(4):
            txt = f"{matrix[r][c]:02X}"
            cell = ctk.CTkLabel(parent, text=txt, width=64, height=30, anchor="center", fg_color="#222222", corner_radius=6, font=("Consolas",12))
            cell.grid(row=r+1, column=c, padx=4, pady=4)

def populate_key_tree(round_keys):
    for i in tree.get_children(): tree.delete(i)
    for idx,rk in enumerate(round_keys):
        # show each row of roundkey as one column entry to match readability
        vals = [' '.join(f"{x:02X}" for x in row) for row in rk]
        tree.insert('', 'end', values=vals)

def build_step_states(plaintext, key_text, round_keys):
    global STEP_STATES
    STEP_STATES=[]
    padded = pad_pkcs7_bytes_from_text(plaintext)
    block = padded[:16]
    state = bytes_to_state_column_major(block)
    # initial
    STEP_STATES.append({'round':0,'phase':'Input State (before AddRoundKey)','state':[row.copy() for row in state],'roundkey':round_keys[0]})
    # after AddRoundKey round0
    ar = add_round_key(state, round_keys[0], log_lines=[])
    STEP_STATES.append({'round':0,'phase':'After AddRoundKey (Round0)','state':[row.copy() for row in ar],'roundkey':round_keys[0]})
    cur = ar
    for r in range(1,10):
        sb = [[SBOX[b] for b in row] for row in cur]
        STEP_STATES.append({'round':r,'phase':'SubBytes','state':[row.copy() for row in sb],'roundkey':round_keys[r]})
        sh = [ sb[0], sb[1][1:]+sb[1][:1], sb[2][2:]+sb[2][:2], sb[3][3:]+sb[3][:3] ]
        STEP_STATES.append({'round':r,'phase':'ShiftRows','state':[row.copy() for row in sh],'roundkey':round_keys[r]})
        mc = mix_columns_verbose(sh, log_lines=[])
        STEP_STATES.append({'round':r,'phase':'MixColumns','state':[row.copy() for row in mc],'roundkey':round_keys[r]})
        ar = add_round_key(mc, round_keys[r], log_lines=[])
        STEP_STATES.append({'round':r,'phase':'AddRoundKey','state':[row.copy() for row in ar],'roundkey':round_keys[r]})
        cur = ar
    # final round 10
    sb = [[SBOX[b] for b in row] for row in cur]
    STEP_STATES.append({'round':10,'phase':'SubBytes','state':[row.copy() for row in sb],'roundkey':round_keys[10]})
    sh = [ sb[0], sb[1][1:]+sb[1][:1], sb[2][2:]+sb[2][:2], sb[3][3:]+sb[3][:3] ]
    STEP_STATES.append({'round':10,'phase':'ShiftRows','state':[row.copy() for row in sh],'roundkey':round_keys[10]})
    ar = add_round_key(sh, round_keys[10], log_lines=[])
    STEP_STATES.append({'round':10,'phase':'AddRoundKey (Final)','state':[row.copy() for row in ar],'roundkey':round_keys[10]})
    return

def build_step_states_from_cipher(cipher_hex, key_text, round_keys):
    # For decrypt flow show initial cipher and final plaintext matrix for table view; full inverse detailed steps are in logs.
    global STEP_STATES
    STEP_STATES=[]
    s = ''.join(cipher_hex.split())
    cb = [int(s[i:i+2],16) for i in range(0,len(s),2)]
    cblk = cb[:16]
    STEP_STATES.append({'round':10,'phase':'Cipher Input','state':bytes_to_state_column_major(cblk),'roundkey':round_keys[10]})
    pblk, _ = aes_decrypt_block_detailed(cblk, round_keys, 0)
    STEP_STATES.append({'round':0,'phase':'Plaintext (after decrypt)','state':bytes_to_state_column_major(pblk),'roundkey':round_keys[0]})

def show_step(idx):
    global CURRENT_STEP
    if idx<0 or idx>=len(STEP_STATES): return
    CURRENT_STEP = idx
    step = STEP_STATES[idx]
    lbl_step.configure(text=f"Step: {idx}  (Round {step['round']} - {step['phase']})")
    show_matrix(state_table, step['state'], title=f"State — {step['phase']}")
    show_matrix(key_table, step['roundkey'], title=f"RoundKey (rows) for Round {step['round']}")

# initial empty matrices
show_matrix(state_table, [[0]*4 for _ in range(4)], title="State")
show_matrix(key_table, [[0]*4 for _ in range(4)], title="RoundKey")

# run loop
if __name__ == "__main__":
    app.mainloop()
