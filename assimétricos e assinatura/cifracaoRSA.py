from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def gerar_chaves():
    chave_privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    chave_publica = chave_privada.public_key()

    return chave_publica, chave_privada

def cifra_mensagem(mensagem, chave_publica):
    mensagem_bytes = mensagem.encode('utf-8')
    mensagem_cifrada = chave_publica.encrypt(mensagem_bytes, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(), label=None))

    return mensagem_cifrada

def decifrar_mensagem(mensagem_cifrada, chave_privada):
    mensagem_decifrada = chave_privada.decrypt(mensagem_cifrada, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(), label=None))

    return mensagem_decifrada.decode('utf-8')

chave_publica, chave_privada = gerar_chaves()
mensagem_original = "Minha primeira cifracao"
print("Mensagem original: ", mensagem_original)

mensagem_cifrada = cifra_mensagem(mensagem_original, chave_publica)

print("Mensagem Cifrada: ", mensagem_cifrada)
print("Mensagem Decifrada: ", decifrar_mensagem(mensagem_cifrada, chave_privada))