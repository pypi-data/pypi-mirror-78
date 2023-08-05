import base64
from Cryptodome import Random
from Cryptodome.Cipher import AES


class AESCipher:

    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv, segment_size=128)
        encrypted = cipher.encrypt(raw.encode())
        return base64.b64encode(iv + encrypted).decode()

    def decrypt(self, enc):
        enc = base64.b64decode(enc.encode())
        iv = enc[:AES.block_size]
        body = enc[AES.block_size:]
        cipher = AES.new(self.key, AES.MODE_CFB, iv, segment_size=128)
        return cipher.decrypt(body).decode()
