import base64
import requests


class TokopediaAPI:
    def __init__(self):
        self.fs_id = "YOUR_FS_ID"
        self.client_id = "YOUR_CLIENT_ID"
        self.client_secret = "YOUR_CLIENT_SECRET"
        self.base_url = "https://fs.tokopedia.net"
        self.token = None

    def get_access_token(self):
        url = "https://accounts.tokopedia.com/token?grant_type=client_credentials"
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Length": "0"
        }

        try:
            response = requests.post(url, headers=headers, timeout=5)
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                return True, "Token berhasil didapatkan"
            return False, f"Gagal mendapatkan token: {response.text}"
        except requests.exceptions.RequestException as e:
            return False, f"Error jaringan saat auth: {str(e)}"

    def sync_products(self, products_data):
        if not self.token:
            success, msg = self.get_access_token()
            if not success:
                if self.client_id == "YOUR_CLIENT_ID":
                    return True, (
                        "(SIMULASI) Sinkronisasi ke Tokopedia berhasil!\n\n"
                        "Untuk koneksi asli, masukkan Client ID dan Secret Anda di kode."
                    )
                return False, f"Gagal Autentikasi: {msg}"

        url = f"{self.base_url}/inventory/v1/fs/{self.fs_id}/product/update"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        # Fix: Fetch correct tuple indices from the 20-column DB schema
        # index 0: id, index 8: harga_jual_toko, index 9: jumlah_masuk
        payload = [
            {"product_id": p[0], "new_stock": p[9], "new_price": p[8]}
            for p in products_data
        ]

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=5)
            if response.status_code == 200:
                return True, "Sinkronisasi ke Tokopedia Seller berhasil!"
            return False, (
                f"Gagal sinkronisasi. Status code: {response.status_code}\n"
                f"Pesan: {response.text}"
            )
        except requests.exceptions.RequestException as e:
            return False, f"Error koneksi API Tokopedia: {str(e)}"