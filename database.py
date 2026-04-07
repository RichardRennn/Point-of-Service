import sqlite3


class DatabaseHandler:
    def __init__(self, db_name="pos_database.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kode_barang TEXT,
                    berat_packing REAL,
                    column1 TEXT,
                    nama_barang TEXT,
                    desc TEXT,
                    hpp REAL,
                    harga_jual_grosir REAL,
                    harga_jual_toko REAL,
                    jumlah_masuk INTEGER,
                    isi_per_bal INTEGER,
                    tgl TEXT,
                    stock_akhir INTEGER,
                    harga_shopee REAL,
                    awal INTEGER,
                    masuk INTEGER,
                    keluar INTEGER,
                    akhir INTEGER,
                    isi_per_bal2 INTEGER,
                    image_path TEXT
                )
            """)
            conn.commit()

    def add_product(self, data):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO products (
                    kode_barang, berat_packing, column1, nama_barang, desc,
                    hpp, harga_jual_grosir, harga_jual_toko,
                    jumlah_masuk, isi_per_bal, tgl, stock_akhir,
                    harga_shopee, awal, masuk, keluar, akhir,
                    isi_per_bal2, image_path
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, data)
            conn.commit()

    def add_products_bulk(self, products):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.executemany("""
                INSERT INTO products (
                    kode_barang, berat_packing, column1, nama_barang, desc,
                    hpp, harga_jual_grosir, harga_jual_toko,
                    jumlah_masuk, isi_per_bal, tgl, stock_akhir,
                    harga_shopee, awal, masuk, keluar, akhir,
                    isi_per_bal2, image_path
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, products)
            conn.commit()

    def get_all_products(self):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM products")
            return c.fetchall()

    def get_product(self, pid):
        """Fetch a single product by id safely"""
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM products WHERE id=?", (pid,))
            return c.fetchone()

    def update_product(self, pid, name, stock, price, image):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute(
                "UPDATE products SET nama_barang=?, jumlah_masuk=?, harga_jual_toko=?, image_path=? WHERE id=?",
                (name, stock, price, image, pid)
            )
            conn.commit()

    def delete_product(self, pid):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM products WHERE id=?", (pid,))
            conn.commit()

    def delete_products_bulk(self, pids):
        """Menghapus banyak produk sekaligus berdasarkan list ID"""
        if not pids:
            return
            
        with self.get_connection() as conn:
            c = conn.cursor()
            formatted_pids = [(pid,) for pid in pids]
            c.executemany("DELETE FROM products WHERE id=?", formatted_pids)
            conn.commit()