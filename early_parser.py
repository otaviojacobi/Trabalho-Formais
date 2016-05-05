#-*- coding: utf-8 -*-
from sys import *

def retiraComments(texto):
    '''
    String -> Lista de Strings
    Retira todos os comentários do texto E passa a gramática para uma lista de Strings
    '''
    texto2 = []
    for line in texto:
        texto2.append(line.partition('#')[0].strip())

    return texto2

def achaTermin(lista_text):
    '''
    Lista de Strings -> Lista de Strings OU -1 para erro
    Acha todos os terminais possíveis e coloca eles em uma lista
    '''
    terminais=[]
    if lista_text[0]=="Terminais":
        return lista_text[1].strip(" }{").replace(' ','').split(",")

    else:
        print ("Something went terrebly wrong...")
        return -1
def achaVariav(lista_text):
    '''
    Lista de Strings -> Lista de Strings OU -1 para erro
    acha todas as variáveis possíveis e colca eles em uma lista
    '''
    variaveis=[]
    if lista_text[2]=="Variaveis":
        return  lista_text[3].strip(" }{").replace(' ','').split(",")
    else:
        print ("Something went terrebly wrong...")
        return -1

def achaInicial(lista_text, variav):
    '''
    Lista de Strings -> String OU -1 para erro
    acha a variável inicial
    '''

    if lista_text[4]=="Inicial":
        inicial = lista_text[5].strip(" }{")
        if inicial in variav:
            return inicial
        else:
            print ("Viariavel inicial nao esta nas variaveis")
            return -1
    else:
        print ("Something went terrebly wrong")
        return -1

def achaRegras(lista_text):
    '''
    Lista de Strings -> Hash OU -1 para erro
    Faz um hash (dicionario) associando o lado esquerdo ao direito da regra
    '''

    regras = {}
    if lista_text[6]=="Regras":
        for line in range(7, len(lista_text)):
            lista = lista_text[line].strip(" }{")
            linha = lista.partition(">")
            esquerda, direita = linha[0].strip(' '), linha[-1].strip(' ')
            try:
                if regras[esquerda]==None:
                    regras[esquerda]=[]
            except KeyError:
                regras[esquerda]=[]

            direita = direita.replace(' ','').split(",")
            regras[esquerda].append(direita)

    return regras

def separaGramatica(gramatica):
    '''
    Lista de Strings -> Lista de Strings, Lista de Strings, String
    Função para organizar a separação das variaveis, terminais , var_inicial e regras
    O tratamento de erros é feito nas funções auxiliares
    '''
    terminais = achaTermin(gramatica)
    variaveis = achaVariav(gramatica)
    inicial = achaInicial(gramatica, variaveis)
    regras = achaRegras(gramatica)

    return terminais, variaveis, inicial, regras

def printStuff(printar, var):
    '''
    Lista de Strings OU string OU dicionario e um caracter informando o que printar
    t-> imprime os terminais, v-> imprime as variaveis, g-> a gramatica sem comentarios
    i-> o simbolo inicial, r-> o dicionário das regas
    '''
    if var=="t" or var=="v" or var=="g":
        for elemento in printar:
            print elemento
    elif var=="i":
        print printar
    elif var=="r":
        for line in printar.keys():
            print line + ": "
            for element in printar[line]:
                print element
    else:
        print ("Parametro incorreto")

def main():
    '•'
    if(len(argv)!= 2):
        arquivo = raw_input("Digite o arquivo para ser usado como gramatica: ")
    else:
        script, arquivo = argv
    try:
        gramatica = open(arquivo, "r")
    except IOError:
        print ("Arquivo inexistente. Digite o nome de um arquivo existente.")
        raise SystemExit, 1

    gramatica = retiraComments(gramatica)
    terminais, variaveis, inicial, regras = separaGramatica(gramatica)
    printStuff(regras, "r")

if __name__ == '__main__':
    main()
