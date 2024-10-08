from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def generate_key():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    public_key = private_key.public_key()

    return public_key, private_key

def sign_message(private_key, message):
    signature = private_key.sign(message, padding.PSS(mgf=padding.MGF1(algorithm=hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())

    return signature

def verify_signature(public_key, message, signature):
    try:
        public_key.verify(signature, message, padding.PSS(mgf=padding.MGF1(algorithm=hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    
    except Exception as error:
        print("Verificação Falhou! {error}")
        return False
    
# Exemplo
public_key, private_key = generate_key()

message = "Esta é a minha segunda mensagem"
message_bytes = message.encode('utf-8')

signature = sign_message(private_key, message_bytes)

valid = verify_signature(public_key, message_bytes, signature)

if valid:
    print("Assinatura verificada com sucesso")
else:
    print("Assinatura inválida!")