class Forma:
    def __init__(self):
        self.image = ""
        self.pontos = []
        self.euclidiana = []
        self.dimension = 2
        self.forma = []
        self.peso = []

    def setDados(self, imagem):
        count = 0
        countaux= 0
        dadoaux = [0,0]
        for dados in imagem:
            if(count == 0):
                self.image = dados
                count += 1
            elif(countaux == 1):
                dadoaux[1] = dados
                self.peso.append(1)
                self.forma.append(dados)
                self.pontos.append(list(dadoaux))
                count += 1
                countaux = 0
            else:
                dadoaux[0] = dados
                self.peso.append(1)
                self.forma.append(dados)
                countaux = 1
    
    #def point_distances():
        #equals = Forma()
        #alternates = Forma()
        #for i in range(0,(len(self.forma)/2)):
            #alternates.forma = alternates.forma + self.forma
            #for i in range(0,(len(self.forma)/2):
                # Duvida

        