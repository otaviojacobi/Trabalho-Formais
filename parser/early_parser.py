#-*- coding: utf-8 -*-
from sys import *
from copy import deepcopy
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import re
from pyvirtualdisplay import Display

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
        return lista_text[1].strip(" }{;").replace(' ','').split(",")

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
        return  lista_text[3].strip(" }{;").replace(' ','').split(",")
    else:
        print ("Something went terrebly wrong...")
        return -1

def achaInicial(lista_text, variav):
    '''
    Lista de Strings -> String OU -1 para erro
    acha a variável inicial
    '''
    if lista_text[4]=="Inicial":
        inicial = lista_text[5].strip(" }{;")
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
            lista = lista_text[line].strip(" }{;")
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

def movePonto(lista_frase):
    '''
    Lista de Strings -> Lista De Strings
    Recebe uma string equivalente a uma das linhas de uma das etapas de derivação
    e move o ponto de marcação uma posição para a direita
    '''

    var_aux=aposPonto(lista_frase)
    if var_aux[0]=='/':
        return lista_frase

    else:
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
            print "NAO TEM PONTO PROVAVEL ERRO"
            lista_frase.insert(0, '@')

        return lista_frase

def aposPonto(lista_frase):
    '''
    Lista de Strings -> String
    Retorna o elemento (variavel ou terminal) imediatamente após o ponto
    '''
    if lista_frase[0]=='@':
        return lista_frase[1]
    else:
        for elemento in range(len(lista_frase)):
            if lista_frase[elemento]=='@':
                return lista_frase[elemento+1]

def criaDNdagram(string_pux, n):
    '''
    Lista de Strings -> Lista de Strings
    Retorna a lista com as strings com o ponto no inicio e '/n' no final
    '''
    fim = '/'+str(n)
    string_pux.insert(0,'@')
    string_pux.append(fim)

    return string_pux

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



def criaD0(regras, inicial, terminais):
    '''
    Hash, String, Lista de Strings -> Hash
    Função que inicializa o parsing criando o conjunto D0 a partir da gramática e siḿbolo inicial
    Provaveis problemas: Se um terminal for igual a variavel (considerando caps), vai dar errado.
    '''
    D0 = {}       #Regra que será o D[0] no main parser
    n_lista =[]   #lista temporaria
    k=[]          #lista de terminais (para verificar condição de parada)
    flag = True   #flag para dizer quando para a execução

    instanciado=deepcopy(regras) #copia as regras para um auxiliar (para nao fazer besteiras com os ponteiros)

    for lista in instanciado[inicial]:         #para cada lista apontada pelo elemento inicial
        n_lista.append(criaDNdagram(lista, 0)) #cria a primeira lista inserindo o ponto e o \0 no final

    D0[inicial]=n_lista #coloca ela no "hash" para o elemento inicial

    while flag: #inicia a iteração
        teste=deepcopy(k) #copia k para uma variavel auxiliar
        save=deepcopy(n_lista) #copia n_lista para uma variavel auxiliar
        n_lista=[] #reinicializa a lista para o inicio da iteração
        for lista2 in save: #para cada lista na lista de lista anterior
            if aposPonto(lista2) not in k: #se o elemento após o ponto não estiver em k
                k.append(aposPonto(lista2)) #adiciona ele em k

        for elemento in teste: #para todos os elementos no k anterior (armazenado em teste)
            if elemento not in D0.keys(): #se o elemento não for uma das já chaves de D0
                D0[elemento]=[] #cria o elemento do hash

            for lista in instanciado[elemento]: #itera para todos os elementos da gramatica
                if lista[0]!='@':               #se o elemento não começar por '@' (erro bizarro com ponteiros, corrigi dessa forma)
                    lista=criaDNdagram(lista,0) #cria ele inserindo o ponto e o \0 no final
                if lista not in D0[elemento]:   #se a lista não estiver já em D0
                    D0[elemento].append(lista)  #insere ela em D0
                if aposPonto(lista) not in k and aposPonto(lista) not in terminais: #se o elemento após o ponto não for terminal(nesse caso, só pode ser variavel)
                    k.append(aposPonto(lista)) #insere ele em k(ou seja, diz que tem mais coisa a ser feita)

        if teste==k: #caso nada tenha mudado entre k no inicio e fim da iteração, quer dizer que não há nada mais a ser feito
            flag=False #para a iteração

    return D0 #retorna o conjunto D[0] feito corretamente

