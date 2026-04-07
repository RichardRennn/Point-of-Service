from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox, QFrame, QHBoxLayout
)
from PyQt5.QtCore import Qt

class PengaturanPage(QWidget):
    def __init__(self, api_handler=None):
        super().__init__()
        self.api = api_handler
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(20)

        # Judul Halaman
        title = QLabel("⚙️ Pengaturan Aplikasi")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #31353b;")
        layout.addWidget(title)

        # --- Kartu Form API ---
        api_card = QFrame()
        api_card.setStyleSheet("background-color: white; border-radius: 12px; border: 1px solid #e5e7e9;")
        api_layout = QVBoxLayout(api_card)
        api_layout.setContentsMargins(30, 30, 30, 30)

        api_title = QLabel("🔌 Konfigurasi API Tokopedia")
        api_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #31353b; margin-bottom: 10px; border: none;")
        api_layout.addWidget(api_title)

        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        self.fs_id_input = QLineEdit()
        self.fs_id_input.setPlaceholderText("Masukkan FS ID")
        self.fs_id_input.setText(self.api.fs_id if self.api else "")

        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Masukkan Client ID")
        self.client_id_input.setText(self.api.client_id if self.api else "")

        self.client_secret_input = QLineEdit()
        self.client_secret_input.setPlaceholderText("Masukkan Client Secret")
        self.client_secret_input.setEchoMode(QLineEdit.Password)
        self.client_secret_input.setText(self.api.client_secret if self.api else "")

        # Style Label
        lbl_style = "font-weight: 600; color: #31353b; font-size: 13px; border: none;"
        l_fs = QLabel("FS ID:"); l_fs.setStyleSheet(lbl_style)
        l_cid = QLabel("Client ID:"); l_cid.setStyleSheet(lbl_style)
        l_csec = QLabel("Client Secret:"); l_csec.setStyleSheet(lbl_style)

        form_layout.addRow(l_fs, self.fs_id_input)
        form_layout.addRow(l_cid, self.client_id_input)
        form_layout.addRow(l_csec, self.client_secret_input)

        api_layout.addLayout(form_layout)

        # Tombol Simpan
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Simpan Pengaturan API")
        self.btn_save.setObjectName("btnPrimary")
        self.btn_save.setFixedWidth(220)
        self.btn_save.clicked.connect(self.save_settings)
        btn_layout.addWidget(self.btn_save, alignment=Qt.AlignLeft)
        
        api_layout.addSpacing(20)
        api_layout.addLayout(btn_layout)

        layout.addWidget(api_card)
        layout.addStretch()

    def save_settings(self):
        if self.api:
            fs_id = self.fs_id_input.text().strip()
            client_id = self.client_id_input.text().strip()
            client_secret = self.client_secret_input.text().strip()

            if not fs_id or not client_id or not client_secret:
                QMessageBox.warning(self, "Peringatan", "Semua kolom API harus diisi!")
                return

            self.api.fs_id = fs_id
            self.api.client_id = client_id
            self.api.client_secret = client_secret
            
            QMessageBox.information(
                self, "Sukses", 
                "✅ Konfigurasi API Tokopedia berhasil diperbarui dan diterapkan ke dalam sistem!"
            )