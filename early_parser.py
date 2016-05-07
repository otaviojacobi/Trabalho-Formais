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

# ERRADO O D0 NÃO DEVE SER CRIADO ASSIM !!!!!!!
# def criaD0(regras):
#     '''
#     Dicionario com as regras -> Dicionario com as regras iniciais (conjunto D0)
#     '''
#     for lista in regras.keys():
#         for elemento in regras[lista]:
#             elemento.insert(0, '@')
#             elemento.append('/0')
#
#     return regras
# ERRADO

def movePontoColoca(lista_frase):
    '''
    Lista de Strings -> Lista De Strings
    Recebe uma string equivalente a uma das linhas de uma das etapas de derivação
    e move o ponto de marcação uma posição para a direita
    '''
    if '@' in lista_frase:
        lista_frase='&'.join(lista_frase)
        esquerda, ponto, direita =lista_frase.partition('@')

        esquerda = esquerda.strip('&').split('&')
        direita = direita.strip('&').split('&')


        direita.insert(1,'@')

        lista_frase = esquerda+direita

        if lista_frase[0]=='':
            lista_frase=lista_frase[1:]
        if lista_frase[-2]=='':
            save=lista_frase[-1]
            lista_frase=lista_frase[0:-2]
            lista_frase.append(save)
    else:
        lista_frase.insert(0, '@')

    return lista_frase

def aposPonto(lista_frase):
    '''
    Lista de Strings -> String
    Retorna o elemento (variavel ou terminal) imediatamente após o ponto
    '''

    for elemento in range(len(lista_frase)):
        if lista_frase[elemento]=='@' and elemento!=len(lista_frase)-1:
            retorno = lista_frase[elemento+1]
        elif elemento==len(lista_frase)-1:
            retorno=None

    if retorno==None:
        print "NAO HA NADA APÓS O PONTO. Ver ERRO."

    return retorno

def criaDNdagram(string_pux, n):
    '''
    '''


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
    #printstuff(gramatica, "g")
    terminais, variaveis, inicial, regras = separaGramatica(gramatica)
    #printstuff(terminais, "t")
    #printstuff(variaveis, "v")
    #printStuff(inicial, "i")
    #printStuff(regras, "r")
    frase = raw_input("Digite a frase a ser parseada: ")
    print aposPonto(movePontoColoca(frase.split(' ')))


if __name__ == '__main__':
    main()
