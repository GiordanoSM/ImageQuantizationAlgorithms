import helper as hp
import bitstring as bs
import sys
from PIL import Image, ImageShow
import numpy as np
import time

def openner (filename, show_image=True):
  if filename[-4:] != '.dit': #Verifica se a extensão do arquivo a ser lido é a esperada
    sys.exit('Erro: Esperado arquivo de extensão: ".dit".')

  try:
    print("Começando a decodificação... (Pode demorar um pouco)")
    start = time.time()

    header = bs.Bits(filename= filename, length=8)#Header sendo F + numero de bits de padding no final do arquivo

    padding_end, mode = checkHeader(header)#Extrai o tamanho do padding do final do arquivo do header e verifica-o

    M = bs.Bits(filename= filename, length=8, offset=8).uint + 1#Numero de elementos/cores no codebook

    num_col = bs.Bits(filename= filename, length=16, offset=16).uint#Número de colunas na imagem original

    pixels = decoder(filename, M, padding_end, 32)#Extrai os pixels codificados

    image_array = reconstructImageArray(pixels, num_col, mode)#Retornar o array com a imagem decodificada

    end = time.time()
    print('Demorou: {} segundos'.format(end - start))

    im = Image.fromarray(image_array)

    if show_image:
      ImageShow.show(im)

  except IOError as ioe:
    sys.exit('ERRO: Arquivo ou diretório "{}" não existente.'.format(ioe.filename))

  except WrongHeader:
    sys.exit('Erro: Header do arquivo não condiz com o esperado.')

  return image_array
#------------------------------
#Tem a função de extrair todos os pixels codificados
def decoder (filename, M, padding_end, offset):
  bpp = int(np.ceil(np.log2(M)))

  data = bs.Bits(filename=filename, offset= offset)

  if padding_end != 0:
    data = data[:-padding_end]

  pixels = []

  delta = 255/M
  y = np.array([delta*(2*i - 1)/2 for i in range(1, M+1)])

  while data != bs.Bits(bin= "0b"):
    idx = data[:bpp].uint
    pixels.append(y[idx])
    data = data[bpp:]

  return np.array(pixels).astype(np.uint8)

#------------------------------
#Tem a função de reorganizar os pixels no formato da imagem original
def reconstructImageArray(pixels, num_col, mode):
  image_array = []

  if not mode: #Se for colorida, reune 3 elementos em um pixel
    pixels = pixels.reshape(-1,3)

  for i in range(0, len(pixels), num_col):
    image_array.append(pixels[i:i+num_col])
  
  return np.array(image_array)

#-------------------------------------------
#Checa se o header corresponde com o esperado e retorna o padding informado por ele
def checkHeader(header):

  if header[:-5] == bs.Bits(bin= '0b111'):
    return header[4:].uint, header[3]

  else: raise WrongHeader

#-------------------------------------------
class WrongHeader(Exception):
  pass

#------------------------------
if __name__ == "__main__":
  if len(sys.argv) > 1:
    filename = sys.argv[1]
  else: filename = input("Informe o nome (caminho) da imagem (.cvq) a ser aberta: ")
  
  openner(filename, use_dit)