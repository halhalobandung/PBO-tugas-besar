import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("apotek.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        tables = [
            """
            CREATE TABLE IF NOT EXISTS pelanggan (
                id_pelanggan TEXT PRIMARY KEY,
                nama_pelanggan TEXT,
                penyakit TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS produk (
                kode_produk TEXT PRIMARY KEY,
                nama_produk TEXT,
                kategori_produk TEXT,
                harga_produk INTEGER,
                stok INTEGER
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS karyawan (
                id_karyawan TEXT PRIMARY KEY,
                nama_karyawan TEXT,
                jenis_kelamin TEXT CHECK(jenis_kelamin IN ('Laki-laki', 'Perempuan'))
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS supplier (
                id_supplier TEXT PRIMARY KEY,
                nama_supplier TEXT,
                kontak_supplier TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS akun (
                id_akun TEXT PRIMARY KEY,
                nama TEXT,
                username TEXT,
                password TEXT,
                peran TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS penjualan_obat (
                id_penjualan INTEGER PRIMARY KEY AUTOINCREMENT,
                id_produk TEXT,
                id_pelanggan TEXT,
                id_karyawan TEXT,
                jumlah INTEGER,
                total_harga INTEGER,
                tanggal_transaksi DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_produk) REFERENCES produk (kode_produk),
                FOREIGN KEY (id_pelanggan) REFERENCES pelanggan (id_pelanggan),
                FOREIGN KEY (id_karyawan) REFERENCES karyawan (id_karyawan)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS pembelian_stok (
                id_pembelian INTEGER PRIMARY KEY AUTOINCREMENT,
                id_produk TEXT,
                id_supplier TEXT,
                jumlah_masuk INTEGER,
                harga_beli_total INTEGER,
                tanggal_beli DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_produk) REFERENCES produk (kode_produk),
                FOREIGN KEY (id_supplier) REFERENCES supplier (id_supplier)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS pembayaran (
                id_pembayaran INTEGER PRIMARY KEY AUTOINCREMENT,
                id_penjualan INTEGER,
                metode_pembayaran TEXT,
                status_pembayaran TEXT,
                tanggal_bayar DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_penjualan) REFERENCES penjualan_obat (id_penjualan)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS absensi_karyawan (
                id_absensi INTEGER PRIMARY KEY AUTOINCREMENT,
                id_karyawan TEXT,
                id_akun TEXT,
                tanggal_masuk DATETIME DEFAULT CURRENT_TIMESTAMP,
                status_kehadiran TEXT,
                FOREIGN KEY (id_karyawan) REFERENCES karyawan (id_karyawan),
                FOREIGN KEY (id_akun) REFERENCES akun (id_akun)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS riwayat_pemesanan (
                id_log INTEGER PRIMARY KEY AUTOINCREMENT,
                tipe_aktivitas TEXT,
                keterangan TEXT,
                waktu_log DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]

        
        for query in tables:
            self.cursor.execute(query)
        self.conn.commit()
            
if __name__ == "__main__":
    db = Database()