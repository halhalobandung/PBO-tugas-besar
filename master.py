import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from models import Produk, Pelanggan, Supplier, Karyawan

class MasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Manajemen Data Master - Apotek")
        self.root.geometry("800x600")

        self.conn = sqlite3.connect("apotek.db")
        self.cursor = self.conn.cursor()

        self.btn_logout = tk.Button(self.root, text="Log Out", command=self.logout, bg="#f44336", fg="white")
        self.btn_logout.pack(anchor="ne", padx=10, pady=5)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)

        self.tab_produk = ttk.Frame(self.notebook)
        self.tab_pelanggan = ttk.Frame(self.notebook)
        self.tab_supplier = ttk.Frame(self.notebook)
        self.tab_karyawan = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_produk, text="Data Produk")
        self.notebook.add(self.tab_pelanggan, text="Data Pelanggan")
        self.notebook.add(self.tab_supplier, text="Data Supplier")
        self.notebook.add(self.tab_karyawan, text="Data Karyawan")

        self.setup_produk_tab()
        self.setup_pelanggan_tab()
        self.setup_supplier_tab()
        self.setup_karyawan_tab()

    def logout(self):
        answer = messagebox.askyesno("Log Out", "Apakah Anda yakin ingin keluar?")
        if answer:
            self.root.destroy()
            from auth import LoginApp
            new_root = tk.Tk()
            app = LoginApp(new_root)
            new_root.mainloop()

    def setup_produk_tab(self):
        frame_input = ttk.LabelFrame(self.tab_produk, text="Input Produk Baru")
        frame_input.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_input, text="Kode Produk:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_kode_produk = ttk.Entry(frame_input)
        self.entry_kode_produk.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Nama Produk:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_nama_produk = ttk.Entry(frame_input)
        self.entry_nama_produk.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_input, text="Kategori:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_kategori_produk = ttk.Entry(frame_input)
        self.entry_kategori_produk.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Harga:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_harga_produk = ttk.Entry(frame_input)
        self.entry_harga_produk.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(frame_input, text="Stok Awal:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_stok_produk = ttk.Entry(frame_input)
        self.entry_stok_produk.grid(row=2, column=1, padx=5, pady=5)

        frame_btn = ttk.Frame(frame_input)
        frame_btn.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(frame_btn, text="Simpan", command=self.simpan_produk).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Update", command=self.update_produk).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Hapus", command=self.hapus_produk).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Clear", command=self.clear_produk).pack(side='left', padx=5)

        self.tree_produk = ttk.Treeview(self.tab_produk, columns=("Kode", "Nama", "Kategori", "Harga", "Stok"), show='headings')
        self.tree_produk.heading("Kode", text="Kode")
        self.tree_produk.heading("Nama", text="Nama Produk")
        self.tree_produk.heading("Kategori", text="Kategori")
        self.tree_produk.heading("Harga", text="Harga")
        self.tree_produk.heading("Stok", text="Stok")
        self.tree_produk.pack(expand=True, fill='both', padx=10, pady=5)
        self.tree_produk.bind("<<TreeviewSelect>>", self.pilih_produk)
        
        self.refresh_produk()

    def setup_pelanggan_tab(self):
        frame_input = ttk.LabelFrame(self.tab_pelanggan, text="Input Pelanggan")
        frame_input.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_input, text="ID Pelanggan:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id_pelanggan = ttk.Entry(frame_input)
        self.entry_id_pelanggan.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Nama Pelanggan:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_nama_pelanggan = ttk.Entry(frame_input)
        self.entry_nama_pelanggan.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_input, text="Riwayat Penyakit:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_penyakit_pelanggan = ttk.Entry(frame_input)
        self.entry_penyakit_pelanggan.grid(row=1, column=1, padx=5, pady=5)

        frame_btn = ttk.Frame(frame_input)
        frame_btn.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(frame_btn, text="Simpan", command=self.simpan_pelanggan).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Update", command=self.update_pelanggan).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Hapus", command=self.hapus_pelanggan).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Clear", command=self.clear_pelanggan).pack(side='left', padx=5)

        self.tree_pelanggan = ttk.Treeview(self.tab_pelanggan, columns=("ID", "Nama", "Penyakit"), show='headings')
        self.tree_pelanggan.heading("ID", text="ID")
        self.tree_pelanggan.heading("Nama", text="Nama")
        self.tree_pelanggan.heading("Penyakit", text="Penyakit")
        self.tree_pelanggan.pack(expand=True, fill='both', padx=10, pady=5)
        self.tree_pelanggan.bind("<<TreeviewSelect>>", self.pilih_pelanggan)
        
        self.refresh_pelanggan()

    def setup_supplier_tab(self):
        frame_input = ttk.LabelFrame(self.tab_supplier, text="Input Supplier")
        frame_input.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_input, text="ID Supplier:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id_supplier = ttk.Entry(frame_input)
        self.entry_id_supplier.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Nama Supplier:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_nama_supplier = ttk.Entry(frame_input)
        self.entry_nama_supplier.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_input, text="Kontak/No HP:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_kontak_supplier = ttk.Entry(frame_input)
        self.entry_kontak_supplier.grid(row=1, column=1, padx=5, pady=5)

        frame_btn = ttk.Frame(frame_input)
        frame_btn.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(frame_btn, text="Simpan", command=self.simpan_supplier).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Update", command=self.update_supplier).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Hapus", command=self.hapus_supplier).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Clear", command=self.clear_supplier).pack(side='left', padx=5)

        self.tree_supplier = ttk.Treeview(self.tab_supplier, columns=("ID", "Nama", "Kontak"), show='headings')
        self.tree_supplier.heading("ID", text="ID")
        self.tree_supplier.heading("Nama", text="Nama Supplier")
        self.tree_supplier.heading("Kontak", text="Kontak")
        self.tree_supplier.pack(expand=True, fill='both', padx=10, pady=5)
        self.tree_supplier.bind("<<TreeviewSelect>>", self.pilih_supplier)

        self.refresh_supplier()

    def setup_karyawan_tab(self):
        frame_input = ttk.LabelFrame(self.tab_karyawan, text="Input Karyawan")
        frame_input.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_input, text="ID Karyawan:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id_karyawan = ttk.Entry(frame_input)
        self.entry_id_karyawan.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Nama Karyawan:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_nama_karyawan = ttk.Entry(frame_input)
        self.entry_nama_karyawan.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_input, text="Jenis Kelamin:").grid(row=1, column=0, padx=5, pady=5)
        self.combo_jk_karyawan = ttk.Combobox(frame_input, values=["Laki-laki", "Perempuan"])
        self.combo_jk_karyawan.grid(row=1, column=1, padx=5, pady=5)

        frame_btn = ttk.Frame(frame_input)
        frame_btn.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(frame_btn, text="Simpan", command=self.simpan_karyawan).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Update", command=self.update_karyawan).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Hapus", command=self.hapus_karyawan).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Clear", command=self.clear_karyawan).pack(side='left', padx=5)

        self.tree_karyawan = ttk.Treeview(self.tab_karyawan, columns=("ID", "Nama", "JK"), show='headings')
        self.tree_karyawan.heading("ID", text="ID")
        self.tree_karyawan.heading("Nama", text="Nama Karyawan")
        self.tree_karyawan.heading("JK", text="Jenis Kelamin")
        self.tree_karyawan.pack(expand=True, fill='both', padx=10, pady=5)
        self.tree_karyawan.bind("<<TreeviewSelect>>", self.pilih_karyawan)

        self.refresh_karyawan()

    def simpan_produk(self):
        try:
            p = Produk(
                self.entry_kode_produk.get(),
                self.entry_nama_produk.get(),
                self.entry_kategori_produk.get(),
                int(self.entry_harga_produk.get()),
                int(self.entry_stok_produk.get())
            )
            p.simpan_produk_baru()
            messagebox.showinfo("Sukses", "Data Produk Berhasil Disimpan")
            self.refresh_produk()
            self.reset_form_produk()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan: {e}")

    def update_produk(self):
        try:
            p = Produk(
                self.entry_kode_produk.get(),
                self.entry_nama_produk.get(),
                self.entry_kategori_produk.get(),
                int(self.entry_harga_produk.get()),
                int(self.entry_stok_produk.get())
            )
            p.update()
            messagebox.showinfo("Sukses", "Data Produk Berhasil Diupdate")
            self.refresh_produk()
            self.reset_form_produk()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal update: {e}")

    def hapus_produk(self):
        try:
            p = Produk(self.entry_kode_produk.get(), "", "", 0, 0)
            answer = messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus?")
            if answer:
                p.delete()
                messagebox.showinfo("Sukses", "Data Produk Berhasil Dihapus")
                self.refresh_produk()
                self.reset_form_produk()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal hapus: {e}")

    def clear_produk(self):
        answer = messagebox.askyesno("Konfirmasi", "APAKAH ANDA YAKIN INGIN MENGHAPUS SELURUH DATA PRODUK?\nTindakan ini tidak dapat dibatalkan.")
        if answer:
            try:
                p = Produk("", "", "", 0, 0)
                p.hapus_semua()
                messagebox.showinfo("Sukses", "Seluruh data produk telah dihapus.")
                self.refresh_produk()
                self.reset_form_produk()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data tabel: {e}")

    def reset_form_produk(self):
        self.entry_kode_produk.delete(0, 'end')
        self.entry_nama_produk.delete(0, 'end')
        self.entry_kategori_produk.delete(0, 'end')
        self.entry_harga_produk.delete(0, 'end')
        self.entry_stok_produk.delete(0, 'end')

    def pilih_produk(self, event):
        selected = self.tree_produk.focus()
        if selected:
            values = self.tree_produk.item(selected, 'values')
            self.reset_form_produk()
            self.entry_kode_produk.insert(0, values[0])
            self.entry_nama_produk.insert(0, values[1])
            self.entry_kategori_produk.insert(0, values[2])
            self.entry_harga_produk.insert(0, values[3])
            self.entry_stok_produk.insert(0, values[4])

    def simpan_pelanggan(self):
        try:
            pl = Pelanggan(
                self.entry_id_pelanggan.get(),
                self.entry_nama_pelanggan.get(), 
                self.entry_penyakit_pelanggan.get()
            )
            pl.simpan()
            messagebox.showinfo("Sukses", "Data Pelanggan Berhasil Disimpan")
            self.refresh_pelanggan()
            self.reset_form_pelanggan()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan: {e}")

    def update_pelanggan(self):
        try:
            pl = Pelanggan(
                self.entry_id_pelanggan.get(),
                self.entry_nama_pelanggan.get(), 
                self.entry_penyakit_pelanggan.get()
            )
            pl.update()
            messagebox.showinfo("Sukses", "Data Pelanggan Berhasil Diupdate")
            self.refresh_pelanggan()
            self.reset_form_pelanggan()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal update: {e}")

    def hapus_pelanggan(self):
        try:
            pl = Pelanggan(self.entry_id_pelanggan.get(), "", "")
            answer = messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus?")
            if answer:
                pl.delete()
                messagebox.showinfo("Sukses", "Data Pelanggan Berhasil Dihapus")
                self.refresh_pelanggan()
                self.reset_form_pelanggan()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal hapus: {e}")

    def clear_pelanggan(self):
        answer = messagebox.askyesno("Konfirmasi", "APAKAH ANDA YAKIN INGIN MENGHAPUS SELURUH DATA PELANGGAN?")
        if answer:
            try:
                pl = Pelanggan("", "", "")
                pl.hapus_semua()
                messagebox.showinfo("Sukses", "Seluruh data pelanggan telah dihapus.")
                self.refresh_pelanggan()
                self.reset_form_pelanggan()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data tabel: {e}")

    def reset_form_pelanggan(self):
        self.entry_id_pelanggan.delete(0, 'end')
        self.entry_nama_pelanggan.delete(0, 'end')
        self.entry_penyakit_pelanggan.delete(0, 'end')

    def pilih_pelanggan(self, event):
        selected = self.tree_pelanggan.focus()
        if selected:
            values = self.tree_pelanggan.item(selected, 'values')
            self.reset_form_pelanggan()
            self.entry_id_pelanggan.insert(0, values[0])
            self.entry_nama_pelanggan.insert(0, values[1])
            self.entry_penyakit_pelanggan.insert(0, values[2])

    def simpan_supplier(self):
        try:
            sp = Supplier(
                self.entry_id_supplier.get(),
                self.entry_nama_supplier.get(), 
                self.entry_kontak_supplier.get()
            )
            sp.simpan()
            messagebox.showinfo("Sukses", "Data Supplier Berhasil Disimpan")
            self.refresh_supplier()
            self.reset_form_supplier()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan: {e}")

    def update_supplier(self):
        try:
            sp = Supplier(
                self.entry_id_supplier.get(),
                self.entry_nama_supplier.get(), 
                self.entry_kontak_supplier.get()
            )
            sp.update()
            messagebox.showinfo("Sukses", "Data Supplier Berhasil Diupdate")
            self.refresh_supplier()
            self.reset_form_supplier()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal update: {e}")

    def hapus_supplier(self):
        try:
            sp = Supplier(self.entry_id_supplier.get(), "", "")
            answer = messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus?")
            if answer:
                sp.delete()
                messagebox.showinfo("Sukses", "Data Supplier Berhasil Dihapus")
                self.refresh_supplier()
                self.reset_form_supplier()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal hapus: {e}")

    def clear_supplier(self):
        answer = messagebox.askyesno("Konfirmasi", "APAKAH ANDA YAKIN INGIN MENGHAPUS SELURUH DATA SUPPLIER?")
        if answer:
            try:
                sp = Supplier("", "", "")
                sp.hapus_semua()
                messagebox.showinfo("Sukses", "Seluruh data supplier telah dihapus.")
                self.refresh_supplier()
                self.reset_form_supplier()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data tabel: {e}")

    def reset_form_supplier(self):
        self.entry_id_supplier.delete(0, 'end')
        self.entry_nama_supplier.delete(0, 'end')
        self.entry_kontak_supplier.delete(0, 'end')

    def pilih_supplier(self, event):
        selected = self.tree_supplier.focus()
        if selected:
            values = self.tree_supplier.item(selected, 'values')
            self.reset_form_supplier()
            self.entry_id_supplier.insert(0, values[0])
            self.entry_nama_supplier.insert(0, values[1])
            self.entry_kontak_supplier.insert(0, values[2])

    def simpan_karyawan(self):
        try:
            kr = Karyawan(
                self.entry_id_karyawan.get(),
                self.entry_nama_karyawan.get(), 
                self.combo_jk_karyawan.get()
            )
            kr.simpan()
            messagebox.showinfo("Sukses", "Data Karyawan Berhasil Disimpan")
            self.refresh_karyawan()
            self.reset_form_karyawan()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan: {e}")

    def update_karyawan(self):
        try:
            kr = Karyawan(
                self.entry_id_karyawan.get(),
                self.entry_nama_karyawan.get(), 
                self.combo_jk_karyawan.get()
            )
            kr.update()
            messagebox.showinfo("Sukses", "Data Karyawan Berhasil Diupdate")
            self.refresh_karyawan()
            self.reset_form_karyawan()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal update: {e}")

    def hapus_karyawan(self):
        try:
            kr = Karyawan(self.entry_id_karyawan.get(), "", "")
            answer = messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus?")
            if answer:
                kr.delete()
                messagebox.showinfo("Sukses", "Data Karyawan Berhasil Dihapus")
                self.refresh_karyawan()
                self.reset_form_karyawan()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal hapus: {e}")

    def clear_karyawan(self):
        answer = messagebox.askyesno("Konfirmasi", "APAKAH ANDA YAKIN INGIN MENGHAPUS SELURUH DATA KARYAWAN?")
        if answer:
            try:
                kr = Karyawan("", "", "")
                kr.hapus_semua()
                messagebox.showinfo("Sukses", "Seluruh data karyawan telah dihapus.")
                self.refresh_karyawan()
                self.reset_form_karyawan()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data tabel: {e}")

    def reset_form_karyawan(self):
        self.entry_id_karyawan.delete(0, 'end')
        self.entry_nama_karyawan.delete(0, 'end')
        self.combo_jk_karyawan.set('')

    def pilih_karyawan(self, event):
        selected = self.tree_karyawan.focus()
        if selected:
            values = self.tree_karyawan.item(selected, 'values')
            self.reset_form_karyawan()
            self.entry_id_karyawan.insert(0, values[0])
            self.entry_nama_karyawan.insert(0, values[1])
            self.combo_jk_karyawan.set(values[2])

    def refresh_produk(self):
        for i in self.tree_produk.get_children():
            self.tree_produk.delete(i)
        self.cursor.execute("SELECT * FROM produk")
        for row in self.cursor.fetchall():
            self.tree_produk.insert("", "end", values=row)

    def refresh_pelanggan(self):
        for i in self.tree_pelanggan.get_children():
            self.tree_pelanggan.delete(i)
        self.cursor.execute("SELECT * FROM pelanggan")
        for row in self.cursor.fetchall():
            self.tree_pelanggan.insert("", "end", values=row)

    def refresh_supplier(self):
        for i in self.tree_supplier.get_children():
            self.tree_supplier.delete(i)
        self.cursor.execute("SELECT * FROM supplier")
        for row in self.cursor.fetchall():
            self.tree_supplier.insert("", "end", values=row)

    def refresh_karyawan(self):
        for i in self.tree_karyawan.get_children():
            self.tree_karyawan.delete(i)
        self.cursor.execute("SELECT * FROM karyawan")
        for row in self.cursor.fetchall():
            self.tree_karyawan.insert("", "end", values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = MasterApp(root)
    root.mainloop()