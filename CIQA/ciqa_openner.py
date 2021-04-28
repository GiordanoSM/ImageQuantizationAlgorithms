from PIL import Image, UnidentifiedImageError, ImageShow
import numpy as np
import bitstring as bs
import sys
import time
 
def openner (filename):

  if filename[-4:] != '.cqa': #Verifica se a extensão do arquivo a ser lido é a esperada
    sys.exit('Erro: Esperado arquivo de extensão: ".cqa".')

  try:
    header = bs.Bits(filename= filename, length=8)

    padding_end = check_header(header)

    N = bs.Bits(filename= filename, length=8, offset=8).uint
    M = bs.Bits(filename= filename, length=8, offset=16).uint

    n_blocos_h = bs.Bits(filename= filename, length=8, offset=24).uint

    padding_lin = bs.Bits(filename= filename, length=8, offset=32).uint
    padding_col = bs.Bits(filename= filename, length=8, offset=40).uint

    start = time.time()
    blocks = decoder(N, M, padding_end, filename)

    image_array = reconstructImageArray(blocks, n_blocos_h, padding_lin, padding_col)
    end = time.time()
    print('Demorou: {} segundos'.format(end - start))
    print(image_array)
    
    im = Image.fromarray(image_array)

    ImageShow.show(im)
 
  except IOError as ioe:
    sys.exit('ERRO: Arquivo ou diretório "{}" não existente.'.format(ioe.filename))

  except WrongHeader:
    sys.exit('Erro: Header do arquivo não condiz com o esperado.')

#-------------------------------------------

def decoder(N, M, padding_end, filename):

  bpp = int(np.ceil(np.log2(M)))

  block_size = 2*8 + bpp*N*N #em bits

  data = bs.Bits(filename=filename, offset= 48)

  if padding_end != 0:
    data = data[:-padding_end]

  blocks = []

  while data != bs.Bits(bin= "0b"):
    block = []

    _min = data[:8].uint
    _max = data[8:16].uint
    values = data[16:block_size]

    delta = (_max - _min)/M
    y = np.array([delta*(2*i - 1)/2 + _min for i in range(1, M+1)]).astype(np.uint8)

    for i in range(0, values.len, bpp):
      block.append(y[values[i:i+bpp].uint])

    blocks.append(np.array(block).reshape((N,N)))

    data = data[block_size:]

  return blocks

#------------------------------------------
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
#Checa se o header corresponde com o esperado e retorna o padding informado por ele
def check_header(header):

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
  else: filename = input("Informe o nome (caminho) do arquivo a ser codificado: ")

  openner(filename)