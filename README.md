# README

## Deskripsi Singkat Algoritma Greedy yang Diimplementasikan

Bot ini menggunakan algoritma greedy untuk menentukan langkah terbaik dalam permainan Diamonds. Algoritma bekerja dengan cara berikut:

- Pada setiap giliran, bot memeriksa kondisi inventory. Jika inventory sudah mencapai kapasitas maksimum (10 diamond), bot akan beralih ke mode "returning" dan kembali ke base untuk menyimpan diamond.
- Jika inventory belum penuh, bot dalam mode "collecting" akan mencari diamond terbaik untuk dikejar berdasarkan skor nilai diamond dibagi jarak (nilai / (jarak + 1)).
- Bot kemudian menentukan langkah berikutnya untuk bergerak satu langkah mendekati diamond target atau base jika sedang returning.
- Sebelum bergerak, bot memeriksa apakah posisi tujuan sudah ditempati bot lain untuk menghindari tabrakan (tackle).
- Jika langkah horizontal tidak memungkinkan karena posisi sudah ditempati, bot mencoba langkah vertikal. Jika kedua arah terhalang, bot tetap diam.

Strategi ini mengoptimalkan pengumpulan diamond dengan fokus pada keputusan lokal yang optimal di tiap langkah, sambil meminimalkan risiko kehilangan inventory akibat bertemu lawan.

---

## Struktur Fungsi Utama dalam Kode

- `next_move(self, board_bot, board)`  
  Mengambil keputusan langkah selanjutnya berdasarkan status bot dan kondisi board saat ini.

- `find_best_diamond(self, board_bot, board)`  
  Mencari diamond dengan nilai terbaik yang dipertimbangkan berdasarkan jarak dari posisi bot.

- `calculate_distance(self, pos1, pos2)`  
  Menghitung jarak Manhattan antara dua posisi pada papan.

- `move_towards(self, current_pos, target_pos, board)`  
  Menghitung langkah satu kotak ke arah target sambil menghindari posisi yang sudah ditempati bot lain.

- `is_occupied(self, pos, board)`  
  Mengecek apakah posisi pada board sudah ditempati bot lain.

---

## Requirement dan Instalasi

- Python 3.7 atau lebih baru  
- Library Python berikut (instal dengan `pip install -r requirements.txt`):  
  - colorama  
  - requests  
  - library lain yang dibutuhkan oleh bot starter pack  
- Game Engine Diamonds sudah dijalankan di localhost (default `http://localhost:8082/`)  
- Starter pack bot sudah di-setup dan dependencies sudah terinstall

---

## Cara Menjalankan Bot

1. Pastikan Game Engine Diamonds sudah berjalan dan siap menerima bot.  
2. Install dependency Python dengan:  
   ```bash
   pip install -r requirements.txt
   ```  
3. Jalankan bot dengan perintah:  
   ```bash
   python main.py --name NamaBotSaya --email email@domain.com --password passwordSaya --team NamaTim --logic Greedy
   ```  
   Keterangan:  
   - Opsi `--logic Greedy` menentukan bot menggunakan algoritma greedy.  
   - Gunakan opsi `--token` jika sudah punya token bot untuk login cepat.  
4. Bot akan otomatis bergabung ke board dan mulai bergerak sesuai logika greedy.  
5. Pantau permainan melalui frontend Game Engine.

---

## Author

- Kelompok: TrioBRE  
- Anggota:  
  - M. Irsyad Ali (123140110)  
  - Marvin Karyanda (123140185)  
  - Yonatanoel Petra Hutabarat (123140100)  
- Dosen Pengampu: Imam Ekowicaksono, S.Si., M.Si.  
- Tahun: 2025  
