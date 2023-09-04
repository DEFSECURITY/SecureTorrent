import socket
import threading
import base64
EOD = b'!!!'
def reqh(data, respond):
    print(data)
    respond(data)
def connh(conn, addr):
    with conn:
        d = b''
        print(addr)
        while True:
            data = conn.recv(1) # recv
            if not data:
                break
            d = d + data
            try:
                if d[-1] == ord('!') and d[-2] == ord('!') and d[-3] == ord('!'): # 3 "!"s is the end
                    def respond(data):
                        conn.send(base64.encodebytes(data))
                        conn.send(EOD)
                    reqh(base64.decodebytes(d[:-3]), respond)
                    d = b''
            except IndexError:
                pass
HOST = '0.0.0.0'
PORT = 9832
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    while True:
        conn, addr = server.accept()
        f = open(conn.fileno(), closefd=False)
        threading.Thread(target=connh, args=[conn, addr]).start()