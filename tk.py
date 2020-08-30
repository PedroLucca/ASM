from tkinter import *
from PIL import ImageTk, Image
import execute
import functions
import cv2
import operations

class PdiApp:
    def __init__(self, Pdi):
        self.atual = 0
        self.path = "C:/Users/Pedro/Documents/PythonPdi/ASM/images/"
        self.path_lines = "C:/Users/Pedro/Documents/PythonPdi/ASM/lines_images/"
        self.images_lines = []
        self.formas = []
        self.texts = []
        self.euclidian_flag = False
        self.pontos_flag = False

        menubar = Menu(Pdi)
        Pdi.config(menu=menubar)
        Pdi.title("PDI - Interface Gráfica - ASM")
        Pdi.geometry('1280x720')

        menu = Menu(menubar)
        menu2 = Menu(menubar)

        menubar.add_cascade(label='Arquivo', menu=menu)
        menubar.add_cascade(label='Operações', menu=menu2)

        #Funções
        def Sair():
            Pdi.destroy()
        
        def line_images():
            i=0
            for forma in self.formas:
                self.images_lines.append("image" + str(i) + ".jpg")
                i += 1
        
        def next_forma():
            if self.atual < (len(self.formas)-1):
                self.atual += 1
                self.canvas.delete(self.canvas_image)
                show_img(0)
                if self.euclidian_flag:
                    show_euclidian()
                elif self.pontos_flag:
                    show_pontos()

        def back_forma():
            if self.atual > 0:
                self.atual -= 1
                self.canvas.delete(self.canvas_image)
                show_img(0)
                if self.euclidian_flag:
                    show_euclidian()
                elif self.pontos_flag:
                    show_pontos()


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
            img = ImageTk.PhotoImage(Image.open(self.path_lines + self.images_lines[self.atual]))
            self.label = Label(image=img)
            self.label.image = img
            self.canvas_image = self.canvas.create_image(80, 0, anchor=NW, image=self.label.image)
            if i == 1:
                buttons()
            

        def Plot():
            self.formas = execute.Plotar(self.path)
            line_images()
            self.canvas = Canvas(Pdi, width = 1366, height = 700, background="white")  
            #canvas.grid(row = 0, column = 2)
            self.canvas.pack()
            show_img(1)
            

        def show_euclidian():
            self.pontos_flag = False
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
        

        menu.add_command(label='Ler arquivo', command=Plot)
        menu.add_command(label='Sair', command=Sair)
        menu2.add_command(label='Mostrar coordenadas', command=show_pontos)
        menu2.add_command(label='Distância Euclidiana', command=show_euclidian)
        

Pdi = Tk()
PdiApp(Pdi)
Pdi.mainloop()