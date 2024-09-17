# Instala o pacote necessário para criptografia com AES
# pip install pycryptodome

# Importa as funções necessárias para criptografia AES
from Crypto.Cipher import AES  # Para criar o cifrador AES
from Crypto.Util.Padding import pad, unpad  # Para adicionar e remover padding à mensagem
from Crypto.Random import get_random_bytes  # Para gerar bytes aleatórios (usado na chave e no IV)

# Função para encriptar uma mensagem usando AES
def aes_encriptar(mensagem, chave):
    # Gera um IV (vetor de inicialização) aleatório do tamanho do bloco do AES (16 bytes)
    iv = get_random_bytes(AES.block_size)
    
    # Cria um objeto de cifragem AES no modo CBC (Cipher Block Chaining) usando a chave e o IV
    cipher = AES.new(chave, AES.MODE_CBC, iv)
    
    # Aplica padding na mensagem para garantir que seu tamanho seja múltiplo do tamanho do bloco AES
    mensagem_padded = pad(mensagem.encode('utf-8'), AES.block_size)
    
    # Encripta a mensagem com padding usando o cifrador AES
    mensagem_encriptada = cipher.encrypt(mensagem_padded)
    
    # Retorna o IV concatenado com a mensagem encriptada (o IV é necessário para a decriptação)
    return iv + mensagem_encriptada

# Função para decriptar uma mensagem encriptada usando AES
def aes_decriptar(mensagem_encriptada, chave):
    # Extrai o IV da mensagem encriptada (os primeiros 16 bytes)
    iv = mensagem_encriptada[:AES.block_size]
    
    # Cria um novo objeto de cifragem AES no modo CBC, usando a chave e o IV extraído
    cipher = AES.new(chave, AES.MODE_CBC, iv)
    
    # Decripta a mensagem (ignora o IV e decripta o restante)
    mensagem_padded = cipher.decrypt(mensagem_encriptada[AES.block_size:])
    
    # Remove o padding da mensagem decriptada
    mensagem = unpad(mensagem_padded, AES.block_size)
    
    # Retorna a mensagem original, convertendo de bytes para string
    return mensagem.decode('utf-8')

# Define a mensagem a ser encriptada
mensagem = "Olá mundo seguro"

# Gera uma chave aleatória de 16 bytes (128 bits)
chave = get_random_bytes(16)

# Encripta a mensagem usando a função aes_encriptar
mensagem_encriptada = aes_encriptar(mensagem, chave)

# Exibe a mensagem original e a mensagem encriptada
print("Texto Original:", mensagem)
print(f"Texto Encriptado: {mensagem_encriptada}")

print()

# Decripta a mensagem encriptada usando a função aes_decriptar
mensagem_decifrada = aes_decriptar(mensagem_encriptada, chave)

# Exibe a mensagem encriptada e a mensagem decriptada (original)
print("Texto Encriptado:", mensagem_encriptada)
print(f"Texto Decriptado: {mensagem_decifrada}")
