import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#cria o client
def listen_for_messages_from_server(client):#recebe mensagens do server
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")
            
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")
            
def add_message(message):#coloca mensagens no historico do chat
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():#função do botão Join conecta como server
    try:
        client.connect(('localhost', 9090))
        print("Successfully connected to server")
        add_message("Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server")
    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")
    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()
    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():#função do botão send envia a mensagem para o server
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")
#parte gráfica da aplicação
root = tk.Tk()
root.geometry("600x600")
root.title("Messenger Client")
root.resizable(False, False)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)
top_frame = tk.Frame(root, width=600, height=100, bg='lightgray')
top_frame.grid(row=0, column=0, sticky=tk.NSEW)
middle_frame = tk.Frame(root, width=600, height=400, bg='gray')
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)
bottom_frame = tk.Frame(root, width=600, height=100, bg='lightgray')
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)
username_label = tk.Label(top_frame, text="Enter username:", font=('Arial', 14), bg='lightgray', fg = 'black')
username_label.pack(side=tk.LEFT, padx=10)
username_textbox = tk.Entry(top_frame, font=('Arial', 14), bg='white', width=23)
username_textbox.pack(side=tk.LEFT)
username_button = tk.Button(top_frame, text="Join", font=('Arial', 13), bg='lightgray', command=connect)
username_button.pack(side=tk.LEFT, padx=15)
message_textbox = tk.Entry(bottom_frame, font=('Arial', 14), bg='white', width=38)
message_textbox.pack(side=tk.LEFT, padx=10)
message_button = tk.Button(bottom_frame, text="Send", font=('Arial', 13), bg='lightgray', command=send_message)
message_button.pack(side=tk.LEFT, padx=10)
message_box = scrolledtext.ScrolledText(middle_frame, font=('Arial', 12), bg='white', width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)
root.mainloop()
    
