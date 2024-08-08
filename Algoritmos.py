from tkinter import *
from tkinter import ttk
from tkinter import font
from Processo import *

def FIFO(App) -> None:
     App.viz_window = Toplevel(App)
     App.viz_window.geometry('900x250')
     clock = 0
     lista_processos = sorted(App.processos_copy, key=lambda processo: processo.get_chegada())
     fila_processos = []
     lista_exec = [processo.exec for processo in App.processos_copy]
    
     row_dict = {processo.get_pid(): i for i, processo in enumerate(App.processos_copy)}
    
     App.titulo = Label(App.viz_window, text='PIDs')
     App.titulo.grid(row=0, column=0, columnspan=1)
    
     for i in row_dict:
        label = Label(App.viz_window, text=f'{i}:')
        label.grid(row=1 + row_dict[i], column=0, columnspan=1)
    
    # Contadores de espera e execução
     tempo_espera = {p.get_pid(): 0 for p in App.processos_copy}
     tempo_execucao = {p.get_pid(): 0 for p in App.processos_copy}

     while len(lista_processos) > 0 or len(fila_processos) > 0:
        while lista_processos and lista_processos[0].get_chegada() <= clock:
            fila_processos.append(lista_processos.pop(0))
        
        if fila_processos:
            processo_atual = fila_processos.pop(0)
            pid = processo_atual.get_pid()
            exec_time = lista_exec[pid]
            
            for _ in range(exec_time):
                for i in lista_processos:    
                    if i.get_chegada() == clock:
                        fila_processos.append(i)
                        lista_processos.pop(0)
                    else:
                        break
                # Adiciona visualização gráfica para o processo em execução
                label = Label(App.viz_window, text='\u25A0')
                label.grid(row=1 + row_dict[pid], column=1 + clock, columnspan=1)
                tempo_execucao[pid] += 1
                
                # Adiciona visualização gráfica para os processos em espera
                for p in fila_processos:
                    cur = p.get_pid()
                    label = Label(App.viz_window, text='\u22A0')
                    label.grid(row=1 + row_dict[cur], column=1 + clock, columnspan=1)
                    tempo_espera[cur] += 1
                
                clock += 1
            
            lista_exec[pid] = 0
            
            if lista_exec[pid] > 0:
                fila_processos.append(processo_atual)
        
        else:
            label = Label(App.viz_window, text='\u25A1')  # Espaço Vazio
            label.grid(row=1, column=1 + clock, columnspan=1)
            clock += 1

    # Cálculo do tempo médio de espera
     total_espera = sum(tempo_espera.values())
     total_execucao = sum(tempo_execucao.values())
     num_processos = len(App.processos_copy)
     tempo_medio_espera = (total_espera + total_execucao) / num_processos
    
    # Adiciona o tempo médio de espera na visualização gráfica
     tempo_medio_label = Label(App.viz_window, text=f"Tempo médio de espera: {tempo_medio_espera:.2f}", font=("Arial", 10))
     tempo_medio_label.grid(row=len(row_dict) + 2, column=0, columnspan=100)
     
     #Legenda gráfico
     App.legenda(App.viz_window, row_dict)

