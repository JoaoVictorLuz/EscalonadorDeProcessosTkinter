from tkinter import *
from tkinter import ttk
from algoritmosDeFato import *

class Processo:
    def __init__(self, pid, tempo_chegada: int, tempo_execucao: int, deadline: int) -> None:
        self.pid = pid
        self.chegada = tempo_chegada
        self.exec = tempo_execucao
        self.deadline = deadline

    
    def get_pid(self) -> int:
        return (self.pid)
    
    def get_chegada(self) -> int:
        return self.chegada
    
    def get_tempo_execucao(self) -> int:
        return self.exec
    
    def set_tempo_execucao(self, tempo_execucao: int) -> None:
        self.exec = tempo_execucao
        return None
    
    def get_deadline(self) -> int:
        return self.deadline
    
    
    def set_deadline(self, deadline: int) -> None:
        self.deadline = deadline
        return None