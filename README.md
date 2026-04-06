# G33 — Sistema de Estoque com Algoritmos de Busca

Trabalho pratico da disciplina de Estrutura de Dados II (EDA2) — 2026.1

O projeto simula um sistema de gerenciamento de estoque para uma loja de hardware. O foco esta na implementacao e comparacao pratica de dois algoritmos de busca — sequencial e binaria — aplicados sobre um inventario gerado automaticamente com 5.000 produtos.

---

## Sobre

O sistema carrega ao iniciar um banco de dados ficticio com pecas de hardware (GPUs, CPUs, SSDs, entre outras), geradas com marcas, modelos e precos aleatorios. A partir dai, o usuario pode cadastrar novos itens, visualizar o inventario e realizar buscas cronometradas para comparar o desempenho de cada algoritmo.

---

## Estrutura do Projeto

```
G33_Busca_EDA2-2026.1/
│
├── main.py               # Logica principal: menu, classe Peca, cadastro e buscas
├── inventario_loja.py    # Geracao do inventario inicial com 5.000 produtos
├── .gitignore            # Ignora ambiente virtual e cache do Python
└── README.md             # Documentacao do projeto
```

---

## Funcionalidades

| Opcao | Descricao |
|-------|-----------|
| 1. Novo cadastro | Registra uma nova peca com validacao de nome e preco |
| 2. Ver inventario | Exibe os primeiros 20 itens do estoque em formato de tabela |
| 3. Pesquisa Sequencial | Busca percorrendo o estoque linearmente e exibe o tempo gasto |
| 4. Pesquisa Binaria | Busca com divisao e conquista apos ordenacao e exibe o tempo gasto |

---

## Algoritmos

### Busca Sequencial

Percorre o estoque item por item do inicio ao fim ate encontrar o elemento buscado. Nao exige nenhuma ordenacao previa.

```python
def buscar_sequencial(nome_busca):
    for peca in estoque:
        if peca.nome.lower() == nome_busca.lower():
            return peca
    return None
```

| Caso | Complexidade |
|------|-------------|
| Melhor | O(1) |
| Medio | O(n/2) |
| Pior | O(n) |

---

### Busca Binaria

Ordena o estoque pelo nome e aplica divisao e conquista, eliminando metade das possibilidades a cada iteracao.

```python
def buscar_binaria(nome_busca):
    estoque.sort(key=lambda p: p.nome.lower())
    esquerda, direita = 0, len(estoque) - 1
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        if estoque[meio].nome.lower() == nome_busca.lower():
            return estoque[meio]
        elif estoque[meio].nome.lower() < nome_busca.lower():
            esquerda = meio + 1
        else:
            direita = meio - 1
    return None
```

| Caso | Complexidade |
|------|-------------|
| Melhor | O(1) |
| Medio | O(log n) |
| Pior | O(log n) |

> Com 5.000 itens, a busca binaria realiza no maximo 13 comparacoes. A busca sequencial pode realizar ate 5.000.

---

## Como Executar

**Pre-requisito:** Python 3.8 ou superior instalado. Nenhuma dependencia externa.

```bash
# Clone o repositorio
git clone https://github.com/BGRANGEIRO/G33_Busca_EDA2-2026.1.git

# Acesse a pasta
cd G33_Busca_EDA2-2026.1

# Execute
python main.py
```

---

## Exemplo de Uso

```
Sincronizando banco de dados...
Sistema pronto.

--- MENU DE ESTOQUE ---
1. Novo cadastro
2. Ver inventario
3. Pesquisa Sequencial
4. Pesquisa Binaria
0. Sair
Opcao: 3

Nome da peca para busca: ASUS GPU v42-137
Tempo (Sequencial): 0.00021400 s
Localizado: [GPU         ] ASUS GPU v42-137               | R$  7345.89

Opcao: 4
Nome da peca para busca: ASUS GPU v42-137
Tempo (Binaria):    0.00000300 s
Localizado: [GPU         ] ASUS GPU v42-137               | R$  7345.89
```

---

## Tecnologias

- Python 3
- `random` — geracao do inventario aleatorio
- `time` — medicao de desempenho com `perf_counter`
- `re` — validacao de nomes com expressoes regulares

---

## Integrantes

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/BGRANGEIRO">
        <img src="https://github.com/BGRANGEIRO.png" width="100px" alt="BGrangeiro"/><br/>
        <b>Brangeiro</b>
      </a><br/>
      Matricula: 222024158
    </td>
    <td align="center">
      <a href="https://github.com/DIAXIZ">
        <img src="https://github.com/Diaxiz.png" width="100px" alt="Dizxiz"/><br/>
        <b>Diaxiz</b>
      </a><br/>
      Matricula: 221007985
    </td>
  </tr>
</table>

---

Disciplina: Estrutura de Dados II — EDA2 | Periodo: 2026.1
