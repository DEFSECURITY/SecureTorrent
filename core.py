import hashlib
import os
import math
from cryptography.fernet import Fernet

def hashFile(file, BUF_SIZE = 1024 * 1024): # 1MB chunks
    hash = hashlib.sha256()
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            hash.update(data)
    return hash.hexdigest()

class FileChunkReader:
    def __init__(self, file, CHUNK_SIZE = 1024 * 1024): # 1MB
        self._chunksize = CHUNK_SIZE
        self._file = open(file, 'rb')
        self.basename = os.path.basename(file)
        self.filesize = os.path.getsize(file)
        self.chunkcount = math.ceil(self.filesize / self._chunksize)
    def readChunk(self, chunk):
        if chunk > self.chunkcount or chunk < 1:
            raise Exception('chunk index out of range!')
        start = self._chunksize * (chunk - 1)
        self._file.seek(start)
        return self._file.read(self._chunksize)

class cypto:
    def __init__(self):
        self._key = False
    def genKey(self):
        return Fernet.generate_key()
    def setKey(self, key):
        self._key = key
        self._fernet = Fernet(key)
    def encrypt(self, data):
        if not self._key:
            raise Exception('no key has been set!')
        return self._fernet.encrypt(data)
    def decrypt(self, data):
        if not self._key:
            raise Exception('no key has been set!')
        return self._fernet.decrypt(data)