import sys
sys.path.append('..')
import socket
import threading
import cypto
import config
import time

class STSocketServerConnectionHandler(threading.Thread):
    def __init__(self, conn, addr, INIT_KEY):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.cypto = cypto.cypto()
        self.cypto.setKey(INIT_KEY)
        self.EOD = b'!!!'
    def run(self):
        with self.conn:
            d = bytearray()
            print('Connected by', self.addr[0])
            while True:
                data = self.conn.recv(1024 * 1024) # 1MB chunks
                if not data:
                    break
                for char in data:
                    d.append(char)
                    try:
                        if str(self.EOD, 'utf-8') == str(d[-len(str(self.EOD, 'utf-8')):], 'utf-8'): # Check for end of data
                            def respond(data):
                                self.conn.send(self.cypto.encrypt(data))
                                self.conn.send(self.EOD)
                            self.commandHandler(self.cypto.decrypt(bytes(d[:-3])), respond)
                            d = bytearray()
                    except IndexError:
                        pass
    def commandHandler(self, data, respond):
        string = str(data, 'utf-8')
        if string == 'NEWKEY':
            newkey = self.cypto.genKey()
            respond(newkey)
            self.cypto.setKey(newkey)
        elif string[:8] == 'FILEINFO':
            pass
        elif string[:8] == 'FILEPART':
            pass
        else:
            respond(b'ERROR 1 Invalid command!')

class STSocketServer(threading.Thread): # todo add a way to stop the server
    def __init__(self, host, port, INIT_KEY):
        super().__init__()
        self.INIT_KEY = INIT_KEY
        self.host = host
        self.port = port
        self.start()
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.host, self.port))
            server.listen()
            print('Listening on', (self.host, self.port))
            while True:
                conn, addr = server.accept()
                STSocketServerConnectionHandler(conn, addr, self.INIT_KEY).start()

class STSocketClient():
    def __init__(self, host, port, INIT_KEY):
        self.cypto = cypto.cypto()
        self.cypto.setKey(INIT_KEY)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.EOD = b'!!!'
    def send(self, data):
        self.socket.send(self.cypto.encrypt(data))
        self.socket.send(self.EOD)
        d = bytearray()
        while True:
            data = self.socket.recv(1024 * 1024) # 1MB chunks
            if not data:
                break
            for char in data:
                d.append(char)
                try:
                    if str(self.EOD, 'utf-8') == str(d[-len(str(self.EOD, 'utf-8')):], 'utf-8'): # Check for end of data
                        data = self.cypto.decrypt(bytes(d[:-3]))
                        string = str(data, 'utf-8')
                        if string[:5] == 'ERROR':
                            raise Exception('Error from server: code: ' + string.split(' ')[1] + ', message: ' + ' '.join(string.split(' ')[2:]))
                        return data
                except IndexError:
                    pass
    def newKey(self):
        r = self.send(b'NEWKEY')
        self.cypto.setKey(r)
    def close(self):
        self.socket.close()

# binary file test
srv = STSocketServer('127.0.0.1', 5000, config.GLOBAL_KEY)
time.sleep(1)
s = STSocketClient('127.0.0.1', 5000, config.GLOBAL_KEY)
s.send(b'test')
print('done')