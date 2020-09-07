# ASM
Interface Gráfica feita com a biblioteca Tkinter, essencialmente, o projeto tem como objetivo a implementação de operações encima de amostras de imagens de face, marcadas com pontos de referência utilizando do algoritmo ASM(Active Shape Models), a interface faria a leitura de um arquivo contendo dados de amostras de imagens com seus nomes de arquivo e pontos de referência nas imagens de face, após isso a aplicação traça um contorno da forma por cima da imagem de amostra e exibe na interface, o formato do contorno depende inteiramente das coordenadas enviadas pelo arquivo auxiliar, além disso se possui as funcionalidades de realizar operações nas formas(conjunto de pontos de uma imagem de face), pode exibir os valores das coordenadas de cada ponto de uma imagem na interface, ademais o algoritmo consegue calcular a distância euclidiana entre os pontos de referência em uma imagem de face, e por último também possui a capacidade de calcular a distância de procrustes entre uma forma e outra, e exibir o resultado de seu alinhamento.

Para rodar a aplicação:

  1)Após baixar o projeto, baixar as dependências do arquivo "requirements.txt" com o comando "pip install -r requirements. txt".
  
  2)Após instalados, modificar o caminhos das pastas "images" e "lines_images" para o caminho específico na sua máquina.
  
  3)Executar o arquivo "tk.py".
  
  4)Após a inicialização, abrir o arquivo ".csv" com a opção "Ler Aquivo" no menu "Arquivo" da interface, contido na pasta "formas" do projeto.

Obs: É necessário uma versão de python3 para a instalação dos requerimentos.
