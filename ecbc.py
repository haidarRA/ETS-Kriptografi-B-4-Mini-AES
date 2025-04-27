import os

# Mini S-Box
S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}
INV_S_BOX = {v: k for k, v in S_BOX.items()}

def substitute(byte):
    high = (byte >> 4) & 0xF
    low = byte & 0xF
    return (S_BOX[high] << 4) | S_BOX[low]

def inverse_substitute(byte):
    high = (byte >> 4) & 0xF
    low = byte & 0xF
    return (INV_S_BOX[high] << 4) | INV_S_BOX[low]

def encrypt_block(block, key):
    b0, b1 = block
    b0 = substitute(b0)
    b1 = substitute(b1)
    b0 ^= key[0]
    b1 ^= key[1]
    return bytes([b0, b1])

def decrypt_block(block, key):
    b0, b1 = block
    b0 ^= key[0]
    b1 ^= key[1]
    b0 = inverse_substitute(b0)
    b1 = inverse_substitute(b1)
    return bytes([b0, b1])

def encrypt_ecb(plaintext, key):
    ciphertext = b""
    for i in range(0, len(plaintext), 2):
        block = plaintext[i:i+2]
        if len(block) < 2:
            block += b'\x00'
        encrypted = encrypt_block(block, key)
        ciphertext += encrypted
    return ciphertext

def decrypt_ecb(ciphertext, key):
    plaintext = b""
    for i in range(0, len(ciphertext), 2):
        block = ciphertext[i:i+2]
        decrypted = decrypt_block(block, key)
        plaintext += decrypted
    return plaintext

def encrypt_cbc(plaintext, key, iv):
    ciphertext = b""
    previous_block = iv
    for i in range(0, len(plaintext), 2):
        block = plaintext[i:i+2]
        if len(block) < 2:
            block += b'\x00'
        block = bytes([block[0] ^ previous_block[0], block[1] ^ previous_block[1]])
        encrypted = encrypt_block(block, key)
        ciphertext += encrypted
        previous_block = encrypted
    return ciphertext

def decrypt_cbc(ciphertext, key, iv):
    plaintext = b""
    previous_block = iv
    for i in range(0, len(ciphertext), 2):
        block = ciphertext[i:i+2]
        decrypted = decrypt_block(block, key)
        decrypted = bytes([decrypted[0] ^ previous_block[0], decrypted[1] ^ previous_block[1]])
        plaintext += decrypted
        previous_block = block
    return plaintext

def get_bytes_from_hexstring(hex_string):
    return bytes.fromhex(hex_string.strip())

# Main program
if __name__ == "__main__":
    print("=== Mini-AES Program ===")
    action = input("Pilih 'encrypt' atau 'decrypt': ").strip().lower()
    mode = input("Pilih mode (ECB/CBC): ").strip().upper()

    if action == "encrypt":
        user_text = input("Masukkan plaintext: ").encode('utf-8')
        key = os.urandom(2)
        iv = os.urandom(2) if mode == "CBC" else None

        print("\nKey (hex):", key.hex())
        if mode == "CBC":
            print("IV  (hex):", iv.hex())

        if mode == "ECB":
            ciphertext = encrypt_ecb(user_text, key)
        elif mode == "CBC":
            ciphertext = encrypt_cbc(user_text, key, iv)
        else:
            print("Mode tidak dikenali.")
            exit(1)

        print("\nCiphertext (hex):", ciphertext.hex())

    elif action == "decrypt":
        hex_cipher = input("Masukkan ciphertext (hex): ")
        ciphertext = get_bytes_from_hexstring(hex_cipher)

        hex_key = input("Masukkan key (hex): ")
        key = get_bytes_from_hexstring(hex_key)

        iv = None
        if mode == "CBC":
            hex_iv = input("Masukkan IV (hex): ")
            iv = get_bytes_from_hexstring(hex_iv)

        if mode == "ECB":
            plaintext = decrypt_ecb(ciphertext, key)
        elif mode == "CBC":
            plaintext = decrypt_cbc(ciphertext, key, iv)
        else:
            print("Mode tidak dikenali.")
            exit(1)

        print("\n=== Hasil Dekripsi ===")
        print("Plaintext:", plaintext.decode('utf-8', errors='ignore'))

    else:
        print("Pilihan tidak valid! Gunakan 'encrypt' atau 'decrypt'.")
