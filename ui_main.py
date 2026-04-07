import os

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QFrame, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QMessageBox, QApplication,
    QStackedWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QPixmap, QPainter, QPainterPath
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from database import DatabaseHandler
from api import TokopediaAPI
from dialogs import ProductDialog, ImportExcelDialog


class POSApp(QMainWindow):
    def __init__(self):
        super().__init__()

        if not os.path.exists("images"):
            os.makedirs("images")

        self.db = DatabaseHandler()
        self.api = TokopediaAPI()

        self.setWindowTitle("Tokopedia Seller Center - POS")
        self.resize(1200, 800)

        self.init_ui()
        self.load_data()

    # ==========================================
    # UI SETUP
    # ==========================================
    def create_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 12))
        shadow.setOffset(0, 4)
        widget.setGraphicsEffect(shadow)

    def init_ui(self):
        main = QWidget()
        self.setCentralWidget(main)

        layout = QHBoxLayout(main)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._build_sidebar())

        # Membuat sistem halaman (Stacked Widget)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #f5f6f9;")
        
        # Inisialisasi Halaman
        self.page_dashboard = self._build_placeholder_page("📊 Halaman Dashboard", "Statistik & Grafik Penjualan akan muncul di sini.")
        self.page_produk = self._build_content()
        self.page_pengaturan = self._build_placeholder_page("⚙️ Pengaturan", "Konfigurasi API dan Toko akan muncul di sini.")

        self.stacked_widget.addWidget(self.page_dashboard)
        self.stacked_widget.addWidget(self.page_produk)
        self.stacked_widget.addWidget(self.page_pengaturan)
        
        # Tampilkan halaman produk secara default
        self.stacked_widget.setCurrentWidget(self.page_produk)
        self.menu_produk.setObjectName("menuBtnActive")

        layout.addWidget(self.stacked_widget)

    def _build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(260)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(20, 30, 20, 20)

        brand_lbl = QLabel("🛍️ TokoPOS")
        brand_lbl.setStyleSheet("font-size: 24px; font-weight: 800; color: #42b549; margin-bottom: 30px;")
        sb_layout.addWidget(brand_lbl)

        # Simpan tombol sebagai atribut kelas agar bisa diubah stylenya
        self.menu_dashboard = QPushButton("📊 Dashboard")
        self.menu_dashboard.setObjectName("menuBtn")
        self.menu_dashboard.clicked.connect(lambda: self.switch_page(0))

        self.menu_produk = QPushButton("📦 Daftar Produk")
        self.menu_produk.setObjectName("menuBtn")
        self.menu_produk.clicked.connect(lambda: self.switch_page(1))

        self.menu_sync = QPushButton("🔄 Sinkronisasi API")
        self.menu_sync.setObjectName("menuBtn")
        self.menu_sync.clicked.connect(self.sync_data)

        self.menu_pengaturan = QPushButton("⚙️ Pengaturan")
        self.menu_pengaturan.setObjectName("menuBtn")
        self.menu_pengaturan.clicked.connect(lambda: self.switch_page(2))

        for btn in [self.menu_dashboard, self.menu_produk, self.menu_sync, self.menu_pengaturan]:
            sb_layout.addWidget(btn)

        sb_layout.addStretch()

        version_lbl = QLabel("Versi 1.1.0")
        version_lbl.setStyleSheet("color: #9fa6b0; font-size: 12px; margin-left: 10px;")
        sb_layout.addWidget(version_lbl)

        return sidebar

    def switch_page(self, index):
        """Fungsi untuk berpindah halaman dan mengubah gaya tombol aktif"""
        self.stacked_widget.setCurrentIndex(index)
        
        # Reset semua tombol menjadi menuBtn biasa
        self.menu_dashboard.setObjectName("menuBtn")
        self.menu_produk.setObjectName("menuBtn")
        self.menu_pengaturan.setObjectName("menuBtn")
        
        # Ubah tombol yang diklik menjadi aktif
        if index == 0:
            self.menu_dashboard.setObjectName("menuBtnActive")
        elif index == 1:
            self.menu_produk.setObjectName("menuBtnActive")
        elif index == 2:
            self.menu_pengaturan.setObjectName("menuBtnActive")
            
        # Perbarui style secara paksa agar berubah seketika
        self.menu_dashboard.style().unpolish(self.menu_dashboard)
        self.menu_dashboard.style().polish(self.menu_dashboard)
        self.menu_produk.style().unpolish(self.menu_produk)
        self.menu_produk.style().polish(self.menu_produk)
        self.menu_pengaturan.style().unpolish(self.menu_pengaturan)
        self.menu_pengaturan.style().polish(self.menu_pengaturan)

    def _build_placeholder_page(self, title_text, desc_text):
        """Membuat halaman sederhana untuk Dashboard & Pengaturan"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel(title_text)
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #31353b;")
        
        desc = QLabel(f"Sedang dalam pengembangan...\n{desc_text}")
        desc.setStyleSheet("font-size: 14px; color: #6d7588;")
        
        layout.addStretch()
        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addWidget(desc, alignment=Qt.AlignCenter)
        layout.addStretch()
        return page

    def _build_content(self):
        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(30, 20, 30, 30)
        cl.setSpacing(20)

        # Topbar
        topbar = QHBoxLayout()
        page_title = QLabel("Daftar Produk")
        page_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #31353b;")

        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 Cari nama produk di etalase...")
        self.search.setObjectName("searchBar")
        self.search.setFixedWidth(350)
        self.search.textChanged.connect(self.load_data)

        profile_lbl = QLabel("👤 Halo, Admin")
        profile_lbl.setStyleSheet("font-weight: 600; color: #31353b; margin-left: 15px;")

        topbar.addWidget(page_title)
        topbar.addStretch()
        topbar.addWidget(self.search)
        topbar.addWidget(profile_lbl)
        cl.addLayout(topbar)

        # Stats Cards
        stats = QHBoxLayout()
        stats.setSpacing(20)
        self.card1, self.lbl_total_produk = self._build_stat_card("Total Produk", "0", "📦")
        self.card2, self.lbl_total_stok   = self._build_stat_card("Total Stok Gudang", "0", "📈")
        self.card3, self.lbl_total_aset   = self._build_stat_card("Estimasi Aset", "Rp 0", "💰")
        for c in [self.card1, self.card2, self.card3]:
            stats.addWidget(c)
        cl.addLayout(stats)

        # Toolbar
        toolbar = QHBoxLayout()

        self.btn_add = QPushButton("➕ Tambah Produk")
        self.btn_add.setObjectName("btnPrimary")
        self.btn_add.clicked.connect(self.add_item)

        self.btn_edit = QPushButton("✏️ Edit Produk")
        self.btn_edit.setObjectName("btnSecondary")
        self.btn_edit.clicked.connect(self.edit_item)

        self.btn_delete = QPushButton("🗑️ Hapus")
        self.btn_delete.setObjectName("btnDanger")
        self.btn_delete.clicked.connect(self.delete_item)

        self.btn_import = QPushButton("📥 Import Excel")
        self.btn_import.setObjectName("btnImport")
        self.btn_import.clicked.connect(self.import_excel)

        toolbar.addWidget(self.btn_add)
        toolbar.addWidget(self.btn_edit)
        toolbar.addWidget(self.btn_delete)
        toolbar.addWidget(self.btn_import)
        toolbar.addStretch()
        cl.addLayout(toolbar)

        # Table
        table_card = QFrame()
        table_card.setObjectName("card")
        self.create_shadow(table_card)
        tl = QVBoxLayout(table_card)
        tl.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(11) # Menambah 1 kolom untuk 'No'
        self.table.setHorizontalHeaderLabels([
            "ID",
            "No",
            "Kode",
            "Nama Barang",
            "HPP",
            "Harga Toko",
            "Stok",
            "Masuk",
            "Keluar",
            "Akhir",
            "Tanggal"
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Pilih baris secara penuh
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Izinkan seleksi multi-baris
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection) 
        
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setFocusPolicy(Qt.NoFocus)

        # Sembunyikan ID Database asli
        self.table.setColumnHidden(0, True) 

        # Atur agar kolom bisa ditarik/diubah ukurannya secara interaktif seperti Excel
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)

        # Lebar default
        self.table.setColumnWidth(1, 40)  # Lebar 'No'
        self.table.setColumnWidth(2, 80)  # Lebar Kode
        self.table.setColumnWidth(3, 300) # Lebar Nama Barang
        self.table.setColumnWidth(4, 120) # HPP
        self.table.setColumnWidth(5, 120) # Harga Toko
        self.table.setColumnWidth(6, 60)  # Stok (Ditampilkan kembali)

        tl.addWidget(self.table)
        cl.addWidget(table_card)

        return content

    def _build_stat_card(self, title, value, icon):
        card = QFrame()
        card.setObjectName("card")
        self.create_shadow(card)

        lyt = QVBoxLayout(card)
        lyt.setContentsMargins(20, 20, 20, 20)

        lbl_title = QLabel(f"{icon}  {title}")
        lbl_title.setStyleSheet("color: #6d7588; font-size: 13px; font-weight: 600;")

        lbl_val = QLabel(value)
        lbl_val.setStyleSheet("color: #31353b; font-size: 24px; font-weight: bold; margin-top: 5px;")

        lyt.addWidget(lbl_title)
        lyt.addWidget(lbl_val)
        return card, lbl_val

    # ==========================================
    # DATA LOGIC
    # ==========================================
    def load_data(self):
        data = self.db.get_all_products()
        keyword = self.search.text().lower()

        self.table.setRowCount(0)
        total_produk = total_stok = total_aset = 0

        # Menghitung Total Statistik DARI KESELURUHAN DATA DATABASE (FIXED)
        for row in data:
            if len(row) < 20:
                stok  = int(row[2]) if len(row) > 2 else 0
                harga = float(row[3]) if len(row) > 3 else 0.0
            else:
                stok  = row[9]
                harga = row[8]
                
            total_produk += 1
            total_stok   += stok
            total_aset   += (stok * harga)
            
        self.lbl_total_produk.setText(str(total_produk))
        self.lbl_total_stok.setText(str(total_stok))
        self.lbl_total_aset.setText(f"Rp {total_aset:,.0f}".replace(",", "."))

        # Menampilkan Data ke Tabel (difilter berdasarkan pencarian)
        no_urut = 1
        for row in data:
            if len(row) < 20:
                kode   = ""
                nama   = str(row[1]) if len(row) > 1 else ""
                hpp    = 0.0
                stok   = int(row[2]) if len(row) > 2 else 0
                harga  = float(row[3]) if len(row) > 3 else 0.0
                masuk  = stok
                keluar = 0
                akhir  = stok
                tgl    = ""
            else:
                kode   = row[1]
                nama   = row[4]
                hpp    = row[6]
                harga  = row[8]
                stok   = row[9]
                masuk  = row[14]
                keluar = row[15]
                akhir  = row[16]
                tgl    = row[11]

            if keyword not in nama.lower():
                continue

            r = self.table.rowCount()
            self.table.insertRow(r)

            # Mengisi kolom tabel
            self.table.setItem(r, 0, QTableWidgetItem(str(row[0]))) # ID Database (Disembunyikan)
            self.table.setItem(r, 1, QTableWidgetItem(str(no_urut))) # No Urut Rapih
            self.table.setItem(r, 2, QTableWidgetItem(str(kode) if kode else ""))
            self.table.setItem(r, 3, QTableWidgetItem(nama))
            self.table.setItem(r, 4, QTableWidgetItem(f"Rp {hpp:,.0f}".replace(",", ".")))
            self.table.setItem(r, 5, QTableWidgetItem(f"Rp {harga:,.0f}".replace(",", ".")))
            self.table.setItem(r, 6, QTableWidgetItem(str(stok)))
            self.table.setItem(r, 7, QTableWidgetItem(str(masuk)))
            self.table.setItem(r, 8, QTableWidgetItem(str(keluar)))
            self.table.setItem(r, 9, QTableWidgetItem(str(akhir)))
            self.table.setItem(r, 10, QTableWidgetItem(str(tgl) if tgl else ""))
            
            no_urut += 1

    def add_item(self):
        dialog = ProductDialog(self)
        if dialog.exec_():
            n, s, p, img = dialog.result_data
            
            # Add exactly 19 elements to align with schema fields
            data = (
                "", 0.0, "", n, "", 0.0, 0.0, p,
                s, 0, "", 0, 0.0, 0, 0, 0, s, 0, img
            )
            self.db.add_product(data)
            self.load_data()
            QMessageBox.information(self, "Sukses", "Produk berhasil ditambahkan!")

    def edit_item(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Pilih Produk", "Silakan pilih salah satu produk di tabel terlebih dahulu.")
            return

        row = selected_items[0].row()
        pid = int(self.table.item(row, 0).text()) # Tetap mengambil ID dari kolom 0
        
        product = self.db.get_product(pid)
        if not product:
            QMessageBox.warning(self, "Error", "Data produk tidak ditemukan di database.")
            return

        if len(product) < 20:
            dialog_data = (product[0], product[1], product[2], product[3], product[4] if len(product)>4 else "")
        else:
            dialog_data = (product[0], product[4], product[9], product[8], product[19])

        dialog = ProductDialog(self, dialog_data)
        if dialog.exec_():
            n, s, p, i = dialog.result_data
            self.db.update_product(pid, n, s, p, i)
            self.load_data()
            QMessageBox.information(self, "Sukses", "Detail produk berhasil diperbarui!")

    def delete_item(self):
        selected_rows = sorted(list(set(item.row() for item in self.table.selectedItems())))
        
        if not selected_rows:
            QMessageBox.warning(self, "Pilih Produk", "Silakan pilih satu atau lebih produk yang ingin dihapus!")
            return

        if len(selected_rows) == 1:
            name = self.table.item(selected_rows[0], 3).text() # Nama Barang ada di kolom 3
            msg_text = f"Apakah Anda yakin ingin menghapus <b>{name}</b> secara permanen?"
        else:
            msg_text = f"Apakah Anda yakin ingin menghapus <b>{len(selected_rows)} produk</b> sekaligus secara permanen?"

        msg = QMessageBox()
        msg.setWindowTitle("Konfirmasi Hapus")
        msg.setText(msg_text)
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)

        if msg.exec_() == QMessageBox.Yes:
            pids = [int(self.table.item(row, 0).text()) for row in selected_rows]
            self.db.delete_products_bulk(pids)
            self.load_data()

    def import_excel(self):
        dialog = ImportExcelDialog(self)
        if not dialog.exec_():
            return

        rows_to_import = dialog.result_data
        skip_dup = dialog.result_skip_dup

        if skip_dup:
            existing_names = {row[4].lower() for row in self.db.get_all_products() if len(row) >= 20}
            rows_to_import = [
                r for r in rows_to_import
                if r["nama_barang"].lower() not in existing_names
            ]

        if not rows_to_import:
            QMessageBox.information(
                self, "Info",
                "Tidak ada produk baru untuk diimpor (semua sudah ada di database)."
            )
            return

        products = [
            (
                r["kode_barang"],
                r["berat_packing"],
                r["column1"],
                r["nama_barang"],
                r["desc"],
                r["hpp"],
                r["harga_jual_grosir"],
                r["harga_jual_toko"],
                r["jumlah_masuk"],
                r["isi_per_bal"],
                r["tgl"],
                r["stock_akhir"],
                r["harga_shopee"],
                r["awal"],
                r["masuk"],
                r["keluar"],
                r["akhir"],
                r["isi_per_bal2"],
                r["image_path"]
            )
            for r in rows_to_import
        ]
        
        self.db.add_products_bulk(products)
        self.load_data()

        QMessageBox.information(
            self, "Import Berhasil",
            f"✅ Berhasil mengimpor <b>{len(products)}</b> produk ke database!"
        )

    def sync_data(self):
        products = self.db.get_all_products()
        if not products:
            QMessageBox.warning(self, "Peringatan", "Etalase kosong, tidak ada data untuk disinkronisasi.")
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        success, message = self.api.sync_products(products)
        QApplication.restoreOverrideCursor()

        if success:
            QMessageBox.information(self, "Sinkronisasi Berhasil", message)
        else:
            QMessageBox.critical(self, "Sinkronisasi Gagal", message)