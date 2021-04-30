import helper as hp
import bitstring as bs
import sys
from PIL import Image
import numpy as np
import time

def encoder (filename, M, directory=''):
  header = bs.Bits(hex='0xE0') #Header sendo E + identificador se é colorida ou preto e branco + numero de bits de padding no final do arquivo

  no_path_name = hp.remove_path(filename) #Adquire somente o nome do arquivo em a ser lido
  filename_result = hp.add_path_cmp(directory, no_path_name) #Cria o nome do codebook junto com o diretório alvo

  try:
    with Image.open(filename) as im:

      if im.mode not in ['RGB', 'YCbCr', 'LAB', 'HSV']: #Verifica se a imagem é colorida
        mode = 0

      elif im.mode == 'L': #Ou se ela é preto e branco
        mode = 1

      else: raise WrongFormat()

      data = np.array(im)

      num_col = np.uint16(data.shape[1]) #Passar como informação lateral

      elements = getElements(data, mode)

      data_out, padding_end = quantizer(M, elements)

  except IOError as ioe:
    sys.exit('ERRO: Arquivo ou diretório "{}" não existente.'.format(ioe.filename))

  except hp.WrongFormat:
    sys.exit('ERRO: O programa aceita somente imagens coloridas.')

  print("Terminado! Criado arquivo '{}'.\n".format(filename_result))

#-----------------------------

def getElements(data, mode):
  pass

#------------------------------

def quantizer (M, elements):
  pass

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