def limpa(palavra):
    palavra = palavra.replace('@', '').replace('/', '').replace('0','').replace('1','').replace('2','').replace('3','').replace('4','')
    palavra = palavra.replace('5', '').replace('6', '').replace('7','').replace('8','')

    return palavra

def insereDaAnterior(anterior, busca, atual, hist, terminais, variaveis):
    '''
    Hash de Lista de Lista, String, Hash de Lista de Lista -> Hash de Lista de Lista
    Verifica todos os que tem o elemento buscado após o ponto em Danterior e insere em Datual
    Esse eh o caso que busca no D anterior, logo, o caso em que adicionamos o caso, essa
    função já insere o histórico corretamente
    '''

    #print hist
    historico = '[' + hist + ']'
    for chave in anterior.keys():        #itera por todo o dicionário anterior
        for lista in anterior[chave]:    #itera por cada lista na lista de lista
            depois = aposPonto(lista)
            if depois==busca:  #se ao iterar por essas listas, encontrar o elemento após o ponto que seja igual ao buscado
                try:
                    mover=movePonto(lista)
                    atual[chave].append(mover)  #Caso a chave já existir no dicionário adiciona a nova lista movendo o ponto um para a direita
                    atual[chave][-1].append(historico) #Appenda o historico na ultima chave gerada
                except KeyError:
                    mover=movePonto(lista)
                    atual[chave]=[]                       #Caso a chave não existir, cria ela e
                    atual[chave].append(mover) #Insere a nova lista movendo o ponto um para a direita
                    atual[chave][-1].append(historico)


    return atual #retorna o Datual atualizado

def insereGram(gramatica, teste, elemento, dr):
    '''
    Hash de Lista de Lista, String, Int, Hash de Lista de Lista -> Hash de Lista de Lista
    Puxa da gramática o teste com ponto no inicio e o \elemento correto
    '''
    for chave in gramatica.keys():          #varre todo o hash
        if chave==teste:                    #caso ache a vriavel procurada como lado esquerdo do dicionário
            for lista in gramatica[chave]:  # para todas as listas que ele apontar
                try:
                    dr[chave].append(criaDNdagram(lista, elemento)) #caso a chave já existir em Dr, adiciona a lista com ponto no inicio e \elemento no final
                except KeyError:                                    #caso chave não existir em Dr
                    dr[chave]=[]                                    #cria o elemento associado
                    dr[chave].append(criaDNdagram(lista, elemento)) #adiciona a lista com ponto no inicio e \elemento no final
    return dr #retorna o Dn atualizado

