from tkinter import *
from tkinter import ttk
import os
from PIL import ImageTk, Image
import execute
import functions
import cv2
import operations
import objeto
import sys

class PdiApp:
    def __init__(self, Pdi):
        self.atual = 0
        self.path = "images/"
        self.path_lines = "lines_images/"
        self.path_texture = "images_texture/"
        self.path_proc = "proc_image/"
        self.path_proc_g = "proc_g_image/"
        self.first_amostra = False
        self.images_lines = []
        self.formas = []
        self.texts = []
        self.proc_texts = []
        self.proc_g_texts = []
        self.forma_align = []
        self.forma_align_generalizada = []
        self.amostra_center = []
        self.euclidian_flag = False
        self.proc_flag = False
        self.proc_g_flag = False
        self.pontos_flag = False
        self.amostras_flag = False
        self.marcador = ""
        self.e1 = ""
        self.target_proc = 0
        self.proc_distancia = 0
        self.magnitude = 0
        self.norm_mean = []
        self.norm_estimate = []
        self.autovalores = []
        self.autovetores = []
        self.forma_corrigida = []
        self.form_autovetores = []
        self.form_autovalores = []
        self.formas_alinhadas = []

        menubar = Menu(Pdi)
        Pdi.config(menu=menubar)
        Pdi.title("PDI - Interface Gráfica - ASM")
        Pdi.geometry('1280x720')

        menu = Menu(menubar)
        menu2 = Menu(menubar)
        menu3 = Menu(menubar)

        menubar.add_cascade(label='Arquivo', menu=menu)
        menubar.add_cascade(label='Operações', menu=menu2)
        menubar.add_cascade(label='Busca', menu=menu3)

        #Funções
        def Sair():
            Pdi.destroy()
            sys.exit()
            
        def line_images():
            i=0
            for forma in self.formas:
                self.images_lines.append("image" + str(i) + ".jpg")
                i += 1
        
        def next_forma():
            if self.atual < (len(self.formas)-1):
                self.atual += 1
                self.canvas.delete(self.canvas_image)
                if self.euclidian_flag:
                    show_img(0)
                    show_euclidian()
                elif self.pontos_flag:
                    show_img(0)
                    show_pontos()
                elif self.amostras_flag:
                    show_img_amostras()
                    show_amostras()
                else:
                    show_img(1)

        def back_forma():
            if self.atual > 0:
                self.atual -= 1
                self.canvas.delete(self.canvas_image)
                if self.euclidian_flag:
                    show_img(0)
                    show_euclidian()
                elif self.pontos_flag:
                    show_img(0)
                    show_pontos()
                elif self.amostras_flag:
                    show_img_amostras()
                    show_amostras()
                else:
                    show_img(1)


        def buttons():
            self.next_button = Button(Pdi, text = "Próxima", command = next_forma, anchor = W, justify=CENTER, 
            font="Arial 10 bold")
            self.back_button = Button(Pdi, text = "Anterior", command = back_forma, anchor = W, justify=CENTER, 
            font="Arial 10 bold")
            self.next_button.configure(height=2,width = 10, activebackground = "grey", relief = RAISED)
            self.back_button.configure(height=2,width = 10, activebackground = "grey", relief = RAISED)
            self.back_window = self.canvas.create_window(650, 600, anchor=NW, window=self.back_button)
            self.next_window = self.canvas.create_window(850, 600, anchor=NW, window=self.next_button)
        
        def show_img(i):
            self.canvas.delete(self.marcador)
            img = ImageTk.PhotoImage(Image.open(self.path_lines + self.images_lines[self.atual]))
            self.label = Label(image=img)
            self.label.image = img
            self.canvas_image = self.canvas.create_image(80, 0, anchor=NW, image=self.label.image)
            self.marcador = self.canvas.create_text(300, 655,fill="black",font="Arial 15 bold",
                        text=str(self.atual+1)+ "/" + str(len(self.formas)), anchor=W)
            if i == 1:
                buttons()

        def show_img_amostras():
            self.canvas.delete(self.marcador)
            img = ImageTk.PhotoImage(Image.open(self.path_texture + self.images_lines[self.atual]))
            self.label = Label(image=img)
            self.label.image = img
            self.canvas_image = self.canvas.create_image(80, 0, anchor=NW, image=self.label.image)
            self.marcador = self.canvas.create_text(300, 655,fill="black",font="Arial 15 bold",
                        text=str(self.atual+1)+ "/" + str(len(self.formas)), anchor=W)
            
            

        def Plot():
            self.formas = execute.Plotar(self.path)
            line_images()
            self.canvas = Canvas(Pdi, width = 1366, height = 800, background="white")  
            #canvas.grid(row = 0, column = 2)
            self.canvas.pack()
            show_img(1)
            

        def show_euclidian():
            self.pontos_flag = False
            self.amostras_flag = False
            for text in self.texts:
                self.canvas.delete(text)
            self.label.text = "Distância Euclidiana entre os pontos:"
            i=0
            k = 60
            self.texts.append(self.canvas.create_text(650, 40,fill="black",font="Arial 15 bold",
                        text=self.label.text, anchor=W))
            for distancia in self.formas[self.atual].euclidiana:
                k += 30
                self.texts.append(self.canvas.create_text(650, k,fill="black",font="Arial 12 bold",
                        text="Distância ponto " + str(i) + " e " + str(i+1) + ": " + str(distancia), anchor=W))
                i+=1
            self.euclidian_flag = True
        
        def show_pontos():
            self.euclidian_flag = False
            self.amostras_flag = False
            for text in self.texts:
                self.canvas.delete(text)
            self.label.text = "Coordenadas dos pontos da face(x,y):"
            i=0
            k = 60
            self.texts.append(self.canvas.create_text(650, 40,fill="black",font="Arial 15 bold",
                        text=self.label.text, anchor=W))
            for ponto in self.formas[self.atual].pontos:
                k += 30
                self.texts.append(self.canvas.create_text(650, k,fill="black",font="Arial 12 bold",
                        text="Ponto " + str(i) +  ": " + str(ponto), anchor=W))
                i+=1
            self.pontos_flag = True

        def show_amostras():
            self.pontos_flag = False
            self.euclidian_flag = False
            for text in self.texts:
                self.canvas.delete(text)
            self.label.text = "Amostras de textura dos pontos(x,y):"
            i=0
            k = 60
            self.texts.append(self.canvas.create_text(600, 40,fill="black",font="Arial 15 bold",
                        text=self.label.text, anchor=W))
            for amostra in self.formas[self.atual].amostra:
                k += 30
                self.texts.append(self.canvas.create_text(600, k,fill="black",font="Arial 10 bold",
                        text="Ponto " + str(i) +  ": " + str(amostra), anchor=W))
                i+=1
            self.amostras_flag = True
            

        def do_proc():
            if self.e1.get() != "":
                self.target_proc = int(self.e1.get())
                #x2 = self.e2.get()
                if((self.target_proc > 0) and (self.target_proc <= len(self.formas)) and (self.target_proc != (self.atual+1))):
                    self.nw.destroy()
                    formas_aux = self.formas
                    [distancia, forma_align] = execute.plot_procrustes(formas_aux, self.path_lines, self.atual, self.target_proc-1)
                    openNewImage_proc(distancia, forma_align)

                else:
                    Label(self.nw,  text ="Valor Inválido! Tente novamente").pack()

        
        def openNewImage_proc(distancia, alinhado): 
            self.nw = Toplevel(Pdi) 
            self.nw.title("PDI - Distância Procrustes")  
            self.nw.geometry("1200x700") 
            #text=IntVar()
            self.canvas_proc = Canvas(self.nw, width = 1366, height = 800, background="white")  
            self.canvas_proc.pack()
            img = ImageTk.PhotoImage(Image.open(self.path_proc + "image_procrustes.jpg"))
            label = Label(image=img)
            label.image = img
            self.canvas_image_proc = self.canvas_proc.create_image(80, 0, anchor=NW, image=label.image)
            self.proc_text = self.canvas_proc.create_text(650, 40,fill="black",font="Arial 15 bold",
                        text="Procrustes sobre a imagem " + str(self.atual+1) + " em relação a imagem " + str(self.target_proc) + ":", anchor=W)
            self.proc_text2 = self.canvas_proc.create_text(650, 70,fill="black",font="Arial 12 bold",
                        text="Distância: " + str(distancia), anchor=W)
            self.proc_text3 = self.canvas_proc.create_text(650, 100,fill="black",font="Arial 12 bold",
                        text="Forma alinhada: ", anchor=W)
            i=0
            k=90
            for ponto in alinhado:
                k += 30
                self.proc_texts.append(self.canvas_proc.create_text(650, k,fill="black",font="Arial 12 bold",
                        text="Ponto " + str(i) +  ": " + str(ponto), anchor=W))
                i+=1
            self.proc_flag = True

        def openNewImage_proc_generalizada(alinhado): 
            self.nw_g = Toplevel(Pdi) 
            self.nw_g.title("PDI - Distância Procrustes Generalizada")  
            self.nw_g.geometry("1200x700") 
            #text=IntVar()
            self.canvas_proc_g = Canvas(self.nw_g, width = 1366, height = 800, background="white")  
            self.canvas_proc_g.pack()
            img = ImageTk.PhotoImage(Image.open(self.path_proc_g + "image_procrustes_g.jpg"))
            label = Label(image=img)
            label.image = img
            self.canvas_image_proc_g = self.canvas_proc_g.create_image(80, 0, anchor=NW, image=label.image)
            self.proc_g_text_g = self.canvas_proc_g.create_text(650, 40,fill="black",font="Arial 15 bold",
                        text="Procrustes Generalizado - Forma média", anchor=W)

            self.proc_g_text2 = self.canvas_proc_g.create_text(650, 70,fill="black",font="Arial 12 bold",
                        text="Forma alinhada: ", anchor=W)
            i=0
            k=90
            for ponto in alinhado:
                k += 30
                self.proc_g_texts.append(self.canvas_proc_g.create_text(650, k,fill="black",font="Arial 12 bold",
                        text="Ponto " + str(i) +  ": " + str(ponto), anchor=W))
                i+=1
            self.proc_g_flag = True
        

        def openNewWindow_proc():
            self.nw = Toplevel(Pdi) 
            self.nw.title("Distância Procrustes")  
            self.nw.geometry("400x100") 
            #text=IntVar()
            Label(self.nw,  text ="Digite o número referente da imagem a ser comparada com a atual:").pack()
            self.e1 = Entry(self.nw)
            self.e1.pack()
            button1 = Button(self.nw, text='Calcular a distância', command=do_proc)
            button1.pack()
        

        def show_procrustes_generalized():
            forma_aux = objeto.Forma()
            forma_aux = self.formas
            #print("\n\nANTES")
            #print(self.formas[0].pontos)
            self.formas_alinhadas, self.forma_align_generalizada, self.norm_estimate, self.norm_mean, self.magnitude, self.form_autovetores, self.form_autovalores = execute.plot_procrustes_generalizada(forma_aux, self.path_lines)
            self.amostra_center = execute.amostra_forma(self.forma_align_generalizada)
            #print("\n\nDEPOIS")
            #print(self.formas[0].pontos)
            openNewImage_proc_generalizada(self.forma_align_generalizada)

        def show_amostras_textura():
            if not self.first_amostra:
                #MUDAR
                self.tw = Toplevel(Pdi) 
                self.tw.title("Amostras de textura")  
                self.tw.geometry("400x100") 
                Label(self.tw,  text ="Digite o valor do parâmetro da textura:").pack()
                self.e2 = Entry(self.tw)
                self.e2.pack()
                button2 = Button(self.tw, text='Gerar amostras', command=do_texturas)
                button2.pack()
            else:
                show_amostras()
                show_img_amostras()

        def do_texturas():
            if self.e2.get() != "":
                self.autovalores, self.autovetores = execute.plot_amostras(self.formas, self.path_lines, int(self.e2.get()))
                self.tw.destroy()
                self.first_amostra = True
                show_amostras()
                show_img_amostras()
            else:
                Label(self.tw,  text ="Valor Inválido! Tente novamente").pack()


        def show_procrustes():
            openNewWindow_proc()
        
        def show_forma_ajustada():
            execute.ajuste_de_forma(self.norm_estimate, self.norm_mean, self.magnitude, self.formas, self.form_autovalores, self.form_autovetores)
            
            
        menu.add_command(label='Ler arquivo', command=Plot)
        menu.add_command(label='Sair', command=Sair)
        menu2.add_command(label='Mostrar coordenadas', command=show_pontos)
        menu2.add_command(label='Distância Euclidiana', command=show_euclidian)
        menu2.add_command(label='Distância Procrustes', command=show_procrustes)
        menu2.add_command(label='Distância Procrustes Generalizada', command=show_procrustes_generalized)
        menu2.add_command(label='Gerar Amostras de Textura', command=show_amostras_textura)
        menu3.add_command(label='Ajuste de forma', command=show_forma_ajustada)
        

Pdi = Tk()
PdiApp(Pdi)
Pdi.mainloop()