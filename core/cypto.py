from cryptography.fernet import Fernet
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