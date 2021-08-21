import cv2
from PIL import Image
from sklearn.preprocessing import normalize
from tkinter import filedialog
import numpy as np
import math
import scipy.spatial as ss
import statistics
from bresenham import bresenham
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
import execute
from skimage.io import imshow, imread
from skimage.color import rgb2hsv, hsv2rgb
from skimage.color import rgb2gray
from skimage import util 

#s1 e st seriam arrays com os pontos da forma, o peso seria um array com os pesos gerados na outra função

def calcular_peso_procrustes(shapes):
    numPoints = len(shapes[0].pontos)/shapes[0].dimension
    distances = []

    for i in range(0,len(shapes)):
        distances.append(shapes[i].pointsDistances())

    mean = statistics.mean(distances)
    squares = []

    for i in range(0,len(distances)):
        dif = distances[i] - mean
        squares.append(dif * dif)

    div = (1.0/len(shapes))
    soma = sum(squares)
    variance = statistics.variance(sum, div)
    weights = []
    #for i in range(0, variance.height):#falta entender
       # weights.append(1.0/variance.lineSum(line: i)!)
    #self.
    return weights

def calcular_forma_media(formas):
    soma = np.zeros((len(formas[0].procrustes_g), 2))

    for forma in formas:
        soma = soma + np.array(forma.procrustes_g)
    return (soma/(len(formas)))


def dist_euclidiana(v1, v2):
    v1, v2 = np.array(v1), np.array(v2)
    distance = math.sqrt(((v2[0] - v1[0]) * (v2[0] - v1[0])) + ((v2[1] - v1[1]) * (v2[1] - v1[1])))
    return distance

def arredondar(alvo):
    i = 0
    while i < len(alvo):
        alvo[i][0] = round(alvo[i][0])
        alvo[i][1] = round(alvo[i][1])
        i += 1
    return alvo

def save_shape():
    img = imread('forma_media/mean_shape.jpg')
    red_filtered = (img[:,:,0] > 180) & (img[:,:,1] < 60) & (img[:,:,2] < 80)
    plt.figure(num=None, figsize=(8, 6), dpi=80)
    img_new = img.copy()
    img_new[:, :, 0] = img_new[:, :, 0] * red_filtered
    img_new[:, :, 1] = img_new[:, :, 1] * red_filtered
    img_new[:, :, 2] = img_new[:, :, 2] * red_filtered

    inverted_img = util.invert(img_new)
    gray = rgb2gray(inverted_img)
    plt.imsave('forma_media/test.jpg', gray, cmap = plt.cm.gray)
    #plt.disconnect()

def get_centro_de_massa():
    img = cv2.imread("forma_media/test.jpg", 0)
    threshold = 200
    ret,thresh = cv2.threshold(img,threshold,255,cv2.THRESH_BINARY)
    height, width = thresh.shape[:2]
    mass = 0
    Xcm  = 0.0
    Ycm  = 0.0

    for i in range(width) :
        for j in range(height):
            if not thresh[j][i]:
                mass += 1
                Xcm  += i
                Ycm  += j

    Xcm = Xcm/mass
    Ycm = Ycm/mass

    return [round(Xcm), round(Ycm)]

