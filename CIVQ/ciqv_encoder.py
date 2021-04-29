import filename_handler as fh
import bitstring as bs
import sys
from PIL import Image, UnidentifiedImageError
import numpy as np
import time
from sklearn.cluster import KMeans

def encoder(filename, codebook_name, directory=""):

  no_path_name = fh.remove_path(filename) #Adquire somente o nome do arquivo em a ser lido
  filename_result = fh.add_path_cqv(directory, no_path_name) #Cria o nome do codebook junto com o diretório alvo

  if codebook_name[-4:] != '.cdb': #Verifica se a extensão do arquivo a ser lido é a esperada
    sys.exit('Erro: Esperado arquivo de extensão: ".cdb".')

  try:
    with open(codebook_name, 'rb') as f_read:
      M, L, codebook = codebookParser(f_read)

    print(codebook)

    with Image.open(filename) as im:
      pass




  except IOError as ioe:
    sys.exit('ERRO: Arquivo ou diretório "{}" não existente.'.format(ioe.filename))

  except WrongFormat:
    sys.exit('ERRO: O programa aceita somente imagem em escala de cinza.')

  print("Terminado! Criado arquivo '{}'.\n".format(filename_result))

#----------------------------------------------

def codebookParser (f_read):
  M = int.from_bytes(f_read.read(1), byteorder='big') + 1
  L = int.from_bytes(f_read.read(1), byteorder='big')

  codebook = []

  buffer = f_read.read(L)

  while(buffer):
    codebook.append(np.frombuffer(buffer, dtype= np.uint8))
    buffer = f_read.read(L)

  return M, L, np.array(codebook)

#----------------------------------------------

class WrongFormat(Exception):
  pass

#----------------------------------------------

if __name__ == "__main__":
  if len(sys.argv) > 1:
    filename = sys.argv[1]
    if len(sys.argv) > 2:
      codebook_name = sys.argv[2]
    else:
      codebook_name = input("Informe o nome (caminho) do codebook (.cdb) a ser utilizado: ")

  else:
    filename = input("Informe o nome (caminho) da imagem a ser utilizada: ")
    codebook_name = input("Informe o nome (caminho) do codebook (.cdb) a ser utilizado: ")

  directory = input("Informe o nome do diretório do resultado (será o atual caso não informado): ")
    
  encoder(filename, codebook_name, directory)