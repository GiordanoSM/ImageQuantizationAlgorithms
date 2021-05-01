import helper as hp
import sys
from PIL import Image, UnidentifiedImageError
import numpy as np
import time
from sklearn.cluster import KMeans

def codebookGen(filename, M, L, directory=""):
  no_path_name = hp.remove_path(filename) #Adquire somente o nome do arquivo em a ser lido
  filename_result = hp.add_path_cdb(directory, no_path_name) #Cria o nome do codebook junto com o diretório alvo

  try:
    with Image.open(filename) as im:
      with open(filename_result, 'wb') as f_write:
        
        if im.mode != 'L': #Verifica se a imagem está em escala de cinza
          raise WrongFormat()

        data = np.asarray(im)

        print("Começando a construção do codebook... (Pode demorar um pouco)")
        start = time.time()

        elements = getElements(M, L, data)

        code_vectors = kmeans(np.array(elements), M)
        
        code_vectors_list = code_vectors.astype(np.uint8).reshape(1,-1)[0]

        f_write.write((M-1).to_bytes(1, byteorder='big'))#M-1 para aceitar M=256
        f_write.write(L.to_bytes(1, byteorder='big'))

        for b in code_vectors_list:
          f_write.write(b.tobytes())

        end = time.time()
        print('Demorou: {} segundos'.format(end - start))




  except IOError as ioe:
    sys.exit('ERRO: Arquivo ou diretório "{}" não existente.'.format(ioe.filename))

  except WrongFormat:
    sys.exit('ERRO: O programa aceita somente imagem em escala de cinza.')

  print("Terminado! Criado arquivo '{}'.\n".format(filename_result))

#----------------------------------

def kmeans (elements, M):

  kmeans = KMeans(n_clusters= M).fit(elements)

  return kmeans.cluster_centers_

#-----------------------------------

def getElements(M, L, data):
  N = int(np.sqrt(L))
  padded_data = pad(N, data)
  return getBlocks(N, padded_data)
  

#-------------------------------------
def getBlocks(N, data):

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
      L = int(input("Informe o tamanho (L) de cada bloco (considera-se um bloco quadrado): "))

  else:
    M = int(input("Informe o tamanho (M) do codebook a ser gerado: "))
    L = int(input("Informe o tamanho (L) de cada bloco (considera-se um bloco quadrado): "))

  if L > 255 or L < 1 or M > 256 or M < 1:
    sys.exit("ERRO: Informe valores de N e M válidos, entre 1 e 255; e 1 e 256, respectivamente.")

  filename = input("Informe o nome (caminho) da imagem a ser utilizada: ")
  directory = input("Informe o nome do diretório do resultado (será o atual caso não informado): ")
    
  codebookGen(filename, M, L, directory)