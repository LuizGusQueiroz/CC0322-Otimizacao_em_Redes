from __future__ import annotations
from typing import List, Set


class Vertice:
    def __init__(self, id: int):
        self.id = id


class Aresta:
    def __init__(self, orig: Vertice, dest: Vertice, weight: float = 1, eh_direcionada: bool = False):
        self.orig: Vertice = orig  # Vértice de origem.
        self.dest: Vertice = dest  # Vértice de destino.
        self.weight: float = weight  # Peso da aresta.
        self.eh_direcionada: bool = eh_direcionada  # Indicador para caso a aresta seja direcionada.
        self.vertices: List[Vertice] = [orig, dest]  # Lista de vértices da aresta.


class Grafo:
    def __init__(self, V: List[Vertice], E: List[Aresta]):
        # Verica se o conjunto V de vértices é não vazio.
        if len(V) == 0:
            raise Exception('O Tamanho de V deve ser maior que 0.')
        # Verifica se em alguma aresta há um vértice que não está em V.
        for aresta in E:
            for vertice in aresta.vertices:
                if vertice not in V:
                    raise Exception(f'O vértice {vertice} não está em V.')
        self.V = V  # Conjunto de vértices.
        self.E = E  # Conjunto de arestas.

    def sao_incidentes(self, v1: Vertice, v2: Vertice, e: Aresta) -> bool:
        """
        Verifica se dois vértices são incidentes numa aresta.
        """
        return (v1 == e.orig and v2 == e.dest) or \
            (v2 == e.orig and v1 == e.dest)

    def sao_vizinhos(self, v1: Vertice, v2: Vertice) -> bool:
        """
        Verifica se dois vértices são vizinhos (ou adjacentes).
        """
        for aresta in self.E:
            if self.sao_incidentes(v1, v2, aresta):
                return True
        return False

    def grau(self, v: Vertice) -> int:
        """
        Calcula o grau de um vértice.
        """
        grau: int = 0
        for aresta in self.E:
            if aresta.eh_direcionada:
                if v == aresta.dest:
                    grau += 1
            else:
                if v in aresta.vertices:
                    grau += 1
        return grau

    def eh_isolado(self, v: Vertice) -> bool:
        """
        Verifica se o vértice é isolado.
        """
        return self.grau(v) == 0

    def eh_terminal(self, v: Vertice) -> bool:
        """
        Verifica se um vértice é terminal.
        """
        return self.grau(v) == 1

    def eh_regular(self) -> bool:
        """
        Determina se o próprio grafo é regular.
        """
        graus: Set[int] = set()
        for vertice in self.V:
            graus.add(self.grau(vertice))
        # Se o grau de todos os vértices for o mesmo, o grafo será regular.
        return len(graus) == 1

    def sequencia_de_graus(self) -> List[int]:
        """
        Lista a sequência de graus do grafo, em ordem crescente.
        """
        graus: List[int] = [self.grau(vertice) for vertice in self.V]
        return sorted(graus)

    def eh_completo(self) -> bool:
        """
        Determina se o grafo é completo, ou seja, é regular e cada vértice tem grau n-1,
        sendo n o tamanho de vértices.
        """
        n = len(self.V)
        return self.eh_regular() and self.grau(self.V[0]) == (n - 1)

    def eh_subgrafo(self, G: Grafo) -> bool:
        """
        Determina se o grafo é subgrafo deste grafo.
        """
        for vertice in G.V:
            if vertice not in self.V:
                return False
        for aresta in G.E:
            if aresta not in self.E:
                return False
        return True

    def eh_subgrafo_proprio(self, G: Grafo) -> bool:
        """
        Determina se o grafo é subgrafo próprio deste grafo, ou seja,
        é subgrafo, mas tem pelo menos 1 vértice ou aresta a menos.
        """
        return self.eh_subgrafo(G) and \
            (len(G.V) != len(self.V) or len(G.E) != len(self.E))
