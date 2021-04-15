import pandas
import numpy as np
import objeto
import operations
import cv2
import matplotlib.pyplot as plt
from tkinter import filedialog

def lerArq():
    local = filedialog.askopenfilename()
    df = pandas.read_csv(local,';')
    array = np.array(df)
    return array

def array_formas(array):
    k = 0
    imagens = []
    while k < (len(array)):
        forma = objeto.Forma()
        forma.setDados(array[k])
        imagens.append(forma)
        k += 1
    return imagens

def calc_distance(pontos, forma):
    contaux = 0
    i = 0
    while i < len(pontos):
        if(contaux == 1):
            forma.euclidiana.append(operations.dist_euclidiana(pontos[i-1], pontos[i]))
            if i != (len(pontos)-1):
                forma.euclidiana.append(operations.dist_euclidiana(pontos[i+1], pontos[i]))
            i += 1
            contaux = 0
        else:
            contaux = 1
            i += 1

def plot_lines(img, path):
    contaux = 0
    i = 0
    image = cv2.imread(path + img.image) 
    while i < len(img.pontos):
        if(contaux == 1):
            image = add_line(image, i, img)
            i += 1
            contaux = 0
        else:
            contaux = 1
            i += 1
    return image

def plot_lines_align(img, path):
    contaux = 0
    i = 0
    image = cv2.imread(path + img.image) 
    #print(path + img.image)
    while i < len(img.pontos):
        if(contaux == 1):
            image = add_line_align(image, i, img)
            i += 1
            contaux = 0
        else:
            contaux = 1
            i += 1
    return image

def plot_lines_amostras(img, name ,path):
    contaux = 0
    i = 0
    image = cv2.imread(path + name) 
    #print(path + img.image)
    image = add_line_amostra(image, img) 
    return image

def add_line(image, i, img):
    imageaux = cv2.line(image, tuple(img.pontos[i-1]), tuple(img.pontos[i]), (0, 0, 255), 2)
    if(i!=(len(img.pontos)-1)):
        imageaux = cv2.line(imageaux, tuple(img.pontos[i]), tuple(img.pontos[i + 1]), (0, 0, 255), 2)
    elif(i == (len(img.pontos)-1)):
        imageaux = cv2.line(imageaux, tuple(img.pontos[i]), tuple(img.pontos[0]), (0, 0, 255), 2)
    return imageaux

def add_line_align(image, i, img):
    imageaux = cv2.line(image, tuple(img.pontos[i-1]), tuple(img.pontos[i]), (255, 0, 0), 2)
    if(i!=(len(img.pontos)-1)):
        imageaux = cv2.line(imageaux, tuple(img.pontos[i]), tuple(img.pontos[i + 1]), (255, 0, 0), 2)
    elif(i == (len(img.pontos)-1)):
        imageaux = cv2.line(imageaux, tuple(img.pontos[i]), tuple(img.pontos[0]), (255, 0, 0), 2)
    return imageaux

def add_line_amostra(image, forma):
    for amostra in forma.amostra:
        imageaux = cv2.line(image, tuple(amostra[0]), tuple(amostra[-1]), (0, 255, 0), 1)
    return imageaux
