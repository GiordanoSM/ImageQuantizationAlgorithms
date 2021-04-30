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

    print(padding_end, M, num_col)
    print(codebook)
    
    end = time.time()
    print('Demorou: {} segundos'.format(end - start))

  except IOError as ioe:
    sys.exit('ERRO: Arquivo ou diretório "{}" não existente.'.format(ioe.filename))

  except WrongHeader:
    sys.exit('Erro: Header do arquivo não condiz com o esperado.')

#------------------------------------------
def codebookParser (filename, M, offset):
  bpp = int(np.ceil(np.log2(M)))
  codebook = []

  for i in range(M):
    buffer = bs.Bits(filename= filename, length=24, offset=offset+i*24).tobytes()
    codebook.append(np.frombuffer(buffer, dtype= np.uint8))

  return np.array(codebook), offset+M*24

#-------------------------------------------
#Tem a função de reorganizar os pixels no formato da imagem original
def reconstructImageArray():
  pass

#-------------------------------------------
#Tem a função de extrair todos os pixels codificados
def decoder(codebook, data, M, padding_end):
  pass

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