def get_center_image(formas):
    image = cv2.imread('images/' + formas[0].image)
    (h, w) = image.shape[:2] #w:image-width and h:image-height
    return [w//2, h//2]

def centralizar_m(m, dif):
    for ponto in m:
        ponto += dif

    return m

def aplicacao_parte_1(formas, m, magnitude):
    execute.salvar_forma_media(magnitude, m, formas)
    save_shape()
    mean_center = get_centro_de_massa()
    center_img = get_center_image(formas)
    diferenca = (np.array(center_img) - np.array(mean_center))
    #print(diferenca)
    m = centralizar_m(m*magnitude, diferenca)
    return m


def normalizar(alvo):
    #for i in alvo:
    #print(alvo)
    m = []
    magnitude = np.linalg.norm(alvo, axis=None, keepdims=True)
    m = (alvo/magnitude)
    #m = m*magnitude#Multiplicar pelo fator de escala

    return np.array(m), magnitude

def alinhar_formas(formas, m):
    i = 0
    while i < len(formas):
        pontos = np.array(formas[i].pontos)
        Z = dist_procrustes(m, pontos)[1]#Alinhar cada forma da lista F com a média m
        #formas[i].pontos = arredondar(Z)
        #print(Z)
        formas[i].procrustes_g = Z
        i += 1
    return formas

def juntar_pontos(formas):
    aux_formas = np.array(formas[0].procrustes_g)
    i = 1
    while i < len(formas):
        #print(formas[i].procrustes_g)
        aux_formas = np.append(aux_formas, formas[i].procrustes_g)
        i += 1
    #print(aux_formas)
    return aux_formas
    

def procrustes_generalizada(formas):
    alvo = np.array(formas[0].pontos)#1.Fazer uma copia de uma forma aleatória
    alvo, magnitude = normalizar(alvo)#2.Normalizar a forma alvo, dividindo o vetor pela sua própria magnitude
    m = alvo #3.Atribuir à forma média m o alvo normalizado
    forma_inicial = juntar_pontos(formas)#4.Guardar o valor atual de F
    formas_alinhadas = alinhar_formas(formas, m)#5.Alinhar cada forma da lista F com a média m
    m = np.array(calcular_forma_media(formas_alinhadas))#6.Atualizar a forma média m
    m = dist_procrustes(alvo, m)[1]#7.Alinhar forma média m com o alvo
    m = normalizar(m)[0]#8.Normalizar a forma média m
    i = 0

    while (np.array_equal(forma_inicial, juntar_pontos(formas)) == False):#9. Se a lista F tiver sofrido alguma mudança durante o processo, ou seja, se F’ != F, voltar ao passo 4.
        if i == 1000:
            mean = aplicacao_parte_1(formas, m, magnitude)
            return formas_alinhadas, mean , m, magnitude
        forma_inicial = juntar_pontos(formas)#4.Guardar o valor atual de F
        formas_alinhadas = alinhar_formas(formas, m)#5.Alinhar cada forma da lista F com a média m
        m = np.array(calcular_forma_media(formas_alinhadas))#6.Atualizar a forma média m
        m = dist_procrustes(alvo, m)[1]#7.Alinhar forma média m com o alvo
        m = normalizar(m)[0]#8.Normalizar a forma média m
        i += 1

    mean = aplicacao_parte_1(formas, m, magnitude)
    return formas_alinhadas, mean , m, magnitude #Lista de formas F alinhadas e forma média m

def amostras_por_ponto(formas):
    matriz_total = []
    i = 0
    #print(len(formas[0].p_derivada_norm[0]))
    while i < len(formas[0].p_derivada_norm[0]):
        k = 0
        matriz_aux = []
        while k < len(formas):
            matriz_aux.append(formas[k].p_derivada_norm[0][i])
            k = k + 1
        matriz_total.append(matriz_aux)
        i = i + 1
    #matriz = np.matrix(matriz_total[0][0][1])
    #print(matriz_total[0][0])
    return matriz_total

def pca_amostras(matriz, formas):
    arrays_formas = []

    p = 0
    while p < len(formas[0].p_derivada_norm[0]):
        array_amostra = []
        for perfil in matriz[p]:
            for ponto in perfil:
                array_amostra.append(list(ponto))
        arrays_formas.append(array_amostra)
        p = p + 1

    autovalores = []
    autovetores = []
    for array in arrays_formas:
        pca = PCA()
        array_aux = (np.array(array)).reshape(len(array)*2, 1)
        pca.fit(array_aux)
        print(array_aux.shape)
        #print(array)
        autovetores.append(list(pca.components_))
        autovalores.append(list(pca.explained_variance_))
        #autovetores.append(list(pca.components_))
        #autovalores.append(list(pca.explained_variance_))

    #print(np.array(autovalores).shape)
    #print("\n")
    #print(np.array(autovetores).shape)
    print(len(autovetores))
    print(autovalores)
    print("passou")
    return autovalores, autovetores

    
def primeira_derivadada(formas):
    for forma in formas:
        for vetor in forma.amostra:
            #print("\n")
            i = 0
            lista_aux = []
            while i <= (len(vetor) - 1):
                #print(vetor)
                if i == (len(vetor) - 1):
                    lista_aux.append(list(np.array(vetor[i]) - np.array(vetor[0])))
                    #print(lista_aux)
                    forma.p_derivada.append(lista_aux)
                    lista_aux = []
                else:
                    #print(np.array(vetor[i]), np.array(vetor[i+1]))
                    lista_aux.append(list(np.array(vetor[i]) - np.array(vetor[i+1])))
                i += 1
        
        #print("\n\n")
        #print(forma.p_derivada)
        #print("\n\n")
    normalizar_amostras(formas)
    matriz = amostras_por_ponto(formas)
    autovalores, autovetores = pca_amostras(matriz, formas)
    return autovalores, autovetores

def normalizar_amostras(formas):
    for forma in formas:
        lista_aux = []
        for vetor in forma.p_derivada:
            #print("\n")
            lista_aux.append(list(normalizar(vetor)[0]))
        
        forma.p_derivada_norm.append(lista_aux)
        #print("\n\n")
        #print(forma.p_derivada)
        #print("\n\n")


def amostras_textura(formas, d):
    for forma in formas:
        i = 0
        while i < len(forma.pontos):
            x1,y1 = forma.pontos[i-1][0], forma.pontos[i-1][1]
            p1 = (forma.pontos[i-1][0], forma.pontos[i-1][1])
            x3,y3 = forma.pontos[i][0], forma.pontos[i][1]
            p3 = (forma.pontos[i][0], forma.pontos[i][1])
            

            if i == (len(forma.pontos) - 1):
                p2 = (forma.pontos[0][0], forma.pontos[0][1])
                x2,y2 = forma.pontos[0][0], forma.pontos[0][1]
                #print("p3", p3)
            else:
                p2 = [forma.pontos[i+1][0], forma.pontos[i+1][1]]
                x2,y2 = forma.pontos[i+1][0], forma.pontos[i+1][1]

            k = float(((y2-y1) * (x3-x1) - (x2-x1) * (y3-y1)) / ((y2-y1)**2 + (x2-x1)**2))
            x4 = float(x3 - k * (y2-y1))
            y4 = float(y3 + k * (x2-x1))

            p4 = [round(x4), round(y4)]
            #print(p4)
            #print(line1)
            
            diferenca = np.array(p3) - np.array(p4)
            #print(diferenca)

            p6 = np.array(p3) + diferenca
            #p4 = np.array(p4) - diferenca
            #print("P4:", p4)
            line = list(bresenham(p4[0], p4[1], p6[0], p6[1]))
            while len(line) <= d:
                p6 = np.array(p6) + diferenca
                p4 = np.array(p4) - diferenca
                #print("P4:", p4)
                #print("PONTOS:", p3, p4, "\n")
                line = list(bresenham(p4[0], p4[1], p6[0], p6[1]))
            #print(line)
            #print(p1,p3,p2)
            
            j = line.index(p3)
            k = j - int(d/2)
            j = j + int(d/2)
            list_aux = []

            while k <= j:
                list_aux.append(line[k])
                k += 1
    
            forma.amostra.append(list_aux)
            i += 1

    autovalores, autovetores = primeira_derivadada(formas)

    return autovalores, autovetores

def amostra_forma(forma, d):
    i = 0
    amostra_centralizada = []
    while i < len(forma):
        x1,y1 = forma[i-1][0], forma[i-1][1]
        p1 = (forma[i-1][0], forma[i-1][1])
        x3,y3 = forma[i][0], forma[i][1]
        p3 = (forma[i][0], forma[i][1])
        #print(i)
        if i == (len(forma) - 1):
            p2 = (forma[0][0], forma[0][1])
            x2,y2 = forma[0][0], forma[0][1]
            #print("p3", p3)
        else:
            p2 = [forma[i+1][0], forma[i+1][1]]
            x2,y2 = forma[i+1][0], forma[i+1][1]

        k = float(((y2-y1) * (x3-x1) - (x2-x1) * (y3-y1)) / ((y2-y1)**2 + (x2-x1)**2))
        x4 = float(x3 - k * (y2-y1))
        y4 = float(y3 + k * (x2-x1))

        p4 = [round(x4), round(y4)]
        #print(p4)
        #print(line1)
        
        diferenca = np.array(p3) - np.array(p4)
        #print(diferenca)

        p6 = np.array(p3) + diferenca
        #p4 = np.array(p4) - diferenca
        #print("P4:", p4)
        line = list(bresenham(p4[0], p4[1], p6[0], p6[1]))
        while len(line) <= d:
            p6 = np.array(p6) + diferenca
            p4 = np.array(p4) - diferenca
            #print("P4:", p4)
            #print("PONTOS:", p3, p4, "\n")
            line = list(bresenham(p4[0], p4[1], p6[0], p6[1]))
        #print(line)
        #print(p1,p3,p2)
        
        j = line.index(p3)
        k = j - int(d/2)
        j = j + int(d/2)
        list_aux = []

        while k <= j:
            list_aux.append(line[k])
            k += 1

        amostra_centralizada.append(list_aux)
        i += 1

    #print(forma)
    #print("\n\n")
    #print(amostra_centralizada)

    return amostra_centralizada

def ajuste_forma(estimativa, forma_media, magnitude, formas, autovalores, autovetores):
    #passo 1
    autovetores = np.array(autovetores)
    autovalores = np.array(autovalores)
    print("AUTOVAL", autovalores.shape)
    print("AUTOVET", autovetores.shape)
    m = dist_procrustes(estimativa, forma_media)[1]
    #print(m)
    #print('\n\n')
    #print(estimativa)
    #passo 2
    print(len(autovalores))
    #print(autovetores)
    #print("\n\n")
    #print(autovetores.reshape(len(autovetores), 1))
    
    res_diff = np.array(m - forma_media)
    print("PRINTANDO DIFF:")
    print(res_diff)
    #print(res_diff.shape)
    
    b = autovetores*res_diff#Precisa mesmo ser a transposta?? Algo a ser testado.
    b = np.array(b)
    print("PRINTANDO B:\n")
    print(autovalores.shape)
    print(res_diff.shape)
    print(autovalores.shape)
    print(b.shape)
    print(b)
    print("CABOU")
    #b = (m - forma_media)
    #print(autovalores)
    #passo 3
    k = 0
    peso = b[0] #OBS: solução temporária enquanto não se resolve o problema
    for i in autovalores:
        i = float(i[0])
        result = 3*math.sqrt(i)
        for j in peso:
            print("J",j)
            #print(abs(j))
            if abs(j[0]) >= result:
                j[0] = result
            if abs(j[1]) >= result:
                j[1] = result
        #k += 1
    
    print(b.shape)
    #passo 4
    x_c = forma_media + (autovalores*b)
    forma_corrigida = x_c[0]
    print("FORMA CORRIGIDA:")
    print(x_c[0])
    forma_ajustada = dist_procrustes(forma_corrigida, estimativa)[1]
    resultado_final = forma_ajustada*magnitude #Não estou fazendo com a inversa, algo a ser testado ainda
    print("RESULTADO FINAL:")
    print(resultado_final)
    return m


 
def dist_procrustes(X, Y, scaling=True, reflection='best'):

    n,m = X.shape
    ny,my = Y.shape

    muX = X.mean(0)
    muY = Y.mean(0)

    X0 = X - muX
    Y0 = Y - muY

    ssX = (X0**2.).sum()
    ssY = (Y0**2.).sum()

    
    normX = np.sqrt(ssX)
    normY = np.sqrt(ssY)

    
    X0 /= normX
    Y0 /= normY

    if my < m:
        Y0 = np.concatenate((Y0, np.zeros(n, m-my)),0)

    
    A = np.dot(X0.T, Y0)
    U,s,Vt = np.linalg.svd(A,full_matrices=False)
    V = Vt.T
    T = np.dot(V, U.T)

    if reflection != 'best':

       
        have_reflection = np.linalg.det(T) < 0

        
        if reflection != have_reflection:
            V[:,-1] *= -1
            s[-1] *= -1
            T = np.dot(V, U.T)

    traceTA = s.sum()

    if scaling:

        
        b = traceTA * normX / normY

        
        d = 1 - traceTA**2

        
        Z = normX*traceTA*np.dot(Y0, T) + muX

    else:
        b = 1
        d = 1 + ssY/ssX - 2 * traceTA * normY / normX
        Z = normY*np.dot(Y0, T) + muX

    
    if my < m:
        T = T[:my,:]
    c = muX - b*np.dot(muY, T)

     
    tform = {'rotation':T, 'scale':b, 'translation':c}

    return d, Z, tform
