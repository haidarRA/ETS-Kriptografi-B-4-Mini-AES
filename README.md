# ETS-Kriptografi-B-4-Mini-AES

`ETS Kriptografi B Kelompok 4`

| Nama Lengkap            | NRP        |
| ----------------------- | ---------- |
| Maulana Ahmad Zahiri    | 5027231010 |
| Furqon Aryadana         | 5027231024 |
| Haidar Rafi Aqyla       | 5027231029 |
| Raditya Hardian Santoso | 5027231033 |
| Danendra Fidel Khansa   | 5027231063 |

Proyek ini adalah implementasi algoritma **Mini-AES 16-bit** menggunakan Python dan GUI berbasis Tkinter.

# `Spesifikasi Algoritma Mini-AES`

- **Plaintext dan Key**: 16-bit (4 nibbles, 4 hex digit)
- **Operasi dalam Algoritma**:
  - **SubNibbles**: Substitusi menggunakan 4-bit S-Box.
  - **ShiftRows**: Pergeseran baris sederhana (swap).
  - **MixColumns**: Operasi matriks pada GF(2⁴).
  - **AddRoundKey**: XOR antara state dan kunci ronde.
- **Jumlah Ronde**: 3 (Initial AddRoundKey + 2 Rounds)
- **Key Expansion**:
  - Kunci awal 16-bit diperluas menjadi 3 kunci ronde (round keys) dengan operasi substitusi dan XOR sederhana.

## Flowchart

### Flowchart Mini-AES

