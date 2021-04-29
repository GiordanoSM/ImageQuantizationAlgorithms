import re
import numpy as np

#Retira parte do nome do arquivo que indica o caminho
def remove_path(filename):
  return re.split(r'\\|/', filename)[-1]

#Adiciona a extensão .cqv e o diretório alvo no novo arquivo
def add_path_cqv(directory, no_path_name):
  _name = no_path_name[:-4] + '.cqv'
  return directory + '/' + _name if directory else _name

#Adiciona a extensão .cdb e o diretório alvo no novo arquivo
def add_path_cdb(directory, no_path_name):
  _name = no_path_name[:-4] + '.cdb'
  return directory + '/' + _name if directory else _name

def codebookParser (f_read):
  M = int.from_bytes(f_read.read(1), byteorder='big') + 1
  L = int.from_bytes(f_read.read(1), byteorder='big')

  codebook = []

  buffer = f_read.read(L)

  while(buffer):
    codebook.append(np.frombuffer(buffer, dtype= np.uint8))
    buffer = f_read.read(L)

  return M, L, np.array(codebook)