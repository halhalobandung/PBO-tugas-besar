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
                id_pelanggan INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_pelanggan TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS produk (
                kode_produk INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_produk TEXT,
                harga_produk INTEGER           
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS karyawan (
                id_karyawan INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_karyawan TEXT,
                jenis_kelamin TEXT CHECK(jenis_kelamin IN ('Laki-laki', 'Perempuan'))
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS supplier (
                id_supplier INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_supplier TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS akun (
                id_akun INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                peran TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS penjualan (
                id_penjualan INTEGER PRIMARY KEY AUTOINCREMENT,
                id_produk INTEGER,
                id_karyawan INTEGER,
                jumlah INTEGER,
                FOREIGN KEY (id_produk) REFERENCES produk (kode_produk),
                FOREIGN KEY (id_karyawan) REFERENCES karyawan (id_karyawan)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS pembelian (
                id_pembelian INTEGER PRIMARY KEY AUTOINCREMENT,
                id_produk INTEGER,
                id_pelanggan INTEGER,
                qty INTEGER,
                harga_total INTEGER,
                FOREIGN KEY (id_produk) REFERENCES produk (kode_produk),
                FOREIGN KEY (id_pelanggan) REFERENCES pelanggan (id_pelanggan)            
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS absensi_karyawan (
                id_absensi INTEGER PRIMARY KEY AUTOINCREMENT,
                id_karyawan INTEGER,
                id_akun INTEGER,
                FOREIGN KEY (id_karyawan) REFERENCES karyawan (id_karyawan),
                FOREIGN KEY (id_akun) REFERENCES akun (id_akun)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS pembayaran (
                id_pembayaran INTEGER PRIMARY KEY AUTOINCREMENT,
                id_produk INTEGER,
                id_pelanggan INTEGER,
                id_karyawan INTEGER,
                qty INTEGER,
                harga_total INTEGER,
                FOREIGN KEY (id_produk) REFERENCES produk (kode_produk),
                FOREIGN KEY (id_pelanggan) REFERENCES pelanggan (id_pelanggan),
                FOREIGN KEY (id_karyawan) REFERENCES karyawan (id_karyawan)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS riwayat_pemesanan (
                id_riwayat INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT DEFAULT CURRENT_TIMESTAMP,
                keterangan TEXT
            )
            """
        ]

        for query in tables:
            self.cursor.execute(query)
        self.conn.commit()

if __name__ == "__main__":
    db = Database()