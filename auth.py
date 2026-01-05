import tkinter as tk
from tkinter import messagebox, ttk
from models import Auth
from master import MasterApp
from transaksi import TransaksiApp

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Sistem Apotek")
        self.root.geometry("400x500")
        self.root.eval('tk::PlaceWindow . center')

        self.auth_model = Auth()

        frame_login = tk.Frame(root)
        frame_login.pack(expand=True)

        tk.Label(frame_login, text="SISTEM MANAJEMEN APOTEK", font=("Arial", 14, "bold")).pack(pady=20)

        tk.Label(frame_login, text="Username").pack(anchor="w", padx=20)
        self.entry_username = tk.Entry(frame_login, width=40)
        self.entry_username.pack(padx=20, pady=5)

        tk.Label(frame_login, text="Password").pack(anchor="w", padx=20)
        self.entry_password = tk.Entry(frame_login, show="*", width=40)
        self.entry_password.pack(padx=20, pady=5)

        tk.Button(frame_login, text="LOGIN", command=self.handle_login, bg="#4CAF50", fg="white", width=20).pack(pady=15)
        
        tk.Button(frame_login, text="Daftar Akun Baru", command=self.buka_register, bg="#2196F3", fg="white", width=20).pack(pady=5)

    def handle_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        user = self.auth_model.login(username, password)

        if user:
            id_akun, nama, peran = user
            messagebox.showinfo("Login Berhasil", f"Selamat Datang, {nama}!\nLogin sebagai: {peran}\nAbsensi telah tercatat.")
            self.root.destroy()
            self.open_dashboard(peran)
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah.")

    def buka_register(self):
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Registrasi Akun")
        reg_window.geometry("350x550")
        
        tk.Label(reg_window, text="ID Akun:").pack(pady=2, anchor="w", padx=20)
        entry_reg_id_akun = tk.Entry(reg_window, width=30)
        entry_reg_id_akun.pack(padx=20)

        tk.Label(reg_window, text="Nama Lengkap:").pack(pady=2, anchor="w", padx=20)
        entry_reg_nama = tk.Entry(reg_window, width=30)
        entry_reg_nama.pack(padx=20)

        tk.Label(reg_window, text="Username:").pack(pady=2, anchor="w", padx=20)
        entry_reg_user = tk.Entry(reg_window, width=30)
        entry_reg_user.pack(padx=20)

        tk.Label(reg_window, text="Password:").pack(pady=2, anchor="w", padx=20)
        entry_reg_pass = tk.Entry(reg_window, show="*", width=30)
        entry_reg_pass.pack(padx=20)

        tk.Label(reg_window, text="ID Karyawan (Data Pegawai):").pack(pady=2, anchor="w", padx=20)
        entry_reg_id_karyawan = tk.Entry(reg_window, width=30)
        entry_reg_id_karyawan.pack(padx=20)

        tk.Label(reg_window, text="Jenis Kelamin:").pack(pady=2, anchor="w", padx=20)
        combo_reg_jk = ttk.Combobox(reg_window, values=["Laki-laki", "Perempuan"], width=27)
        combo_reg_jk.pack(padx=20)
        combo_reg_jk.current(0)

        tk.Label(reg_window, text="Peran:").pack(pady=2, anchor="w", padx=20)
        combo_reg_peran = ttk.Combobox(reg_window, values=["Admin", "Kasir"], width=27)
        combo_reg_peran.pack(padx=20)
        combo_reg_peran.current(1)

        def proses_daftar():
            id_akun = entry_reg_id_akun.get()
            nama = entry_reg_nama.get()
            user = entry_reg_user.get()
            pw = entry_reg_pass.get()
            role = combo_reg_peran.get()
            id_kar = entry_reg_id_karyawan.get()
            jk = combo_reg_jk.get()

            if not id_akun or not nama or not user or not pw or not id_kar or not jk:
                messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
                return

            sukses = self.auth_model.registrasi(id_akun, nama, user, pw, role, id_kar, jk)
            
            if sukses:
                messagebox.showinfo("Sukses", "Akun berhasil dibuat! Silakan Login.")
                reg_window.destroy()
            else:
                messagebox.showerror("Gagal", "Username atau ID sudah digunakan!")

        tk.Button(reg_window, text="SIMPAN", command=proses_daftar, bg="#4CAF50", fg="white", width=15).pack(pady=20)

    def open_dashboard(self, peran):
        new_root = tk.Tk()
        if peran == "Admin":
            app = MasterApp(new_root)
        elif peran == "Kasir":
            app = TransaksiApp(new_root)
        else:
            app = TransaksiApp(new_root)
        
        new_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()