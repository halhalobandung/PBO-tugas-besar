import sqlite3
from db_config import Database

class Model:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.conn
        self.cursor = self.db.cursor

class Pelanggan(Model):
    def __init__(self, id_pelanggan, nama, penyakit):
        super().__init__()
        self.id = id_pelanggan
        self.nama = nama
        self.penyakit = penyakit

    def simpan(self):
        query = "INSERT INTO pelanggan (id_pelanggan, nama_pelanggan, penyakit) VALUES (?, ?, ?)"
        self.cursor.execute(query, (self.id, self.nama, self.penyakit))
        self.conn.commit()

    def update(self):
        query = "UPDATE pelanggan SET nama_pelanggan = ?, penyakit = ? WHERE id_pelanggan = ?"
        self.cursor.execute(query, (self.nama, self.penyakit, self.id))
        self.conn.commit()

    def delete(self):
        query = "DELETE FROM pelanggan WHERE id_pelanggan = ?"
        self.cursor.execute(query, (self.id,))
        self.conn.commit()

    def hapus_semua(self):
        query = "DELETE FROM pelanggan"
        self.cursor.execute(query)
        self.conn.commit()

class Karyawan(Model):
    def __init__(self, id_karyawan, nama, jenis_kelamin):
        super().__init__()
        self.id = id_karyawan
        self.nama = nama
        self.jenis_kelamin = jenis_kelamin

    def simpan(self):
        query = "INSERT INTO karyawan (id_karyawan, nama_karyawan, jenis_kelamin) VALUES (?, ?, ?)"
        self.cursor.execute(query, (self.id, self.nama, self.jenis_kelamin))
        self.conn.commit()

    def update(self):
        query = "UPDATE karyawan SET nama_karyawan = ?, jenis_kelamin = ? WHERE id_karyawan = ?"
        self.cursor.execute(query, (self.nama, self.jenis_kelamin, self.id))
        self.conn.commit()

    def delete(self):
        query = "DELETE FROM karyawan WHERE id_karyawan = ?"
        self.cursor.execute(query, (self.id,))
        self.conn.commit()

    def hapus_semua(self):
        query = "DELETE FROM karyawan"
        self.cursor.execute(query)
        self.conn.commit()

class Supplier(Model):
    def __init__(self, id_supplier, nama, kontak):
        super().__init__()
        self.id = id_supplier
        self.nama = nama
        self.kontak = kontak

    def simpan(self):
        query = "INSERT INTO supplier (id_supplier, nama_supplier, kontak_supplier) VALUES (?, ?, ?)"
        self.cursor.execute(query, (self.id, self.nama, self.kontak))
        self.conn.commit()

    def update(self):
        query = "UPDATE supplier SET nama_supplier = ?, kontak_supplier = ? WHERE id_supplier = ?"
        self.cursor.execute(query, (self.nama, self.kontak, self.id))
        self.conn.commit()

    def delete(self):
        query = "DELETE FROM supplier WHERE id_supplier = ?"
        self.cursor.execute(query, (self.id,))
        self.conn.commit()

    def hapus_semua(self):
        query = "DELETE FROM supplier"
        self.cursor.execute(query)
        self.conn.commit()

class Produk(Model):
    def __init__(self, kode, nama, kategori, harga, stok):
        super().__init__()
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        self.__harga = harga
        self.__stok = stok

    def get_harga(self):
        return self.__harga

    def get_stok(self):
        return self.__stok

    def simpan_produk_baru(self):
        query = "INSERT INTO produk (kode_produk, nama_produk, kategori_produk, harga_produk, stok) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, (self.kode, self.nama, self.kategori, self.__harga, self.__stok))
        self.conn.commit()

    def update(self):
        query = "UPDATE produk SET nama_produk = ?, kategori_produk = ?, harga_produk = ?, stok = ? WHERE kode_produk = ?"
        self.cursor.execute(query, (self.nama, self.kategori, self.__harga, self.__stok, self.kode))
        self.conn.commit()

    def delete(self):
        query = "DELETE FROM produk WHERE kode_produk = ?"
        self.cursor.execute(query, (self.kode,))
        self.conn.commit()
    
    def hapus_semua(self):
        query = "DELETE FROM produk"
        self.cursor.execute(query)
        self.conn.commit()

    def tambah_stok(self, jumlah):
        if jumlah > 0:
            self.__stok += jumlah
            self.cursor.execute("UPDATE produk SET stok = ? WHERE kode_produk = ?", (self.__stok, self.kode))
            self.conn.commit()

    def kurangi_stok(self, jumlah):
        if 0 < jumlah <= self.__stok:
            self.__stok -= jumlah
            self.cursor.execute("UPDATE produk SET stok = ? WHERE kode_produk = ?", (self.__stok, self.kode))
            self.conn.commit()
            return True
        return False

