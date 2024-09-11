#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criado em Qua Jul 12 15:54:26 XXXX

@author: eduardo
"""

# Decodificador para imagens BMP

# Importando bibliotecas
from PIL import Image

# Converte uma string binária para texto usando codificação ASCII
def binario_para_texto(binario_str):
    texto_resultado = ''
    for i in range(0, len(binario_str) // 8):
        texto_resultado += chr(int(binario_str[i*8:i*8+8], 2))
    return texto_resultado

# Solicitando ao usuário o nome do arquivo de imagem para decodificar
print('Digite o nome da imagem para decodificar:')
imagem_entrada = input()
print('Digite o número de caracteres a decodificar:')
num_caracteres = int(input())
num_bits = num_caracteres * 8

# Carregando os dados de pixel da imagem
imagem_pre = Image.open(imagem_entrada)
largura, altura = imagem_pre.size
pixels = imagem_pre.load()

# Encontrando o bit menos significativo de cada pixel
string_binaria = ''
bit_atual = 0
for x in range(0, largura):
    if (bit_atual >= num_bits):
        break

    # Obtendo o pixel atual
    pixel_atual = pixels[x, 0]

    # Alterando os valores de r, g e b do pixel
    for cor in range(0, 3):
        if (bit_atual >= num_bits):
            break
        cor_binaria = list(format(pixel_atual[cor], 'b').zfill(8))
        string_binaria += cor_binaria[7]

        bit_atual += 1

# Interpretando os bits para obter ASCII
print(binario_para_texto(string_binaria))
print()
