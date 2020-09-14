import cv2
from PIL import Image
from sklearn.preprocessing import normalize
from tkinter import filedialog
import numpy as np
import math
import scipy.spatial as ss
import statistics

#s1 e st seriam arrays com os pontos da forma, o peso seria um array com os pesos gerados na outra função
def alinhamento(s1,st,peso):
    num = (len(s1)/2)
    (s,r,tx,ty) = trans_similaridade(s1,st,peso)
    #print((math.cos(r)))
    new = []
    for i in st:
        new.append(0)
    k = 0
    while k < num:
        new[2*k]   = ((st[2*k]*(math.cos(r)) - st[2*k+1]*(math.sin(r)))*s) + tx
        new[2*k+1] = ((st[2*k]*(math.sin(r)) + st[2*k+1]*(math.cos(r)))*s) + ty
        k += 1
    return new

def trans_similaridade(s1,st,peso):
    num = (len(s1)/2)
    X1 = 0.0 
    Y1 = 0.0
    X2 = 0.0
    Y2 = 0.0
    W = 0.0
    Z = 0.0
    C1 = 0.0
    C2 = 0.0
    k=0

    while k < num:
        X1  += peso[k] * s1[2*k]
        Y1  += peso[k] * s1[2*k + 1]
        X2  += peso[k] * st[2*k]
        Y2  += peso[k] * st[2*k + 1]
        Z   += peso[k] * (st[2*k] * st[2*k] + st[2*k + 1] * st[2*k + 1])
        W   += peso[k]
        C1  += peso[k] * (s1[2*k] * st[2*k] + s1[2*k + 1] * st[2*k + 1])
        C2  += peso[k] * (s1[2*k + 1] * st[2*k] - s1[2*k] * st[2*k + 1])
        k += 1
      
    K0 = X2 * X2 + Y2 * Y2
    K1 = -Y2 * W
    K2 = X2 * W
    K3 = X2 * Y1 - X1 * Y2
    K4 = -X2 * Z
    K5 = X2 * Y2
    K6 = Y2*Y2 - W*Z
    K7 = C1*Y2 - Y1*Z
        
    ty = (X2 * C2 - Y1 * Z + Y2 * C1)/(X2 * X2 - W * Z + Y2 * Y2)
    tx = (K0*K7 - K3*K4 - ty * (K0 * K6 - K2 * K4))/(K0 * K5 - K1 * K4)

    ay = (K3 - tx * K1 - ty * K2)/K0
    ax = (X1 + ay*Y2 - tx*W)/X2

    the = math.atan2(ay,ax)
    s = ax/math.cos(the)
    return (s,the,tx,ty)

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
    i = 0
    k= 1
    media = []
    teste = []
    while i < (len(formas[0].pontos)):
        soma = formas[0].pontos[i]
        while k < (len(formas)):
            soma += formas[k].pontos[i]
            k += 1
            if k == (len(formas)-1):
                x = np.array(soma)
                x = x/len(formas)
                teste.append(x)
                media.append(soma)
                
        i += 1
        k=1
    media = np.array(media)
    media = media/(len(formas))
    print(teste)
    print(media)
    return media


def dist_euclidiana(v1, v2):
    v1, v2 = np.array(v1), np.array(v2)
    distance = math.sqrt(((v2[0] - v1[0]) * (v2[0] - v1[0])) + ((v2[1] - v1[1]) * (v2[1] - v1[1])))
    return distance

def normalizar(alvo):
    m = np.array(alvo/np.linalg.norm(alvo, ord=np.inf, axis=0, keepdims=True))
    return m

def procrustes_generalizada(formas):
    alvo = np.array(formas[0].pontos)#Fazer uma copia de uma forma aleatória
    m = normalizar(alvo)#Atribuir à forma média m o alvo normalizado
    formasaux = formas#Guardar o valor atual de F
    for forma in formas:
        forma.pontos = np.array(forma.pontos)
        [d, Z, transform] = dist_procrustes(m,forma.pontos)#Alinhar cada forma da lista F com a média m
        forma.pontos = Z
    m = np.array(calcular_forma_media(formas))#Atualizar a forma média m
    [d, Z, transform] = dist_procrustes(alvo, m)#Alinhar forma média m com o alvo
    m = normalizar(Z)#Normalizar a forma média m
    return formas, m #Lista de formas F alinhadas e forma média m
    
    


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
