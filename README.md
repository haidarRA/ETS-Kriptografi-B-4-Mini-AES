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

## Spesifikasi Algoritma Mini-AES

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
| Test Case | Plaintext | Key   | Expected Ciphertext | Status |
|:---------:|:---------:|:-----:|:-------------------:|:------:|
| 1         | 1234      | 5678  | 910A                | ✅      |
| 2         | 0000      | FFFF  | 02FD       | ✅      |
| 3         | ABCD      | 0123  | AB97       | ✅      |

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

