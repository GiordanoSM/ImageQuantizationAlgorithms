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
    print("Começando a decodificação... (Pode demorar um pouco)")
    start = time.time()

    header = bs.Bits(filename= filename, length=8)#Header sendo F + numero de bits de padding no final do arquivo
  
    padding_end = checkHeader(header)#Extrai o tamanho do padding do final do arquivo do header e verifica-o

    M = bs.Bits(filename= filename, length=8, offset=8).uint + 1#Numero de elementos no codebook
    L = bs.Bits(filename= filename, length=8, offset=16).uint#Tamanho de cada bloco

    codebook, offset = codebookParser(filename, M, L, 24)
    #print(codebook, offset)

    n_blocos_h = bs.Bits(filename= filename, length=8, offset=offset).uint#informa a quantidade de blocos na horizontal

    padding_lin = bs.Bits(filename= filename, length=8, offset=offset+8).uint#número de linhas colocadas como padding
    padding_col = bs.Bits(filename= filename, length=8, offset=offset+16).uint#número de colunas colocadas como padding

    blocks = decoder(codebook, filename, M, L, padding_end, offset+24)#Extrai os blocos individualmente dos dados

    image_array = reconstructImageArray(blocks, n_blocos_h, padding_lin, padding_col)#Retornar o array com a imagem decodificada

    end = time.time()
    print('Demorou: {} segundos'.format(end - start))

    im = Image.fromarray(image_array)

    if show_image:
      ImageShow.show(im)

  except IOError as ioe:
    sys.exit('ERRO: Arquivo ou diretório "{}" não existente.'.format(ioe.filename))

  except WrongHeader:
    sys.exit('Erro: Header do arquivo não condiz com o esperado.')


#------------------------------------------
#Tem a função de reorganizar os blocos no formato da imagem original
def reconstructImageArray(blocks, n_blocos_h, padding_lin, padding_col):

  lines = []

  for i in range(0, len(blocks), n_blocos_h):
    lines.append(np.concatenate(blocks[i:i+n_blocos_h], axis=1))

  image_array = np.concatenate(lines, axis=0)
  
  return removeImagePadding(image_array, padding_lin, padding_col)

#------------------------------------------
def removeImagePadding(array, padding_lin, padding_col):
  if padding_lin != 0:
    array = np.delete(array, np.s_[-padding_lin:], axis= 0)
  if padding_col != 0:
    array = np.delete(array, np.s_[-padding_col:], axis= 1)
  return array

#-------------------------------------------
#Tem a função de extrair todos os blocos existentes mantendo seus formatos originais
def decoder(codebook, filename, M, L, padding_end, offset):
  bpb = int(np.ceil(np.log2(M)))
  N = int(np.sqrt(L))

  data = bs.Bits(filename=filename, offset= offset)

  if padding_end != 0:
    data = data[:-padding_end]

  blocks = []

  while data != bs.Bits(bin= "0b"):
    idx = data[:bpb].uint
    blocks.append(codebook[idx].reshape((N,N)))
    data = data[bpb:]

  return blocks

#------------------------------------------
def codebookParser (filename, M, L, offset):
  bpb = int(np.ceil(np.log2(M)))

  codebook = []

  for i in range(M):
    buffer = bs.Bits(filename= filename, length=L*8, offset=offset+i*L*8).tobytes()
    codebook.append(np.frombuffer(buffer, dtype= np.uint8))

  return np.array(codebook), offset+M*L*8

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