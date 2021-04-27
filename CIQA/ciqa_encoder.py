import filename_handler as fh
import bitstring as bs
import sys
from PIL import Image, UnidentifiedImageError
import numpy as np
import time

#PIL, numpy, bitstring
def encoder (N, M, filename, directory):
  header = bs.Bits(hex='0xF0') #Header sendo F + numero de bits de padding no final do arquivo

  no_path_name = fh.remove_path(filename) #Adquire somente o nome do arquivo em a ser lido
  filename_result = fh.add_path_cqa(directory, no_path_name) #Cria o nome do arquivo comprimido junto com o diretório alvo

  try:
    with Image.open(filename) as im:
      with open(filename_result, 'wb') as f_write:

        if im.mode != 'L': #Verifica se a imagem está em escala de cinza
          raise WrongFormat()

        data = np.asarray(im)


        print("Começando a quantização... (Pode demorar um pouco)")
        start = time.time()
        data_out, paddings = adaptiveQuantizer(N, M, data)

        header.tofile(f_write)

        bs.Bits(uint=N, length=8).tofile(f_write)
        bs.Bits(uint=M, length=8).tofile(f_write)

        bs.Bits(uint=paddings[0], length=8).tofile(f_write)
        bs.Bits(uint=paddings[1], length=8).tofile(f_write)

        data_out.tofile(f_write)

        f_write.seek(0)
        f_write.write((header[:4] + bs.Bits(uint= paddings[2], length= 4)).tobytes()) #Informa a quantidade final de padding no cabeçalho
        end = time.time()
        print('Demorou: {} segundos'.format(end - start))

  except IOError as ioe:
    sys.exit('ERRO: Arquivo ou diretório "{}" não existente.'.format(ioe.filename))

  except WrongFormat:
    sys.exit('ERRO: O programa aceita somente imagem em escala de cinza.')

  print("Terminado! Criado arquivo '{}'.\n".format(filename_result))

#-------------------------------------

class WrongFormat(Exception):
  pass

#-------------------------------------

def adaptiveQuantizer(N, M, data):

  data_out = bs.Bits(bin='0b')
  blocks_out = []

  padded_data, paddings = pad(N, data)

  blocks = getBlocks(N, padded_data)

  bpp = np.ceil(np.log2(M))

  for b in blocks:
    info = (np.min(b), np.max(b))
    delta = (info[1] - info[0])/M
    y = np.array([delta*(2*i - 1)/2 for i in range(1, M+1)])

    data_out = data_out + quantizeFunc(b, y, bpp, info)

  missing = lambda x: (8 - (x % 8))%8

  paddings.append((8 - (data_out.len % 8)) % 8)

  return data_out, paddings

#------------------------------------

def quantizeFunc(block, y, bpp, info):
  out = bs.Bits(uint=info[0], length=8) + bs.Bits(uint=info[1], length=8)

  for i in np.reshape(block, (1,-1))[0]:
    idx = findNearestIdx(y, i)
    out = out + bs.Bits(uint=idx, length=int(bpp))

  return out

#------------------------------------
def findNearestIdx(array, value):
    return (np.abs(array - value)).argmin()

#-------------------------------------
#Bem comportado até padding maximo de 255
def pad (N, data):
  missing = lambda x: (N - (x % N)) % N
  paddings = [np.uint8(missing(data.shape[0])), np.uint8(missing(data.shape[1]%N))]
  
  return np.pad(data, ((0,missing(data.shape[0])), (0,missing(data.shape[1])))), paddings

#-------------------------------------

def getBlocks(N, data):
  n_blocks_h = data.shape[0]/N
  n_blocks_v = data.shape[1]/N

  blocks = []

  for l in range(0, data.shape[0], N):
    for c in range(0, data.shape[1], N):
      blocks.append(data[l:l+N,range(c, c+N)])

  return blocks

#-------------------------------------

if __name__ == '__main__':
  if len(sys.argv) > 1:
    N = int(sys.argv[1])
    if len(sys.argv) > 2:
      M = int(sys.argv[2])
    else:
      M = int(input("Informe o número de níveis (M) do quantizador: "))

  else:
    N = int(input("Informe o tamanho do bloco (N) a ser utilizado: "))
    M = int(input("Informe o número de níveis (M) do quantizador: "))

  if N > 255 or N < 0 or M > 255 or M < 0:
    sys.exit("ERRO: Informe valores de N e M entre 0 e 255.")

  filename = input("Informe o nome (caminho) do arquivo a ser codificado: ")
  directory = input("Informe o nome do diretório do resultado (será o atual caso não informado): ")

  encoder(N, M, filename, directory)