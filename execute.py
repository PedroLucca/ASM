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
    imagens_aux = imagens
    #print(imagens[0].pontos)
    x1 = np.array(imagens_aux[i1].pontos)
    x2 = np.array(imagens_aux[i2].pontos)
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
    #print(path)
    image = functions.plot_lines_align(proc, path)
    cv2.imwrite("proc_image/image_procrustes.jpg", image)
    return d, procrustesx

def plot_procrustes_generalizada(imagens,path):
    proc_aux = objeto.Forma()
    imagens_g = imagens
    #print("\n\nANTES")
    #print(imagens[0].pontos)
    alinhados, mean, m, magnitude = operations.procrustes_generalizada(imagens_g)
    #print("\n\nDEPOIS")
    #print(imagens[0].pontos)
    #print(Z)
    #m = (m*magnitude)#Multiplicando pelo fator de escala
    #print("\n")
    #print(magnitude)
    #print("\n")
    procrustes_g = []
    dadoaux = [0,0]
    for ponto in mean:
        dadoaux[0] = round(ponto[0])
        dadoaux[1] = round(ponto[1])
        procrustes_g.append(list(dadoaux))
    #print(procrustesx)
    mean = mean/magnitude
    
    proc_aux.image = "image0.jpg"
    proc_aux.pontos = procrustes_g
    #print(path)
    image = functions.plot_lines_align(proc_aux, path)
    cv2.imwrite("proc_g_image/image_procrustes_g.jpg", image)
    return alinhados, procrustes_g, mean, m, magnitude

def plot_amostras(formas, path, d):
    i = 0
    autovalores, autovetores = operations.amostras_textura(formas, d)
    for forma in formas:
        nome = "image" + str(i) + ".jpg"
        image = functions.plot_lines_amostras(forma, nome , path)
        cv2.imwrite("images_texture/image" + str(i) + ".jpg", image)
        i += 1

    return autovalores, autovetores


def salvar_forma_media(magnitude, m, formas):
    path = "images/"
    proc_aux = objeto.Forma()
    #print("\n\nANTES")
    #print(imagens[0].pontos)
    #alinhados, m, magnitude = operations.procrustes_generalizada(imagens_g)
    #print("\n\nDEPOIS")
    #print(imagens[0].pontos)
    #print(Z)
    m = (m*magnitude)#Multiplicando pelo fator de escala
    #print("\n")
    #print(magnitude)
    #print("\n")
    procrustes_g = []
    dadoaux = [0,0]
    for ponto in m:
        dadoaux[0] = round(ponto[0])
        dadoaux[1] = round(ponto[1])
        procrustes_g.append(list(dadoaux))
    #print(procrustesx)
    
    proc_aux.image = formas[0].image
    proc_aux.pontos = procrustes_g
    #print(path)
    image = functions.plot_lines(proc_aux, path)
    cv2.imwrite("forma_media/mean_shape.jpg", image)

def amostra_forma(m):
        amostra = operations.amostra_forma(m, 10)
        return amostra

def ajuste_de_forma(estimativa, forma_media, magnitude, formas, autovalores, autovetores):
    operations.ajuste_forma(estimativa, forma_media, magnitude, formas, autovalores, autovetores)