def SJF(App) -> None:
     App.viz_window = Toplevel(App)
     App.viz_window.geometry('900x250')

     clock = 0

    # Ordena primeiro por tempo de chegada e depois por tempo de execução (em caso de empate)
     lista_processos = sorted(App.processos_copy, key=lambda processo: processo.get_chegada())  
     lista_chegou = []  # Lista que guarda os processos à medida que eles chegam na CPU
     lista_exec = [processo.exec for processo in App.processos_copy]  # Lista dos tempos de execução restantes

    # Associa cada Processo a uma linha na janela de visualização
     row_dict = {processo.get_pid(): i for i, processo in enumerate(App.processos_copy)}

    # Imprime coluna com PID dos Processos
     App.titulo = Label(App.viz_window, text='PIDs')
     App.titulo.grid(row=0, column=0, columnspan=1)

     for i in row_dict:
        label = Label(App.viz_window, text=f'{i}:')
        label.grid(row=1 + row_dict[i], column=0, columnspan=1)

     max_columns = 100  # Define um valor máximo para as colunas
    
     tempo_espera = 0
     tempo_execucao = 0
    
     while len(lista_processos) > 0 or len(lista_chegou) > 0:
        # Adiciona processos que chegaram até o momento
        while lista_processos and lista_processos[0].get_chegada() <= clock:
            lista_chegou.append(lista_processos.pop(0))

        
        if lista_chegou:
            lista_chegou = sorted(lista_chegou, key=lambda processo: processo.get_tempo_execucao())
            cur_processo = lista_chegou[0].get_pid()
            if clock >= max_columns:
                break  # Evita acessar colunas fora dos limites

            if lista_exec[cur_processo] <= 0:
                lista_chegou.pop(0)
                continue

            # Continua a execução do processo atual até ele terminar
            while lista_exec[cur_processo] > 0:
                for i in lista_processos:    
                    if i.get_chegada() == clock:
                        lista_chegou.append(i)
                        lista_processos.pop(0)
                    else:
                        break
                lista_exec[cur_processo] -= 1

                # Adiciona símbolo de execução
                label = Label(App.viz_window, text='\u25A0')  # Executando
                label.grid(row=1 + row_dict[cur_processo], column=1 + clock, columnspan=1)
                tempo_execucao += 1

                # Adiciona símbolo de espera para outros processos
                for i in lista_chegou:
                    if i.get_pid() != cur_processo:
                        cur = i.get_pid()
                        label = Label(App.viz_window, text='\u22A0')  # Esperando
                        label.grid(row=1 + row_dict[cur], column=1 + clock, columnspan=1)
                        tempo_espera += 1

                clock += 1

            lista_chegou.pop(0)  # Remove o processo atual da fila após a execução completa
        else:
            if clock >= max_columns:
                break  # Evita acessar colunas fora dos limites
            
            label = Label(App.viz_window, text='\u25A1')  # Espaço Vazio
            label.grid(row=1, column=1 + clock, columnspan=1)
            clock += 1

    # Calcula e exibe o tempo médio de espera
     num_processos = len(App.processos_copy)
     tempo_medio_espera = (tempo_espera + tempo_execucao) / num_processos 
     label = Label(App.viz_window, text=f'Tempo Médio de Espera: {tempo_medio_espera:.2f}')
     label.grid(row=1 + len(row_dict), column=0, columnspan=max_columns)
     
     #Legenda gráfico
     App.legenda(App.viz_window, row_dict)


