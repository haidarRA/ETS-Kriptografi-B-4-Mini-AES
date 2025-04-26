# ETS-Kriptografi-B-4-Mini-AES

`ETS Kriptografi B Kelompok 4`

| Nama Lengkap            | NRP        |
| ----------------------- | ---------- |
| Maulana Ahmad Zahiri    | 5027231010 |
| Furqon Aryadana         | 5027231024 |
| Haidar Rafi Aqyla       | 5027231029 |
| Raditya Hardian Santoso | 5027231033 |
| Danendra Fidel Khansa   | 5027231063 |





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

