# TokoPOS — Refactored

Aplikasi POS berbasis PyQt5 untuk Tokopedia Seller Center.

## Struktur Proyek

```
pos_app/
├── main.py        # Entry point — jalankan file ini
├── database.py    # DatabaseHandler (SQLite)
├── api.py         # TokopediaAPI (sinkronisasi ke Tokopedia)
├── dialogs.py     # ProductDialog + ImportExcelDialog
├── ui_main.py     # POSApp (main window & logika UI)
├── styles.py      # apply_style() — tema Tokopedia
└── README.md
```

## Cara Menjalankan

```bash
pip install PyQt5 requests openpyxl
python main.py
```

## Fitur Import Excel

Klik tombol **📥 Import Excel** di toolbar untuk mengimpor produk dari file `.xlsx`.

Kolom yang dibaca dari file Excel (sesuai Dataset.xlsx):

| Kolom Excel     | Indeks | Keterangan              |
|-----------------|--------|-------------------------|
| NAMA BARANG     | 3      | Nama produk             |
| HARGA JUAL TOKO | 7      | Harga satuan (Rp)       |
| JUMLAH MASUK    | 8      | Stok awal               |

Fitur import:
- Preview data sebelum dimasukkan ke database
- Progress bar saat membaca file besar (background thread)
- Opsi skip duplikat (lewati produk yang sudah ada)
- Laporan jumlah produk berhasil/dilewati

## Mengubah Kolom Excel

Jika format Excel berbeda, ubah konstanta di `dialogs.py` → class `ExcelImportWorker`:

```python
COL_NAME  = 3   # indeks kolom NAMA BARANG
COL_PRICE = 7   # indeks kolom HARGA JUAL TOKO
COL_STOCK = 8   # indeks kolom JUMLAH MASUK
```

## Konfigurasi API Tokopedia

Isi kredensial di `api.py`:

```python
self.fs_id        = "YOUR_FS_ID"
self.client_id    = "YOUR_CLIENT_ID"
self.client_secret = "YOUR_CLIENT_SECRET"
```
