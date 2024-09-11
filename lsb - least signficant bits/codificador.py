#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criado em Qua Jul 12 15:17:37 XXXX

@author: eduardo
"""
# Codificador para imagens BMP

# Importando bibliotecas
from PIL import Image

# Converte uma string para binário usando codificação ASCII
def texto_para_binario(texto):
    return ''.join((format(ord(caractere), 'b')).zfill(8) for caractere in texto)

# Solicitando ao usuário o nome do arquivo de imagem para abrir
print('Digite o nome do arquivo de imagem para abrir:')
imagem_entrada = input()
print('Digite o texto a ser codificado:')
texto_entrada = input()
print('Digite o nome do arquivo de imagem para salvar:')
imagem_saida = input()

# Convertendo a mensagem para binário
mensagem_binaria = texto_para_binario(texto_entrada)

# Carregando os dados de pixel da imagem
imagem_pre = Image.open(imagem_entrada)
largura, altura = imagem_pre.size
pixels = imagem_pre.load()

# Alterando o bit menos significativo de cada pixel para corresponder a cada bit da mensagem codificada
bit_atual = 0
for x in range(0, largura):
    if (bit_atual >= len(mensagem_binaria)):
        break

    # Obtendo o pixel atual
    pixel_atual = pixels[x, 0]
    #print('[%d, %d]: [%d, %d, %d]'%(x, 0, pixel_atual[0], pixel_atual[1], pixel_atual[2]))

    # Alterando os valores de r, g e b do pixel
    novo_pixel = list(pixel_atual)
    for cor in range(0, 3):
        if (bit_atual >= len(mensagem_binaria)):
            break
        cor_binaria = list(format(pixel_atual[cor], 'b').zfill(8))
        cor_binaria[7] = mensagem_binaria[bit_atual]
        cor_binaria = ''.join(cor_binaria)
        novo_pixel[cor] = int(cor_binaria, 2)

        bit_atual += 1

    # Sobrescrevendo o pixel antigo
    pixel_atual = tuple(novo_pixel)
    pixels[x, 0] = pixel_atual

    # Exibindo o pixel modificado
    #print('  -> [%d, %d, %d]'%(pixel_atual[0], pixel_atual[1], pixel_atual[2]))
    #print('  (%c, %c, %c)'%(mensagem_binaria[bit_atual-3], mensagem_binaria[bit_atual-2], mensagem_binaria[bit_atual-1]))

# Reescrevendo os dados de pixel da imagem em uma nova imagem
imagem_pre.save(imagem_saida)
