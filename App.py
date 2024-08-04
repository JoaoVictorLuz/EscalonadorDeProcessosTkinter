from tkinter import *
from tkinter import ttk
from tkinter import font
from algoritmosDeFato import *
from Processo import *

class App(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry('900x450')
        self.title('Simulador SO')
        self.config(bg="gray")
        self.pid_counter = 0
        self.widgets = {}
        self.processos = []   
        self.input_widget()             # Faz aparecer caixas de entrada na tela inicial
        self.buttons_beginning()        # Faz aparecer botôes na tela inicial



    def buttons_beginning(self):
        self.new_process_window_button = Button(self, text='Criar Processos', font=('Arial 20 bold'), command=self.create_process_window)
        self.new_process_window_button.grid(row=1, column=20, columnspan=5, padx=5, pady=5)
        self.run_button = Button(self, text='RUN', font=('Arial 20 bold'), command=self.escalonador)
        self.run_button.grid(row=20, column=2, columnspan=5)
        
    def create_process(self)-> None:
        chegada = int(self.chegada_input.get())
        tempo_execucao = int(self.tempo_execucao_input.get())
        deadline = int(self.deadline_input.get())
        self.new_process = Processo(self.pid_counter, chegada, tempo_execucao, deadline)
        self.output_process(self.new_process)
        self.chegada_input.delete(0, END)
        self.tempo_execucao_input.delete(0, END)
        self.deadline_input.delete(0, END)
        self.pid_counter += 1
        
    def input_widget(self) -> None:

        self.quantum_label = Label(self, text = 'Quantum', font=('Arial 15'))
        self.quantum_label.grid(row=0, column=0, padx=5, pady=5)
        self.quantum_input = Entry(self, width = 8)
        self.quantum_input.grid(row=1, column=0, padx=10, pady=10)
        
        self.sobrecarga_label = Label(self, text = 'Sobrecarga do Sistema', font=('Arial 15'))
        self.sobrecarga_label.grid(row=0, column=1, padx=10, pady=10)
        self.sobrecarga_input = Entry(self, width = 10)
        self.sobrecarga_input.grid(row=1, column=1)

        self.algoritmo_label = Label (self, text = 'Algoritmo de Escalonamento', font=('Arial 15'))
        self.algoritmo_label.grid(row=0, column=2, padx=10, pady=10)
        itens = ['FIFO', 'SJF', 'ROUND ROBIN', 'EDF']
        self.algoritmo_input = ttk.Combobox (self,values=itens)
        self.algoritmo_input.grid(row=1, column=2)



    def output_process(self, process: Processo) -> None:
        pid=process.pid
        output = Label(self, text = f"PID:{pid}  Tempo de Chegada:{process.get_chegada()}  Tempo de Execução:{process.get_tempo_execucao()}  Deadline:{process.get_deadline()}")
        output.grid(columnspan = 3, column=0, padx=3, pady=3)
        self.processos.append(process)
        delete_button = Button (self, text='X', command=lambda: eliminar_processo(process), bg="red", fg="black")   
        delete_button.grid(column=2, padx=1, pady=1) 
        self.widgets[pid] = (output, delete_button)
        def eliminar_processo(process: Processo):
            pid_to_remove = process.pid
            output, delete_button = self.widgets[pid_to_remove]
            output.destroy()
            delete_button.destroy()
            self.processos.remove(process)
            del self.widgets[pid_to_remove]
            for i in range(pid_to_remove, len(self.processos)-1):
                self.processos[i].pid -= 1 
                new_pid = self.processos[i].pid
            
                output, delete_button = self.widgets.pop(new_pid + 1) 
                output.config(text=f"PID:{new_pid}  Tempo de Chegada:{self.processos[i].get_chegada()}  Tempo de Execução:{self.processos[i].get_tempo_execucao()}  Deadline:{self.processos[i].get_deadline()}")
                self.widgets[new_pid] = (output, delete_button)  
        
        
            self.pid_counter -= 1
    
    def escalonador(self) -> None:
     if self.algoritmo_input is not None:
        algoritmo = self.algoritmo_input.get()
        self.processos_copy = [Processo(p.get_pid(), p.get_chegada(), p.get_tempo_execucao(), p.get_deadline()) for p in self.processos]
        if algoritmo == "FIFO":
            self.FIFO()
        elif algoritmo == "SJF":
            self.SJF()
        elif algoritmo == "ROUND ROBIN":
            quantum = int(self.quantum_input.get())
            sobrecarga = int(self.sobrecarga_input.get())
            self.roundRobin(quantum, sobrecarga)
        elif algoritmo == "EDF":
            quantum = int(self.quantum_input.get())
            sobrecarga = int(self.sobrecarga_input.get())
            self.EDF(quantum, sobrecarga)

    
    def create_process_window(self) -> None:
        self.window = Toplevel(self)
        self.window.geometry('400x400')

        self.chegada_label = Label(self.window, text='Tempo de Chegada')
        self.chegada_label.grid(row = 0, column= 0, padx=5, pady=5)
        self.chegada_input = Entry(self.window, width = 10)
        self.chegada_input.grid(row=1, column=0)

        self.tempo_execucao_label = Label(self.window, text='Tempo de Execução')
        self.tempo_execucao_label.grid(row=0, column=1, padx=5, pady=5)
        self.tempo_execucao_input = Entry(self.window, width = 10)
        self.tempo_execucao_input.grid(row=1, column=1)

        self.deadline_label = Label(self.window, text = 'Deadline')
        self.deadline_label.grid(row=0, column=2, padx=5, pady=5)
        self.deadline_input = Entry(self.window, width = 8)
        self.deadline_input.grid(row=1, column=2, padx=5, pady=5)

        self.new_process_button = Button(self.window, text='Criar', font=('Arial 10 bold'), command=self.create_process)
        self.new_process_button.grid( row=2, column=0, columnspan=5, padx=5, pady=5)
    
  
   
    def FIFO(self) -> None:
     self.viz_window = Toplevel(self)
     self.viz_window.geometry('800x250')
    
     clock = 0
     lista_processos = sorted(self.processos_copy, key=lambda processo: processo.get_chegada())
     fila_processos = []
     lista_exec = [processo.exec for processo in self.processos_copy]
    
     row_dict = {processo.get_pid(): i for i, processo in enumerate(self.processos_copy)}
    
     self.titulo = Label(self.viz_window, text='PIDs')
     self.titulo.grid(row=0, column=0, columnspan=1)
    
     for i in row_dict:
        label = Label(self.viz_window, text=f'{i}:')
        label.grid(row=1 + row_dict[i], column=0, columnspan=1)
    
     while len(lista_processos) > 0 or len(fila_processos) > 0:
        while lista_processos and lista_processos[0].get_chegada() <= clock:
            fila_processos.append(lista_processos.pop(0))
        
        if fila_processos:
            processo_atual = fila_processos.pop(0)
            pid = processo_atual.get_pid()
            exec_time = lista_exec[pid]
            
            for _ in range(exec_time):
                label = Label(self.viz_window, text='\u25A0')
                label.grid(row=1 + row_dict[pid], column=1 + clock, columnspan=1)
                
                for p in fila_processos:
                    cur = p.get_pid()
                    label = Label(self.viz_window, text='\u25A9')
                    label.grid(row=1 + row_dict[cur], column=1 + clock, columnspan=1)
                
                clock += 1
            
            lista_exec[pid] = 0
            
            if lista_exec[pid] > 0:
                fila_processos.append(processo_atual)
        
        else:
            label = Label(self.viz_window, text='\u25A1')
            label.grid(row=1, column=1 + clock, columnspan=1)
            clock += 1

     return None

        
    def SJF(self) -> None:
     self.viz_window = Toplevel(self)
     self.viz_window.geometry('800x250')

     clock = 0
     lista_processos = sorted(self.processos_copy, key=lambda processo: processo.get_chegada())  # Ordena por tempo de chegada
     lista_chegou = []  # Lista que guarda os processos à medida que eles chegam na CPU
     lista_exec = [processo.exec for processo in self.processos_copy]  # Lista dos tempos de execução restantes

    # Associa cada Processo a uma linha na janela de visualização
     row_dict = {processo.get_pid(): i for i, processo in enumerate(self.processos_copy)}

    # Imprime coluna com PID dos Processos
     self.titulo = Label(self.viz_window, text='PIDs')
     self.titulo.grid(row=0, column=0, columnspan=1)

     for i in row_dict:
        label = Label(self.viz_window, text=f'{i}:')
        label.grid(row=1 + row_dict[i], column=0, columnspan=1)

     max_columns = 100  # Define um valor máximo para as colunas
     while len(lista_processos) > 0 or len(lista_chegou) > 0:
        # Adiciona processos que chegaram até o momento
        while lista_processos and lista_processos[0].get_chegada() <= clock:
            lista_chegou.append(lista_processos.pop(0))

        lista_chegou[1:] = sorted(lista_chegou[1:], key=lambda processo: processo.get_tempo_execucao())  # Ordena por tempo de execução

        if lista_chegou:
            cur_processo = lista_chegou[0].pid
            if clock >= max_columns:
                break  # Evita acessar colunas fora dos limites
            
            if lista_exec[cur_processo] <= 0:
                lista_chegou.pop(0)
                continue

            lista_exec[cur_processo] -= 1

            label = Label(self.viz_window, text='\u25A0')  # Executando
            label.grid(row=1 + row_dict[cur_processo], column=1 + clock, columnspan=1)

            for i in lista_chegou:
                if i.get_pid() != cur_processo:
                    cur = i.get_pid()
                    label = Label(self.viz_window, text='\u25A9')  # Esperando
                    label.grid(row=1 + row_dict[cur], column=1 + clock, columnspan=1)

            clock += 1
        else:
            if clock >= max_columns:
                break  # Evita acessar colunas fora dos limites
            
            label = Label(self.viz_window, text='\u25A1')  # Espaço Vazio
            label.grid(row=1, column=1 + clock, columnspan=1)
            clock += 1

     return None

        
        
    def roundRobin(self, quantum, sobrecarga) -> None:
     self.viz_window = Toplevel(self)
     self.viz_window.geometry('800x250')
    
     clock = 0
     lista_processos = sorted(self.processos_copy, key=lambda processo: processo.get_chegada())  # Ordena por tempo de chegada
     fila_processos = []
     lista_exec = [processo.exec for processo in self.processos_copy]  # Lista dos tempos de execução restantes
    
    # Associa cada Processo a uma linha na janela de visualização
     row_dict = {processo.get_pid(): i for i, processo in enumerate(self.processos_copy)}

    # Imprime coluna com PID dos Processos
     self.titulo = Label(self.viz_window, text='PIDs')
     self.titulo.grid(row=0, column=0, columnspan=1)

     for i in row_dict:
        label = Label(self.viz_window, text=f'{i}:')
        label.grid(row=1 + row_dict[i], column=0, columnspan=1)
    
     while len(lista_processos) > 0 or len(fila_processos) > 0:
        # Adiciona processos que chegaram até o momento
        while lista_processos and lista_processos[0].get_chegada() <= clock:
            fila_processos.append(lista_processos.pop(0))

        if fila_processos:
            processo_atual = fila_processos.pop(0)
            pid = processo_atual.get_pid()
            exec_time = min(quantum, lista_exec[pid])  # Tempo a ser executado no quantum
            
            # Executa o processo
            for _ in range(exec_time):
                label = Label(self.viz_window, text='\u25A0')  # Executando
                label.grid(row=1 + row_dict[pid], column=1 + clock, columnspan=1)

                # Processos em espera
                for p in fila_processos:
                    cur = p.get_pid()
                    label = Label(self.viz_window, text='\u25A9')  # Esperando
                    label.grid(row=1 + row_dict[cur], column=1 + clock, columnspan=1)

                clock += 1
            
            lista_exec[pid] -= exec_time  # Subtrai o tempo executado
            
            if lista_exec[pid] > 0:
                fila_processos.append(processo_atual)  # Reinsere no final da fila se ainda não terminou
            
            # Verifica se o processo terminou dentro do quantum
            if lista_exec[pid] > 0:
                # Adiciona sobrecarga
                for _ in range(sobrecarga):
                    for p in fila_processos:
                        cur = p.get_pid()
                        label = Label(self.viz_window, text='\u26DE')  # Bola cortada (sobrecarga)
                        label.grid(row=1 + row_dict[cur], column=1 + clock, columnspan=1)
                    clock += 1
        else:
            # Se nenhum processo está disponível, avança o tempo
            label = Label(self.viz_window, text='\u25A1')  # Espaço Vazio
            label.grid(row=1, column=1 + clock, columnspan=1)
            clock += 1

     return None




    def EDF(self, quantum, sobrecarga) -> None:
     self.viz_window = Toplevel(self)
     self.viz_window.geometry('400x400') 
            
     clock = 0
     lista_processos = sorted(self.processos_copy, key=lambda processo: processo.get_chegada())
     fila_processos = []
    
     while lista_processos or fila_processos:
        # Adiciona processos que chegaram até o momento
        while lista_processos and lista_processos[0].get_chegada() <= clock:
            fila_processos.append(lista_processos.pop(0))
        
        if fila_processos:
            fila_processos.sort(key=lambda p: p.get_deadline())  # Ordena por deadline
            processo = fila_processos[0]
            processo.set_tempo_execucao(processo.get_tempo_execucao() - 1)
            
            label = Label(self.viz_window, text=f'\u25A0{processo.get_pid()}')
            label.grid(row=1000 + fila_processos.index(processo), column=clock, columnspan=1)
            
            if processo.get_tempo_execucao() <= 0:
                fila_processos.pop(0)

        else:
            # Se nenhum processo está disponível, avança o tempo
            label = Label(self.viz_window, text=' ')
            label.grid(row=1000, column=clock, columnspan=1)
        
        clock += 1
