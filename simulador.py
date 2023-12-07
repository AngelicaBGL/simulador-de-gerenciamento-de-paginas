import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class Pagina:
    def __init__(self, id_pagina):
        self.id_pagina = id_pagina
        self.bit_referencia = 0

class Memoria:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.paginas = []
        self.operacoes_contador = 0
        self.limpar_bits_referencia_intervalo = 5  # Intervalo padrão para limpar bits de referência

    def adicionar_pagina(self, pagina):
        if len(self.paginas) < self.capacidade:
            self.paginas.append(pagina)
        else:
            while True:
                pagina_mais_antiga = self.paginas.pop(0)
                if pagina_mais_antiga.bit_referencia == 0:
                    break
                else:
                    pagina_mais_antiga.bit_referencia = 0
                    self.paginas.append(pagina_mais_antiga)

            self.paginas.append(pagina)
            self.paginas[-1].bit_referencia = 1

        self.operacoes_contador += 1
        if self.operacoes_contador >= self.limpar_bits_referencia_intervalo:
            self.limpar_bits_referencia()
            self.operacoes_contador = 0

    def limpar_bits_referencia(self):
        for pagina in self.paginas:
            pagina.bit_referencia = 0

    def exibir_status_memoria(self):
        status = ""
        for pagina in self.paginas:
            status += f"Página {pagina.id_pagina}: Referenciada = {pagina.bit_referencia}\n"
        return status

class AlgoritmoSegundaChance:
    @staticmethod
    def substituir_pagina(memoria, nova_pagina):
        while True:
            pagina_mais_antiga = memoria.paginas.pop(0)
            if pagina_mais_antiga.bit_referencia == 0:
                break
            else:
                pagina_mais_antiga.bit_referencia = 0
                memoria.paginas.append(pagina_mais_antiga)

        memoria.paginas.append(nova_pagina)

class SimuladorGerenciadorPagina:
    #interface grafica
    def __init__(self, mestre):
        self.mestre = mestre
        mestre.title("Simulador de Gerenciamento de Páginas")
        mestre.configure(bg='#4B0082')  

        self.memoria = None
        self.algoritmo_segunda_chance = AlgoritmoSegundaChance()

        # Componentes da interface
        self.rotulo = tk.Label(mestre, text="Selecione um arquivo:",bg='#4B0082')
        self.rotulo.pack()

        self.botao_carregar = tk.Button(mestre, text="Carregar Arquivo",bg='#9370DB', fg="white", command=self.carregar_arquivo)
        self.botao_carregar.pack()

    
        self.exibicao_texto = tk.Text(mestre, height=30, width=50,bg='#8A2BE2', fg="white")
        self.exibicao_texto.pack()


        self.configurar_memoria_entry = tk.Entry(mestre)
        self.configurar_memoria_entry.insert(tk.END, "5")  # Valor padrão para o tamanho da memória
        self.configurar_memoria_entry.configure(bg='#8A2BE2', fg="white")
        self.configurar_memoria_label = tk.Label(mestre, text="Tamanho da Memória:",bg='#4B0082', fg="white")
        self.configurar_memoria_label.pack()
        self.configurar_memoria_entry.pack()

        self.configurar_intervalo_entry = tk.Entry(mestre)
        self.configurar_intervalo_entry.insert(tk.END, "5")  # Valor padrão para o intervalo de limpeza de bits
        self.configurar_intervalo_entry.configure(bg='#8A2BE2', fg="white")
        self.configurar_intervalo_label = tk.Label(mestre, text="Intervalo para Limpar Bits:",bg='#4B0082', fg="white")
        self.configurar_intervalo_label.pack()
        self.configurar_intervalo_entry.pack()

        self.botao_simular_tudo = tk.Button(mestre, text="Simular Tudo",bg='#4B0082', fg="white", command=self.simular_tudo)
        self.botao_simular_tudo.pack()

        self.botao_simular_passo_a_passo = tk.Button(mestre, text="Simular Passo a Passo",bg='#4B0082', fg="white", command=self.simular_passo_a_passo)
        self.botao_simular_passo_a_passo.pack()

        # Variáveis de controle
        self.total_page_faults = 0
        self.requisicoes_pagina = []
        self.simulacao_passo_a_passo = False

    def carregar_arquivo(self):
        # Diálogo para selecionar arquivo
        caminho_arquivo = filedialog.askopenfilename()
        if caminho_arquivo:
            # Lê o conteúdo do arquivo e converte para lista de inteiros
            with open(caminho_arquivo, 'r') as arquivo:
                self.requisicoes_pagina = [int(id_pagina) for id_pagina in arquivo.read().split(',')]
                self.exibicao_texto.insert(tk.END, "Arquivo carregado.\n")

    def simular_tudo(self):
        self.total_page_faults = 0
        self.simulacao_passo_a_passo = False
        self.iniciar_simulacao()

    def simular_passo_a_passo(self):
        self.total_page_faults = 0
        self.simulacao_passo_a_passo = True
        self.iniciar_simulacao()

    def configurar_memoria(self):
        # Configura a memória com base nos valores inseridos pelo usuário na interface
        capacidade_memoria = int(self.configurar_memoria_entry.get())
        self.memoria = Memoria(capacidade_memoria)

        intervalo_limpeza_bits = int(self.configurar_intervalo_entry.get())
        self.memoria.limpar_bits_referencia_intervalo = intervalo_limpeza_bits

    def iniciar_simulacao(self):
        if not self.requisicoes_pagina:
            self.exibicao_texto.insert(tk.END, "Carregue um arquivo antes de simular.\n")
            return

        self.configurar_memoria()

        for id_pagina in self.requisicoes_pagina:
            nova_pagina = Pagina(id_pagina)
            pagina_presente = any(pagina.id_pagina == nova_pagina.id_pagina for pagina in self.memoria.paginas)

            if not pagina_presente:
                self.memoria.adicionar_pagina(nova_pagina)
                self.total_page_faults += 1
                self.exibicao_texto.insert(tk.END, f"Página {id_pagina} carregada na memória.\n")
            else:
                self.exibicao_texto.insert(tk.END, f"Página {id_pagina} já está na memória.\n")

            self.exibicao_texto.insert(tk.END, self.memoria.exibir_status_memoria() + "\n")
            self.exibicao_texto.see(tk.END)  # Rolar para a parte inferior

            if self.simulacao_passo_a_passo:
                self.mestre.update()
                self.mestre.after(1000)  # Aguarda 1 segundo entre os passos

        self.exibicao_texto.insert(tk.END, f"Total de page faults: {self.total_page_faults}\n")

if __name__ == "__main__":
    root = tk.Tk()
    simulador = SimuladorGerenciadorPagina(root)
    root.mainloop()#loop para deixar a janela sempre aberta
