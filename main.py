import tkinter as tk
from db_config import Database
from auth import LoginApp

if __name__ == "__main__":
    _ = Database()
    
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()