from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Função para gerar as chaves pública e privada
def gerar_chaves():
    chave_privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    chave_publica = chave_privada.public_key()
    return chave_publica, chave_privada

# Função para cifrar a mensagem (confidencialidade)
def cifra_mensagem(mensagem, chave_publica):
    mensagem_bytes = mensagem.encode('utf-8')
    mensagem_cifrada = chave_publica.encrypt(
        mensagem_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return mensagem_cifrada

# Função para decifrar a mensagem (confidencialidade)
def decifrar_mensagem(mensagem_cifrada, chave_privada):
    mensagem_decifrada = chave_privada.decrypt(
        mensagem_cifrada,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return mensagem_decifrada.decode('utf-8')

# Função para assinar a mensagem (autenticidade e irretratabilidade)
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

# Função para verificar a assinatura (integridade e autenticidade)
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
mensagem_original = "Esta é uma mensagem segura"
mensagem_bytes = mensagem_original.encode('utf-8')

# Passo 1: O remetente assina a mensagem (autenticidade e irretratabilidade)
assinatura = assinar_mensagem(chave_privada_remetente, mensagem_bytes)

# Passo 2: O remetente cifra a mensagem com a chave pública do destinatário (confidencialidade)
mensagem_cifrada = cifra_mensagem(mensagem_original, chave_publica_destinatario)

print("Mensagem cifrada: ", mensagem_cifrada)

# Passo 3: O destinatário decifra a mensagem com sua chave privada (confidencialidade)
mensagem_decifrada = decifrar_mensagem(mensagem_cifrada, chave_privada_destinatario)
print("Mensagem decifrada: ", mensagem_decifrada)

# Passo 4: O destinatário verifica a assinatura com a chave pública do remetente (integridade e autenticidade)
assinatura_valida = verificar_assinatura(chave_publica_remetente, mensagem_bytes, assinatura)

if assinatura_valida:
    print("Assinatura válida: A mensagem é autêntica e não foi alterada.")
else:
    print("Assinatura inválida: A mensagem foi alterada ou não é do remetente.")
