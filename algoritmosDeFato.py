
from copy import deepcopy
from Processo import * 


def pid_para_letra(lista_de_processos_com_pid_numerico):
    numero_para_letra = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P'}
    for processo in lista_de_processos_com_pid_numerico:
        if processo.pid in numero_para_letra:
            processo.pid = numero_para_letra[processo.pid]
    lista_de_processos_com_pid_alfabetico = lista_de_processos_com_pid_numerico
    return lista_de_processos_com_pid_alfabetico

def fifo(lista_de_processos):
    lista_de_processos_para_execucao = deepcopy(lista_de_processos)
    lista_de_processos_para_execucao = pid_para_letra(lista_de_processos_para_execucao)
    lista_de_processos_disponiveis = sorted(lista_de_processos_para_execucao, key=lambda proces: proces.get_chegada())
    timer = 0 

    while len(lista_de_processos_disponiveis) != 0:
        timer += 1
        (lista_de_processos_disponiveis[0]).exec -= 1
        if (lista_de_processos_disponiveis[0]).exec <= 0:
            lista_de_processos_disponiveis.pop(0)
        if len(lista_de_processos_disponiveis) == 0:
            return
        else:
            for processo in lista_de_processos_disponiveis:
                print(processo.get_pid() + str(processo.get_tempo_execucao()), end=' ')
                
            print()
    print(" ")
            

def sjf(lista_de_processos):
    lista_de_processos_para_execucao = deepcopy(lista_de_processos)
    lista_de_processos_para_execucao = pid_para_letra(lista_de_processos_para_execucao)
    timer = 0 
    lista_de_processos_disponiveis = []
    lista_de_processos_ja_executados = []

    while len(lista_de_processos) != len(lista_de_processos_ja_executados):

        for processo in lista_de_processos_para_execucao[:]:
            if processo.get_chegada() == timer:
                lista_de_processos_disponiveis.append(processo)
                lista_de_processos_para_execucao.remove(processo)

        for processo in lista_de_processos_disponiveis:
            print(processo.get_pid() + str(processo.get_tempo_execucao()), end=' ')
        print()

        if lista_de_processos_disponiveis:
            primeiro_elemento = lista_de_processos_disponiveis[0]
            resto_ordenado = sorted(lista_de_processos_disponiveis[1:], key=lambda proces: proces.get_tempo_execucao())
            lista_de_processos_disponiveis = [primeiro_elemento] + resto_ordenado
        
        
        
        if lista_de_processos_disponiveis and (lista_de_processos_disponiveis[0]).get_tempo_execucao() <= 0:          
            lista_de_processos_ja_executados.append(lista_de_processos_disponiveis[0])
            lista_de_processos_disponiveis.pop(0)

        if lista_de_processos_disponiveis:
            (lista_de_processos_disponiveis[0]).exec -= 1 
        timer += 1  
    print(" ")




def roundRobin(lista_de_processos, quantum_do_sistema, sobrecarga_do_sistema):
    lista_de_processos_para_execucao = deepcopy(lista_de_processos)
    lista_de_processos_para_execucao = pid_para_letra(lista_de_processos_para_execucao)
    timer = 0 
    tempo_de_execucao_do_primeiro_processo = 0
    lista_de_processos_disponiveis = []
    lista_de_processos_ja_executados = []
    total_de_tempo_de_sobrecarga = 0 

    while len(lista_de_processos) != len(lista_de_processos_ja_executados):
        for processo in lista_de_processos_para_execucao[:]:
                if processo.get_chegada() == timer:
                    lista_de_processos_disponiveis.append(processo)
                    lista_de_processos_para_execucao.remove(processo)

        for processo in lista_de_processos_disponiveis:
            print(processo.get_pid() + str(processo.get_tempo_execucao()), end=' ')
        print()


        if lista_de_processos_disponiveis and (lista_de_processos_disponiveis[0]).get_tempo_execucao() <= 0:          
                lista_de_processos_ja_executados.append(lista_de_processos_disponiveis[0])
                lista_de_processos_disponiveis.pop(0)
                tempo_de_execucao_do_primeiro_processo = 0

        
        if tempo_de_execucao_do_primeiro_processo == quantum_do_sistema:
            primeiro_elemento = lista_de_processos_disponiveis.pop(0)
            lista_de_processos_disponiveis.append(primeiro_elemento)
            tempo_de_execucao_do_primeiro_processo = 0 
            total_de_tempo_de_sobrecarga += sobrecarga_do_sistema


        if lista_de_processos_disponiveis:
            (lista_de_processos_disponiveis[0]).exec -= 1 
        timer += 1 
        tempo_de_execucao_do_primeiro_processo += 1
    print(" ")



