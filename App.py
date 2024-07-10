from tkinter import *
from tkinter import ttk
from algoritmosDeFato import *
from Processo import *

class App(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry('700x450')
        self.title('Simulador SO')
        self.config(bg="gray")
        self.pid_counter = 0
        self.processos = []   
        self.input_widget()             # Faz aparecer caixas de entrada na tela inicial
        self.buttons_beginning()        # Faz aparecer botôes na tela inicial



    def buttons_beginning(self):
        self.new_process_button = Button(self, text='Criar Processo', font=('Arial 10 bold'), command=self.create_process)
        self.new_process_button.grid(row=2, column=0, columnspan=5, padx=5, pady=5)
        self.run_button = Button(self, text='RUN', font=('Arial 10 bold'), command=self.escalonador)
        self.run_button.grid(row=2, column=20, columnspan=5)          
        
        
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
        self.chegada_label = Label(self, text='Tempo de Chegada')
        self.chegada_label.grid(row = 0, column= 0, padx=5, pady=5)
        self.chegada_input = Entry(self, width = 10)
        self.chegada_input.grid(row=1, column=0)

        self.tempo_execucao_label = Label(self, text='Tempo de Execução')
        self.tempo_execucao_label.grid(row=0, column=1, padx=5, pady=5)
        self.tempo_execucao_input = Entry(self, width = 10)
        self.tempo_execucao_input.grid(row=1, column=1)

        self.deadline_label = Label(self, text = 'Deadline')
        self.deadline_label.grid(row=0, column=2, padx=5, pady=5)
        self.deadline_input = Entry(self, width = 8)
        self.deadline_input.grid(row=1, column=2, padx=5, pady=5)

        self.quantum_label = Label(self, text = 'Quantum')
        self.quantum_label.grid(row=0, column=3, padx=5, pady=5)
        self.quantum_input = Entry(self, width = 8)
        self.quantum_input.grid(row=1, column=3, padx=5, pady=5)
        
        self.sobrecarga_label = Label(self, text = 'Sobrecarga do Sistema')
        self.sobrecarga_label.grid(row=0, column=4, padx=5, pady=5)
        self.sobrecarga_input = Entry(self, width = 10)
        self.sobrecarga_input.grid(row=1, column=4)

        self.algoritmo_label = Label (self, text = 'Algoritmo de Escalonamento')
        self.algoritmo_label.grid(row=0, column=20, padx=5, pady=5)
        itens = ['FIFO', 'SJF', 'ROUND ROBIN', 'EDF']
        self.algoritmo_input = ttk.Combobox (self,values=itens)
        self.algoritmo_input.grid(row=1, column=20)



    def output_process(self, process: Processo) -> None:
        self.output = Label(self, text = f"PID:{process.get_pid()}  Tempo de Chegada:{process.get_chegada()}  Tempo de Execução:{process.get_tempo_execucao()}  Deadline:{process.get_deadline()}")
        self.output.grid(columnspan = 3)
        self.processos.append(process)

    def escalonador(self) -> None:
        if self.algoritmo_input is not None:
            self.quantum=int(self.quantum_input.get())
            self.sobrecarga=int(self.sobrecarga_input.get())
            algoritmo=self.algoritmo_input.get()
            if algoritmo == "FIFO":
                return fifo(self.processos)
            if algoritmo == "SJF":
                return sjf(self.processos)
            if algoritmo == "ROUND ROBIN":
                return roundRobin(self.processos, self.quantum, self.sobrecarga )
            if algoritmo == "EDF":
                return edf(self.processos, self.quantum, self.sobrecarga)
