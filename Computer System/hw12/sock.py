import socket
from datetime import datetime
from pymongo import MongoClient
from concurrent import futures as cf

tcp_ip = 'localhost'
tcp_port = 5000

#підключення бази даних
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["messages_db"]
collection = db["messages"]

#конект нових користувачів
def connection_client(client_socket, address):
    print(f'Підключення нового клієнта {address}')
    client_socket.settimeout(3.0)
    try:
        data_recv = client_socket.recv(1024)
        if data_recv:
            data_str = data_recv.decode()

            #розьиття рядка користувач + його повідомлення
            parts = data_str.split("&")
            username = parts[0].split("=")[1]
            message = parts[1].split("=")[1]

            docs = {'date': str(datetime.now()),
            'username': username,
            'message': message}

            collection.insert_one(docs)
            print(f'Дані успішно завантажено на сервер')

    except socket.timeout:
        print(f'Зʼєднання розірвано через довге підключення')

    except Exception as error_db:
        print(f'Помилка обробки даних')

    finally:
        client_socket.close()

#запуск сервера на 5000 порту, прослуховування підключень та передача даних на сервак
def run_server(tcp_ip, tcp_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((tcp_ip, tcp_port))
    server.listen(10)
    server.settimeout(2.0)
    print("Socket server працює на localhost 5000")

    try:
        with cf.ThreadPoolExecutor(10) as client_pool:
            while True:
                try:
                    client_socket, address = server.accept()
                    print(f'Підключення встановлено {address}')
                    client_pool.submit(connection_client, client_socket, address)
                except socket.timeout:
                    continue

    except KeyboardInterrupt:
        print('Вимушена зупинка сервера')
    
    finally:server.close()

def run_socket_server():
    run_server(tcp_ip, tcp_port)

if __name__ == '__main__':
    run_socket_server()