![Image](https://github.com/user-attachments/assets/00d98bfb-90e8-43e1-ab14-6636372cab76)

### Flowchart Key Expansion

![Image](https://github.com/user-attachments/assets/c9b44ae7-fa4b-445f-aa03-b723014c9660)

## Implementasi Program

- Input plaintext dan key dalam 4 digit hex.
- Proses enkripsi ditampilkan step-by-step:
  - SubNibbles
  - ShiftRows
  - MixColumns (hanya di round 1)
  - AddRoundKey

Menampilkan Ciphertext hasil akhir.

## Penjelasan Testcase

Berikut 3 test case yang digunakan untuk validasi:
| Test Case | Plaintext | Key | Expected Ciphertext | Status |
|:---------:|:---------:|:-----:|:-------------------:|:------:|
| 1 | 1234 | 5678 | 910A | ✅ |
| 2 | 0000 | FFFF | 02FD | ✅ |
| 3 | ABCD | 0123 | AB97 | ✅ |

**Test Case 1**

Plaintext: 1234

Key: 5678

Expected Ciphertext: 910A

Penjelasan:
Proses enkripsi mengikuti semua tahapan Mini-AES: AddRoundKey, SubNibbles, ShiftRows, MixColumns, AddRoundKey.
Setiap transformasi dilakukan benar dan menghasilkan ciphertext akhir 910A.
Validasi berhasil.

**Test Case 2**

Plaintext: 0000

Key: FFFF

Expected Ciphertext: 02FD

Penjelasan:
Plaintext semua nol (0000) dikombinasikan dengan key semua satu (FFFF) memunculkan perubahan bit maksimal.
Melalui semua operasi Mini-AES, didapat hasil akhir 02FD.
Transformasi bitwise dan substitusi terbukti berjalan dengan baik.

**Test Case 3**

Plaintext: ABCD

Key: 0123

Expected Ciphertext: AB97

Penjelasan:
Plaintext dan key yang lebih acak memberikan ciphertext AB97 setelah semua tahapan Mini-AES.
Ini memperlihatkan algoritma berhasil melakukan difusi dan konfusi terhadap input data.

## Analisis: kelebihan dan keterbatasan Mini-AES

### Kelebihan Mini-AES

1. **Kesederhanaan dan Kemudahan Pemahaman**  
   Mini-AES menyederhanakan AES standar menjadi versi 16-bit yang jauh lebih mudah dipahami dan diimplementasikan. Dengan jumlah round yang lebih sedikit (3 round) dan operasi pada GF(2^4) yang lebih sederhana dibandingkan GF(2^8), algoritma ini sangat cocok untuk pembelajaran konsep dasar kriptografi.

2. **Nilai Edukatif yang Tinggi**  
   Struktur yang mirip dengan AES standar memberikan pengalaman belajar yang baik tanpa kompleksitas penuh. Implementasi ini memungkinkan pemahaman tentang konsep-konsep penting seperti substitusi, permutasi, difusi, kebingungan, dan operasi matematika dasar dalam kriptografi.

3. **Komputasi Ringan**  
   Dengan ukuran state dan kunci yang kecil (hanya 16-bit), Mini-AES membutuhkan sumber daya komputasi yang sangat minimal. Ini memungkinkan implementasi dan pengujian yang cepat bahkan pada perangkat dengan spesifikasi rendah.

4. **Demonstrasi Prinsip Kriptografi**  
   Meskipun sederhana, Mini-AES tetap mendemonstrasikan prinsip-prinsip dasar kriptografi modern seperti difusi (MixColumns), kebingungan (SubNibbles), dan ekspansi kunci, yang merupakan konsep fundamental dalam desain cipher blok.

5. **Platform Eksperimen yang Baik**  
   Mini-AES memberikan platform yang baik untuk bereksperimen dengan modifikasi algoritma kriptografi tanpa kerumitan yang berlebihan, memungkinkan analisis dan pemahaman dampak perubahan pada keamanan.

### Keterbatasan Mini-AES

1. **Keamanan yang Sangat Terbatas**  
   Dengan ukuran kunci hanya 16-bit, Mini-AES memiliki ruang kunci yang sangat kecil (hanya 2^16 = 65.536 kemungkinan kunci). Dengan komputasi modern, serangan brute force dapat dijalankan dalam hitungan milidetik.

2. **S-Box Sederhana**  
   S-Box 4-bit yang digunakan dalam Mini-AES tidak memiliki properti kriptografis sekuat S-Box 8-bit pada AES standar. Ini mengurangi tingkat kebingungan dan ketahanan terhadap analisis kriptanalisis.

3. **Difusi Terbatas**  
   Operasi MixColumns pada matriks 2x2 sederhana tidak memberikan tingkat difusi yang sama dengan matriks 4x4 pada AES standar, membuat algoritma lebih rentan terhadap serangan berbasis pola.

4. **Jumlah Round yang Minimal**  
   Dengan hanya 3 round (dibandingkan dengan 10, 12, atau 14 round pada AES standar), Mini-AES tidak mencapai tingkat pengacakan yang diperlukan untuk keamanan yang memadai.

5. **Tidak Layak untuk Aplikasi Keamanan Nyata**  
   Mini-AES sama sekali tidak boleh digunakan untuk mengamankan data sensitif dalam skenario dunia nyata karena keterbatasan keamanannya yang signifikan.

# `Spesifikasi Tambahan`

## Implementasi Dekripsi Mini-AES

### Fungsi Dekripsi

berikut merupakan fungsi dekripsi dari Mini_AES

```sh
def decrypt(ciphertext, key):
    round_keys = key_expansion(key)
    state = ciphertext

    # Round 2
    state = add_round_key(state, round_keys[2])
    state = inv_shift_rows(state)
    state = inv_sub_nibbles(state)

    # Round 1
    state = add_round_key(state, round_keys[1])
    state = inv_mix_columns(state)
    state = inv_shift_rows(state)
    state = inv_sub_nibbles(state)

    # Round 0
    state = add_round_key(state, round_keys[0])

    return state
```

### Implementasi Inverse Operation :

- Inverse S-Box :
  ```sh
  def inv_sub_nibbles(state):
    return [INV_SBOX[n] for n in state]
  ```
  Fungsi ini menggunakan dictionary `INV_SBOX`, yang merupakan invers dari `SBOX` yang digunakan pada enkripsi, untuk melakukan substitusi nibble secara terbalik.
- Inverse MixColumns :

  ```sh
  def inv_mix_columns(state):
    return [
        gf_mul(0x3, state[0]) ^ gf_mul(0x2, state[1]),
        gf_mul(0x2, state[0]) ^ gf_mul(0x3, state[1]),
        gf_mul(0x3, state[2]) ^ gf_mul(0x2, state[3]),
        gf_mul(0x2, state[2]) ^ gf_mul(0x3, state[3])
    ]
  ```

  implementasi saat ini mengasumsikan bahwa operasi MixColumns adalah `involusi` (invers dari dirinya sendiri) dalam konteks Mini-AES ini

- Inverse ShiftRows

  ```sh
  def inv_shift_rows(state):
    return [state[0], state[3], state[2], state[1]]
  ```

  Fungsi ini melakukan pergeseran baris secara terbalik dari operasi shift_rows pada enkripsi.

### Output

![output hasil dekripsi](/img/output-dekripsi.png)

## Analisis Avalanche Effect pada Mini-AES

Avalanche Effect adalah properti penting dalam algoritma kriptografi yang menyatakan bahwa perubahan kecil pada input (plaintext atau key) seharusnya menghasilkan perubahan signifikan pada output (ciphertext). Ini adalah salah satu karakteristik kunci dari algoritma kriptografi yang baik, karena mempersulit analisis statistik dan serangan kriptanalisis.

## Definisi Formal

Avalanche Effect didefinisikan sebagai berikut: Jika kita mengubah 1 bit dari input (plaintext atau key), idealnya sekitar 50% dari bit-bit output (ciphertext) akan berubah. Properti ini memastikan bahwa hubungan input-output sangat non-linear dan sulit untuk diprediksi.

## Implementasi Pengujian Avalanche Effect

Dalam implementasi ini, kami melakukan pengujian Avalanche Effect pada Mini-AES dengan dua pendekatan:

1. **Perubahan pada Plaintext**: Mengubah 1 bit dari plaintext dan membandingkan ciphertext hasil dengan ciphertext asli.
2. **Perubahan pada Key**: Mengubah 1 bit dari key dan membandingkan ciphertext hasil dengan ciphertext asli.

## Metode Pengujian

Prosedur pengujian yang digunakan:

1. Enkripsi plaintext asli dengan key asli untuk mendapatkan ciphertext referensi
2. Untuk setiap posisi bit (0-15) dalam input (plaintext atau key):
   - Flip bit pada posisi tersebut
   - Enkripsi input yang dimodifikasi
   - Hitung berapa banyak bit yang berubah dalam ciphertext
   - Hitung persentase perubahan (jumlah bit yang berubah / total bit)
3. Hitung rata-rata persentase perubahan bit untuk semua posisi bit

## Penambahan ECB dan CBC `ecbc.py`

### 1. **Modul yang Digunakan**

- `os`: Digunakan untuk menghasilkan angka acak (random bytes) yang akan digunakan sebagai kunci (key) dan vektor inisialisasi (IV).
- `S_BOX`: Ini adalah sebuah tabel yang digunakan untuk substitusi byte, yang merupakan bagian penting dari algoritma kriptografi simetris. Setiap byte dari data akan diganti menggunakan S-Box ini.
- `INV_S_BOX`: Merupakan invers dari S-Box yang digunakan untuk proses dekripsi.

### 2. **Fungsi Substitusi dan Invers Substitusi**

- `substitute(byte)`: Fungsi ini menerima satu byte dan menggantinya dengan nilai yang sesuai berdasarkan S-Box.
- `inverse_substitute(byte)`: Fungsi ini melakukan invers dari substitusi dengan menggunakan tabel invers S-Box untuk proses dekripsi.

### 3. **Enkripsi dan Dekripsi Blok**

- `encrypt_block(block, key)`: Fungsi ini mengenkripsi sebuah blok yang terdiri dari 2 byte menggunakan substitusi byte dan XOR dengan kunci.
- `decrypt_block(block, key)`: Fungsi ini mendekripsi sebuah blok yang terdiri dari 2 byte dengan cara pertama-tama melakukan XOR dengan kunci, lalu melakukan invers substitusi byte.

### 4. **Mode ECB (Electronic Codebook)**

- `encrypt_ecb(plaintext, key)`: Fungsi ini mengenkripsi plaintext dengan menggunakan mode ECB, yang membagi plaintext menjadi blok-blok berukuran 2 byte. Setiap blok kemudian dienkripsi secara independen.
- `decrypt_ecb(ciphertext, key)`: Fungsi ini mendekripsi ciphertext yang sudah dienkripsi dengan mode ECB dengan cara yang mirip, yaitu memecah ciphertext menjadi blok-blok dan mendekripsinya satu per satu.

**Mode ECB** memiliki kelemahan karena pola data yang sama dalam plaintext akan menghasilkan ciphertext yang sama, sehingga bisa rentan terhadap analisis pola.

### 5. **Mode CBC (Cipher Block Chaining)**

![Proses Enkripsi CBC](/img/CBCenkrip.png)

- `encrypt_cbc(plaintext, key, iv)`: Fungsi ini mengenkripsi plaintext dengan mode CBC. Pada mode ini, blok plaintext pertama akan di-XOR dengan IV (Inisialization Vector) sebelum dienkripsi, dan hasilnya digunakan untuk XOR dengan blok plaintext berikutnya. Ini memberikan sifat chaining antara blok-blok.
- `decrypt_cbc(ciphertext, key, iv)`: Fungsi ini mendekripsi ciphertext yang sudah dienkripsi dengan mode CBC dengan cara pertama-tama mendekripsi setiap blok, lalu melakukan XOR dengan blok sebelumnya (atau IV untuk blok pertama) untuk mendapatkan plaintext asli.

**Mode CBC** lebih aman dibandingkan dengan ECB karena setiap blok ciphertext bergantung pada blok sebelumnya, yang mencegah pola yang mudah dikenali.

### 6. **Fungsi Pembantu**

- `get_bytes_from_hexstring(hex_string)`: Fungsi ini mengkonversi string hex menjadi bytes, yang diperlukan saat menerima input dari pengguna dalam format hexadecimal.

### 7. **Alur Utama Program**

- Program meminta input dari pengguna untuk menentukan apakah akan melakukan enkripsi atau dekripsi (`encrypt` atau `decrypt`).
- Jika memilih **enkripsi**:
  - Pengguna memasukkan plaintext yang akan dienkripsi.
  - Kunci (key) dan IV (jika mode CBC) dihasilkan secara acak menggunakan `os.urandom()`.
  - Proses enkripsi dilakukan sesuai dengan mode yang dipilih (ECB atau CBC), dan hasilnya ditampilkan dalam format hexadecimal.
- Jika memilih **dekripsi**:
  - Pengguna memasukkan ciphertext dalam format hex dan kunci yang digunakan saat enkripsi.
  - IV diminta jika mode yang dipilih adalah CBC.
  - Proses dekripsi dilakukan sesuai dengan mode yang dipilih, dan hasilnya (plaintext) ditampilkan.

### 8. **Proses enkripsi dan dekripsi:**

- Pada mode **ECB**, setiap blok plaintext (ukuran 2 byte) diproses secara terpisah dan langsung dienkripsi.
- Pada mode **CBC**, sebelum mengenkripsi blok plaintext, blok pertama di-XOR dengan IV, dan blok berikutnya di-XOR dengan hasil enkripsi blok sebelumnya.

### HASIL ENKRIP DAN DEKRIP CBC

![Proses Enkripsi CBC](/img/CBCenkrip.png)

![Proses Dekripsi CBC](/img/CBCdekrip.png)

### HASIL ENKRIP DAN DEKRIP ECB

![Proses Enkripsi ECBC](/img/ECBenkrip.png)

![Proses Enkripsi ECBC](/img/ECBdekrip.png)

## Export dan Import File `txtcsv.py`

Alur Kerja:

- **Input:** Sebuah string dalam format hexadecimal.
- **Proses:**
  - Fungsi `strip()` menghapus spasi ekstra di awal atau akhir string.
  - Fungsi `bytes.fromhex()` digunakan untuk mengubah string hex yang sudah dibersihkan menjadi bytes.
- **Output:** Data dalam format bytes.

![Proses log](/img/tocsv.png)
