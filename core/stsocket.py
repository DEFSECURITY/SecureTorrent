"""
A small breakdown of the protocol:
Data is encrypted using Fernet which is base64 encoded all data ends with '!!!'.
The data is encrypted using INIT_KEY but can be changed at any time with a call form the client to change the key to a new random key, the server then sends the new key to the client.

Commands that the server accepts:
NEWKEY -> send a new random key to the client and set that as the key.
FILEINFO [file hash] -> send the file "[file hash]"'s information to the client. (a JSON string with the following fields: name, size, chunkcount).
FILEPART [file hash] [chunk number] -> send the chunk "[chunk number]" of the file "[file hash]" to the client.

Errors format is as follows:
ERROR [code] [message]
The code consists of two digits.
Digit one is the type of error, digit two is the error code.
The following error types are:
0: Server error - ie, the server is full. (not yet implemented)
1: Request error - the server does not recognize the command or it's parameters.
2: File error - error with the requested file.

Errors that the server will send to the client:
ERROR 00 -> the server is full. (not yet implemented)
ERROR 10 -> the command is not recognized.
ERROR 11 -> bad request. ie, the parameters are incorrect.
ERROR 20 -> the file does not exist.
ERROR 21 -> invalid chunk index.
"""

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
        self.daemon = True # try to kill the connection when the server is killed
        self.start()
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
                            self.commandHandler(self.cypto.decrypt(bytes(d[:-len(self.EOD)])), respond)
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
                respond(b'ERROR 11 Bad request!')
        elif string[:8] == 'FILEPART':
            if len(string.split(' ')) > 2 and string.split(' ')[1] and string.split(' ')[2]:
                fileid = string.split(' ')[1]
                if fileid not in openfiles:
                    respond(b'ERROR 20 File not found!')
                    return
                try:
                    respond(openfiles[fileid].readChunk(int(string.split(' ')[2])))
                except filechunkreader.FileChunkReaderChunkIndexError:
                    respond(b'ERROR 21 Invalid chunk index!')
            else:
                respond(b'ERROR 11 Bad request!')
        else:
            respond(b'ERROR 10 Invalid command!')

class STSocketServer(threading.Thread): # todo add a way to stop the server
    def __init__(self, host, port, INIT_KEY):
        super().__init__()
        self.INIT_KEY = INIT_KEY
        self.host = host
        self.port = port
        self.updatefiles()
        self.daemon = True # try to kill the server when the program is closed
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
                STSocketServerConnectionHandler(conn, addr, self.INIT_KEY)

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
                        data = self.cypto.decrypt(bytes(d[:-len(self.EOD)]))
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