from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import utils
import os

# Função para gerar as chaves pública e privada
def gerar_chaves():
    chave_privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    chave_publica = chave_privada.public_key()
    return chave_publica, chave_privada

# Função para cifrar a chave simétrica (usando RSA)
def cifra_chave_simetrica(chave_simetrica, chave_publica_destinatario):
    chave_simetrica_cifrada = chave_publica_destinatario.encrypt(
        chave_simetrica,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return chave_simetrica_cifrada

# Função para decifrar a chave simétrica (usando RSA)
def decifrar_chave_simetrica(chave_simetrica_cifrada, chave_privada_destinatario):
    chave_simetrica = chave_privada_destinatario.decrypt(
        chave_simetrica_cifrada,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return chave_simetrica

# Função para cifrar a mensagem com AES (usando a chave simétrica)
def cifra_mensagem_simetrica(mensagem, chave_simetrica):
    iv = os.urandom(16)  # Gera um vetor de inicialização aleatório
    cifra = Cipher(algorithms.AES(chave_simetrica), modes.CFB(iv), backend=default_backend())
    encryptor = cifra.encryptor()
    mensagem_cifrada = encryptor.update(mensagem.encode('utf-8')) + encryptor.finalize()
    return iv, mensagem_cifrada

# Função para decifrar a mensagem com AES (usando a chave simétrica)
def decifrar_mensagem_simetrica(mensagem_cifrada, chave_simetrica, iv):
    cifra = Cipher(algorithms.AES(chave_simetrica), modes.CFB(iv), backend=default_backend())
    decryptor = cifra.decryptor()
    mensagem_decifrada = decryptor.update(mensagem_cifrada) + decryptor.finalize()
    return mensagem_decifrada.decode('utf-8')

# Função para assinar a mensagem (usando RSA)
def assinar_mensagem(private_key, mensagem):
    assinatura = private_key.sign(
        mensagem,
        padding.PSS(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return assinatura

# Função para verificar a assinatura (usando RSA)
def verificar_assinatura(public_key, mensagem, assinatura):
    try:
        public_key.verify(
            assinatura,
            mensagem,
            padding.PSS(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False

# Exemplo de uso

# Gerar as chaves pública e privada do remetente (para assinatura) e destinatário (para criptografia)
chave_publica_remetente, chave_privada_remetente = gerar_chaves()
chave_publica_destinatario, chave_privada_destinatario = gerar_chaves()

# Mensagem original
mensagem_original = "Esta é uma mensagem confidencial com assinatura"
mensagem_bytes = mensagem_original.encode('utf-8')

# Gera uma chave simétrica aleatória para AES
chave_simetrica = os.urandom(32)  # Chave de 256 bits para AES

# Cifra a mensagem com a chave simétrica (AES)
iv, mensagem_cifrada = cifra_mensagem_simetrica(mensagem_original, chave_simetrica)

# Cifra a chave simétrica com a chave pública do destinatário (RSA)
chave_simetrica_cifrada = cifra_chave_simetrica(chave_simetrica, chave_publica_destinatario)

# Assina a mensagem com a chave privada do remetente (RSA)
assinatura = assinar_mensagem(chave_privada_remetente, mensagem_bytes)

# --- No lado do destinatário ---

# Decifra a chave simétrica com a chave privada do destinatário (RSA)
chave_simetrica_decifrada = decifrar_chave_simetrica(chave_simetrica_cifrada, chave_privada_destinatario)

# Decifra a mensagem com a chave simétrica decifrada (AES)
mensagem_decifrada = decifrar_mensagem_simetrica(mensagem_cifrada, chave_simetrica_decifrada, iv)
print("Mensagem decifrada: ", mensagem_decifrada)

# Verifica a assinatura com a chave pública do remetente (RSA)
assinatura_valida = verificar_assinatura(chave_publica_remetente, mensagem_bytes, assinatura)

if assinatura_valida:
    print("Assinatura válida: A mensagem é autêntica e não foi alterada.")
else:
    print("Assinatura inválida: A mensagem foi alterada ou não é do remetente.")
