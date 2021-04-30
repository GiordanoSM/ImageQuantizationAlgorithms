import helper as hp
import bitstring as bs
import sys
from PIL import Image, UnidentifiedImageError
import numpy as np
import time
from sklearn.cluster import KMeans

def encoder(filename, M, directory=''):

  header = bs.Bits(hex='0xF0') #Header sendo F + numero de bits de padding no final do arquivo

  no_path_name = hp.remove_path(filename) #Adquire somente o nome do arquivo em a ser lido
  filename_result = hp.add_path_cmp(directory, no_path_name) #Cria o nome do codebook junto com o diretório alvo

  try:
    with Image.open(filename) as im:

      if im.mode not in ['RGB', 'YCbCr', 'LAB', 'HSV']: #Verifica se a imagem é colorida
            raise WrongFormat()

      data = np.asarray(im)

      num_col = np.uint16(data.shape[1]) #Passar como informação lateral

      elements = getElements(data) #Retorna lista com todos os elementos (pixels)

      print("Começando a codificação... (Pode demorar um pouco)")
      start = time.time()

      codebook, idxs = makeCodebook(M, elements) #Retorna uint8 codebook e índices

      print(idxs.size)

      #M: codificar -1

      #padding = (8 - (data_out.len % 8)) % 8

      end = time.time()
      print('Demorou: {} segundos'.format(end - start))

  except IOError as ioe:
    sys.exit('ERRO: Arquivo ou diretório "{}" não existente.'.format(ioe.filename))

  except hp.WrongFormat:
    sys.exit('ERRO: O programa aceita somente imagens coloridas.')

  print("Terminado! Criado arquivo '{}'.\n".format(filename_result))

#------------------------------
def getElements(data):
  return np.reshape(data, (1,-1,3))[0]

#------------------------------
def makeCodebook(M, elements):

  kmeans = KMeans(n_clusters= M).fit(elements)
  return kmeans.cluster_centers_.astype(np.uint8), kmeans.labels_.astype(np.uint8)

"""#------------------------------
def pad (L, data):
  missing = lambda x: (L - (x % L)) % L
  padding_col = np.uint8(missing(data.shape[1]%L))
  return np.pad(data, ((0,0), (0,missing(data.shape[1])), (0,0))), padding_col
"""
#------------------------------
if __name__ == "__main__":
  if len(sys.argv) > 1:
    M = int(sys.argv[1])
    if len(sys.argv) > 2:
      filename = sys.argv[2]
    else:
      filename = input("Informe o nome (caminho) da imagem a ser codificada: ")

  else:
    M = int(input("Informe o tamanho (M) do codebook (número de cores) a ser gerado: "))
    filename = input("Informe o nome (caminho) da imagem a ser codificada: ")

  directory = input("Informe o nome do diretório do resultado (será o atual caso não informado): ")
    
  encoder(filename, M, directory)