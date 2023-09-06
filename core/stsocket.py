import sys
sys.path.append('..')
import filechunkreader
import socket
import threading
import cypto
import config
import time
import json
import os
openfiles = {}
class STSocketServerConnectionHandler(threading.Thread):
    def __init__(self, conn, addr, INIT_KEY):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.cypto = cypto.cypto()
        self.cypto.setKey(INIT_KEY)
        self.EOD = '!!!'
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
                        if self.EOD == str(d[-len(self.EOD):], 'utf-8'): # Check for end of data
                            def respond(data):
                                self.conn.send(self.cypto.encrypt(data))
                                self.conn.send(bytes(self.EOD, 'utf-8'))
                            self.commandHandler(self.cypto.decrypt(bytes(d[:-3])), respond)
                            d = bytearray()
                    except IndexError:
                        pass
    def commandHandler(self, data, respond):
        global openfiles
        string = ''
        try:
            string = str(data, 'utf-8')
        except:
            pass
        if string == 'NEWKEY':
            newkey = self.cypto.genKey()
            respond(newkey)
            self.cypto.setKey(newkey)
        elif string[:8] == 'FILEINFO':
            if len(string.split(' ')) > 1 and string.split(' ')[1]:
                fileid = string.split(' ')[1]
                if fileid not in openfiles:
                    respond(b'ERROR 20 File not found!')
                    return
                data = {'name': openfiles[fileid].basename, 'size': openfiles[fileid].filesize, 'chunkcount': openfiles[fileid].chunkcount}
                respond(bytes(json.dumps(data), 'utf-8'))
            else:
                respond(b'ERROR 12 Bad request!')
        elif string[:8] == 'FILEPART':
            if len(string.split(' ')) > 2 and string.split(' ')[1] and string.split(' ')[2]:
                fileid = string.split(' ')[1]
                if fileid not in openfiles:
                    respond(b'ERROR 20 File not found!')
                    return
                respond(openfiles[fileid].readChunk(int(string.split(' ')[2])))
            else:
                respond(b'ERROR 12 Bad request!')
        else:
            respond(b'ERROR 11 Invalid command!')

class STSocketServer(threading.Thread): # todo add a way to stop the server
    def __init__(self, host, port, INIT_KEY):
        super().__init__()
        self.INIT_KEY = INIT_KEY
        self.host = host
        self.port = port
        self.updatefiles()
        self.start()
    def updatefiles(self):
        global openfiles
        f = open(config.APP_DATA + '/files.json')
        filelist = json.load(f)
        f.close()
        for file in filelist:
            openfiles[file] = filechunkreader.FileChunkReader(filelist[file])
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
        self.EOD = '!!!'
    def send(self, data): # returns an array [0: binary data, 1: string (if valid utf-8)]
        self.socket.send(self.cypto.encrypt(data))
        self.socket.send(bytes(self.EOD, 'utf-8'))
        d = bytearray()
        while True:
            data = self.socket.recv(1024 * 1024) # 1MB chunks
            if not data:
                break
            for char in data:
                d.append(char)
                try:
                    if self.EOD == str(d[-len(self.EOD):], 'utf-8'): # Check for end of data
                        data = self.cypto.decrypt(bytes(d[:-3]))
                        string = ''
                        try:
                            string = str(data, 'utf-8')
                        except:
                            pass
                        if string[:5] == 'ERROR':
                            raise Exception('Error from server: code: ' + string.split(' ')[1] + ', message: ' + ' '.join(string.split(' ')[2:]))
                        return data, string
                except IndexError:
                    pass
    def newKey(self):
        r = self.send(b'NEWKEY')[0]
        self.cypto.setKey(r)
    def close(self):
        self.socket.close()

# binary file test
srv = STSocketServer('127.0.0.1', 5000, config.GLOBAL_KEY)
time.sleep(1)
s = STSocketClient('127.0.0.1', 5000, config.GLOBAL_KEY)
fileid = '500afe4eeb535c5ecd1c205e18be8c3db97dce216088e57fdad8e08a3a4028c3'
file = json.loads(s.send(bytes('FILEINFO ' + fileid, 'utf-8'))[1])
print(file)
f = open(file['name'], 'wb')
for i in range(file['chunkcount']):
    f.write(s.send(bytes('FILEPART ' + fileid + ' ' + str(i + 1), 'utf-8'))[0])
print('Done')