from app.client.client import Client
import tkinter as tk

root= tk.Tk()
root.title('Register Client')
canvas = tk.Canvas(root, width=400, height=300, relief='raised')
canvas.pack()

label1 = tk.Label(root, text='Register user')
label1.config(font=('helvetica', 14))
canvas.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Type your username:')
label2.config(font=('helvetica', 10))
canvas.create_window(200, 100, window=label2)

entry_login = tk.Entry (root) 
canvas.create_window(200, 120, window=entry_login)

label3 = tk.Label(root, text='Type your password:')
label3.config(font=('helvetica', 10))
canvas.create_window(200, 160, window=label3)

entry_password = tk.Entry (root) 
canvas.create_window(200, 180, window=entry_password)

def register_client():
    x1 = entry_login.get()
    x2 = entry_password.get()
    if x1.strip() != "":
        client = Client(x1.strip())
        try:
            client.register_client()
            root.destroy()
            client.open_gui()
        except Exception as e:
            print(e)
        finally:
            client.kill_daemon()

button1 = tk.Button(text='Register', command=register_client, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas.create_window(200, 230, window=button1)
root.mainloop()