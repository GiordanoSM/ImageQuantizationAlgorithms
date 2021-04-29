import helper as hp
import bitstring as bs
import sys
from PIL import Image, UnidentifiedImageError, ImageShow
import numpy as np
import time

def openner (filename, show_image=True):
  
  if filename[-4:] != '.cvq': #Verifica se a extensão do arquivo a ser lido é a esperada
    sys.exit('Erro: Esperado arquivo de extensão: ".cvq".')

  try:
    header = bs.Bits(filename= filename, length=8)#Header sendo F + numero de bits de padding no final do arquivo
  
    padding_end = checkHeader(header)#Extrai o tamanho do padding do final do arquivo do header e verifica-o


  except IOError as ioe:
    sys.exit('ERRO: Arquivo ou diretório "{}" não existente.'.format(ioe.filename))

  except WrongHeader:
    sys.exit('Erro: Header do arquivo não condiz com o esperado.')

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