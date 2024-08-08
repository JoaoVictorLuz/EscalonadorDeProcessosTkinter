from tkinter import *
from tkinter import ttk
from tkinter import font
from Processo import *
from Algoritmos import * 

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

    def legenda(self, vizwindow, dict):
        legenda_exec = Label(vizwindow, text="Executando: \u25A0")
        legenda_exec.grid(row=len(dict) + 3, column=0, columnspan=1)
        legenda_espera = Label(vizwindow, text="Espera: \u22A0")
        legenda_espera.grid(row=len(dict) + 4, column=0, columnspan=1)
        lengenda_sobrecarga = Label(vizwindow, text="Sobrecarga: \u26DE")
        lengenda_sobrecarga.grid(row=len(dict) + 5, column=0, columnspan=1)
        nada_executa = Label(vizwindow, text="Sem processos: \u25A1")
        nada_executa.grid(row=len(dict) + 6, column= 0, columnspan=1)
        legenda_deadline = Label(vizwindow, text="Ultrapassou Deadline(EDF): \u25A3")
        legenda_deadline.grid(row=len(dict) + 7, column=0, columnspan=1)
        return None

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
        algoritmo = self.algoritmo_input.get()
        self.processos_copy = [Processo(p.get_pid(), p.get_chegada(), p.get_tempo_execucao(), p.get_deadline()) for p in self.processos]
        if algoritmo == "FIFO":
            FIFO(self)
        elif algoritmo == "SJF":
            SJF(self)
        elif algoritmo == "ROUND ROBIN":
            quantum = int(self.quantum_input.get())
            sobrecarga = int(self.sobrecarga_input.get())
            roundRobin(self, quantum, sobrecarga)
        elif algoritmo == "EDF":
            quantum = int(self.quantum_input.get())
            sobrecarga = int(self.sobrecarga_input.get())
            EDF(self, quantum, sobrecarga)

    
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
    
   





