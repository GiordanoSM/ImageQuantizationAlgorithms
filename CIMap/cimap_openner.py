import helper as hp
import bitstring as bs
import sys
from PIL import Image, UnidentifiedImageError, ImageShow
import numpy as np
import time

def openner (filename, show_image=True):
  
  if filename[-4:] != '.cmp': #Verifica se a extensão do arquivo a ser lido é a esperada
    sys.exit('Erro: Esperado arquivo de extensão: ".cmp".')

  try:
    print("Começando a decodificação... (Pode demorar um pouco)")
    start = time.time()

    header = bs.Bits(filename= filename, length=8)#Header sendo F + numero de bits de padding no final do arquivo
  
    padding_end = checkHeader(header)#Extrai o tamanho do padding do final do arquivo do header e verifica-o

    M = bs.Bits(filename= filename, length=8, offset=8).uint + 1#Numero de elementos/cores no codebook

    num_col = bs.Bits(filename= filename, length=16, offset=16).uint#Número de colunas na imagem original

    codebook, offset = codebookParser(filename, M, 32)

    pixels = decoder(codebook, filename, M, padding_end, offset)#Extrai os pixels codificados

    image_array = reconstructImageArray(pixels, num_col)#Retornar o array com a imagem decodificada

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

#------------------------------------------
def codebookParser (filename, M, offset):
  codebook = []

  for i in range(M):
    buffer = bs.Bits(filename= filename, length=24, offset=offset+i*24).tobytes()
    codebook.append(np.frombuffer(buffer, dtype= np.uint8))

  return np.array(codebook), offset+M*24

#-------------------------------------------
#Tem a função de reorganizar os pixels no formato da imagem original
def reconstructImageArray(pixels, num_col):
  image_array = []

  for i in range(0, len(pixels), num_col):
    image_array.append(pixels[i:i+num_col])

  #image_array = np.concatenate(lines, axis=0)
  
  return np.array(image_array)

#-------------------------------------------
#Tem a função de extrair todos os pixels codificados
def decoder(codebook, filename, M, padding_end, offset):
  bpp = int(np.ceil(np.log2(M)))

  data = bs.Bits(filename=filename, offset= offset)

  if padding_end != 0:
    data = data[:-padding_end]

  blocks = []

  while data != bs.Bits(bin= "0b"):
    idx = data[:bpp].uint
    blocks.append(codebook[idx])
    data = data[bpp:]

  return np.array(blocks)

#-------------------------------------------
#Checa se o header corresponde com o esperado e retorna o padding informado por ele
def checkHeader(header):

  if header[:-4] == bs.Bits(hex= '0xf'):
    return header[4:].uint

  else: raise WrongHeader

#-------------------------------------------
class WrongHeader(Exception):
  pass
#-------------------------------------------

if __name__ == '__main__':
  if len(sys.argv) > 1:
    filename = sys.argv[1]
  else: filename = input("Informe o nome (caminho) da imagem (.cvq) a ser aberta: ")

  openner(filename)