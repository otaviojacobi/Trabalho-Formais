#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter
import Image, ImageTk # sudo apt-get install python-pil.imagetk
from tkFileDialog import askopenfilename
from parser.early_parser import *

class app_tk(Tkinter.Tk):
    # Construtor para janela principal do app
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent # mantem registro de quem eh a janela mae
        self.initialize() # metodo que cria os artificios da interface

    def initialize(self):
        self.grid() # define como posicionar os artificios: grid(row, column) ou coordenada (x,y)

        # metodo entry eh a barra de entrada de texto
        self.entryVariable = Tkinter.StringVar() #define uma variavel para salvar o texto escrito 
        self.entry = Tkinter.Entry(self, textvariable=self.entryVariable) #diz para salvar o texto na variavel
        self.entry.grid(column=0, row=0, sticky='EW') #posicao da barra
        self.entryVariable.set('Digite a sentenca aqui') #inicia com um texto padrao

        # chama metodo Button para cada um dos botoes
            # Botao de sair chama o metodo Quit
        buttonQuit = Tkinter.Button(self, text=u'Sair', command=self.Quit)
        buttonQuit.grid(column=1, row=3)
    
            # Botao de Parse chama o metodo Parse
        buttonParse = Tkinter.Button(self, text=u'Fazer o parsing da sentenca', command=self.Parse)
        buttonParse.grid(column=1, row=0)

            # Botao Rand chama o metodo Rand
        buttonRand = Tkinter.Button(self, text=u'Gerar sentenca aleatoria', command=self.Rand)
        buttonRand.grid(column=1, row=1)
        
        # metodo label eh a saida de texto da interface
        self.labelVariable = Tkinter.StringVar() # define a variavel onde salvar o texto que se deseja escrever na saida de texto
        label = Tkinter.Label(self, textvariable=self.labelVariable, anchor='w', fg='red', bg='white') # configura barra com a variavel, ancora da posicao (w=west=esquerda), fg e bg eh a cor do texto
        label.grid(column=0, row=5, columnspan=2, sticky='EW')

        # algumas opcoes do grid
        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, False) #a janela nao modifica o tamanho na coordenada y
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set() # poe o foco sempre na barra de entrada de texto
        self.entry.selection_range(0, Tkinter.END) # e sempre seleciona o que tiver escrito nela para facilitar a escrita de novas frase
        
    def Parse(self):
        gramatica = open(askopenfilename(), 'r') #abre o navegador de arquivos
        gramatica = retiraComments(gramatica)
        terminais, variaveis, inicial, regras = separaGramatica(gramatica)

        frase = self.entryVariable.get() #pega frase da entrada de texto
        pertence, D, arv_bonita = parse(frase, inicial, terminais, regras, variaveis)
        saida = open('saida.txt', 'w')
        if pertence:
            save_D(D, saida)
            salva_arvore(arv_bonita)
            self.mostraArv()
            self.labelVariable.set('SENTENCA PERTENCE A GRAMATICA') #escreve na saida de texto
        elif D!=-1:
            save_D(D, saida)
            self.labelVariable.set('SENTENCA NAO PERTENCE A GRAMATICA')
        else:
            saida.write('Nao pertence !')
            self.labelVariable.set('SENTENCA NAO PERTENCE A GRAMATICA')
        saida.close()
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def Rand(self):
        gramatica = open(askopenfilename(), 'r') #abre o navegador de arquivos
        gramatica = retiraComments(gramatica)
        terminais, variaveis, inicial, regras = separaGramatica(gramatica) 
        
        frase = gera_frase(regras, inicial, variaveis, terminais)
        pertence, D, arv_bonita = parse(frase, inicial, terminais, regras, variaveis)
        saida = open('saida.txt', 'w')
        if pertence:
            save_D(D, saida)
            salva_arvore(arv_bonita)
            self.mostraArv()
            self.labelVariable.set('SENTENCA PERTENCE A GRAMATICA') #escreve na saida de texto
        elif D!=-1:
            save_D(D, saida)
            self.labelVariable.set('SENTENCA NAO PERTENCE A GRAMATICA')
        else:
            saida.write('Nao pertence !')
            self.labelVariable.set('SENTENCA NAO PERTENCE A GRAMATICA')
        saida.close()
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def Quit(self):
        exit()

    # metodo mostra arvore gera uma janela filha onde mostra a imagem da arvore de derivacao
    def mostraArv(self):
        im = Image.open('Derivation_Tree.png') #abre arquivo
        tkimage = ImageTk.PhotoImage(im)
        win = Tkinter.Toplevel() #TopLevel cria janelas filhas
        win.title('Arvore de Derivacao')
        label = Tkinter.Label(win, image=tkimage) #escreve na janela a label com a imgem
        label.image = tkimage #mantem registro da imagem MALDITA TKINTER QUE NAO MOSTRA IMAGEM SEM ISSO >>NAO MEXER<< 
        label.pack()

#funcao main soh contem o loop da janela principal 
if __name__ == '__main__':
    app = app_tk(None)
    app.title('Early Parser')
    app.mainloop()