def earley_parser(frase, inicial, terminais, regras, variaveis):
    '''
    String, String, Lista de Strings, Hash de Lista de Lista, lista -> Lista de Hash de Lista de Lista ou -1
    Função principal do programa, faz o parsing seguindo as regras do algoritmo de Earley
    Retorna -1 caso não termine o parsing (rejeita), senão, retorna a lista de Hashs que pode ou não ter reconhecido a sentença
    '''
    D=[]                                         #D é a lista que guarda cada derivação, D0 é acessado por D[0], D1 por D[1] e assim por diante
    D.append(criaD0(regras, inicial, terminais)) # Aqui cria o D[0]
    frase = frase.split(' ')                    #Separa a frase passada para gerar o DN respectivo a cada palavra
    save = deepcopy(regras)                     #Copia as regras em uma var auxiliar (uso a deepcopy pq se fizesse save=regras teria somente um ponteiro para o mesmo hash)
    for elemento in range(1, len(frase)+1):     #LOOP PRINCIAPL, CRIA D1 depois CRIA D2... até DN
        if frase[elemento-1] in terminais:      #se o elemento a ser parseado está no conjunto de terminais...
            k_chaves=[]                         #inicializa a lista dizendo quais variaveis já foram puxadas do Dn-1
            k_terminais=[]                      #inicializa a lista dizendo quais variaives já foram puxadas da gramática
            dr={}                               #inicializa o dicionário DN para cada iteração
            i=elemento-1                        #somente para ver qual a posição do Dn-1, onde i = Dn-1
            found = False                       #flag para caso tenha encontrado o elemento
            for chaves in D[i].keys():          #itera para todos os elementos do dicionario
                lista_de_lista= D[i][chaves]
                for lista in lista_de_lista:    #itera pra todas as listas em cada lista do dicionário
                    if aposPonto(lista) == frase[elemento-1]:  #caso o elemento apos o ponto seja o que a gente está buscando
                        found = True                           #encontrou a primeira (ou primeiras) regras de Dn em Dn-1
                        lista = movePonto(lista)               #essa nova lista recebe a lista que estava em Dn-1 movendo o ponto uma posição
                        try:                                   #caso elemento já exista no dicionario, insere ele lá
                            dr[chaves].append(lista)
                        except KeyError:
                            dr[chaves]=[]                      #se ainda não existir a chave ainda nas regras, cria ele
                            dr[chaves].append(lista)           #e insere
                                   #Aqui já inseriu em Dn todas as regras de da palavra pedida que existiam após ponto em Dn-1
            if found==False:       #senão achou nenhuma regra em Dn-1 que tinha a palavra pedida após o ponto, a sentença não pertence a gramática
                    D=-1
                    return D       #para a execução aqui mesmo
            else:                  #se achou, vai expandindo pra cada uma dos elementos diferentes que achar após o ponto
                da={}              #inicializa um dicionario auxiliar para ficar comparando se ele foi alterado na ultima iteração
                while da!=dr:      #enquanto ainda se adicionar algo no dicionário, continua verificando o próximo
                    da=deepcopy(dr)    #novamente, uso deepcopy pra criar uma copia bruta e não somente um ponteiro pro mesmo lugar
                    for _chaves in dr.keys():         #passa em todas as listas de lista do dicionário
                        for _lista in dr[_chaves]:    #passa em todas as listas individualmente
                            teste=aposPonto(_lista)   #teste recebe o que está após o ponto em cada lista
                            if teste[0]=='/':         #se for '/' após o ponto, CASO1 -> Puxa de n (onde /n) todas as regras que tem o lado esquerdo da regra atual após o ponto
                                n=int(teste[1:])                    #passa de string para numero
                                ja_visto = _chaves + str(n)  #lembrar que mesmo que já tenha NP por exemplo, se for NP /n(diferentes), ambos devem ser incluidos na contagem
                                if ja_visto not in k_chaves: #por isso cria um "k_chaves" que verifica se aquela variavel já foi verificado naquele específico D
                                    hist = _chaves +'>'+ ''.join(_lista)
                                    dr=insereDaAnterior(D[n], _chaves, dr, hist, terminais, variaveis) #insere as regras puxando do anterior
                                    k_chaves.append(_chaves+str(n))        #informa pra k_chaves que já leu _chaves(terminal) naqele Dn específico

                            elif teste in variaveis and teste not in k_terminais: #se for variavl após o ponto, CASO2 -> puxa da gramática com ponto no inicio e /n no fim
                                regras=deepcopy(save)  #resolve problemas que davam com a regra(stupid code),faz isso resetando a gramática para a inicial que ficou salva
                                dr=insereGram(regras, teste, elemento, dr) #puxa da gramática os elementos que tem o lado esquerdo igual a variavel após o ponto
                                k_terminais.append(teste)#informa que já leu esse terminal da gramática
            D.append(dr) #Após criar o Dn, insere na lista
    return D #retorna a lista de hashs

