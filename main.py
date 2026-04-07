import tkinter as tk
from tkinter import ttk, messagebox
import time
from inventario_loja import inventory_initial

# Configuração de Estilo (Cores Modernas)
CORES = {"bg": "#121212", "card": "#1E1E1E", "acc": "#0078D4", "txt": "#FFFFFF", "muted": "#AAAAAA"}

class Peca:
    def __init__(self, nome, categoria, preco):
        self.nome, self.categoria, self.preco = nome, categoria, float(preco)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão de Estoque")
        self.geometry("880x520")
        self.configure(bg=CORES["bg"])
        
        # Dados originais
        self.estoque = [Peca(p["nome"], p["categoria"], p["preco"]) for p in inventory_initial]
        
        self._configurar_temas()
        self._criar_layout_base()
        self.abrir_inventario()

    def _configurar_temas(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=CORES["card"], foreground=CORES["txt"], 
                        fieldbackground=CORES["card"], rowheight=28, borderwidth=0)
        style.configure("Treeview.Heading", background="#2D2D2D", foreground=CORES["acc"], relief="flat")
        style.map("Treeview", background=[("selected", CORES["acc"])])

    def _criar_layout_base(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg="#181818", width=180)
        self.sidebar.pack(side="left", fill="y")
        
        tk.Label(self.sidebar, text="ESTOQUE", bg="#181818", fg=CORES["acc"], font=("Arial", 12, "bold")).pack(pady=25)
        
        botoes = [("Inventário", self.abrir_inventario), ("Cadastrar", self.abrir_cadastro), ("Buscar", self.abrir_busca)]
        for texto, comando in botoes:
            tk.Button(self.sidebar, text=texto, command=comando, bg="#181818", fg=CORES["txt"], 
                      relief="flat", overrelief="flat", activebackground=CORES["acc"], 
                      cursor="hand2", font=("Arial", 10)).pack(fill="x", ipady=10, padx=10, pady=2)

        # Área de Conteúdo
        self.container = tk.Frame(self, bg=CORES["bg"])
        self.container.pack(side="right", expand=True, fill="both", padx=20, pady=20)

    def limpar_tela(self):
        for w in self.container.winfo_children(): w.destroy()

    def abrir_inventario(self):
        self.limpar_tela()
        tk.Label(self.container, text="Lista de Itens", bg=CORES["bg"], fg=CORES["txt"], font=("Arial", 14)).pack(anchor="w", pady=(0, 10))
        
        colunas = ("cat", "nome", "preco")
        tv = ttk.Treeview(self.container, columns=colunas, show="headings")
        tv.heading("cat", text="CATEGORIA"); tv.heading("nome", text="PRODUTO"); tv.heading("preco", text="PREÇO")
        tv.column("preco", width=100, anchor="e")
        
        for p in self.estoque:
            tv.insert("", "end", values=(p.categoria, p.nome, f"R$ {p.preco:,.2f}"))
        tv.pack(expand=True, fill="both")

    def abrir_cadastro(self):
        self.limpar_tela()
        f = tk.Frame(self.container, bg=CORES["card"], padx=20, pady=20)
        f.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(f, text="Novo Cadastro", bg=CORES["card"], fg=CORES["txt"], font=("Arial", 12, "bold")).pack(pady=10)
        
        campos = {}
        for label in ["Nome", "Categoria", "Preço"]:
            tk.Label(f, text=label, bg=CORES["card"], fg=CORES["muted"]).pack(anchor="w")
            e = tk.Entry(f, bg=CORES["bg"], fg="white", insertbackground="white", relief="flat", width=30)
            e.pack(pady=(0, 10), ipady=5); campos[label] = e

        def salvar():
            try:
                self.estoque.append(Peca(campos["Nome"].get(), campos["Categoria"].get(), campos["Preço"].get()))
                messagebox.showinfo("Sucesso", "Item adicionado!")
                self.abrir_inventario()
            except: messagebox.showerror("Erro", "Verifique os dados.")

        tk.Button(f, text="SALVAR", command=salvar, bg=CORES["acc"], fg="white", font=("Arial", 10, "bold")).pack(pady=10, fill="x")

    def abrir_busca(self):
        self.limpar_tela()
        tk.Label(self.container, text="Pesquisar Produto", bg=CORES["bg"], fg=CORES["txt"], font=("Arial", 14)).pack(anchor="w")
        
        txt_busca = tk.Entry(self.container, bg=CORES["card"], fg="white", font=("Arial", 12), relief="flat")
        txt_busca.pack(fill="x", pady=10, ipady=8)
        
        lbl_res = tk.Label(self.container, text="", bg=CORES["bg"], fg=CORES["acc"], justify="left")
        lbl_res.pack(pady=10, anchor="w")

        def realizar_busca(modo):
            termo = txt_busca.get().lower()
            inicio = time.perf_counter()
            if modo == "bin": self.estoque.sort(key=lambda x: x.nome.lower())
            
            res = next((p for p in self.estoque if p.nome.lower() == termo), None)
            fim = time.perf_counter() - inicio
            
            if res:
                lbl_res.config(text=f"ENCONTRADO: {res.nome} | {res.categoria} | R$ {res.preco:.2f}\nTempo: {fim:.8f}s", fg="#4CAF50")
            else:
                lbl_res.config(text=f"Não encontrado.\nTempo: {fim:.8f}s", fg="#F44336")

        btn_f = tk.Frame(self.container, bg=CORES["bg"])
        btn_f.pack(fill="x")
        tk.Button(btn_f, text="Busca Sequencial", command=lambda: realizar_busca("seq"), bg="#333", fg="white").pack(side="left", padx=5)
        tk.Button(btn_f, text="Busca Binária", command=lambda: realizar_busca("bin"), bg="#333", fg="white").pack(side="left")

if __name__ == "__main__":
    App().mainloop()