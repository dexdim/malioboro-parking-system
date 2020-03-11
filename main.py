import tkinter
from tkinter import *


def parkirin():
    import masuk


def parkirout():
    import keluar


def login():
    import login


def about():
    tkinter.messagebox.showinfo(
        title="Informasi", message="Sistem Parkir Malioboro")


root = Tk()
root['bg'] = 'gray'
root.title("Sistem Parkir Malioboro 2.0")
root.geometry("1024x720")

menubar = Menu(root)
master = Menu(menubar, tearoff=0)

fl = Menu(master, tearoff=0)  # Menu File
master.add_command(label="Login", command=login)
master.add_command(label="Portal Masuk", command=parkirin)
master.add_command(label="Portal Keluar", command=parkirout)
master.add_separator()
master.add_command(label="Keluar", command=root.destroy)
menubar.add_cascade(label="File", menu=master)  # Menu Utama (File)

tt = Menu(menubar, tearoff=0)  # Menu Laporan
tt.add_command(label="Tentang", command=about)
menubar.add_cascade(label="Tentang", menu=tt)  # Menu Utama 3 (Tentang)

root.config(menu=menubar)
root.mainloop()
