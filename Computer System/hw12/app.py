from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
from db import init_db, save_message, get_messages
import os

BASE = os.path.dirname(os.path.abspath(__file__))

class processing_requests(BaseHTTPRequestHandler):
    def do_GET(self):
        filename = 'index.html' if self.path == '/' else self.path.lstrip('/')
        file_path = os.path.join(BASE, filename)
                                 
        try:
            with open(file_path, 'rb') as file: #відкриття та читання файлу
                content = file.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content)
            messages = get_messages()
            print(messages)

        except FileNotFoundError: #якщо файл не знайдено, переходимо до інструкції 
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(os.path.join(BASE, 'error.html'), 'rb') as file:
                self.wfile.write(file.read())

    def do_POST(self): #зчитування даних
        if self.path == '/message':
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length)
        
            save_message(data.decode())

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #передача даних через порт
            sock.connect(('localhost', 5000))
            sock.send(data)
            sock.close()

            self.send_response(302) #перехід на головну стр
            self.send_header('location', '/')
            self.end_headers()
            
init_db()
if __name__ == '__main__':
    print('Сервер працює на http://localhost:3000')
    HTTPServer(('localhost', 3000), processing_requests).serve_forever()