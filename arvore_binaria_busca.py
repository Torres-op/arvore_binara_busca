import tkinter as tk
from tkinter import messagebox, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from matplotlib.figure import Figure

class No:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = 1

class ArvoreAVL:
    def __init__(self):
        self.raiz = None
    
    def altura(self, no):
        return no.altura if no else 0
    
    def fator_balanceamento(self, no):
        return self.altura(no.esquerda) - self.altura(no.direita) if no else 0
    
    def atualizar_altura(self, no):
        if no:
            no.altura = max(self.altura(no.esquerda), self.altura(no.direita)) + 1
    
    def rotacao_direita(self, y):
        x = y.esquerda
        T2 = x.direita
        
        x.direita = y
        y.esquerda = T2
        
        self.atualizar_altura(y)
        self.atualizar_altura(x)
        
        return x
    
    def rotacao_esquerda(self, x):
        y = x.direita
        T2 = y.esquerda
        
        y.esquerda = x
        x.direita = T2
        
        self.atualizar_altura(x)
        self.atualizar_altura(y)
        
        return y
    
    def balancear(self, no):
        self.atualizar_altura(no)
        fb = self.fator_balanceamento(no)
        
        if fb > 1 and self.fator_balanceamento(no.esquerda) >= 0:
            return self.rotacao_direita(no)
        
        if fb < -1 and self.fator_balanceamento(no.direita) <= 0:
            return self.rotacao_esquerda(no)
        
        if fb > 1 and self.fator_balanceamento(no.esquerda) < 0:
            no.esquerda = self.rotacao_esquerda(no.esquerda)
            return self.rotacao_direita(no)
        
        if fb < -1 and self.fator_balanceamento(no.direita) > 0:
            no.direita = self.rotacao_direita(no.direita)
            return self.rotacao_esquerda(no)
        
        return no
    
    def inserir(self, valor):
        self.raiz = self._inserir_rec(self.raiz, valor)
    
    def _inserir_rec(self, no, valor):
        if not no:
            return No(valor)
        
        if valor < no.valor:
            no.esquerda = self._inserir_rec(no.esquerda, valor)
        elif valor > no.valor:
            no.direita = self._inserir_rec(no.direita, valor)
        else:
            return no 
        
        return self.balancear(no)
    
    def buscar(self, valor):
        return self._buscar_rec(self.raiz, valor)
    
    def _buscar_rec(self, no, valor):
        if not no:
            return None
        if valor == no.valor:
            return no
        if valor < no.valor:
            return self._buscar_rec(no.esquerda, valor)
        return self._buscar_rec(no.direita, valor)
    
    def remover(self, valor):
        self.raiz = self._remover_rec(self.raiz, valor)
    
    def _remover_rec(self, no, valor):
        if not no:
            return None
        
        if valor < no.valor:
            no.esquerda = self._remover_rec(no.esquerda, valor)
        elif valor > no.valor:
            no.direita = self._remover_rec(no.direita, valor)
        else:
            if not no.esquerda and not no.direita:
                return None
            if not no.esquerda:
                return no.direita
            if not no.direita:
                return no.esquerda
            
            sucessor = self._encontrar_minimo(no.direita)
            no.valor = sucessor.valor
            no.direita = self._remover_rec(no.direita, sucessor.valor)
        
        return self.balancear(no)
    
    def _encontrar_minimo(self, no):
        while no.esquerda:
            no = no.esquerda
        return no
    
    def em_ordem(self):
        resultado = []
        self._em_ordem_rec(self.raiz, resultado)
        return resultado
    
    def _em_ordem_rec(self, no, resultado):
        if no:
            self._em_ordem_rec(no.esquerda, resultado)
            resultado.append(no.valor)
            self._em_ordem_rec(no.direita, resultado)
    
    def contar_nos(self):
        return self._contar_nos_rec(self.raiz)
    
    def _contar_nos_rec(self, no):
        if not no:
            return 0
        return 1 + self._contar_nos_rec(no.esquerda) + self._contar_nos_rec(no.direita)

class ArvoreGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌳 Árvore Binária de Busca Balanceada (AVL)")
        self.root.geometry("1400x800")
        self.root.configure(bg='#1e293b')
        
        self.arvore = ArvoreAVL()
        self.destacado = None
        
        self.criar_interface()
        self.gerar_arvore_inicial()
    
    def criar_interface(self):
        main_frame = tk.Frame(self.root, bg='#1e293b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_frame = tk.Frame(main_frame, bg='#334155', relief=tk.RAISED, borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5), pady=0)
        
        title = tk.Label(left_frame, text="🌳 Árvore Binária de Busca", 
                        font=('Arial', 20, 'bold'), 
                        bg='#334155', fg='white')
        title.pack(pady=15)
        
        lista_frame = tk.LabelFrame(left_frame, text="Lista Inicial", 
                                   font=('Arial', 12, 'bold'),
                                   bg='#334155', fg='white',
                                   padx=10, pady=10)
        lista_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.lista_text = scrolledtext.ScrolledText(lista_frame, height=4, 
                                                    font=('Arial', 10),
                                                    bg='#475569', fg='white',
                                                    insertbackground='white')
        self.lista_text.pack(fill=tk.X, pady=5)
        self.lista_text.insert('1.0', '15,10,20,8,12,17,25,6,11,14,19,30,5,13,18,22,35,3,7,16,21,27,40,2,4')
        
        btn_gerar = tk.Button(lista_frame, text="🎲 Gerar Árvore", 
                             command=self.gerar_arvore_inicial,
                             font=('Arial', 11, 'bold'),
                             bg='#8b5cf6', fg='white',
                             activebackground='#7c3aed',
                             cursor='hand2', relief=tk.RAISED, borderwidth=2)
        btn_gerar.pack(fill=tk.X, pady=5)
        
        op_frame = tk.LabelFrame(left_frame, text="Operações", 
                                font=('Arial', 12, 'bold'),
                                bg='#334155', fg='white',
                                padx=10, pady=10)
        op_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(op_frame, text="Valor:", font=('Arial', 11),
                bg='#334155', fg='white').pack(anchor='w')
        
        self.entrada = tk.Entry(op_frame, font=('Arial', 12),
                               bg='#475569', fg='white',
                               insertbackground='white',
                               relief=tk.SOLID, borderwidth=2)
        self.entrada.pack(fill=tk.X, pady=5)
        self.entrada.bind('<Return>', lambda e: self.inserir())
        
        btn_inserir = tk.Button(op_frame, text="➕ Inserir", 
                               command=self.inserir,
                               font=('Arial', 11, 'bold'),
                               bg='#10b981', fg='white',
                               activebackground='#059669',
                               cursor='hand2', relief=tk.RAISED, borderwidth=2)
        btn_inserir.pack(fill=tk.X, pady=3)
        
        btn_buscar = tk.Button(op_frame, text="🔍 Buscar", 
                              command=self.buscar,
                              font=('Arial', 11, 'bold'),
                              bg='#3b82f6', fg='white',
                              activebackground='#2563eb',
                              cursor='hand2', relief=tk.RAISED, borderwidth=2)
        btn_buscar.pack(fill=tk.X, pady=3)
        
        btn_remover = tk.Button(op_frame, text="🗑️ Remover", 
                               command=self.remover,
                               font=('Arial', 11, 'bold'),
                               bg='#ef4444', fg='white',
                               activebackground='#dc2626',
                               cursor='hand2', relief=tk.RAISED, borderwidth=2)
        btn_remover.pack(fill=tk.X, pady=3)
        
        btn_limpar = tk.Button(op_frame, text="🔄 Limpar Árvore", 
                              command=self.limpar,
                              font=('Arial', 11, 'bold'),
                              bg='#6b7280', fg='white',
                              activebackground='#4b5563',
                              cursor='hand2', relief=tk.RAISED, borderwidth=2)
        btn_limpar.pack(fill=tk.X, pady=3)
        
        info_frame = tk.LabelFrame(left_frame, text="📊 Estatísticas", 
                                  font=('Arial', 12, 'bold'),
                                  bg='#334155', fg='white',
                                  padx=10, pady=10)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.label_total = tk.Label(info_frame, text="Total de nós: 0",
                                   font=('Arial', 10),
                                   bg='#334155', fg='#93c5fd',
                                   anchor='w')
        self.label_total.pack(fill=tk.X, pady=2)
        
        self.label_altura = tk.Label(info_frame, text="Altura: 0",
                                    font=('Arial', 10),
                                    bg='#334155', fg='#93c5fd',
                                    anchor='w')
        self.label_altura.pack(fill=tk.X, pady=2)
        
        self.label_msg = tk.Label(left_frame, text="",
                                 font=('Arial', 10, 'bold'),
                                 bg='#334155', fg='#fbbf24',
                                 wraplength=280,
                                 justify='center')
        self.label_msg.pack(pady=10)
        
        right_frame = tk.Frame(main_frame, bg='#1e293b')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.fig = Figure(figsize=(10, 8), facecolor='#1e293b')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#0f172a')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def mostrar_mensagem(self, msg):
        self.label_msg.config(text=msg)
        self.root.after(3000, lambda: self.label_msg.config(text=""))
    
    def gerar_arvore_inicial(self):
        try:
            texto = self.lista_text.get('1.0', tk.END).strip()
            numeros = [int(n.strip()) for n in texto.split(',') if n.strip()]
            
            if not numeros:
                messagebox.showwarning("Aviso", "Lista vazia!")
                return
            
            self.arvore = ArvoreAVL()
            for num in numeros:
                self.arvore.inserir(num)
            
            self.destacado = None
            self.mostrar_mensagem(f"✅ Árvore criada com {len(numeros)} elementos!")
            self.atualizar_visualizacao()
            
        except ValueError:
            messagebox.showerror("Erro", "Lista contém valores inválidos!")
    
    def inserir(self):
        try:
            valor = int(self.entrada.get())
            
            if self.arvore.buscar(valor):
                messagebox.showwarning("Aviso", f"O valor {valor} já existe!")
                return
            
            self.arvore.inserir(valor)
            self.destacado = valor
            self.entrada.delete(0, tk.END)
            self.mostrar_mensagem(f"✅ Valor {valor} inserido e balanceado!")
            self.atualizar_visualizacao()
            
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido!")
    
    def buscar(self):
        try:
            valor = int(self.entrada.get())
            
            if self.arvore.buscar(valor):
                self.destacado = valor
                self.mostrar_mensagem(f"✅ Valor {valor} encontrado!")
                self.atualizar_visualizacao()
            else:
                self.destacado = None
                messagebox.showinfo("Busca", f"Valor {valor} não encontrado!")
                
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido!")
    
    def remover(self):
        try:
            valor = int(self.entrada.get())
            
            if not self.arvore.buscar(valor):
                messagebox.showwarning("Aviso", f"Valor {valor} não existe!")
                return
            
            self.arvore.remover(valor)
            self.destacado = None
            self.entrada.delete(0, tk.END)
            self.mostrar_mensagem(f"✅ Valor {valor} removido e rebalanceado!")
            self.atualizar_visualizacao()
            
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido!")
    
    def limpar(self):
        self.arvore = ArvoreAVL()
        self.destacado = None
        self.entrada.delete(0, tk.END)
        self.mostrar_mensagem("🗑️ Árvore limpa!")
        self.atualizar_visualizacao()
    
    def criar_grafo(self, no, G, pos, x=0, y=0, nivel=1, espacamento=1.0):
        if no:
            G.add_node(no.valor)
            pos[no.valor] = (x, y)
            
            if no.esquerda:
                G.add_edge(no.valor, no.esquerda.valor)
                novo_espacamento = espacamento / 2
                self.criar_grafo(no.esquerda, G, pos, 
                               x - espacamento, y - 1, nivel + 1, novo_espacamento)
            
            if no.direita:
                G.add_edge(no.valor, no.direita.valor)
                novo_espacamento = espacamento / 2
                self.criar_grafo(no.direita, G, pos, 
                               x + espacamento, y - 1, nivel + 1, novo_espacamento)
    
    def atualizar_visualizacao(self):
        self.ax.clear()
        self.ax.set_facecolor('#0f172a')
        self.ax.axis('off')
        
        if not self.arvore.raiz:
            self.ax.text(0.5, 0.5, 'Árvore Vazia\nInsira elementos para visualizar',
                        horizontalalignment='center',
                        verticalalignment='center',
                        transform=self.ax.transAxes,
                        fontsize=16, color='white',
                        bbox=dict(boxstyle='round', facecolor='#334155', alpha=0.8))
            self.canvas.draw()
            self.atualizar_estatisticas()
            return
        
        G = nx.DiGraph()
        pos = {}
        self.criar_grafo(self.arvore.raiz, G, pos)
        
        node_colors = []
        for node in G.nodes():
            if node == self.destacado:
                node_colors.append('#10b981')
            else:
                node_colors.append('#3b82f6')
        
        nx.draw(G, pos, ax=self.ax,
               node_color=node_colors,
               node_size=800,
               with_labels=True,
               font_size=12,
               font_weight='bold',
               font_color='white',
               edge_color='#94a3b8',
               width=2,
               arrows=False,
               linewidths=2,
               edgecolors='#1e40af')
        
        self.canvas.draw()
        self.atualizar_estatisticas()
    
    def atualizar_estatisticas(self):
        total = self.arvore.contar_nos()
        altura = self.arvore.altura(self.arvore.raiz) if self.arvore.raiz else 0
        
        self.label_total.config(text=f"Total de nós: {total}")
        self.label_altura.config(text=f"Altura: {altura}")

def main():
    root = tk.Tk()
    app = ArvoreGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
