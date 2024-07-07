from copy import deepcopy

p1, p2, p3, p4 = [4,0], [2,2], [1,4], [3,6]
lista_de_processos = [p1, p2, p3, p4]


def fifo(lista_de_processos, quantum_do_sistema, sobrecarga_do_sistema):
    lista_de_processos_local = deepcopy(lista_de_processos)
    lista_de_processos_ordenada = sorted(lista_de_processos_local, key=lambda proces: proces[1])

    while len(lista_de_processos_ordenada) != 0:
        lista_de_processos_ordenada[0][0] -= 1
        if lista_de_processos_ordenada[0][0] <= 0:
            lista_de_processos_ordenada.pop(0)
        if len(lista_de_processos_ordenada) == 0:
            return
        else:
            for processo in lista_de_processos_ordenada:
                print(processo[0], end=' ')
                
            print()



def sjf(lista_de_processos, quantum_do_sistema, sobrecarga_do_sistema):
    lista_de_processos_para_execucao = deepcopy(lista_de_processos)
    timer = 0 
    lista_de_processos_disponiveis = []
    lista_de_processos_ja_executados = []

    while len(lista_de_processos) != len(lista_de_processos_ja_executados):

        for processo in lista_de_processos_para_execucao[:]:
            if processo[1] == timer:
                lista_de_processos_disponiveis.append(processo)
                lista_de_processos_para_execucao.remove(processo)

        primeiro_elemento = lista_de_processos_disponiveis[0]
        resto_ordenado = sorted(lista_de_processos_disponiveis[1:], key=lambda proces: proces[0])
        lista_de_processos_disponiveis = [primeiro_elemento] + resto_ordenado
        
        for processo in lista_de_processos_disponiveis:
            print(processo[0], end=' ')
        print()
        
        if lista_de_processos_disponiveis[0][0] <= 0:          
            lista_de_processos_ja_executados.append(lista_de_processos_disponiveis[0])
            lista_de_processos_disponiveis.pop(0)

        lista_de_processos_disponiveis[0][0] -= 1 
        timer += 1      



quantum = 2 
sobrecarga = 1 
def roundRobin(lista_de_processos, quantum_do_sistema, sobrecarga_do_sistema):
    lista_de_processos_para_execucao = deepcopy(lista_de_processos)
    timer = 0 
    tempo_de_execucao_do_primeiro_processo = 0
    lista_de_processos_disponiveis = []
    lista_de_processos_ja_executados = []
    total_de_tempo_de_sobrecarga = 0 

    while len(lista_de_processos) != len(lista_de_processos_ja_executados):
        for processo in lista_de_processos_para_execucao[:]:
                if processo[1] == timer:
                    lista_de_processos_disponiveis.append(processo)
                    lista_de_processos_para_execucao.remove(processo)



        print(lista_de_processos_disponiveis)


        if lista_de_processos_disponiveis[0][0] <= 0:          
                lista_de_processos_ja_executados.append(lista_de_processos_disponiveis[0])
                lista_de_processos_disponiveis.pop(0)
                tempo_de_execucao_do_primeiro_processo = 0

        
        if tempo_de_execucao_do_primeiro_processo == quantum_do_sistema:
            primeiro_elemento = lista_de_processos_disponiveis.pop(0)
            lista_de_processos_disponiveis.append(primeiro_elemento)
            tempo_de_execucao_do_primeiro_processo = 0 
            total_de_tempo_de_sobrecarga += sobrecarga_do_sistema


        if lista_de_processos_disponiveis:
            lista_de_processos_disponiveis[0][0] -= 1 
        timer += 1 
        tempo_de_execucao_do_primeiro_processo += 1

    print(total_de_tempo_de_sobrecarga)

p5, p6, p7, p8 = [4,0,7,'A'], [2,2,5,'B'], [1,4,8,'C'], [3,6,5,'D']
lista_de_processos_edf = [p5, p6, p7, p8]

def edf(lista_de_processos, quantum_do_sistema, sobrecarga_do_sistema):
    lista_de_processos_para_execucao = deepcopy(lista_de_processos)
    timer = 0 
    tempo_de_execucao_do_primeiro_processo = 0
    lista_de_processos_disponiveis = []
    lista_de_processos_ja_executados = []
    total_de_tempo_de_sobrecarga = 0 

    while len(lista_de_processos) != len(lista_de_processos_ja_executados):
        for processo in lista_de_processos_para_execucao[:]:
                if processo[1] == timer:
                    lista_de_processos_disponiveis.append(processo)
                    lista_de_processos_para_execucao.remove(processo)



        print(lista_de_processos_disponiveis)


        if lista_de_processos_disponiveis[0][0] <= 0:          
                lista_de_processos_ja_executados.append(lista_de_processos_disponiveis[0])
                lista_de_processos_disponiveis.pop(0)
                tempo_de_execucao_do_primeiro_processo = 0

        
        lista_de_processos_pre_ordenacao = deepcopy(lista_de_processos_disponiveis)
        lista_de_processos_disponiveis.sort(key=lambda proces: proces[2])
        if lista_de_processos_disponiveis and (lista_de_processos_pre_ordenacao[0] != lista_de_processos_disponiveis[0]):
             tempo_de_execucao_do_primeiro_processo = 0
        
        
        if tempo_de_execucao_do_primeiro_processo == quantum_do_sistema:
            primeiro_elemento = lista_de_processos_disponiveis.pop(0)
            lista_de_processos_disponiveis.append(primeiro_elemento)
            tempo_de_execucao_do_primeiro_processo = 0 
            total_de_tempo_de_sobrecarga += sobrecarga_do_sistema

        print(lista_de_processos_disponiveis)

        if lista_de_processos_disponiveis:
            lista_de_processos_disponiveis[0][0] -= 1 
            for processo2 in lista_de_processos_disponiveis:
                processo2[2] -= 1 
                

        timer += 1 
        tempo_de_execucao_do_primeiro_processo += 1

    print(total_de_tempo_de_sobrecarga)


edf(lista_de_processos_edf, quantum, sobrecarga)
#roundRobin(lista_de_processos, quantum, sobrecarga)

       









