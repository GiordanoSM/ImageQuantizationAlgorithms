import re

#Retira parte do nome do arquivo que indica o caminho
def remove_path(filename):
  return re.split(r'\\|/', filename)[-1]

#Adiciona a extensão .cqa e o diretório alvo no novo arquivo
def add_path_cqa(directory, no_path_name):
  _name = no_path_name[:-4] + '.cqa'
  return directory + '/' + _name if directory else _name