def roundRobin(App, quantum, sobrecarga) -> None:
     App.viz_window = Toplevel(App)
     App.viz_window.geometry('900x250')

     clock = 0
     lista_processos = sorted(App.processos_copy, key=lambda processo: processo.get_chegada())  # Ordena por tempo de chegada
     fila_processos = []
     lista_exec = [processo.exec for processo in App.processos_copy]  # Lista dos tempos de execução restantes

    # Associa cada Processo a uma linha na janela de visualização
     row_dict = {processo.get_pid(): i for i, processo in enumerate(App.processos_copy)}

    # Imprime coluna com PID dos Processos
     App.titulo = Label(App.viz_window, text='PIDs')
     App.titulo.grid(row=0, column=0, columnspan=1)

     for i in row_dict:
        label = Label(App.viz_window, text=f'{i}:')
        label.grid(row=1 + row_dict[i], column=0, columnspan=1)

    # Contadores
     total_espera = 0
     total_execucao = 0
     total_sobrecarga = 0

     while len(lista_processos) > 0 or len(fila_processos) > 0:
        # Adiciona processos que chegaram até o momento
        while lista_processos and lista_processos[0].get_chegada() <= clock:
            fila_processos.append(lista_processos.pop(0))

        if fila_processos:
            processo_atual = fila_processos[0] # fila_processos.pop(0)
            pid = processo_atual.get_pid()
            exec_time = min(quantum, lista_exec[pid])  # Tempo a ser executado no quantum

            # Executa o processo
            for _ in range(exec_time):
                for i in lista_processos:    
                    if i.get_chegada() == clock:
                        fila_processos.append(i)
                        lista_processos.pop(0)
                    else:
                        break
                
                label = Label(App.viz_window, text='\u25A0')  # Executando
                label.grid(row=1 + row_dict[pid], column=1 + clock, columnspan=1)

                # Atualiza o contador de execução
                total_execucao += 1

                # Processos em espera
                for p in fila_processos:
                    if p == fila_processos[0]: continue
                    cur = p.get_pid()
                    label = Label(App.viz_window, text='\u22A0')  # Esperando
                    label.grid(row=1 + row_dict[cur], column=1 + clock, columnspan=1)

                    # Atualiza o contador de espera
                    total_espera += 1

                clock += 1

            lista_exec[pid] -= exec_time  # Subtrai o tempo executado

            # Adiciona sobrecarga
            if lista_exec[pid] > 0 and len(fila_processos) > 0:
                for _ in range(sobrecarga): # Verifica se chegou algum processo durante a sobrecarga
                    for i in lista_processos:    
                        if i.get_chegada() == clock:
                            fila_processos.append(i)
                            lista_processos.pop(0)
                        else:
                            break
                    
                    for p in fila_processos:
                        cur = p.get_pid()
                        
                        if p == fila_processos[0]:
                            label = Label(App.viz_window, text='\u26DE')  # Bola cortada (sobrecarga)
                            label.grid(row=1 + row_dict[cur], column=1 + clock, columnspan=1)
                        
                        else:
                            label = Label(App.viz_window, text='\u22A0')  # Esperando
                            label.grid(row=1 + row_dict[cur], column=1 + clock, columnspan=1)
                        
                        total_sobrecarga += 1

                    clock += 1
            
            fila_processos.pop(0)
            
            if lista_exec[pid] > 0:
                fila_processos.append(processo_atual)  # Reinsere no final da fila se ainda não terminou

        else:
            # Se nenhum processo está disponível, avança o tempo
            label = Label(App.viz_window, text='\u25A1')  # Espaço Vazio
            label.grid(row=1, column=1 + clock, columnspan=1)
            clock += 1

    # Calcula o tempo médio de espera
     num_processos = len(App.processos_copy)
     tempo_medio_espera = (total_espera + total_execucao + total_sobrecarga) / num_processos
     App.tempo_medio_espera_label = Label(App.viz_window, text=f'Tempo Médio de Espera: {tempo_medio_espera:.2f}')
     App.tempo_medio_espera_label.grid(row=len(row_dict) + 1, column=0, columnspan=1)
     
     #Legenda gráfico
     App.legenda(App.viz_window, row_dict)


