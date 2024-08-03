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
        self.run_button = Button(self, text='RUN', font=('Arial 20 bold'), command=lambda: [self.viz_window(), self.escalonador()])
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
            for i in range(pid_to_remove, len(self.processos)):
                self.processos[i].pid -= 1 
                new_pid = self.processos[i].pid
            
                output, delete_button = self.widgets.pop(new_pid + 1) 
                output.config(text=f"PID:{new_pid}  Tempo de Chegada:{self.processos[i].get_chegada()}  Tempo de Execução:{self.processos[i].get_tempo_execucao()}  Deadline:{self.processos[i].get_deadline()}")
                self.widgets[new_pid] = (output, delete_button)  
        
        
            self.pid_counter -= 1
    
    def escalonador(self) -> None:
        if self.algoritmo_input is not None:
            self.quantum=int(self.quantum_input.get())
            self.sobrecarga=int(self.sobrecarga_input.get())
            algoritmo=self.algoritmo_input.get()
            if algoritmo == "FIFO":
              self.FIFO()
            elif algoritmo == "SJF":
              self.SJF()
            elif algoritmo == "ROUND ROBIN":
              self.roundRobin(self.quantum, self.sobrecarga)
            elif algoritmo == "EDF":
              self.EDF()
    
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
    

    def viz_window(self) -> None: # JANELA PARA VISUALIÇAO DO GRAFICO
        self.viz_window = Toplevel(self)
        self.viz_window.geometry('400x400')   

    
    def FIFO(self) -> None:
            
            self.viz_window = Toplevel(self)
            self.viz_window.geometry('400x400') 
            
            clock = 0
            
            lista_processos = sorted(self.processos, key=lambda processo: processo.get_chegada())

            row_dict = {}
            
            for i in range(len(lista_processos)):
                row_dict[lista_processos[i].pid] = i
            
            while len(lista_processos) > 0:
                cur_pid = lista_processos[0].pid 
                
                if lista_processos[0].get_tempo_execucao() <= 0:
                    lista_processos.pop(0)
                    clock  += 1
                    continue
            
                if lista_processos[0].get_chegada() > clock: 
                    clock += 1
                    label = Label(self.viz_window, text = '\u25A1')
                    label.grid(row = 1000 + row_dict[cur_pid], column = clock, columnspan=1)
                    continue
                
                cur_pid = lista_processos[0].pid 

                temp = lista_processos[0].get_tempo_execucao()
                lista_processos[0].set_tempo_execucao(temp-1)
                
                label = Label(self.viz_window, text = '\u25A0')
                label.grid(row = 1000 + row_dict[cur_pid], column = clock, columnspan=1)

                clock += 1

            return None
        
    def SJF(self) -> None:
     clock = 0
     lista_processos = sorted(self.processos, key=lambda processo: processo.get_chegada())
    
     while lista_processos:
        # Adiciona processos que chegaram até o momento
        processos_disponiveis = [p for p in lista_processos if p.get_chegada() <= clock]
        
        if processos_disponiveis:
            # Seleciona o processo com menor tempo de execução
            processo = min(processos_disponiveis, key=lambda p: p.get_tempo_execucao())
            processo.set_tempo_execucao(processo.get_tempo_execucao() - 1)
            
            label = Label(self.viz_window, text=f'\u25A0{processo.get_pid()}')
            label.grid(row=1000 + lista_processos.index(processo), column = clock, columnspan=1)
            
            if processo.get_tempo_execucao() <= 0:
                lista_processos.remove(processo)
        else:
            # Se nenhum processo está disponível, avança o tempo
            label = Label(self.viz_window, text=' ')
            Label(self.viz_window, text='').grid(row=row + 1, column=clock, columnspan=1)

        
        clock += 1
         
     return None
        
        
    def roundRobin(self, quantum, sobrecarga) -> None:
     timer = 0
     lista_de_processos_disponiveis = []
     lista_de_processos_ja_executados = []
     tempo_de_execucao_do_primeiro_processo = 0
    
    # Põe o pid na grade
     row_dict = {processo.get_pid(): i for i, processo in enumerate(self.processos)}

     while len(lista_de_processos_ja_executados) < len(self.processos):
        processo_em_espera = True  # Suponha que o processo esteja em espera até que seja iniciado
        
        # Adiciona processos disponíveis à lista
        for processo in self.processos:
            if processo.get_chegada() == timer:
                if processo not in lista_de_processos_disponiveis and processo not in lista_de_processos_ja_executados:
                    lista_de_processos_disponiveis.append(processo)
        
        # Visualização
        for processo in self.processos:
            if processo.get_chegada() <= timer and processo not in lista_de_processos_disponiveis and processo not in lista_de_processos_ja_executados:
                processo_em_espera = True
                label = Label(self.viz_window, bg='yellow', width=2, height=2)
                label.grid(row=1000 + row_dict[processo.get_pid()], column=timer, columnspan=1)
        
        for processo in lista_de_processos_disponiveis:
            if processo.get_tempo_execucao() > 0:
                label = Label(self.viz_window, bg='green', width=2, height=2)  # Bloco verde para execução
                label.grid(row=1000 + row_dict[processo.get_pid()], column=timer, columnspan=1)

        if processo_em_espera:
            label = Label(self.viz_window, bg='yellow', width=2, height=2)
            label.grid(row=1000 + row_dict[processo.get_pid()], column=timer, columnspan=1)

        # Executa o processo atual
        if lista_de_processos_disponiveis:
            processo_atual = lista_de_processos_disponiveis[0]
            if processo_atual.get_tempo_execucao() > 0:
                processo_atual.set_tempo_execucao(processo_atual.get_tempo_execucao() - 1)
                tempo_de_execucao_do_primeiro_processo += 1
                if tempo_de_execucao_do_primeiro_processo == quantum:
                    lista_de_processos_disponiveis.append(lista_de_processos_disponiveis.pop(0))  # Rotaciona o processo
                    tempo_de_execucao_do_primeiro_processo = 0
                    # Adiciona sobrecarga
                    label = Label(self.viz_window, bg='red', width=2, height=2)
                    label.grid(row=1000 + row_dict[processo_atual.get_pid()], column=timer, columnspan=1)
                    timer += sobrecarga  # Adiciona sobrecarga

            if processo_atual.get_tempo_execucao() <= 0:
                lista_de_processos_ja_executados.append(lista_de_processos_disponiveis.pop(0))

        timer += 1  # Avança o tempo

    # Ajuste final para a última linha no gráfico
     for processo in self.processos:
        if processo.get_tempo_execucao() <= 0:
            row_dict.pop(processo.get_pid())
       
     return None


    def EDF(self) -> None:
     clock = 0
     lista_processos = sorted(self.processos, key=lambda processo: processo.get_chegada())
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
