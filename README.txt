MODEL SPK KNN - DATA MINING KKN

ISI FOLDER
- app.py                         : aplikasi Streamlit
- requirements.txt               : pustaka Python yang dibutuhkan
- data/Data_Mining_KKN.xlsx      : dataset Excel yang disertakan

CARA MENJALANKAN DI WINDOWS
1. Install Python 3.10 atau lebih baru dari https://www.python.org/downloads/
   Saat instalasi, centang "Add Python to PATH".
2. Ekstrak ZIP ini ke sebuah folder.
3. Buka folder hasil ekstrak, klik address bar File Explorer, ketik cmd, lalu Enter.
4. Jalankan perintah berikut satu per satu:

   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   python -m streamlit run app.py

5. Browser akan terbuka. Jika tidak, salin alamat lokal yang muncul di terminal
   (biasanya http://localhost:8501) ke browser.
6. Masukkan nilai pasien baru, pilih K, lalu klik Hitung Prediksi.

CATATAN
- Kode membaca dataset bawaan dari folder data secara otomatis.
- Dataset Excel harus memiliki judul kolom pada baris ketiga seperti file tugas.
- Aplikasi membutuhkan koneksi internet saat pertama kali memasang pustaka Python.
- Jika perintah "python" tidak ditemukan, coba gunakan "py" sebagai pengganti.
- Klasifikasi ini hanya untuk pembelajaran dan bukan diagnosis medis.
