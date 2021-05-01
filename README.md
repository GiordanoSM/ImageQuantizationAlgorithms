# ImageQuantizationAlgorithms
## Informações
***Autor:** Giordano Süffert Monteiro

**Versão Python:** 3.7.1

**Necessários os seguintes pacotes instalados utilizando 'pip install':** bitstring, PIL, numpy, sklearn

**Cada programa deve ser executado na linha de comando dentro do seu diretório correspondente**

## CIQA

### ciqa_encoder.py

Será pedido para serem informados os parâmetros N (dimensão de um bloco quadrado), M (níveis do quantizador) e o nome (path) da image gray scale a ser codificada. De forma opcional, poderá ser informado um diretório diferente no qual o resultado (arquivo .cqa) será salvo.

**Exemplo:**
  >python3 ciqa_encoder.py

  >Informe o tamanho tamanho dos lados do bloco (N) a ser utilizado: 4

  >Informe o número de níveis (M) do quantizador: 2

  >Informe o nome (caminho) do arquivo a ser codificado: ../ImageDatabase/peppers.bmp

  >Informe o nome do diretório do resultado (será o atual caso não informado): results

### ciqa_openner.py

Será pedido para ser informado o nome (path) do arquivo codificado (*.cqa) que será aberto e mostrado.

**Exemplo:**
  >python3 ciqa_openner.py

  >Informe o nome (caminho) da imagem (.cqa) a ser aberta: results/peppers.cqa

## CIVQ

### civq_codebook.py

Será pedido para serem informados os parâmetros M (tamanho do codebook), L (tamanho de cada bloco) e o nome (path) da image gray scale a ser utilizada como base. De forma opcional, poderá ser informado um diretório diferente no qual o codebook resultante (arquivo .cdb) será salvo.

**Exemplo:**
  >python3 civq_codebook.py

  >Informe o tamanho (M) do codebook a ser gerado: 32

  >Informe o tamanho (L) de cada bloco (considera-se um bloco quadrado): 4

  >Informe o nome (caminho) da imagem a ser utilizada: ../ImageDatabase/baboon.bmp

  >Informe o nome do diretório do resultado (será o atual caso não informado): codebooks

### civq_encoder.py

Será pedido para serem informados o nome (path) da image gray scale a ser codificada e o nome (path) do arquivo contendo o codebook a ser utilizado (.cdb). De forma opcional, poderá ser informado um diretório diferente no qual o resultado (arquivo .cqa) será salvo.

**Exemplo:**
  >python3 civq_encoder.py

  >Informe o nome (caminho) da imagem a ser utilizada: ../ImageDatabase/baboon.bmp

  >Informe o nome (caminho) do codebook (.cdb) a ser utilizado: codebooks/baboon.cdb

### civq_openner.py

Será pedido para ser informado o nome (path) do arquivo codificado (*.cvq) que será aberto e mostrado.

**Exemplo:**
  >python3 civq_openner.py

  >Informe o nome (caminho) da imagem (.cvq) a ser aberta: results/baboon.cvq

## CIMap

### cimap_encoder.py

Será pedido para serem informados os parâmetros M (número de cores) e o nome (path) da image colorida a ser codificada. De forma opcional, poderá ser informado um diretório diferente no qual o resultado (arquivo .cmp) será salvo.

**Exemplo:**
  >python3 cimap_encoder.py

  >Informe o tamanho (M) do codebook (número de cores) a ser gerado: 16

  >Informe o nome (caminho) da imagem a ser codificada: ../ImageDatabase/kodim05.bmp

  >Informe o nome do diretório do resultado (será o atual caso não informado): results

### cimap_openner.py

Será pedido para ser informado o nome (path) do arquivo codificado (*.cmp) que será aberto e visualizado.

**Exemplo:**
  >python3 cimap_openner.py

  >Informe o nome (caminho) da imagem (.cmp) a ser aberta: results/kodim05.cqa

## Dithering

### dit_encoder.py

Será pedido para serem informados os parâmetros M (níveis do quantizador), o nome (path) da image a ser codificada e se deve ser utilizado dithering. De forma opcional, poderá ser informado um diretório diferente no qual o resultado (arquivo .dit) será salvo.

**Exemplo:**
  >python3 dit_encoder.py

  >Informe o número de níveis (M) do quantizador: 8

  >Informe o nome (caminho) da imagem a ser codificada: ../ImageDatabase/lena_colour.bmp

  >Informe o nome do diretório do resultado (será o atual caso não informado): results

  >Deve ser utilizado Dithering? (S/N): S

### dit_openner.py

Será pedido para ser informado o nome (path) do arquivo codificado (*.dit) que será aberto e visualizado.

**Exemplo:**
  >python3 dit_openner.py

  >Informe o nome (caminho) da imagem (.dit) a ser aberta: results/lena_colour.dit