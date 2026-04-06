# interface.py
# Interface grafica para o sistema de estoque usando Tkinter (biblioteca padrao do Python).
# Esse arquivo substitui o loop de terminal do main.py — a logica de negocio
# (cadastro, busca sequencial, busca binaria) foi copiada daqui e adaptada
# para retornar valores em vez de printar direto no console.
#
# Para rodar: python interface.py
# Dependencias: nenhuma alem do Python padrao (3.10+)

import tkinter as tk
from tkinter import ttk
import time
import re
import sys
import os

# Garante que o Python encontre o inventario_loja.py mesmo se o script
# for chamado de outro diretorio. Sem isso, o import quebra dependendo
# de onde voce esta no terminal.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inventario_loja import inventory_initial


# ---------------------------------------------------------------------------
# Modelo de dados
# ---------------------------------------------------------------------------

class Peca:
    """Representa uma peca no estoque."""
    def __init__(self, nome, categoria, preco):
        self.nome = nome
        self.categoria = categoria
        self.preco = preco  # float, sempre positivo


# Lista global que guarda todas as pecas cadastradas.
# Optei por lista simples igual ao main.py para nao mudar a estrutura.
estoque: list[Peca] = []


# ---------------------------------------------------------------------------
# Logica de negocio (mesma do main.py, so que sem print/input)
# ---------------------------------------------------------------------------

def validar_nome_peca(nome: str) -> bool:
    """
    Aceita letras (incluindo acentuadas), numeros, espacos e hifen.
    Rejeita nomes vazios ou com caracteres especiais tipo @, !, /, etc.
    """
    return bool(re.fullmatch(r"[A-Za-z0-9À-ÿ \-]+", nome.strip()))


def cadastrar_peca(nome: str, categoria: str, preco, silencioso=False) -> bool:
    """
    Valida e adiciona uma peca ao estoque global.
    Retorna True se deu certo, False se o nome ou preco for invalido.
    O parametro 'silencioso' existe so pra compatibilidade com o carregamento
    inicial — nao muda nada no comportamento.
    """
    if not validar_nome_peca(nome):
        return False

    # Tenta converter o preco para float — pode vir como string do campo de texto
    try:
        valor = float(preco)
        if valor < 0:
            return False
    except ValueError:
        return False

    estoque.append(Peca(nome, categoria, valor))
    return True


def buscar_sequencial(nome_busca: str):
    """
    Percorre o estoque do inicio ao fim comparando cada nome.
    Pior caso: O(n) — passa por todos os itens sem encontrar nada.
    Retorna a peca encontrada (ou None) junto com o tempo gasto em segundos.
    """
    inicio = time.perf_counter()

    for peca in estoque:
        if peca.nome.lower() == nome_busca.lower():
            elapsed = time.perf_counter() - inicio
            return peca, elapsed

    elapsed = time.perf_counter() - inicio
    return None, elapsed


def buscar_binaria(nome_busca: str):
    """
    Ordena o estoque alfabeticamente e aplica busca binaria.
    Muito mais rapido que a sequencial para listas grandes: O(log n).

    Detalhe: a ordenacao acontece toda vez que a funcao e chamada,
    o que adiciona um custo extra. Em producao valeria manter a lista
    sempre ordenada ou usar um dict, mas aqui o objetivo e didatico.
    """
    # Precisa ordenar antes — busca binaria so funciona em lista ordenada
    estoque.sort(key=lambda p: p.nome.lower())

    inicio = time.perf_counter()
    esquerda, direita = 0, len(estoque) - 1
    alvo = nome_busca.lower()

    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        item_meio = estoque[meio].nome.lower()

        if item_meio == alvo:
            elapsed = time.perf_counter() - inicio
            return estoque[meio], elapsed
        elif item_meio < alvo:
            # Alvo esta na metade direita
            esquerda = meio + 1
        else:
            # Alvo esta na metade esquerda
            direita = meio - 1

    elapsed = time.perf_counter() - inicio
    return None, elapsed


# ---------------------------------------------------------------------------
# Paleta de cores
# Centralizei tudo aqui pra facilitar mudar o tema depois.
# ---------------------------------------------------------------------------

CORES = {
    "bg":           "#0f1117",   # fundo principal, quase preto
    "surface":      "#1a1d27",   # fundo de cards e header
    "border":       "#2a2d3a",   # bordas e separadores
    "accent":       "#4f8ef7",   # azul principal, botoes e selecao
    "accent2":      "#7c3aed",   # roxo, botao de busca binaria
    "success":      "#22c55e",   # verde para mensagens de sucesso
    "warning":      "#f59e0b",   # amarelo para avisos
    "danger":       "#ef4444",   # vermelho para erros
    "text":         "#e2e8f0",   # texto principal
    "muted":        "#64748b",   # texto secundario / labels
}

