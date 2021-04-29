import filename_handler as fh
import bitstring as bs
import sys
from PIL import Image, UnidentifiedImageError
import numpy as np
import time
from scipy.spatial.distance import cdist
#from scipy.cluster.vq import vq, kmeans, whiten

def codebookGen(filename, M, L, directory=""):
  no_path_name = fh.remove_path(filename) #Adquire somente o nome do arquivo em a ser lido
  filename_result = fh.add_path_cdb(directory, no_path_name) #Cria o nome do codebook junto com o diretório alvo

  try:
    with Image.open(filename) as im:
      with open(filename_result, 'wb') as f_write:
        
        if im.mode != 'L': #Verifica se a imagem está em escala de cinza
          raise WrongFormat()

        data = np.asarray(im)

        elements = getElements(M, L, data)

        code_vectors = LBG(elements, M)


  except IOError as ioe:
    sys.exit('ERRO: Arquivo ou diretório "{}" não existente.'.format(ioe.filename))

  except WrongFormat:
    sys.exit('ERRO: O programa aceita somente imagem em escala de cinza.')

  print("Terminado! Criado arquivo '{}'.\n".format(filename_result))

#----------------------------------

def LBG (elements, M, D=[]):
  #np.random.seed(time.time())
  np.random.seed((1000,2000))

  n_dimensions = elements[0].size

  epsilon = 0.025

  y = []

  idxs = []

  for i in range(M):
    y.append(np.random.rand(n_dimensions)*255)

  distances = cdist(np.array(elements), np.array(y))

  for e in distances:
    idxs.append(e.argmin())

  D1 = np.sum([cdist([elements[i]], [y[idxs[i]]]) for i in range(len(elements))])/len(elements)

  #print(idxs)
  #print(D1)

#-----------------------------------

def getElements(M, L, data):
  N = int(np.sqrt(L))
  padded_data = pad(N, data)
  return getBlocks(N, padded_data)
  

#-------------------------------------
#Bem comportado até 255 blocos na horizontal
def getBlocks(N, data):
  n_blocks_h = data.shape[0]/N
  n_blocks_v = data.shape[1]/N

  blocks = []

  for l in range(0, data.shape[0], N):
    for c in range(0, data.shape[1], N):
      blocks.append(data[l:l+N,range(c, c+N)].reshape(1,-1)[0])

  return blocks

#-----------------------------------

def pad (N, data):
  missing = lambda x: (N - (x % N)) % N
  return np.pad(data, ((0,missing(data.shape[0])), (0,missing(data.shape[1]))))

#-----------------------------------

class WrongFormat(Exception):
  pass

#-----------------------------------

if __name__ == "__main__":
  if len(sys.argv) > 1:
    M = int(sys.argv[1])
    if len(sys.argv) > 2:
      L = int(sys.argv[2])
    else:
      filename = int(input("Informe o tamanho (M) do codebook a ser gerado: "))

  else:
    M = int(input("Informe o tamanho (M) do codebook a ser gerado: "))
    L = int(input("Informe o tamanho (L) de cada bloco (considera-se um bloco quadrado): "))

  filename = input("Informe o nome (caminho) da imagem a ser utilizada: ")
  directory = input("Informe o nome do diretório do resultado (será o atual caso não informado): ")
    
  codebookGen(filename, M, L, directory)