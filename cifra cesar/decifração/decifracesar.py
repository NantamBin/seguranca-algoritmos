def decifracesar(texto, chave):
    resultado = ""

    # iterando o texto
    for i in range(len(texto)):
        char = texto[i]

        # letras maiusculas
        if char.isupper():
            resultado += chr((ord(char) - 65 - chave) % 26 + 65)
        
        # letras minusculas
        elif char.islower():
            resultado += chr((ord(char) - 97 - chave) % 26 + 97)

        # outros caracteres
        else:
            resultado += char

    return resultado

#exemplo
meuTexto = "NBBN ENAVNUQX MN VNDB XUQXB ENV MX ENAMN MJ WJCDANIJ"
chave = 9

print("Texto original: ", meuTexto)
print("Texto decifrado: ", decifracesar(meuTexto, chave))