# Cor de destaque por categoria na tabela.
# Facilita identificar visualmente o tipo do produto.
TAG_COLORS = {
    "GPU":          "#7c3aed",
    "CPU":          "#2563eb",
    "RAM":          "#059669",
    "SSD M.2":      "#d97706",
    "Motherboard":  "#dc2626",
    "Power Supply": "#0891b2",
    "Water Cooler": "#7c3aed",
}


# ---------------------------------------------------------------------------
# Classe principal da janela
# ---------------------------------------------------------------------------

class App(tk.Tk):
    """
    Janela principal do sistema. Herda de tk.Tk diretamente para simplificar
    — nao precisamos de uma janela separada sendo gerenciada de fora.

    Estrutura da interface:
        - Header fixo no topo com titulo e contador total
        - Notebook com 3 abas: Inventario, Cadastrar, Busca
    """

    def __init__(self):
        super().__init__()

        self.title("Sistema de Estoque")
        self.geometry("950x650")
        self.minsize(800, 540)  # evita que a janela fique pequena demais pra usar
        self.configure(bg=CORES["bg"])

        # Ordem importa: estilo precisa existir antes de criar os widgets
        self._configurar_estilos()
        self._construir_interface()

        # Carrega o inventario inicial depois que a janela ja existe,
        # assim o Treeview ja esta pronto pra receber os dados
        self._carregar_inventario()

    # -----------------------------------------------------------------------
    # Configuracao visual do ttk
    # -----------------------------------------------------------------------

    def _configurar_estilos(self):
        """
        ttk usa um sistema de estilos separado do tk puro.
        O tema "clam" e o mais flexivel para customizacao — os outros
        temas do Windows/Mac ignoram varias configuracoes de cor.
        """
        style = ttk.Style(self)
        style.theme_use("clam")

        # Estilo base que afeta todos os widgets ttk
        style.configure(".",
            background=CORES["bg"],
            foreground=CORES["text"],
            fieldbackground=CORES["surface"],
            troughcolor=CORES["border"],
            borderwidth=0,
            relief="flat",
        )

        # Notebook = o container das abas
        style.configure("TNotebook",
            background=CORES["bg"],
            borderwidth=0,
            tabmargins=[0, 0, 0, 0],
        )

        # Cada aba individual
        style.configure("TNotebook.Tab",
            background=CORES["surface"],
            foreground=CORES["muted"],
            padding=[18, 10],
            borderwidth=0,
            font=("Courier", 10, "bold"),
        )
        # Aba selecionada fica com fundo azul
        style.map("TNotebook.Tab",
            background=[("selected", CORES["accent"])],
            foreground=[("selected", "#ffffff")],
        )

        # Tabela de itens (Treeview)
        style.configure("Treeview",
            background=CORES["surface"],
            foreground=CORES["text"],
            fieldbackground=CORES["surface"],
            rowheight=28,
            font=("Courier", 9),
            borderwidth=0,
        )
        style.configure("Treeview.Heading",
            background=CORES["border"],
            foreground=CORES["accent"],
            relief="flat",
            font=("Courier", 9, "bold"),
        )
        style.map("Treeview",
            background=[("selected", CORES["accent"])],
            foreground=[("selected", "#ffffff")],
        )

        # Scrollbar lateral da tabela
        style.configure("Vertical.TScrollbar",
            background=CORES["border"],
            arrowcolor=CORES["muted"],
            troughcolor=CORES["bg"],
        )

    # -----------------------------------------------------------------------
    # Construcao do layout principal
    # -----------------------------------------------------------------------

    def _construir_interface(self):
        """Monta o header e o notebook com as tres abas."""

        # Header — barra fixa no topo com o titulo do sistema
        header = tk.Frame(self, bg=CORES["surface"], height=56)
        header.pack(fill="x")
        header.pack_propagate(False)  # impede o frame de encolher pro tamanho do conteudo

        tk.Label(
            header,
            text="SISTEMA DE ESTOQUE",
            bg=CORES["surface"],
            fg=CORES["accent"],
            font=("Courier", 14, "bold")
        ).pack(side="left", padx=20, pady=14)

        # Contador total fica no canto direito do header
        self.lbl_total = tk.Label(
            header,
            text="",
            bg=CORES["surface"],
            fg=CORES["muted"],
            font=("Courier", 9)
        )
        self.lbl_total.pack(side="right", padx=20)

        # Notebook com as abas
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=12, pady=12)

        self._criar_aba_inventario(nb)
        self._criar_aba_cadastro(nb)
        self._criar_aba_busca(nb)

    # -----------------------------------------------------------------------
    # Aba 1: Inventario
    # -----------------------------------------------------------------------

    def _criar_aba_inventario(self, nb):
        """
        Lista todos os itens do estoque em uma tabela com scroll.
        Tem filtro por texto e por categoria que atualizam a tabela em tempo real.
        """
        frame = tk.Frame(nb, bg=CORES["bg"])
        nb.add(frame, text="  Inventario  ")

        # Barra de filtros no topo da aba
        barra = tk.Frame(frame, bg=CORES["bg"])
        barra.pack(fill="x", pady=(8, 4), padx=8)

        tk.Label(
            barra, text="Filtrar:",
            bg=CORES["bg"], fg=CORES["muted"],
            font=("Courier", 9)
        ).pack(side="left")

        # StringVar com trace: chama _aplicar_filtro toda vez que o usuario digita
        self.filtro_var = tk.StringVar()
        self.filtro_var.trace_add("write", lambda *_: self._aplicar_filtro())

        tk.Entry(
            barra,
            textvariable=self.filtro_var,
            bg=CORES["surface"],
            fg=CORES["text"],
            insertbackground=CORES["accent"],  # cor do cursor de texto
            relief="flat",
            font=("Courier", 10),
            width=28
        ).pack(side="left", padx=(6, 16), ipady=4)

        # Dropdown de categoria
        self.cat_var = tk.StringVar(value="Todas")
        categorias = ["Todas", "GPU", "CPU", "RAM", "SSD M.2", "Motherboard", "Power Supply", "Water Cooler"]
        ttk.OptionMenu(
            barra,
            self.cat_var,
            "Todas",
            *categorias,
            command=lambda _: self._aplicar_filtro()
        ).pack(side="left")

        # Label que mostra quantos itens estao visiveis depois do filtro
        self.lbl_contagem = tk.Label(
            barra, text="",
            bg=CORES["bg"], fg=CORES["muted"],
            font=("Courier", 9)
        )
        self.lbl_contagem.pack(side="right")

        # Tabela principal
        colunas = ("categoria", "nome", "preco")
        self.tree = ttk.Treeview(frame, columns=colunas, show="headings", selectmode="browse")

        self.tree.heading("categoria", text="CATEGORIA")
        self.tree.heading("nome",      text="NOME DO PRODUTO")
        self.tree.heading("preco",     text="PRECO (R$)")

        self.tree.column("categoria", width=120, anchor="center")
        self.tree.column("nome",      width=540, anchor="w")
        self.tree.column("preco",     width=110, anchor="e")

        # Scrollbar vinculada ao Treeview
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=(0, 8))
        scrollbar.pack(side="right", fill="y", pady=(0, 8), padx=(0, 8))

    # -----------------------------------------------------------------------
    # Aba 2: Cadastro
    # -----------------------------------------------------------------------

    def _criar_aba_cadastro(self, nb):
        """
        Formulario simples para adicionar um novo item ao estoque.
        O card fica centralizado na aba usando place() com ancora no centro.
        """
        frame = tk.Frame(nb, bg=CORES["bg"])
        nb.add(frame, text="  Cadastrar  ")

        # Card centralizado — uso place aqui porque pack/grid nao centralizam bem
        # um widget de tamanho fixo dentro de um frame que expande
        card = tk.Frame(
            frame,
            bg=CORES["surface"],
            highlightbackground=CORES["border"],
            highlightthickness=1
        )
        card.place(relx=0.5, rely=0.44, anchor="center", width=460)

        tk.Label(
            card, text="Novo Item",
            bg=CORES["surface"], fg=CORES["text"],
            font=("Courier", 13, "bold")
        ).pack(pady=(22, 16))

        # Funcao auxiliar pra nao repetir o mesmo bloco de label + entry 3 vezes
        def criar_campo(label_texto, variavel):
            linha = tk.Frame(card, bg=CORES["surface"])
            linha.pack(fill="x", padx=28, pady=5)
            tk.Label(
                linha, text=label_texto,
                bg=CORES["surface"], fg=CORES["muted"],
                font=("Courier", 9), width=10, anchor="w"
            ).pack(side="left")
            entry = tk.Entry(
                linha,
                textvariable=variavel,
                bg=CORES["border"],
                fg=CORES["text"],
                insertbackground=CORES["accent"],
                relief="flat",
                font=("Courier", 10)
            )
            entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(4, 0))
            return entry

        self.c_nome  = tk.StringVar()
        self.c_cat   = tk.StringVar()
        self.c_preco = tk.StringVar()

        criar_campo("Nome:", self.c_nome)

        # Campo de categoria usa dropdown em vez de texto livre
        # pra evitar que o usuario escreva uma categoria que nao existe
        linha_cat = tk.Frame(card, bg=CORES["surface"])
        linha_cat.pack(fill="x", padx=28, pady=5)
        tk.Label(
            linha_cat, text="Categoria:",
            bg=CORES["surface"], fg=CORES["muted"],
            font=("Courier", 9), width=10, anchor="w"
        ).pack(side="left")
        categorias = ["GPU", "CPU", "RAM", "SSD M.2", "Motherboard", "Power Supply", "Water Cooler"]
        self.c_cat.set(categorias[0])
        ttk.OptionMenu(linha_cat, self.c_cat, categorias[0], *categorias).pack(side="left", padx=(4, 0))

        criar_campo("Preco (R$):", self.c_preco)

        # Label de feedback — muda de cor conforme sucesso ou erro
        self.lbl_status = tk.Label(card, text="", bg=CORES["surface"], font=("Courier", 9))
        self.lbl_status.pack(pady=(8, 0))

        tk.Button(
            card,
            text="CADASTRAR",
            bg=CORES["accent"],
            fg="#ffffff",
            activebackground=CORES["accent2"],
            font=("Courier", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=self._cadastrar
        ).pack(pady=(8, 24), ipadx=20, ipady=8)

    # -----------------------------------------------------------------------
    # Aba 3: Busca
    # -----------------------------------------------------------------------

    def _criar_aba_busca(self, nb):
        """
        Campo de busca unico com dois botoes: um pra cada algoritmo.
        Exibe o resultado e o tempo de execucao logo abaixo.
        """
        frame = tk.Frame(nb, bg=CORES["bg"])
        nb.add(frame, text="  Busca  ")

        card = tk.Frame(
            frame,
            bg=CORES["surface"],
            highlightbackground=CORES["border"],
            highlightthickness=1
        )
        card.place(relx=0.5, rely=0.38, anchor="center", width=580)

        tk.Label(
            card, text="Pesquisa de Pecas",
            bg=CORES["surface"], fg=CORES["text"],
            font=("Courier", 13, "bold")
        ).pack(pady=(22, 12))

        # Campo de texto para o nome que sera buscado
        linha_input = tk.Frame(card, bg=CORES["surface"])
        linha_input.pack(padx=28, fill="x")

        tk.Label(
            linha_input, text="Nome exato:",
            bg=CORES["surface"], fg=CORES["muted"],
            font=("Courier", 9)
        ).pack(side="left")

        self.b_nome = tk.StringVar()
        tk.Entry(
            linha_input,
            textvariable=self.b_nome,
            bg=CORES["border"],
            fg=CORES["text"],
            insertbackground=CORES["accent"],
            relief="flat",
            font=("Courier", 10)
        ).pack(side="left", fill="x", expand=True, ipady=6, padx=(8, 0))

        # Botoes lado a lado, cada um chama um algoritmo diferente
        linha_botoes = tk.Frame(card, bg=CORES["surface"])
        linha_botoes.pack(pady=14)

        def criar_botao(parent, texto, cor, comando):
            # Funcao local pra evitar repeticao nos dois botoes
            tk.Button(
                parent,
                text=texto,
                bg=cor,
                fg="#ffffff",
                activebackground=CORES["border"],
                font=("Courier", 9, "bold"),
                relief="flat",
                cursor="hand2",
                command=comando
            ).pack(side="left", padx=6, ipadx=14, ipady=8)

        criar_botao(linha_botoes, "Busca Sequencial", CORES["accent"],  self._executar_busca_seq)
        criar_botao(linha_botoes, "Busca Binaria",    CORES["accent2"], self._executar_busca_bin)

        # Area de resultado — dois labels: um pro item, um pro tempo
        area_resultado = tk.Frame(card, bg=CORES["surface"])
        area_resultado.pack(fill="x", padx=28, pady=(0, 22))

        self.lbl_resultado = tk.Label(
            area_resultado,
            text="",
            bg=CORES["surface"],
            fg=CORES["text"],
            font=("Courier", 10),
            wraplength=500,
            justify="left"
        )
        self.lbl_resultado.pack(anchor="w")

        self.lbl_tempo = tk.Label(
            area_resultado,
            text="",
            bg=CORES["surface"],
            fg=CORES["muted"],
            font=("Courier", 8)
        )
        self.lbl_tempo.pack(anchor="w", pady=(2, 0))

    # -----------------------------------------------------------------------
    # Acoes e logica de atualizacao da interface
    # -----------------------------------------------------------------------

    def _carregar_inventario(self):
        """
        Popula o estoque com os dados do inventario_loja.py e atualiza a tabela.
        Chamado uma unica vez no __init__, depois que todos os widgets existem.
        """
        for p in inventory_initial:
            cadastrar_peca(p["nome"], p["categoria"], p["preco"], silencioso=True)

        self._atualizar_tabela()
        self._atualizar_contador_total()

    def _atualizar_tabela(self, filtro="", categoria="Todas"):
        """
        Limpa e repopula o Treeview aplicando os filtros ativos.
        Chamado sempre que o estoque muda ou o usuario altera o filtro.
        """
        # Limpa tudo antes de reinserir — mais simples do que fazer diff
        self.tree.delete(*self.tree.get_children())

        count = 0
        for peca in estoque:
            # Filtra por categoria se nao for "Todas"
            if categoria != "Todas" and peca.categoria != categoria:
                continue

            # Filtra por texto — busca parcial, case insensitive
            if filtro and filtro.lower() not in peca.nome.lower():
                continue

            # Tag usada pra colorir a linha de acordo com a categoria.
            # Os espacos e pontos sao removidos porque nomes de tags nao aceitam esses caracteres.
            tag = peca.categoria.replace(" ", "_").replace(".", "")
            cor = TAG_COLORS.get(peca.categoria, CORES["accent"])
            self.tree.tag_configure(tag, foreground=cor)

            self.tree.insert(
                "", "end",
                values=(peca.categoria, peca.nome, f"R$ {peca.preco:,.2f}"),
                tags=(tag,)
            )
            count += 1

        self.lbl_contagem.config(text=f"{count} itens exibidos")

    def _aplicar_filtro(self):
        """Lida com qualquer mudanca nos controles de filtro."""
        self._atualizar_tabela(self.filtro_var.get(), self.cat_var.get())

    def _atualizar_contador_total(self):
        """Atualiza o numero total de itens no header."""
        self.lbl_total.config(text=f"Total em estoque: {len(estoque)} itens")

    def _cadastrar(self):
        """
        Le os campos do formulario, tenta cadastrar a peca e
        exibe feedback visual dependendo do resultado.
        """
        nome  = self.c_nome.get().strip()
        cat   = self.c_cat.get()
        preco = self.c_preco.get().strip()

        # Valida campos vazios antes de chamar a logica de negocio
        if not nome or not preco:
            self.lbl_status.config(text="Preencha todos os campos.", fg=CORES["warning"])
            return

        sucesso = cadastrar_peca(nome, cat, preco)

        if sucesso:
            self.lbl_status.config(text="Item cadastrado com sucesso!", fg=CORES["success"])

            # Limpa os campos de texto para o proximo cadastro
            self.c_nome.set("")
            self.c_preco.set("")

            # Atualiza a tabela mantendo os filtros que ja estavam ativos
            filtro_atual    = self.filtro_var.get() if hasattr(self, "filtro_var") else ""
            categoria_atual = self.cat_var.get()    if hasattr(self, "cat_var")    else "Todas"
            self._atualizar_tabela(filtro_atual, categoria_atual)
            self._atualizar_contador_total()
        else:
            self.lbl_status.config(text="Nome ou preco invalido.", fg=CORES["danger"])

    def _exibir_resultado_busca(self, resultado, tempo, tipo_busca):
        """
        Atualiza os labels de resultado na aba de busca.
        Recebe a peca encontrada (ou None) e o tempo em segundos.
        """
        if resultado:
            texto = f"{resultado.nome}  |  {resultado.categoria}  |  R$ {resultado.preco:,.2f}"
            self.lbl_resultado.config(text=texto, fg=CORES["success"])
        else:
            self.lbl_resultado.config(text="Item nao encontrado.", fg=CORES["danger"])

        # Mostra o tipo de busca e o tempo com 8 casas decimais, igual ao terminal
        self.lbl_tempo.config(text=f"[{tipo_busca}]  Tempo: {tempo:.8f} s")

    def _executar_busca_seq(self):
        """Aciona a busca sequencial com o nome digitado."""
        nome = self.b_nome.get().strip()
        if not nome:
            return
        resultado, tempo = buscar_sequencial(nome)
        self._exibir_resultado_busca(resultado, tempo, "Sequencial")

    def _executar_busca_bin(self):
        """Aciona a busca binaria com o nome digitado."""
        nome = self.b_nome.get().strip()
        if not nome:
            return
        resultado, tempo = buscar_binaria(nome)
        self._exibir_resultado_busca(resultado, tempo, "Binaria")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app = App()
    app.mainloop()