def EDF(App, quantum, sobrecarga) -> None:
     App.viz_window = Toplevel(App)
     App.viz_window.geometry('900x250')

     clock = 0
     lista_processos = sorted(App.processos_copy, key=lambda processo: processo.get_chegada())
     fila_processos = []
     lista_exec = {processo.get_pid(): processo.get_tempo_execucao() for processo in App.processos_copy}
     deadlines = {processo.get_pid(): processo.get_deadline() for processo in App.processos_copy}

    # Associa cada Processo a uma linha na janela de visualização
     row_dict = {processo.get_pid(): i for i, processo in enumerate(App.processos_copy)}

    # Imprime coluna com PID dos Processos
     App.titulo = Label(App.viz_window, text='PIDs')
     App.titulo.grid(row=0, column=0, columnspan=1)

     for i in row_dict:
        label = Label(App.viz_window, text=f'{i}:')
        label.grid(row=1 + row_dict[i], column=0, columnspan=1)

    # Inicializa contadores
     total_espera = 0
     total_execucao = 0
     total_sobrecarga = 0

     while len(lista_processos) > 0 or len(fila_processos) > 0:
        # Adiciona processos que chegaram até o momento
        while lista_processos and lista_processos[0].get_chegada() <= clock:
            fila_processos.append(lista_processos.pop(0))

        if fila_processos:
            # Ordena fila de processos por deadline
            fila_processos.sort(key=lambda p: deadlines[p.get_pid()])
            processo_atual = fila_processos[0]
            pid = processo_atual.get_pid()
            exec_time = min(quantum, lista_exec[pid])

            for _ in range(exec_time):
                for i in lista_processos:    
                    if i.get_chegada() == clock:
                        fila_processos.append(i)
                        lista_processos.pop(0)
                    else:
                        break
                if  deadlines[pid]<0:
                    symbol = '\u25A3'  # Processo ultrapassou a deadline
                else:
                    symbol = '\u25A0'  # Executando
                
                label = Label(App.viz_window, text=symbol)
                label.grid(row=1 + row_dict[pid], column=1 + clock, columnspan=1)

                total_execucao += 1
                # Processos em espera
                for p in fila_processos:
                    if p == fila_processos[0]: continue
                    cur = p.get_pid()                    
                    symbol = '\u22A0'  # Esperando
                    label = Label(App.viz_window, text=symbol)
                    label.grid(row=1 + row_dict[cur], column=1 + clock, columnspan=1)
                    total_espera += 1
                clock += 1

            lista_exec[pid] -= exec_time  # Subtrai o tempo executado
            for i in fila_processos:
                deadlines[i.pid]=deadlines[i.pid]-exec_time   #subtrai tempo de execução da deadline

            # Adiciona sobrecarga
            if lista_exec[pid] > 0 and len(fila_processos) > 0: 
                for _ in range(sobrecarga): # Verifica se chegou algum processo durante a sobrecarga
                    for i in lista_processos:    
                        if i.get_chegada() == clock:
                            fila_processos.append(i)
                            lista_processos.pop(0)
                        else:
                            break
                    
                    for p in fila_processos:
                        cur = p.get_pid()
                        
                        if p == fila_processos[0]:
                            label = Label(App.viz_window, text='\u26DE')  # Bola cortada (sobrecarga)
                            label.grid(row=1 + row_dict[cur], column=1 + clock, columnspan=1)
                            deadlines[cur]=deadlines[cur]-1 #Diminui a deadline
                        else:
                            label = Label(App.viz_window, text='\u22A0')  # Esperando
                            label.grid(row=1 + row_dict[cur], column=1 + clock, columnspan=1)
                            deadlines[cur]=deadlines[cur]-1 #Diminui a deadline
                        total_sobrecarga += 1
                    
                    clock += 1
            
            fila_processos.pop(0)
            if lista_exec[pid] > 0:                    #Reincere o processo caso não tenha acabado
                fila_processos.append(processo_atual) 
       
        else:
            # Se nenhum processo está disponível, avança o tempo
            label = Label(App.viz_window, text='\u25A1')  # Espaço Vazio
            label.grid(row=1, column=1 + clock, columnspan=1)
            clock += 1
        for i in fila_processos:
         print(deadlines[i.pid])

    # Calcula o tempo médio de espera
     num_processos = len(App.processos_copy)
     tempo_medio_espera = (total_espera + total_execucao + total_sobrecarga) / num_processos
     App.tempo_medio_espera_label = Label(App.viz_window, text=f"Tempo Médio de Espera: {tempo_medio_espera:.2f}")
     App.tempo_medio_espera_label.grid(row=len(row_dict) + 2, column=0, columnspan=1)
     
     #Legenda gráfico
     App.legenda(App.viz_window, row_dict)
     
