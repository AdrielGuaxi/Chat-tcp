import socket
import threading

active_clients = [] #lista de clientes conectados no server
def listen_for_messages(client, username): #função que recebe as mensagens dos clients conectados
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':   
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        else:
            print(f"The message send from client {username} is empty")
            
def send_message_to_client(client, message):#função que transmite mensagens para um client 
    client.sendall(message.encode())
    
def send_messages_to_all(message):#função que usa a send_message_to_client em loop para mandar a mensagem para todos os clients
    for user in active_clients:
        send_message_to_client(user[1], message)
        
def client_handler(client):#função que gere os dados cliente no server como username e gere o chat
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")
    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#cria o server
server.bind(('localhost', 9090))#atribui endereço ao servidor
server.listen()#abre para conexões
print("Waiting for connection")
while 1:
    client, address = server.accept()#aceita conexões
    print(f"Successfully connected to client {address[0]} {address[1]}")
    threading.Thread(target=client_handler, args=(client, )).start()#começa o chat