def edf(lista_de_processos, quantum_do_sistema, sobrecarga_do_sistema):
    lista_de_processos_para_execucao = deepcopy(lista_de_processos)
    lista_de_processos_para_execucao = pid_para_letra(lista_de_processos_para_execucao)
    timer = 0 
    tempo_de_execucao_do_primeiro_processo = 0
    lista_de_processos_disponiveis = []
    lista_de_processos_ja_executados = []
    total_de_tempo_de_sobrecarga = 0

    while len(lista_de_processos) != len(lista_de_processos_ja_executados):
        for processo in lista_de_processos_para_execucao[:]:
                if processo.get_chegada() == timer:
                    lista_de_processos_disponiveis.append(processo)
                    lista_de_processos_para_execucao.remove(processo)



        for processo in lista_de_processos_disponiveis:
            print(processo.get_pid() + str(processo.get_tempo_execucao()), end=' ')
        print()


        if lista_de_processos_disponiveis and (lista_de_processos_disponiveis[0]).get_tempo_execucao() <= 0:          
                lista_de_processos_ja_executados.append(lista_de_processos_disponiveis[0])
                lista_de_processos_disponiveis.pop(0)
                tempo_de_execucao_do_primeiro_processo = 0

        
        lista_de_processos_pre_ordenacao = deepcopy(lista_de_processos_disponiveis)
        lista_de_processos_disponiveis.sort(key=lambda proces: proces.get_deadline())
        if lista_de_processos_disponiveis and ((lista_de_processos_pre_ordenacao[0]).get_pid() != (lista_de_processos_disponiveis[0]).get_pid()):
             tempo_de_execucao_do_primeiro_processo = 0
        
        
        if tempo_de_execucao_do_primeiro_processo == quantum_do_sistema:
            if len(lista_de_processos_disponiveis) >= 2 and (lista_de_processos_disponiveis[0]).get_deadline() == (lista_de_processos_disponiveis[1]).get_deadline():
                primeiro_elemento = lista_de_processos_disponiveis.pop(0)
                lista_de_processos_disponiveis.append(primeiro_elemento)
            tempo_de_execucao_do_primeiro_processo = 0 
            total_de_tempo_de_sobrecarga += sobrecarga_do_sistema

        if lista_de_processos_disponiveis:
            (lista_de_processos_disponiveis[0]).exec -= 1 
            for processo2 in lista_de_processos_disponiveis:
                processo2.deadline -= 1 
                

        timer += 1 
        tempo_de_execucao_do_primeiro_processo += 1

    print(" ")






    def fifo_dois(lista_de_processos):
        lista_de_processos.sort(key = lambda processo: processo.chegada)

        while len(lista_de_processos) > 0:
            if(lista_de_processos[0].get_tempo_execucao() > 0):
                atual = lista_de_processos[0].get_tempo_execucao()
                lista_de_processos[0].set_tempo_execucao(atual-1)
            else:
                lista_de_processos.pop()
        
            if len(lista_de_processos) == 0: return
            else:
                print()
        

if __name__ == "__main__" :
    p1, p2, p3, p4 = Processo(0, 0, 4, 7), Processo(1, 2, 2, 5), Processo(2, 4, 1, 8), Processo(3, 6, 3 ,10)
    lista_de_processos = [p1, p2, p3, p4]
    quantum = 2 
    sobrecarga = 1 

    fifo(lista_de_processos)
    print("", "")
    sjf(lista_de_processos)
    print("", "")
    roundRobin(lista_de_processos, quantum, sobrecarga)
    print("", "")
    edf(lista_de_processos, quantum, sobrecarga)








