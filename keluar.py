import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import pymysql
from datetime import *
from tkinter import messagebox
import time


class PortalKeluar:
    def __init__(self, parent, title):
        self.parent = parent
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOW", self.keluar)
        lebar = 400
        tinggi = 250
        setTengahX = (self.parent.winfo_screenwidth()-lebar)//2
        setTengahY = (self.parent.winfo_screenwidth()-tinggi)//2
        self.parent.geometry("%ix%i+%i+%i" %
                             (lebar, tinggi, setTengahX, setTengahY))
        self.parent.resizable(False, False)
        self.interface()
        self.isiListBox()
        self.isiData()
        self.aturKejadian()
        self.listboxData.focus_set()
        self.mati()

    def hitung(self, event=None):
        perjam = self.entPerJam.get()
        # MENCARI SELISIH WAKTU
        # selisih hari
        tglmasuk, waktumasuk = self.entDateTimeMasuk.get().split(" ")
        Dmasuk, Mmasuk, Ymasuk = tglmasuk.split("-")
        jammasuk, mntmasuk, dtmasuk = waktumasuk.split(":")
        # selisih jam
        tglnow, waktunow = self.entDateTime.get().split(" ")
        Dnow, Mnow, Ynow = tglnow.split("-")
        jamnow, mntnow, dtnow = waktunow.split(":")

        # hitung
        getSelisihHari = ((int(Dnow)-int(Dmasuk)) +
                          (int(Mnow)-int(Mmasuk))+(int(Ynow)-int(Ymasuk)))*24
        # print(getSelisihHari)
        getSelisihWaktu = (((int(jamnow)-int(jammasuk))*3600) +
                           ((int(mntnow)-int(mntmasuk))*60)+(int(dtnow)-int(dtmasuk)))/3600
        # print(getSelisihWaktu)
        getTotalSelisih = round(getSelisihHari + getSelisihWaktu, 2)
        # print(getTotalSelisih)
        bulatkan = str(getTotalSelisih).split(".")
        # print(bulatkan)
        if(int(bulatkan[1]) > 0):
            totaljam = int(bulatkan[0])+1
        else:
            totaljam = int(bulatkan[0])

        totalBayar = int(perjam)*totaljam
        self.entBayar.config(state="normal")
        self.entBayar.delete(0, END)
        self.entBayar.insert(0, totalBayar)
        self.entBayar.config(state="readonly")

    def keluar(self, event=None):
        self.parent.destroy()

    def simpanubahdata(self, event=None):
        con = pymysql.connect(db='parkiran', user='root', passwd='',
                              host='127.0.0.1', port=3306, autocommit=True)
        cur = con.cursor()
        # get text data
        parkirId = self.entParkirId.get()
        waktukeluar = self.entDateTime.get()
        bayar = self.entBayar.get()
        cur.execute("UPDATE parkir_data SET jam_keluar= %s,total_bayar=%s WHERE id=%s",
                    (waktukeluar, bayar, parkirId))
        messagebox.showinfo(title="Sukses", message="Data sudah di tersimpan.")
        cur.close()
        con.close()
        self.hidup()
        self.kosong()
        self.mati()
        self.isiListBox()

    def kosong(self):
        self.entNopol.delete(0, END)
        self.entParkirId.delete(0, END)
        self.entTipe.delete(0, END)
        self.entDateTimeMasuk.delete(0, END)
        self.entPerJam.delete(0, END)
        self.entBayar.delete(0, END)

    def mati(self):
        self.entDateTime.config(state="readonly")
        self.entParkirId.config(state="readonly")
        self.entTipe.config(state="readonly")
        self.entDateTimeMasuk.config(state="readonly")
        self.entBayar.config(state="readonly")
        self.entPerJam.config(state="readonly")

    def hidup(self):
        self.entParkirId.config(state="normal")
        self.entTipe.config(state="normal")
        self.entDateTimeMasuk.config(state="normal")
        self.entPerJam.config(state="normal")
        self.entBayar.config(state="normal")
        self.entPerJam.config(state="normal")

    def aturKejadian(self):
        self.listboxData.bind('<ButtonRelease-1>', self.onKlikLB)
        self.listboxData.bind('<KeyRelease-1>', self.onKlikLB)

    def onKlikLB(self, event=None):
        self.isiData()

    def isiData(self):
        indeks = self.listboxData.curselection()
        kode = int(indeks[0])
        self.dipilih = kode
        # apusDT
        self.hidup()
        self.entParkirId.delete(0, END)
        self.entNopol.delete(0, END)
        self.entTipe.delete(0, END)
        self.entDateTimeMasuk.delete(0, END)
        self.entPerJam.delete(0, END)
        self.entBayar.delete(0, END)
        # isiDT
        self.entParkirId.insert(END, self.dataparkir[kode][0])
        self.entNopol.insert(END, self.dataparkir[kode][1])
        self.entTipe.insert(END, self.dataparkir[kode][2])
        self.entDateTimeMasuk.insert(END, self.dataparkir[kode][3])
        self.entPerJam.insert(END, self.dataparkir[kode][7])
        self.mati()

    def isiListBox(self):
        con = pymysql.connect(db='parkiran', user='root', passwd='',
                              host='127.0.0.1', port=3306, autocommit=True)
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM parkir_data INNER JOIN perjam ON jenis_kendaraan = jenis WHERE total_bayar = ''")
        self.dataparkir = cur.fetchall()
        self.listboxData.delete(0, END)
        for dat in range(len(self.dataparkir)):
            self.listboxData.insert(END, self.dataparkir[dat][1])
        self.listboxData.selection_set(0)
        cur.close()
        con.close()

    def interface(self):
        mainFrame = Frame(self.parent)
        mainFrame.pack(fill=BOTH, expand=YES)
        # frmkiri
        fr_kiri = Frame(mainFrame, bd=10)
        fr_kiri.pack(fill=BOTH, expand=YES, side=LEFT)

        t = Label(fr_kiri, text="Nopol:")
        t.pack()
        scroll = Scrollbar(fr_kiri, orient=VERTICAL)
        self.listboxData = Listbox(
            fr_kiri, width=15, yscrollcommand=scroll.set)

        self.listboxData.pack(fill=Y, side=LEFT)
        scroll.configure(command=self.listboxData.yview)
        scroll.pack(side=LEFT, fill=Y)
        # frmkanan
        fr_kanan = Frame(mainFrame, bd=10)
        fr_kanan.pack(fill=BOTH, expand=YES, side=RIGHT)

        fr_katas = Frame(fr_kanan)
        fr_katas.pack(side=TOP, expand=YES)

        Label(fr_katas, text='DateTime').grid(row=0, column=0, sticky=W)
        self.entDateTime = Entry(fr_katas, width=20)
        self.entDateTime.grid(row=0, column=1, sticky=W)
        dtime = time.strftime("%Y-%m-%d %H:%M:%S")
        self.entDateTime.insert(0, dtime)

        Label(fr_katas, text='No. Polisi').grid(row=1, column=0, sticky=W)
        self.entNopol = Entry(fr_katas, width=20)
        self.entNopol.grid(row=1, column=1, sticky=W)

        Label(fr_katas, text='Parkir Id').grid(row=2, column=0, sticky=W)
        self.entParkirId = Entry(fr_katas, width=20)
        self.entParkirId.grid(row=2, column=1)

        Label(fr_katas, text='Tipe Kendaraan (Roda)').grid(
            row=3, column=0, sticky=W)
        self.entTipe = Entry(fr_katas, width=20)
        self.entTipe.grid(row=3, column=1)

        Label(fr_katas, text='Jam Masuk').grid(row=4, column=0, sticky=W)
        self.entDateTimeMasuk = Entry(fr_katas, width=20)
        self.entDateTimeMasuk.grid(row=4, column=1)

        Label(fr_katas, text='Per Jam').grid(row=5, column=0, sticky=W)
        self.entPerJam = Entry(fr_katas, width=20)
        self.entPerJam.grid(row=5, column=1)

        self.btnHitung = Button(fr_katas, text='Hitung',
                                command=self.hitung, width=10)
        self.btnHitung.grid(row=6, column=1)

        Label(fr_katas, text='Total Bayar').grid(row=7, column=0, sticky=W)
        self.entBayar = Entry(fr_katas, width=20)
        self.entBayar.grid(row=7, column=1)

        fr_kawah = Frame(fr_kanan)
        fr_kawah.pack(side=BOTTOM, expand=YES)

        self.btnSimpan = Button(fr_kawah, text='Simpan',
                                command=self.simpanubahdata, width=10)
        self.btnSimpan.pack(side=LEFT)


root = Tk()
PortalKeluar(root, "-- Portal Keluar --")
root.mainloop()
