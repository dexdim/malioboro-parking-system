import tkinter.ttk
from tkinter import *
from tkinter import messagebox
import pymysql


class Login():
    def __init__(self, parent, title):
        self.parent = parent
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOWS", self.keluar)
        lebar = 250
        tinggi = 130
        setTengahX = (self.parent.winfo_screenwidth()-lebar)//2
        setTengahY = (self.parent.winfo_screenheight()-tinggi)//2
        self.parent.geometry("%ix%i+%i+%i" %
                             (lebar, tinggi, setTengahX, setTengahY))
        self.parent.resizable(False, False)
        self.tampilan()

    def keluar(self, event=None):
        self.parent.destroy()

    def cekuser(self):
        con = pymysql.connect(db='parkiran', user='root', passwd='',
                              host='127.0.0.1', port=3306, autocommit=True)
        uname = self.entryUsername.get()
        upass = self.entryPassword.get()
        cur = con.cursor()
        cur.execute(
            "SELECT username,password FROM user WHERE username = %s AND password= %s", (uname, upass))
        if(cur.rowcount > 0):
            root.destroy()
            import main
        else:
            messagebox.showwarning(
                title="Error!", message="Username/Password anda salah!")
            self.entryUsername.delete(0, END)
            self.entryPassword.delete(0, END)
            self.entryUsername.focus_set()

    def tampilan(self):
        frameUtama = Frame(self.parent)
        frameUtama.grid(row=0, column=1)
        Label(frameUtama, text=' ').grid(row=0, column=0)
        Label(frameUtama, text=' ').grid(row=1, column=0)
        self.labelUsername = Label(
            frameUtama, text="Username", width=9, height=2)
        self.labelUsername.grid(row=1, column=1)
        self.labelPassword = Label(
            frameUtama, text="Password", width=9, height=2)
        self.labelPassword.grid(row=2, column=1, )
        self.entryUsername = Entry(frameUtama, width=25)
        self.entryUsername.grid(row=1, column=2)
        self.entryPassword = Entry(frameUtama, show='*', width=25)
        self.entryPassword.grid(row=2, column=2)
        self.btnLogin = Button(frameUtama, text='Login',
                               command=self.cekuser, width=10)
        self.btnLogin.grid(row=3, column=2)
        self.entryUsername.focus_set()


root = Tk()
Login(root, "-- Form Login --")
root.mainloop()
