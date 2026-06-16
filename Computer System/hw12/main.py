from multiprocessing import Process
from app import run_http_server
from sock import run_socket_server

#pапуск окремих процесів http та socket
if __name__ == '__main__':
    http_process = Process(target= run_http_server)
    socket_process = Process(target= run_socket_server)
    http_process.start()
    socket_process.start()

    http_process.join()
    socket_process.join()
