from inventario_loja import inventory_initial
import time
import re

class Peca:
    def __init__(self, nome, categoria, preco):
        self.nome = nome
        self.categoria = categoria
        self.preco = preco

    def __str__(self):
        return f"[{self.categoria:12}] {self.nome:30} | R$ {self.preco:>8.2f}"

estoque = []

def validar_nome_peca(nome):
    return bool(re.fullmatch(r"[A-Za-z0-9À-ÿ \-]+", nome.strip()))

def validar_preco(preco):
    try:
        valor = float(preco)
        return valor >= 0
    except ValueError:
        return False

def cadastrar_peca(nome, categoria, preco, silencioso=False):
    if not validar_nome_peca(nome):
        if not silencioso:
            print(f"Erro: Nome '{nome}' invalido!")
        return False
    
    nova_peca = Peca(nome, categoria, float(preco))
    estoque.append(nova_peca)
    return True

def listar_estoque():
    if not estoque:
        print("\nEstoque vazio.")
    else:
        print(f"\n--- Listando 20 de {len(estoque)} itens ---")
        print(f"{'CATEGORIA':<14} | {'NOME DO PRODUTO':<30} | {'PRECO'}")
        print("-" * 65)
        for peca in estoque[:20]:
            print(peca)
        print("-" * 65)

def buscar_sequencial(nome_busca):
    inicio = time.perf_counter()
    for peca in estoque:
        if peca.nome.lower() == nome_busca.lower():
            fim = time.perf_counter()
            print(f"Tempo (Sequencial): {fim - inicio:.8f} s")
            return peca
    fim = time.perf_counter()
    print(f"Tempo (Sequencial): {fim - inicio:.8f} s")
    return None

def buscar_binaria(nome_busca):
    estoque.sort(key=lambda p: p.nome.lower())
    
    inicio = time.perf_counter()
    esquerda, direita = 0, len(estoque) - 1
    
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        item_meio = estoque[meio].nome.lower()
        alvo = nome_busca.lower()
        
        if item_meio == alvo:
            fim = time.perf_counter()
            print(f"Tempo (Binaria): {fim - inicio:.8f} s")
            return estoque[meio]
        elif item_meio < alvo:
            esquerda = meio + 1
        else:
            direita = meio - 1
            
    fim = time.perf_counter()
    print(f"Tempo (Binaria): {fim - inicio:.8f} s")
    return None

def main():
    print("Sincronizando banco de dados...")
    for p in inventory_initial:
        cadastrar_peca(p["nome"], p["categoria"], p["preco"], silencioso=True)
    print("Sistema pronto.\n")

    while True:
        print("--- MENU DE ESTOQUE ---")
        print("1. Novo cadastro")
        print("2. Ver inventario")
        print("3. Pesquisa Sequencial")
        print("4. Pesquisa Binaria")
        print("0. Sair")

        opcao = input("Opcao: ")

        if opcao == "1":
            n = input("Nome: ")
            c = input("Categoria: ")
            p = input("Preco: ")
            if cadastrar_peca(n, c, p):
                print("Item registrado.")

        elif opcao == "2":
            listar_estoque()

        elif opcao == "3":
            nome = input("Nome da peca para busca: ")
            res = buscar_sequencial(nome)
            if res:
                print(f"Localizado: {res}")
            else:
                print("Item nao encontrado.")

        elif opcao == "4":
            nome = input("Nome da peca para busca: ")
            res = buscar_binaria(nome)
            if res:
                print(f"Localizado: {res}")
            else:
                print("Item nao encontrado.")

        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")

if __name__ == "__main__":
    main()