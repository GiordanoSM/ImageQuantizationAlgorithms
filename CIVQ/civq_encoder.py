import helper as hp
import bitstring as bs
import sys
from PIL import Image, UnidentifiedImageError
import numpy as np
import time
from scipy.spatial.distance import euclidean

def encoder(filename, codebook_name, directory=""):

  header = bs.Bits(hex='0xF0') #Header sendo F + numero de bits de padding no final do arquivo

  no_path_name = hp.remove_path(filename) #Adquire somente o nome do arquivo em a ser lido
  filename_result = hp.add_path_cqv(directory, no_path_name) #Cria o nome do codebook junto com o diretório alvo

  if codebook_name[-4:] != '.cdb': #Verifica se a extensão do arquivo a ser lido é a esperada
    sys.exit('Erro: Esperado arquivo de extensão: ".cdb".')

  try:
    with open(codebook_name, 'rb') as f_read:

      print("Começando a codificação... (Pode demorar um pouco)")
      start = time.time()

      M, L, codebook = codebookParser(f_read)
      #print(codebook)
      f_read.seek(0)

      with Image.open(filename) as im:
        with open(filename_result, 'wb') as f_write:

          if im.mode != 'L': #Verifica se a imagem está em escala de cinza
            raise WrongFormat()

          data = np.asarray(im)

          header.tofile(f_write)

          f_write.write(f_read.read())

          N = int(np.sqrt(L))
          padded_data, paddings = pad(N, data)

          blocks, n_blocks_h = getBlocks(N, padded_data)

          bs.Bits(uint=n_blocks_h-1, length=8).tofile(f_write)#informa a quantidade de blocos na horizontal
          bs.Bits(uint=paddings[0], length=8).tofile(f_write)#número de linhas colocadas como padding
          bs.Bits(uint=paddings[1], length=8).tofile(f_write)#número de colunas colocadas como padding

          data_out, padding_end = quantizer(blocks, codebook)

          data_out.tofile(f_write)

          f_write.seek(0)
          f_write.write((header[:4] + bs.Bits(uint= padding_end, length= 4)).tobytes()) #Informa a quantidade final de padding no cabeçalho
          end = time.time()
          print('Demorou: {} segundos'.format(end - start))

  except IOError as ioe:
    sys.exit('ERRO: Arquivo ou diretório "{}" não existente.'.format(ioe.filename))

  except WrongFormat:
    sys.exit('ERRO: O programa aceita somente imagem em escala de cinza.')

  print("Terminado! Criado arquivo '{}'.\n".format(filename_result))

#-------------------------------------

def quantizer(blocks, codebook):
  data_out = bs.Bits(bin='0b')
  bpb = int(np.ceil(np.log2(codebook.shape[0])))

  for b in blocks.astype(np.int16):
    distances = []
    for c in codebook.astype(np.int16):
      distances.append(euclidean(b, c))
    data_out = data_out + bs.Bits(uint=np.array(distances).argmin(),length= bpb)

  padding = (8 - (data_out.len % 8)) % 8

  return data_out, padding

#-------------------------------------
#Bem comportado até padding maximo de 255
def pad (N, data):
  missing = lambda x: (N - (x % N)) % N
  paddings = [np.uint8(missing(data.shape[0])), np.uint8(missing(data.shape[1]%N))]
  
  return np.pad(data, ((0,missing(data.shape[0])), (0,missing(data.shape[1])))), paddings

#----------------------------------------------
#Bem comportado até 255 blocos na horizontal
def getBlocks(N, data):
  n_blocks_h = data.shape[1]/N
  n_blocks_v = data.shape[0]/N

  blocks = []

  for l in range(0, data.shape[0], N):
    for c in range(0, data.shape[1], N):
      blocks.append(data[l:l+N,range(c, c+N)].reshape(1,-1)[0])

  return np.array(blocks), int(n_blocks_h)

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