import hashlib
def hashFile(file, BUF_SIZE = 1024 * 1024): # 1MB chunks
    hash = hashlib.sha256()
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            hash.update(data)
    return hash.hexdigest()