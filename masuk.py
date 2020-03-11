import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import pymysql
from datetime import *
from tkinter import messagebox
import time


class Baru:
    def __init__(self, parent, title):
        self.parent = parent
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOW", self.keluar)
        lebar = 250
        tinggi = 150
        setTengahX = (self.parent.winfo_screenwidth()-lebar)//2
        setTengahY = (self.parent.winfo_screenheight()-tinggi)
        self.parent.geometry("%ix%i+%i+%i" %
                             (lebar, tinggi, setTengahX, (setTengahY/2)))
        self.parent.resizable(False, False)
        self.interface()
        self.mati()

    def interface(self):
        newFrame = Frame(self.parent)
        newFrame.pack(side=LEFT)
        Label(newFrame, text='-- Portal Masuk --').grid(row=0, column=0, sticky=W)
        Label(newFrame, text='DateTime').grid(row=1, column=0, sticky=W)
        self.entDateTime = Entry(newFrame, width=20)
        self.entDateTime.grid(row=1, column=1)
        dtime = time.strftime("%Y-%m-%d %H:%M:%S")
        self.entDateTime.insert(0, dtime)
        Label(newFrame, text='No. Polisi').grid(row=2, column=0, sticky=W)
        self.entNopol = Entry(newFrame, width=20)
        self.entNopol.grid(row=2, column=1)
        Label(newFrame, text='Tipe Kendaraan (Roda)').grid(
            row=3, column=0, sticky=W)
        self.entTipe = ttk.Combobox(
            newFrame, values=('Motor', 'Mobil'), width=17)
        self.entTipe.grid(row=3, column=1)
        Label(newFrame, text='').grid(row=4, column=0, sticky=W)
        self.btnBaru = Button(newFrame, text='Tambah',
                              command=self.tambah, width=10)
        self.btnBaru.grid(row=10, column=0)
        self.btnSimpan = Button(newFrame, text='Simpan',
                                command=self.simpan, width=10)
        self.btnSimpan.grid(row=10, column=1)
        Label(newFrame, text='').grid(row=12, column=0, sticky=W)

    def keluar(self, event=None):
        self.parent.destroy()

    def simpan(self, event=None):
        con = pymysql.connect(db='parkiran', user='root', passwd='',
                              host='127.0.0.1', port=3306, autocommit=True)
        cur = con.cursor()
        # get text data
        nopol = self.entNopol.get()
        waktu = self.entDateTime.get()
        jenis = self.entTipe.get()
        cur.execute(
            "INSERT INTO parkir_data(nopol,jenis,jam_masuk) VALUES(%s,%s,%s)", (nopol, jenis, waktu,))
        messagebox.showinfo(title="Sukses", message="Data sudah di tersimpan.")
        cur.close()
        con.close()
        self.kosong()
        self.mati()
        self.btnBaru.config(stat="normal")
        self.btnSimpan.config(stat="disabled")

    def tambah(self, event=None):
        self.entNopol.config(state="normal")
        self.entTipe.config(state="normal")
        self.btnBaru.config(state="disabled")
        self.btnSimpan.config(state="normal")
        self.entNopol.focus_set()

    def kosong(self, event=None):
        self.entNopol.delete(0, END)
        self.entTipe.delete(0, END)

    def mati(self, event=None):
        self.entDateTime.config(state="readonly")
        self.entNopol.config(state="readonly")
        self.entTipe.config(state="disabled")
        self.btnSimpan.config(stat="disabled")


root = Tk()
Baru(root, "-- Portal Masuk --")
root.mainloop()
