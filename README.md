# ASM - Active Shape Models

**ASM** é uma aplicação com interface gráfica desenvolvida em Python utilizando a biblioteca **Tkinter**. Seu principal objetivo é trabalhar com amostras de imagens faciais marcadas por pontos de referência, utilizando o algoritmo **Active Shape Models (ASM)**.

## Funcionalidades

- Leitura de arquivos `.csv` contendo imagens e pontos de referência.
- Traçado do contorno facial sobre a imagem com base nas coordenadas.
- Exibição das coordenadas de cada ponto na interface.
- Operações geométricas entre formas (conjuntos de pontos).
- Cálculo da **distância euclidiana** entre pontos de uma mesma imagem.
- Cálculo da **distância de Procrustes** entre diferentes formas.
- Visualização do alinhamento entre formas.

---

## Como Executar o Projeto

1. Clone o repositório e acesse a pasta do projeto:

    ```bash
    git clone https://seu-repositorio.git
    cd nome-do-projeto
    ```

2. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

    > ⚠️ É necessário ter o **Python 3** instalado no sistema.

3. Execute a aplicação:

    ```bash
    python tk.py
    ```

4. Após iniciar a interface, vá em **Arquivo > Ler Arquivo** e selecione um arquivo `.csv` localizado na pasta `formas`.

---

**Desenvolvido por:** Pedro Lucca Monteiro Soares  
**E-mail:** pedrolucca27@gmail.com  
**LinkedIn:** [linkedin.com/in/pedro-lucca-dev](https://www.linkedin.com/in/pedro-lucca-dev)
