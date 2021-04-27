import filename_handler as fh
import bitstring as bs
import sys

#PIL, numpy, bitstring
def encoder (N, M, filename, directory):
  header = bs.Bits(hex='0xF0') #Header sendo F + numero de bits de padding no final do arquivo

  no_path_name = fh.remove_path(filename) #Adquire somente o nome do arquivo em a ser lido
  filename_result = fh.add_path_cqa(directory, no_path_name) #Cria o nome do arquivo comprimido junto com o diretório alvo

  try:
    with open(filename_result, 'wb') as f_write:
      pass
    pass

  except IOError as ioe:
    sys.exit('Arquivo ou diretório "{}" não existente.'.format(ioe.filename))

  print("Terminado! Criado arquivo '{}'.\n".format(filename_result))

#-------------------------------------

if __name__ == '__main__':
  if len(sys.argv) > 1:
    N = int(sys.argv[1])
    if len(sys.argv) > 2:
      M = int(sys.argv[2])
    else:
      M = input("Informe o número de níveis (M) do quantizador: ")

  else:
    N = input("Informe o tamanho do bloco (N) a ser utilizado: ")
    M = input("Informe o número de níveis (M) do quantizador: ")

  filename = input("Informe o nome (caminho) do arquivo a ser codificado: ")
  directory = input("Informe o nome do diretório do resultado (será o atual caso não informado): ")
  
  encoder(N, M, filename, directory)