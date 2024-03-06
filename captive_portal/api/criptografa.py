import rsa
import os
import base64
from configs import configs as confs


class Criptografa:

    def __init__(self):
        script_dir = os.path.dirname(__file__)
        self.public = os.path.join(script_dir, confs.private_key)
        self.private = os.path.join(script_dir, confs.public_key)

    def gera_chaves(self):
        publicKey, privateKey = rsa.newkeys(512)
        # salva chaves em arquivos
        with open(self.public, 'w+') as f:
            f.write(publicKey.save_pkcs1().decode('utf-8'))
        with open(self.private, 'w+') as f:
            f.write(privateKey.save_pkcs1().decode('utf-8'))

    def criptografa(self, mensagem):
        with open(self.public, 'r') as f:
            key = f.read()
        publicKey = rsa.PublicKey.load_pkcs1(key.encode('utf-8'))
        crypto = rsa.encrypt(mensagem.encode('utf-8'), publicKey)
        # converte crypto para base64 e texto
        return base64.b64encode(crypto).decode('utf-8')

    def descriptografa(self, mensagem):
        # decodifica base64 e converte para bytes
        mensagem = base64.b64decode(mensagem)
        with open(self.private, 'r') as f:
            key = f.read()
        privateKey = rsa.PrivateKey.load_pkcs1(key.encode('utf-8'))
        message = rsa.decrypt(mensagem, privateKey)
        return message.decode('utf-8')


if __name__ == "__main__":
    gn = Criptografa()
    # gn.gera_chaves()
    mensagem = "teste"
    crypto = gn.criptografa(mensagem)
    print(crypto)
    message = gn.descriptografa(crypto)
    print(message)
