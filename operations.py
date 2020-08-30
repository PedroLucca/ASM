import cv2
from PIL import Image
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
    variance = statistics.variance(sum, div)#falta entender
    weights = []
    #for i in range(0, variance.height):#falta entender
       # weights.append(1.0/variance.lineSum(line: i)!)
    #self.
    return weights


def dist_euclidiana(v1, v2):
    v1, v2 = np.array(v1), np.array(v2)
    distance = math.sqrt(((v2[0] - v1[0]) * (v2[0] - v1[0])) + ((v2[1] - v1[1]) * (v2[1] - v1[1])))
    return distance

def dist_procrustes(v1,v2):
    d = ss.procrustes(v2,v1)[-1]
    print(d)
    return d
