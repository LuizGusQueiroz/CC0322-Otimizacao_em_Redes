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
        v_ids: List[int] = [v.id for v in V]
        for aresta in E:
            for vertice in aresta.vertices:
                if vertice.id not in v_ids:
                    raise Exception(f'O vértice {vertice} não está em V.')
        self.V = V  # Conjunto de vértices.
        self.E = E  # Conjunto de arestas.

    def sao_incidentes(self, v1: Vertice, v2: Vertice, e: Aresta, direcionado: bool = False) -> bool:
        """
        Verifica se dois vértices são incidentes numa aresta.
        """
        # No direcionado verifica apenas um caso.
        if direcionado:
            return v1.id == e.orig.id and v2.id == e.dest.id
        # No não direcionado verifica os dois casos.
        return (v1.id == e.orig.id and v2.id == e.dest.id) or \
            (v2.id == e.orig.id and v1.id == e.dest.id)

    def sao_vizinhos(self, v1: Vertice, v2: Vertice, direcionado: bool = False) -> bool:
        """
        Verifica se dois vértices são vizinhos (ou adjacentes).
        """
        for aresta in self.E:
            if self.sao_incidentes(v1, v2, aresta, direcionado):
                return True
        return False

    def grau(self, v: Vertice) -> int:
        """
        Calcula o grau de um vértice.
        """
        grau: int = 0
        for aresta in self.E:
            if aresta.eh_direcionada:
                if v.id == aresta.dest.id:
                    grau += 1
            else:
                v_ids: List[int] = [vertice.id for vertice in aresta.vertices]
                if v.id in v_ids:
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

    def get_adj_list(self, v: Vertice) -> List[Vertice]:
        """
        Gera a lista de adjacência de um vértice.
        """
        adj_l: List[Vertice] = []
        for aresta in self.E:
            adj_l_ids: List[int] = [adj.id for adj in adj_l]
            if aresta.orig.id == v.id and \
               aresta.dest.id not in adj_l_ids:
                adj_l.append(aresta.dest)
            elif aresta.dest.id == v.id and \
                 aresta.orig.id not in adj_l_ids:
                adj_l.append(aresta.orig)
        return adj_l

    def get_adj_mtx(self) -> List[List[int]]:
        """
        Gera a matriz de adjacência do grafo.
        """
        # O +1 é para adicionar o cabeçalho.
        adj_mtx: List[List[int]] = []
        v_ids: List[int] = sorted([vertice.id for vertice in self.V])  # Ids dos vértices do grafo.
        adj_mtx.append([0] + v_ids)
        for vertice_1 in self.V:
            new_row: List[int] = [vertice_1.id]  # Nova linha que será adicionada à matriz de adjacência.
            adj_l: List[Vertice] = self.get_adj_list(vertice_1)
            adj_ids: List[int] = [vertice.id for vertice in adj_l]  # Ids dos vértices adjacentes.
            for vertice_2 in self.V:
                # Adiciona 1 caso o vértice seja adjacente, e 1 caso contrário.
                new_row.append(int(vertice_2.id in adj_ids))
            adj_mtx.append(new_row)
        return adj_mtx

    def eh_cadeia(self, V: List[Vertice]) -> bool:
        """
        Verifica se a lista V de vértices é uma cadeia (ou passeio).
        """
        if len(V) < 2:
            return False
        i = 0
        while i < len(V) - 1:
            v0: Vertice = V[i]
            v1: Vertice = V[i+1]
            if not self.sao_vizinhos(v0, v1):
                return False
            i += 1
        return True

    def eh_caminho(self, V: List[Vertice]) -> bool:
        """
        Determina se a lista V de vértices é um caminho.
        """
        if len(V) < 2:
            return False
        i = 0
        while i < len(V) - 1:
            v0: Vertice = V[i]
            v1: Vertice = V[i+1]
            if not self.sao_vizinhos(v0, v1, direcionado=True):
                return False
            i += 1
        return True

    def eh_ciclo(self, V: List[Vertice]) -> bool:
        """
        Determina se a lista V de vértices é um ciclo, ou seja,
        um caminho onde o primeiro elemento é o último.
        """
        return self.eh_caminho(V) and V[0].id == V[-1].id

    def eh_conexo(self) -> bool:
        """
        Determina se o grafo é conexo, ou seja, cada vértice
        pode ser alcançável a partir de qualquer vértice.
        """
        V: List[Vertice] = [self.V[0]]
        i = 0
        while i < len(V):
            v_ids = [vertice.id for vertice in V]
            vertice: Vertice = V[i]
            adj_l: List[Vertice] = self.get_adj_list(vertice)
            for adj in adj_l:
                if adj.id not in v_ids:
                    V.append(adj)
            i += 1
        return len(V) == len(self.V)

    def eh_arvore(self) -> bool:
        """
        Determina se o grafo é uma árvore, ou seja, é conexo e tem
        exatamente n-1 arestas, sendo n o número de vértices.
        """
        return self.eh_conexo() and len(self.E) == (len(self.V) - 1)

    def eh_arvore_geradora(self, G: Grafo) -> bool:
        """
        Determina se o grafo G é uma árvore geradora, ou seja, é subgrafo de
        deste grafo e é uma árvore.
        """
        return self.eh_subgrafo(G) and G.eh_arvore()
