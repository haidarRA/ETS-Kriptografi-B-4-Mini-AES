# Mengimpor modul os untuk keperluan random bytes (kunci dan IV)
import os

# Mini S-Box untuk substitusi byte (mirip prinsip S-Box di AES)
S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

# Membuat Invers dari S-Box untuk dekripsi
INV_S_BOX = {v: k for k, v in S_BOX.items()}

# Fungsi substitusi satu byte menggunakan S-Box
def substitute(byte):
    high = (byte >> 4) & 0xF  # Mengambil 4 bit atas
    low = byte & 0xF          # Mengambil 4 bit bawah
    return (S_BOX[high] << 4) | S_BOX[low]  # Substitusi dan gabungkan kembali

# Fungsi invers substitusi satu byte menggunakan inverse S-Box
def inverse_substitute(byte):
    high = (byte >> 4) & 0xF  # Mengambil 4 bit atas
    low = byte & 0xF          # Mengambil 4 bit bawah
    return (INV_S_BOX[high] << 4) | INV_S_BOX[low]  # Invers substitusi

# Fungsi untuk mengenkripsi 1 blok (2 bytes) dengan kunci
def encrypt_block(block, key):
    b0, b1 = block                   # Pecah blok menjadi 2 byte
    b0 = substitute(b0)              # Substitusi byte pertama
    b1 = substitute(b1)              # Substitusi byte kedua
    b0 ^= key[0]                     # XOR dengan kunci byte pertama
    b1 ^= key[1]                     # XOR dengan kunci byte kedua
    return bytes([b0, b1])            # Kembalikan hasil sebagai bytes

# Fungsi untuk mendekripsi 1 blok (2 bytes) dengan kunci
def decrypt_block(block, key):
    b0, b1 = block                   # Pecah blok menjadi 2 byte
    b0 ^= key[0]                     # XOR dengan kunci byte pertama
    b1 ^= key[1]                     # XOR dengan kunci byte kedua
    b0 = inverse_substitute(b0)      # Invers substitusi byte pertama
    b1 = inverse_substitute(b1)      # Invers substitusi byte kedua
    return bytes([b0, b1])            # Kembalikan hasil sebagai bytes

# Fungsi untuk mengenkripsi plaintext dengan mode ECB
def encrypt_ecb(plaintext, key):
    ciphertext = b""                 # Inisialisasi hasil ciphertext kosong
    for i in range(0, len(plaintext), 2):  # Iterasi per 2 byte
        block = plaintext[i:i+2]           # Ambil blok 2 byte
        if len(block) < 2:                 # Jika blok kurang dari 2 byte
            block += b'\x00'                # Tambah padding 0
        encrypted = encrypt_block(block, key)  # Enkripsi blok
        ciphertext += encrypted            # Gabungkan hasil
    return ciphertext

# Fungsi untuk mendekripsi ciphertext dengan mode ECB
def decrypt_ecb(ciphertext, key):
    plaintext = b""                   # Inisialisasi hasil plaintext kosong
    for i in range(0, len(ciphertext), 2):  # Iterasi per 2 byte
        block = ciphertext[i:i+2]          # Ambil blok 2 byte
        decrypted = decrypt_block(block, key)  # Dekripsi blok
        plaintext += decrypted          # Gabungkan hasil
    return plaintext

# Fungsi untuk mengenkripsi plaintext dengan mode CBC
def encrypt_cbc(plaintext, key, iv):
    ciphertext = b""                     # Inisialisasi ciphertext
    previous_block = iv                   # Inisialisasi previous block dengan IV
    for i in range(0, len(plaintext), 2):  # Iterasi per 2 byte
        block = plaintext[i:i+2]           # Ambil blok 2 byte
        if len(block) < 2:                 # Padding jika kurang dari 2 byte
            block += b'\x00'
        # XOR dengan previous_block untuk CBC chaining
        block = bytes([block[0] ^ previous_block[0], block[1] ^ previous_block[1]])
        encrypted = encrypt_block(block, key)  # Enkripsi blok
        ciphertext += encrypted                # Gabungkan hasil
        previous_block = encrypted             # Update previous block
    return ciphertext

# Fungsi untuk mendekripsi ciphertext dengan mode CBC
def decrypt_cbc(ciphertext, key, iv):
    plaintext = b""                      # Inisialisasi plaintext
    previous_block = iv                  # Inisialisasi previous block dengan IV
    for i in range(0, len(ciphertext), 2):# Iterasi per 2 byte
        block = ciphertext[i:i+2]         # Ambil blok 2 byte
        decrypted = decrypt_block(block, key)  # Dekripsi blok
        # XOR hasil dekripsi dengan previous_block
        decrypted = bytes([decrypted[0] ^ previous_block[0], decrypted[1] ^ previous_block[1]])
        plaintext += decrypted            # Gabungkan hasil
        previous_block = block            # Update previous block
    return plaintext

# Fungsi bantu untuk mengubah string hex menjadi bytes
def get_bytes_from_hexstring(hex_string):
    return bytes.fromhex(hex_string.strip())

# Main program
if __name__ == "__main__":
    print("=== Mini-AES Program ===")  # Menampilkan judul
    action = input("Pilih 'encrypt' atau 'decrypt': ").strip().lower()  # Memilih aksi
    mode = input("Pilih mode (ECB/CBC): ").strip().upper()              # Memilih mode operasi

    if action == "encrypt":
        user_text = input("Masukkan plaintext: ").encode('utf-8')  # Input plaintext
        key = os.urandom(2)               # Membuat kunci random 2 bytes
        iv = os.urandom(2) if mode == "CBC" else None  # Membuat IV jika mode CBC

        print("\nKey (hex):", key.hex())  # Menampilkan kunci dalam hex
        if mode == "CBC":
            print("IV  (hex):", iv.hex()) # Menampilkan IV dalam hex jika CBC

        # Proses enkripsi sesuai mode
        if mode == "ECB":
            ciphertext = encrypt_ecb(user_text, key)
        elif mode == "CBC":
            ciphertext = encrypt_cbc(user_text, key, iv)
        else:
            print("Mode tidak dikenali.")
            exit(1)

        print("\nCiphertext (hex):", ciphertext.hex())  # Menampilkan hasil ciphertext

    elif action == "decrypt":
        hex_cipher = input("Masukkan ciphertext (hex): ")    # Input ciphertext dalam hex
        ciphertext = get_bytes_from_hexstring(hex_cipher)    # Konversi ke bytes

        hex_key = input("Masukkan key (hex): ")              # Input kunci dalam hex
        key = get_bytes_from_hexstring(hex_key)              # Konversi ke bytes

        iv = None
        if mode == "CBC":
            hex_iv = input("Masukkan IV (hex): ")            # Input IV dalam hex
            iv = get_bytes_from_hexstring(hex_iv)            # Konversi ke bytes

        # Proses dekripsi sesuai mode
        if mode == "ECB":
            plaintext = decrypt_ecb(ciphertext, key)
        elif mode == "CBC":
            plaintext = decrypt_cbc(ciphertext, key, iv)
        else:
            print("Mode tidak dikenali.")
            exit(1)

        print("\n=== Hasil Dekripsi ===")
        print("Plaintext:", plaintext.decode('utf-8', errors='ignore'))  # Menampilkan hasil plaintext

    else:
        print("Pilihan tidak valid! Gunakan 'encrypt' atau 'decrypt'.")  # Validasi pilihan