class Transaksi(Model):
    def __init__(self, id_produk, jumlah):
        super().__init__()
        self.id_produk = id_produk
        self.jumlah = jumlah
    
    def proses_transaksi(self):
        pass

class Penjualan(Transaksi):
    def __init__(self, id_produk, id_pelanggan, id_karyawan, jumlah, total_harga):
        super().__init__(id_produk, jumlah)
        self.id_pelanggan = id_pelanggan
        self.id_karyawan = id_karyawan
        self.total_harga = total_harga

    def proses_transaksi(self):
        self.cursor.execute("SELECT stok FROM produk WHERE kode_produk = ?", (self.id_produk,))
        res = self.cursor.fetchone()
        if res:
            stok_sekarang = res[0]
            if stok_sekarang >= self.jumlah:
                query = "INSERT INTO penjualan_obat (id_produk, id_pelanggan, id_karyawan, jumlah, total_harga) VALUES (?, ?, ?, ?, ?)"
                self.cursor.execute(query, (self.id_produk, self.id_pelanggan, self.id_karyawan, self.jumlah, self.total_harga))
                id_penjualan = self.cursor.lastrowid
                
                sisa_stok = stok_sekarang - self.jumlah
                self.cursor.execute("UPDATE produk SET stok = ? WHERE kode_produk = ?", (sisa_stok, self.id_produk))
                
                query_bayar = "INSERT INTO pembayaran (id_penjualan, metode_pembayaran, status_pembayaran) VALUES (?, ?, ?)"
                self.cursor.execute(query_bayar, (id_penjualan, "Tunai", "Lunas"))
                
                query_log = "INSERT INTO riwayat_pemesanan (tipe_aktivitas, keterangan) VALUES (?, ?)"
                keterangan = f"Penjualan {self.id_produk} x{self.jumlah} kepada {self.id_pelanggan}"
                self.cursor.execute(query_log, ("Penjualan", keterangan))

                self.conn.commit()
                return True
        return False

class Pembelian(Transaksi):
    def __init__(self, id_produk, id_supplier, jumlah, harga_beli_total):
        super().__init__(id_produk, jumlah)
        self.id_supplier = id_supplier
        self.harga_beli_total = harga_beli_total

    def proses_transaksi(self):
        query = "INSERT INTO pembelian_stok (id_produk, id_supplier, jumlah_masuk, harga_beli_total) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (self.id_produk, self.id_supplier, self.jumlah, self.harga_beli_total))
        id_pembelian = self.cursor.lastrowid
        
        self.cursor.execute("SELECT stok FROM produk WHERE kode_produk = ?", (self.id_produk,))
        res = self.cursor.fetchone()
        if res:
            stok_sekarang = res[0]
            stok_baru = stok_sekarang + self.jumlah
            self.cursor.execute("UPDATE produk SET stok = ? WHERE kode_produk = ?", (stok_baru, self.id_produk))
            
            query_log = "INSERT INTO riwayat_pemesanan (tipe_aktivitas, keterangan) VALUES (?, ?)"
            keterangan = f"Restock {self.id_produk} x{self.jumlah} dari {self.id_supplier}"
            self.cursor.execute(query_log, ("Pembelian Stok", keterangan))
            
            self.conn.commit()

class Auth(Model):
    def login(self, username, password):
        query = "SELECT id_akun, nama, peran FROM akun WHERE username = ? AND password = ?"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        
        if result:
            id_akun, nama, peran = result
            
            self.cursor.execute("SELECT id_karyawan FROM karyawan WHERE nama_karyawan = ?", (nama,))
            karyawan_res = self.cursor.fetchone()
            
            if karyawan_res:
                id_karyawan = karyawan_res[0]
                self.cursor.execute("INSERT INTO absensi_karyawan (id_karyawan, id_akun, status_kehadiran) VALUES (?, ?, 'Hadir')", (id_karyawan, id_akun))
                self.conn.commit()
                
        return result

    def registrasi(self, id_akun, nama, username, password, peran, id_karyawan, jenis_kelamin):
        self.cursor.execute("SELECT id_akun FROM akun WHERE username = ?", (username,))
        if self.cursor.fetchone():
            return False
        
        self.cursor.execute("SELECT id_karyawan FROM karyawan WHERE id_karyawan = ?", (id_karyawan,))
        if self.cursor.fetchone():
            return False

        query_akun = "INSERT INTO akun (id_akun, nama, username, password, peran) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query_akun, (id_akun, nama, username, password, peran))
        
        query_karyawan = "INSERT INTO karyawan (id_karyawan, nama_karyawan, jenis_kelamin) VALUES (?, ?, ?)"
        self.cursor.execute(query_karyawan, (id_karyawan, nama, jenis_kelamin))
        
        self.conn.commit()
        return True