def limpa_arvores(D):
    '''
    MELHORAR ESSA FUNCAO
    '''
    for dicionario in D:
        for chave in dicionario.keys():
            for lista in dicionario[chave]:
                for i in range(len(lista)):
                    if '[' in lista[i]:
                        lista[i]=re.sub('@/[0-9]*', '', lista[i])
                        nova=""
                        for j in range(len(lista[i])):
                            if lista[i][j]=='>':
                                try:
                                    if lista[i][j+1].islower() or lista[i][j+1].isdigit():
                                        nova+=' '
                                    elif lista[i][j+1].isupper():
                                        nova+='#'

                                except IndexError:
                                    nova+=lista[i][j]
                            else:
                                nova+=lista[i][j]

                        nova=re.sub('#[A-Z]*?\[','#[',nova,flags=re.DOTALL)
                        nova=nova.replace('>','').replace('#', '')

                        lista[i]=nova
    return D

def ver_se_parsed(inicial, D):
    '''
    String, Lista de Hash de Lista de Lista -> Bool
    Verifica se a sentença foi aceita ou rejeitada
    '''
    arv_bonita=1
    if D!=-1:                         #caso D=-1, foi rejeita por não achar palavra inicial em Dn-1
        for chave in D[-1].keys():    #varre todo a última derivação
            if chave==inicial:        #se achar uma regra que tenha o lado esquerdo como símbolo inicial
                for lista in D[-1][chave]:
                    if aposPonto(lista)=='/0': #E tenha o ponto antes de um /0
                        lista_aux=[]
                        for string in lista:
                            if '[' in string:
                                lista_aux.append(string)
                        arv_bonita= ' '.join(lista_aux)

                        #print "A ARVORE DE DERIVACAO DEITADA EH: " #+ inicial + '>' + '(' + arv_bonita + ')\n\n'
                        arv_bonita = '['  + inicial + arv_bonita + ']'
                        i=-1
                        nova_string=''
                        for char in arv_bonita:
                        	if char == '[':
                        		i+=1
                        		nova_string+='\n'
                        		for n in range(i):
                        			nova_string+='   '
                        		nova_string+='['
                        	elif char == ']':
                        		i-=1
                        		nova_string+=']'
                        	else:
                        		nova_string+=char

                        #print nova_string
                        return True, arv_bonita            #somente assim aceita
    return False, arv_bonita #senaõ, rejeita

def save_D(D, arquivo):
    '''
    Salva a derivação em um arquivo .txt
    '''
    for i in range(len(D)):
        arquivo.write("D%d=\n"%i)
        for chave in D[i].keys():
            for lista in D[i][chave]:
                lista1=[]
                for string in lista:
                    if string=="@":
                        string='•'
                    lista1.append(string)
                arquivo.write(chave+" > "+ ' '.join(lista1) + '\n')
        arquivo.write('\n')
    arquivo.close()

def salva_arvore(arv_bonita):
    '''
    Acessa Web para printar a árvore e salva-la
    '''
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Firefox()
    driver.get("http://mshang.ca/syntree/")
    driver.maximize_window()

    inputElement = driver.find_element_by_id("i")
    inputElement.clear()
    inputElement.send_keys(arv_bonita)

    nome = "Derivation_Tree.png"

    outputElement = driver.find_element_by_id("image-goes-here")
    location = outputElement.location
    size = outputElement.size
    driver.save_screenshot(nome)

    driver.close()

    im = Image.open(nome)

    left = int(location['x'])
    top = int(location['y'])
    right = int(location['x']) + int(size['width'])
    bottom = int(location['y']) + int(size['height'])

    im = im.crop((left, top, right, bottom))
    im.save(nome)

def gera_frase(regras, inicial, variaveis, terminais):
    flag = True
    lista_de_exp =[]

    inicio=regras[inicial][random.randint(0,len(regras[inicial])-1)]

    while flag:
        for string in inicio:
            if string in variaveis:
                lista_de_exp+=regras[string][random.randint(0,len(regras[string])-1)]
            else:
                lista_de_exp+=[string]
        inicio=lista_de_exp
        flag=False
        for element in inicio:
            if element in variaveis:
                flag=True
                lista_de_exp=[]

    return ' '.join(lista_de_exp)

def parse(frase, inicial, terminais, regras, variaveis):
    try:
        D= earley_parser(frase, inicial, terminais, regras, variaveis)
    except:
        D=-1

    if D!=-1:
        D=limpa_arvores(D)

    pertence, arv_bonita = ver_se_parsed(inicial, D)

    return pertence, D, arv_bonita
