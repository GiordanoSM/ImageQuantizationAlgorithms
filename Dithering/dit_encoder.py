import helper as hp
import bitstring as bs
import sys
from PIL import Image
import numpy as np
import time

def encoder (filename, M, directory=''):
  header = bs.Bits(hex='0xE0') #Header sendo E + identificador se é colorida ou preto e branco + numero de bits de padding no final do arquivo

  no_path_name = hp.remove_path(filename) #Adquire somente o nome do arquivo em a ser lido
  filename_result = hp.add_path_dit(directory, no_path_name) #Cria o nome do codebook junto com o diretório alvo

  try:
    with Image.open(filename) as im:

      if im.mode in ['RGB', 'YCbCr', 'LAB', 'HSV']: #Verifica se a imagem é colorida
        mode = 0

      elif im.mode == 'L': #Ou se ela é preto e branco
        mode = 1

      else: raise hp.WrongFormat()

      print("Começando a quantização... (Pode demorar um pouco)")
      start = time.time()

      data = np.array(im)

      num_col = np.uint16(data.shape[1]) #Passar como informação lateral

      elements = getElements(data)

      data_out, padding_end = quantizer(M, elements)

      with open(filename_result, 'wb') as f_write:

        header.tofile(f_write)
        bs.Bits(uint=M-1, length=8).tofile(f_write) #M-1 para aceitar M=256
        bs.Bits(uint=num_col, length=16).tofile(f_write) #2 bytes para a largura da imagem original

        data_out.tofile(f_write)

        f_write.seek(0)
        #Informa a quantidade final de padding no cabeçalho e se a imagem é colorida ou não
        f_write.write((header[:3] + bs.Bits(uint= mode, length= 1) + bs.Bits(uint= padding_end, length= 4)).tobytes())

      end = time.time()
      print('Demorou: {} segundos'.format(end - start))

  except IOError as ioe:
    sys.exit('ERRO: Arquivo ou diretório "{}" não existente.'.format(ioe.filename))

  except hp.WrongFormat:
    sys.exit('ERRO: O programa aceita somente imagens coloridas.')

  print("Terminado! Criado arquivo '{}'.\n".format(filename_result))

#-----------------------------

def getElements(data):
  return data.reshape(-1)

#------------------------------

def quantizer (M, elements):
  bpp = int(np.ceil(np.log2(M)))
  data_out = bs.Bits(bin='0b')

  delta = 255/M
  y = np.array([delta*(2*i - 1)/2 for i in range(1, M+1)])

  for p in elements:
    idx = findNearestIdx(y, p)
    data_out = data_out + bs.Bits(uint=idx, length= bpp)

  padding_end = (8 - (data_out.len % 8)) % 8

  return data_out, padding_end

#------------------------------

def findNearestIdx(array, value):
  return (np.abs(array-value)).argmin()

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