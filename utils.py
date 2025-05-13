from typing import List
from Grafo import Vertice, Aresta, Grafo


def txt_to_graph(path: str) -> Grafo:
    """
    Cria um grafo a partir de um arquivo txt contendo a lista de adjacência de um grafo, no formato:
    # Direcionado
    False
    # Vértices
    A B C D E
    # Arestas: origem destino peso
    A B 6
    A C 5
    B B 4
    B E 3
    C E 2
    E E 1
    """
    with open(path, 'r') as file:
        # Lê o arquivo e o separa por linha.
        lines = file.read().split('\n')
    # A linha 1 deve conter a informação sobre o direcionamento das arestas.
    direcionado = lines[1] == 'True'
    # Os vértices devem estar listados na linha 3.
    vertices: List[str] = lines[3].split()
    # Cria objetos Vertice para cada vértice fornecido.
    V: List[Vertice] = [Vertice(v) for v in vertices]
    # As arestas devem estar listadas a partir da linha 5.
    # Como em cada linha, deve estar origem, destino e weight separado
    # por espaço, com o line.split() é possível atribuir os valores facilmente.
    E: List[Aresta] = []
    for line in lines[5:]:
        orig, dest, weight = line.split()
        orig = Vertice(orig)
        dest = Vertice(dest)
        weight = float(weight)
        e = Aresta(orig, dest, weight, direcionado)
        E.append(e)


    return Grafo(V, E)
