import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from models import Penjualan, Pembelian

class TransaksiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Transaksi Apotek")
        self.root.geometry("900x600")

        self.conn = sqlite3.connect("apotek.db")
        self.cursor = self.conn.cursor()

        self.btn_logout = tk.Button(self.root, text="Log Out", command=self.logout, bg="#f44336", fg="white")
        self.btn_logout.pack(anchor="ne", padx=10, pady=5)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)

        self.tab_penjualan = ttk.Frame(self.notebook)
        self.tab_pembelian = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_penjualan, text="Kasir / Penjualan")
        self.notebook.add(self.tab_pembelian, text="Restock / Pembelian")

        self.setup_penjualan_ui()
        self.setup_pembelian_ui()

    def logout(self):
        answer = messagebox.askyesno("Log Out", "Apakah Anda yakin ingin keluar?")
        if answer:
            self.root.destroy()
            from auth import LoginApp
            new_root = tk.Tk()
            app = LoginApp(new_root)
            new_root.mainloop()

    def setup_penjualan_ui(self):
        frame_top = ttk.LabelFrame(self.tab_penjualan, text="Formulir Penjualan")
        frame_top.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_top, text="ID Produk:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_jual_produk = ttk.Entry(frame_top)
        self.entry_jual_produk.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_top, text="ID Pelanggan:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_jual_pelanggan = ttk.Entry(frame_top)
        self.entry_jual_pelanggan.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_top, text="ID Karyawan:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_jual_karyawan = ttk.Entry(frame_top)
        self.entry_jual_karyawan.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_top, text="Jumlah Beli:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_jual_jumlah = ttk.Entry(frame_top)
        self.entry_jual_jumlah.grid(row=1, column=3, padx=5, pady=5)

        self.lbl_total = ttk.Label(frame_top, text="Total: Rp 0", font=("Arial", 14, "bold"))
        self.lbl_total.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        ttk.Button(frame_top, text="Cek Harga", command=self.cek_harga_jual).grid(row=2, column=2, padx=5, pady=5)
        ttk.Button(frame_top, text="Proses Transaksi", command=self.proses_penjualan).grid(row=2, column=3, padx=5, pady=5)

        self.tree_penjualan = ttk.Treeview(self.tab_penjualan, columns=("ID", "Produk", "Pelanggan", "Jumlah", "Total", "Tanggal"), show='headings')
        self.tree_penjualan.heading("ID", text="ID Transaksi")
        self.tree_penjualan.heading("Produk", text="ID Produk")
        self.tree_penjualan.heading("Pelanggan", text="ID Pelanggan")
        self.tree_penjualan.heading("Jumlah", text="Qty")
        self.tree_penjualan.heading("Total", text="Total Harga")
        self.tree_penjualan.heading("Tanggal", text="Tanggal")
        self.tree_penjualan.pack(expand=True, fill='both', padx=10, pady=5)
        
        self.refresh_penjualan()

    def setup_pembelian_ui(self):
        frame_top = ttk.LabelFrame(self.tab_pembelian, text="Formulir Pembelian Stok")
        frame_top.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_top, text="ID Produk:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_beli_produk = ttk.Entry(frame_top)
        self.entry_beli_produk.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_top, text="ID Supplier:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_beli_supplier = ttk.Entry(frame_top)
        self.entry_beli_supplier.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_top, text="Jumlah Masuk:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_beli_jumlah = ttk.Entry(frame_top)
        self.entry_beli_jumlah.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_top, text="Total Harga Beli:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_beli_total = ttk.Entry(frame_top)
        self.entry_beli_total.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(frame_top, text="Proses Restock", command=self.proses_pembelian).grid(row=2, column=0, columnspan=4, sticky='ew', padx=5, pady=10)

        self.tree_pembelian = ttk.Treeview(self.tab_pembelian, columns=("ID", "Produk", "Supplier", "Jumlah", "Total", "Tanggal"), show='headings')
        self.tree_pembelian.heading("ID", text="ID Beli")
        self.tree_pembelian.heading("Produk", text="ID Produk")
        self.tree_pembelian.heading("Supplier", text="ID Supplier")
        self.tree_pembelian.heading("Jumlah", text="Qty Masuk")
        self.tree_pembelian.heading("Total", text="Biaya")
        self.tree_pembelian.heading("Tanggal", text="Tanggal")
        self.tree_pembelian.pack(expand=True, fill='both', padx=10, pady=5)

        self.refresh_pembelian()

    def cek_harga_jual(self):
        try:
            id_produk = self.entry_jual_produk.get()
            qty = int(self.entry_jual_jumlah.get())
            
            self.cursor.execute("SELECT harga_produk FROM produk WHERE kode_produk=?", (id_produk,))
            res = self.cursor.fetchone()
            if res:
                total = res[0] * qty
                self.lbl_total.config(text=f"Total: Rp {total}")
                return total
            else:
                messagebox.showerror("Error", "Produk tidak ditemukan")
                return 0
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus angka")
            return 0
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
            return 0

    def proses_penjualan(self):
        total = self.cek_harga_jual()
        if total > 0:
            try:
                jual = Penjualan(
                    self.entry_jual_produk.get(),
                    self.entry_jual_pelanggan.get(),
                    self.entry_jual_karyawan.get(),
                    int(self.entry_jual_jumlah.get()),
                    total
                )
                if jual.proses_transaksi():
                    messagebox.showinfo("Sukses", "Transaksi Penjualan Berhasil")
                    self.refresh_penjualan()
                else:
                    messagebox.showerror("Gagal", "Stok tidak mencukupi atau Produk tidak ditemukan")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def proses_pembelian(self):
        try:
            beli = Pembelian(
                self.entry_beli_produk.get(),
                self.entry_beli_supplier.get(),
                int(self.entry_beli_jumlah.get()),
                int(self.entry_beli_total.get())
            )
            beli.proses_transaksi()
            messagebox.showinfo("Sukses", "Stok Berhasil Ditambahkan")
            self.refresh_pembelian()
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def refresh_penjualan(self):
        for i in self.tree_penjualan.get_children():
            self.tree_penjualan.delete(i)
        self.cursor.execute("SELECT id_penjualan, id_produk, id_pelanggan, jumlah, total_harga, tanggal_transaksi FROM penjualan_obat ORDER BY id_penjualan DESC")
        for row in self.cursor.fetchall():
            self.tree_penjualan.insert("", "end", values=row)

    def refresh_pembelian(self):
        for i in self.tree_pembelian.get_children():
            self.tree_pembelian.delete(i)
        self.cursor.execute("SELECT id_pembelian, id_produk, id_supplier, jumlah_masuk, harga_beli_total, tanggal_beli FROM pembelian_stok ORDER BY id_pembelian DESC")
        for row in self.cursor.fetchall():
            self.tree_pembelian.insert("", "end", values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = TransaksiApp(root)
    root.mainloop()