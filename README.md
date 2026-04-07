# G33 — Sistema de Estoque com Algoritmos de Busca

Trabalho pratico da disciplina de Estrutura de Dados II (EDA2) — 2026.1

O projeto simula um sistema de gerenciamento de estoque para uma loja de hardware. O foco esta na implementacao e comparacao pratica de dois algoritmos de busca — sequencial e binaria — aplicados sobre um inventario gerado automaticamente com 5.000 produtos. O sistema conta com uma interface grafica desenvolvida em Tkinter.

---

## Sobre

O sistema carrega ao iniciar um banco de dados ficticio com pecas de hardware (GPUs, CPUs, SSDs, entre outras), geradas com marcas, modelos e precos aleatorios. A partir dai, o usuario pode cadastrar novos itens, visualizar o inventario completo e realizar buscas cronometradas para comparar o desempenho de cada algoritmo, tudo por meio de uma interface grafica moderna.

---

## Estrutura do Projeto

```
G33_Busca_EDA2-2026.1/
|
+-- main.py               # Interface grafica (Tkinter): menu lateral, telas de inventario, cadastro e busca
+-- interface.py          # Interface do projeto
+-- inventario_loja.py    # Geracao do inventario inicial com 5.000 produtos
+-- .gitignore            # Ignora ambiente virtual e cache do Python
+-- README.md             # Documentacao do projeto
```

---

## Interface Grafica

A interface foi construida com a biblioteca nativa `tkinter` e segue um tema escuro com acentos em azul. A navegacao e feita por um menu lateral fixo com tres secoes principais.

### Telas disponíveis

**Inventario** — exibe todos os itens do estoque em uma tabela com colunas de categoria, nome do produto e preco. Suporta rolagem para navegar pelos 5.000 registros.

**Cadastro** — formulario centralizado para registrar uma nova peca informando nome, categoria e preco. Apos salvar, o sistema redireciona automaticamente para o inventario atualizado.

**Busca** — campo de pesquisa livre com dois botoes de acao: um para busca sequencial e outro para busca binaria. O resultado exibe o item encontrado com nome, categoria e preco, alem do tempo de execucao em segundos com alta precisao.

---

## Funcionalidades

| Secao         | Descricao                                                                 |
|---------------|---------------------------------------------------------------------------|
| Inventario    | Exibe todos os itens do estoque em formato de tabela com rolagem          |
| Cadastrar     | Registra uma nova peca com nome, categoria e preco                        |
| Busca Sequencial | Percorre o estoque linearmente e exibe o tempo gasto                   |
| Busca Binaria | Ordena o estoque e aplica divisao e conquista, exibindo o tempo gasto     |

---

## Algoritmos

### Busca Sequencial

Percorre o estoque item por item do inicio ao fim ate encontrar o elemento buscado. Nao exige nenhuma ordenacao previa.

```python
def realizar_busca(modo):
    termo = txt_busca.get().lower()
    inicio = time.perf_counter()
    res = next((p for p in self.estoque if p.nome.lower() == termo), None)
    fim = time.perf_counter() - inicio
```

| Caso   | Complexidade |
|--------|--------------|
| Melhor | O(1)         |
| Medio  | O(n/2)       |
| Pior   | O(n)         |

---

### Busca Binaria

Ordena o estoque pelo nome e aplica divisao e conquista, eliminando metade das possibilidades a cada iteracao.

```python
def realizar_busca(modo):
    termo = txt_busca.get().lower()
    inicio = time.perf_counter()
    if modo == "bin":
        self.estoque.sort(key=lambda x: x.nome.lower())
    res = next((p for p in self.estoque if p.nome.lower() == termo), None)
    fim = time.perf_counter() - inicio
```

| Caso   | Complexidade |
|--------|--------------|
| Melhor | O(1)         |
| Medio  | O(log n)     |
| Pior   | O(log n)     |

Com 5.000 itens, a busca binaria realiza no maximo 13 comparacoes. A busca sequencial pode realizar ate 5.000.

---

## Como Executar

Pre-requisito: Python 3.8 ou superior instalado. Nenhuma dependencia externa — `tkinter` ja faz parte da instalacao padrao do Python.

```bash
# Clone o repositorio
git clone https://github.com/eda2-2026/G33_Busca_EDA2-2026.1

# Acesse a pasta
cd G33_Busca_EDA2-2026.1

# Execute
python main.py
```

A janela do sistema sera aberta automaticamente com o inventario carregado.

---

## Tecnologias

- Python 3
- `tkinter` — interface grafica nativa
- `ttk` — widgets com tema visual aprimorado
- `random` — geracao do inventario aleatorio
- `time` — medicao de desempenho com `perf_counter`

---

## Video no youtube mostrando o projeto
link: https://youtu.be/30jW7tPwQn8

## Integrantes

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/BGRANGEIRO">
        <img src="https://github.com/BGRANGEIRO.png" width="100px" alt="Brangeiro"/><br/>
        <b>Brangeiro</b>
      </a><br/>
      Matricula: 222024158
    </td>
    <td align="center">
      <a href="https://github.com/DIAXIZ">
        <img src="https://github.com/Diaxiz.png" width="100px" alt="Diaxiz"/><br/>
        <b>Diaxiz</b>
      </a><br/>
      Matricula: 221007985
    </td>
  </tr>
</table>

---

Disciplina: Estrutura de Dados II — EDA2 | Periodo: 2026.1
