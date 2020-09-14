import functions
import cv2
import operations
import numpy as np
import objeto
import math

#arquivo de testes das funções
def Plotar(path):
    i = 0
    array = functions.lerArq()
    imagens = functions.array_formas(array)
    #print(imagens[1].forma)
    # #print(operations.alinhamento(imagens[0].forma,imagens[1].forma,imagens[0].peso))
    for forma in imagens:
        functions.calc_distance(forma.pontos, forma)
        image = functions.plot_lines(forma, path)
        cv2.imwrite("lines_images/image" + str(i) + ".jpg", image)
        i += 1
    return imagens

def plot_procrustes(imagens,path,i1,i2):
    proc = objeto.Forma()
    x1 = np.array(imagens[i1].pontos)
    x2 = np.array(imagens[i2].pontos)
    [d, Z, transform] = operations.dist_procrustes(x1,x2)
    #print(Z)
    procrustesx = []
    dadoaux = [0,0]
    for ponto in Z:
        dadoaux[0] = round(ponto[0])
        dadoaux[1] = round(ponto[1])
        procrustesx.append(list(dadoaux))
    #print(procrustesx)
    proc.image = "image"+ str(i1) +".jpg"
    proc.pontos = procrustesx
    image = functions.plot_lines_align(proc, path)
    cv2.imwrite("C:/Users/Pedro/Documents/PythonPdi/ASM/proc_image/image_procrustes.jpg", image)
    return d, procrustesx
