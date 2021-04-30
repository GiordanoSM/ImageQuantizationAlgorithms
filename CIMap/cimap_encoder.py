import helper as hp
import bitstring as bs
import sys
from PIL import Image, UnidentifiedImageError
import numpy as np
import time
from sklearn.cluster import KMeans

def encoder(filename, M, directory=''):

  header = bs.Bits(hex='0xF0') #Header sendo F + numero de bits de padding no final do arquivo

  no_path_name = hp.remove_path(filename) #Adquire somente o nome do arquivo em a ser lido
  filename_result = hp.add_path_cmp(directory, no_path_name) #Cria o nome do codebook junto com o diretório alvo

  try:
    with Image.open(filename) as im:

      if im.mode not in ['RGB', 'YCbCr', 'LAB', 'HSV']: #Verifica se a imagem é colorida
            raise WrongFormat()

      data = np.asarray(im)

      num_col = np.uint16(data.shape[1]) #Passar como informação lateral

      elements = getElements(data) #Retorna lista com todos os elementos (pixels)

      print("Começando a codificação... (Pode demorar um pouco)")
      start = time.time()

      codebook, idxs = makeCodebook(M, elements) #Retorna uint8 codebook e índices

      data_out, padding_end = quantizer(M, idxs)

      with open(filename_result, 'wb') as f_write:
        header.tofile(f_write)
        bs.Bits(uint=M-1, length=8).tofile(f_write) #M-1 para aceitar M=256
        bs.Bits(uint=num_col, length=16).tofile(f_write) #2 bytes para a largura da imagem original

        for p in codebook: #Escreve o codebook no arquivo (codebook já é uint8)
          f_write.write(p.tobytes())

        data_out.tofile(f_write)

        f_write.seek(0)
        f_write.write((header[:4] + bs.Bits(uint= padding_end, length= 4)).tobytes()) #Informa a quantidade final de padding no cabeçalho

      end = time.time()
      print('Demorou: {} segundos'.format(end - start))

  except IOError as ioe:
    sys.exit('ERRO: Arquivo ou diretório "{}" não existente.'.format(ioe.filename))

  except hp.WrongFormat:
    sys.exit('ERRO: O programa aceita somente imagens coloridas.')

  print("Terminado! Criado arquivo '{}'.\n".format(filename_result))

#------------------------------
def getElements(data):
  return np.reshape(data, (1,-1,3))[0]

#------------------------------
def makeCodebook(M, elements):

  kmeans = KMeans(n_clusters= M).fit(elements)
  return kmeans.cluster_centers_.astype(np.uint8), kmeans.labels_.astype(np.uint8)

#------------------------------
def quantizer (M, idxs):
  data_out = bs.Bits(bin='0b')
  bpp = int(np.ceil(np.log2(M)))

  for i in idxs: #Gera bits dos índices dos pixels que serão escritos no arquivo utilizando bpp bits para cada
    data_out = data_out + bs.Bits(uint=i, length=bpp)

  padding_end = (8 - (data_out.len % 8)) % 8

  return data_out, padding_end

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