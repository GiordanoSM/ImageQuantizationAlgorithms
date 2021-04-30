import helper as hp
import bitstring as bs
import sys
from PIL import Image, UnidentifiedImageError
import numpy as np
import time
from sklearn.cluster import KMeans

def encoder(filename, M, directory=''):

  L = 3 #Número de pixel em um elemento/bloco, faz um elemento como L pixels na horizontal

  header = bs.Bits(hex='0xF0') #Header sendo F + numero de bits de padding no final do arquivo

  no_path_name = hp.remove_path(filename) #Adquire somente o nome do arquivo em a ser lido
  filename_result = hp.add_path_cmp(directory, no_path_name) #Cria o nome do codebook junto com o diretório alvo

  try:
    with Image.open(filename) as im:

      if im.mode not in ['RGB', 'YCbCr', 'LAB', 'HSV']: #Verifica se a imagem é colorida
            raise WrongFormat()

      data = np.asarray(im)

      padded_data, padding_col = pad(L, data)
  
      #print(padded_data)

      blocks, n_blocks_h = getBlocks(padded_data, L)

      #codebook, idxs = makeCodebook(M, blocks)

      #n_blocks_h e M: codificar -1

      #padding = (8 - (data_out.len % 8)) % 8

  except IOError as ioe:
    sys.exit('ERRO: Arquivo ou diretório "{}" não existente.'.format(ioe.filename))

  except hp.WrongFormat:
    sys.exit('ERRO: O programa aceita somente imagens coloridas.')

  print("Terminado! Criado arquivo '{}'.\n".format(filename_result))

#------------------------------
def getBlocks(data, L):
  n_blocks_h = data.shape[1]/L

  blocks = []

  for l in range(data.shape[0]):
    for c in range(0, data.shape[1], L):
      blocks.append(data[l:l+1,range(c, c+L)][0])#Pega cada bloco como um array de pixels

  return np.array(blocks), int(n_blocks_h)

#------------------------------
def makeCodebook(m, blocks):
  pass
  #return codebook, idxs

#------------------------------
def pad (L, data):
  missing = lambda x: (L - (x % L)) % L
  padding_col = np.uint8(missing(data.shape[1]%L))
  return np.pad(data, ((0,0), (0,missing(data.shape[1])), (0,0))), padding_col

#------------------------------
if __name__ == "__main__":
  if len(sys.argv) > 1:
    M = int(sys.argv[1])
    if len(sys.argv) > 2:
      filename = sys.argv[2]
    else:
      filename = input("Informe o nome (caminho) da imagem a ser codificada: ")

  else:
    M = int(input("Informe o tamanho (M) do codebook a ser gerado: "))
    filename = input("Informe o nome (caminho) da imagem a ser codificada: ")

  directory = input("Informe o nome do diretório do resultado (será o atual caso não informado): ")
    
  encoder(filename, M, directory)