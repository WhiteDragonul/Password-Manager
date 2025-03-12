import tkinter as tk
from tkinter import messagebox
import os
import sqlite3

root=tk.Tk()
root.title("Criptare parole")
root.geometry("400x300")


def init_db():
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def save_password():
    service=entry_service.get()
    username=entry_username.get()
    password=entry_password.get()

    if not service or not username or not password:
        messagebox.showerror("Eroare!","Completati campul de service, username sau parola!")
        return
    conn=sqlite3.connect("password_manager.db")
    cursor=conn.cursor()

    cursor.execute("INSERT INTO passwords (service,username,password) VALUES (?, ?, ?)",
                   (service,username,password))

    conn.commit()
    conn.close()

    messagebox.showinfo("Succes!","Parola a fost salvata!")

    entry_service.delete(0,tk.END)
    entry_username.delete(0,tk.END)
    entry_password.delete(0,tk.END)

def view_password():
    conn=sqlite3.connect("password_manager.db")
    cursor=conn.cursor()
    cursor.execute("SELECT service, username, password from passwords")
    records=cursor.fetchall()
    conn.close()

    password_list=tk.Toplevel(root)
    password_list.title("Parole Salvate")

    tk.Label(password_list, text="Serviciu | Utilizator | Parola", font=("Arial",12,"bold")).pack(pady=5)


    for record in records:
        tk.Label(password_list,text=f"{record[0]} | {record[1]} | {record[2]} ").pack()

def search_password():
    service=entry_service.get()

    if not service:
        messagebox.showerror("Eroare!","Introdu numele serviciului!")
        return
    conn=sqlite3.connect("password_manager.db")
    cursor=conn.cursor()

    cursor.execute("SELECT username, password FROM passwords WHERE service= ?",(service,))
    record=cursor.fetchone()

    conn.close()

    if record:
        messagebox.showinfo("Rezultat", f"Utilizator: {record[0]}\nParolă: {record[1]}")
    else:
        messagebox.showerror("Eroare!","Serviciul nu a fost gasit!")

def delete_password():
    service=entry_service.get()
    username=entry_username.get()

    if not service or not username:
        messagebox.showerror("Eroare!","Campurile service si username sunt obligatorii!")
        return
    conn=sqlite3.connect("password_manager.db")
    cursor=conn.cursor()

    cursor.execute("DELETE FROM passwords WHERE service= ? AND username= ?",
                   (service,username))
    conn.commit()

    conn.close()

    messagebox.showinfo("Succes!","Parola a fost stearsa!")

init_db()

tk.Label(root,text="Serviciu:").pack(pady=5)
entry_service=tk.Entry(root,width=40)
entry_service.pack()

tk.Label(root,text="Utilizator:").pack(pady=5)
entry_username=tk.Entry(root,width=40)
entry_username.pack()

tk.Label(root,text="Parola").pack(pady=5)
entry_password=tk.Entry(root,width=40,show="*")
entry_password.pack()

btn_save=tk.Button(root,text="Salveaza Parola",command=save_password)
btn_save.pack(pady=5)

btn_view=tk.Button(root,text="Vizualizeaza Parola",command=view_password)
btn_view.pack(pady=5)

btn_search=tk.Button(root,text="Cauta Parola",command=search_password)
btn_search.pack(pady=5)

btn_delete=tk.Button(root,text="Sterge Parola",command=delete_password)
btn_delete.pack(pady=5)


root.mainloop()