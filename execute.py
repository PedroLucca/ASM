import functions
import cv2
import operations

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
        cv2.imwrite("C:/Users/Pedro/Documents/PythonPdi/ASM/lines_images/image" + str(i) + ".jpg", image)
        i += 1
    return imagens
