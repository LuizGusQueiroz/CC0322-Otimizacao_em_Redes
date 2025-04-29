from __future__ import annotations
from typing import List, Dict, Set


class Vertice:
    def __init__(self, id: str):
        self.id = id

    def __eq__(self, other: Vertice) -> bool:
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self) -> str:
        return str(self.id)

    def __repr__(self) -> str:
        return str(self.id)


class Aresta:
    def __init__(self, orig: Vertice, dest: Vertice, weight: float = 1, eh_direcionada: bool = False):
        self.orig: Vertice = orig  # Vértice de origem.
        self.dest: Vertice = dest  # Vértice de destino.
        self.weight: float = weight  # Peso da aresta.
        self.eh_direcionada: bool = eh_direcionada  # Indicador para caso a aresta seja direcionada.
        self.vertices: List[Vertice] = [orig, dest]  # Lista de vértices da aresta.

    def __eq__(self, other: Aresta) -> bool:
        """
        Para se comparar duas arestas, caso ambas sejam direcionadas, o vértice de origem
        deve ser o mesmo em ambas, e o de destino também, caso contrário, estas serão iguais
        caso o caso acima seja satisfeito, ou se tiverem origem e destino trocados.
        """
        if self.weight != other.weight:
            return False
        if self.eh_direcionada and other.eh_direcionada:
            return self.orig == other.orig and self.dest == other.dest
        else:
            return self.orig in other.vertices and \
                self.dest in other.vertices

    def __hash__(self):
        return hash(f'{self.orig.id}-{self.dest.id}-{self.weight}')

    def __str__(self) -> str:
        return f'{self.orig.id}-{self.dest.id}-{self.weight}'

    def __repr__(self) -> str:
        return f'{self.orig.id}-{self.dest.id}-{self.weight}'


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

    def sao_incidentes(self, v1: Vertice, v2: Vertice, e: Aresta, direcionado: bool = False) -> bool:
        """
        Verifica se dois vértices são incidentes numa aresta.
        """
        # No direcionado verifica apenas um caso.
        if direcionado:
            return v1 == e.orig and v2 == e.dest
        # No não direcionado verifica os dois casos.
        return [v1, v2] == e.vertices or [v2, v1] == e.vertices

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
                if v == aresta.dest:
                    grau += 1
            elif v in aresta.vertices:
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
            if aresta.eh_direcionada:
                if aresta.orig == v and aresta.dest not in adj_l:
                    adj_l.append(aresta.dest)
            else:
                if aresta.orig == v and aresta.dest not in adj_l:
                    adj_l.append(aresta.dest)
                elif aresta.dest == v and aresta.orig not in adj_l:
                    adj_l.append(aresta.orig)
        return adj_l

    def get_adj_mtx(self) -> List[List[int]]:
        """
        Gera a matriz de adjacência do grafo.
        """
        adj_mtx: List[List[int]] = []
        v_ids: List[str] = sorted([vertice.id for vertice in self.V])  # Ids dos vértices do grafo.
        adj_mtx.append([0] + v_ids)  # Define a primeira linha de cabeçalho.
        for vertice_1 in self.V:
            new_row: List[int] = [vertice_1.id]  # Nova linha que será adicionada à matriz de adjacência.
            adj_l: List[Vertice] = self.get_adj_list(vertice_1)
            for vertice_2 in self.V:
                # Adiciona 1 caso o vértice seja adjacente, e 0 caso contrário.
                new_row.append(int(vertice_2 in adj_l))
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
            v1: Vertice = V[i + 1]
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
            v1: Vertice = V[i + 1]
            if not self.sao_vizinhos(v0, v1, direcionado=True):
                return False
            i += 1
        return True

    def eh_ciclo(self, V: List[Vertice] | List[Aresta]) -> bool:
        """
        Determina se a lista V de vértices é um ciclo, ou seja,
        um caminho onde o primeiro elemento é o último.
        """
        # Ajusta a lista para caso arestas tenham sido passadas.
        if isinstance(V[0], Aresta):
            V = [V[0].orig] + [e.dest for e in V]
        return self.eh_caminho(V) and V[0] == V[-1]

    def eh_conexo(self) -> bool:
        """
        Determina se o grafo é conexo, ou seja, cada vértice
        pode ser alcançável a partir de qualquer vértice.
        """
        V: List[Vertice] = [self.V[0]]
        i = 0
        while i < len(V):
            vertice: Vertice = V[i]
            adj_l: List[Vertice] = self.get_adj_list(vertice)
            for adj in adj_l:
                if adj not in V:
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

    def alg_kruskal(self) -> Grafo:
        """
        Implementação do algoritmo de kruskal, que retorna uma
        árvore geradora do grafo.
        """
        E: List[Aresta] = sorted(self.E, key=lambda e: e.weight)
        V_AG: List[Vertice] = [E[0].orig]
        E_AG: List[Aresta] = [E[0]]
        for aresta in E:
            vertice = aresta.dest
            if not self.eh_ciclo(V_AG + [vertice]):
                V_AG.append(vertice)
                E_AG.append(aresta)

        [print(v.id) for v in V_AG]
        print()
        [print(e.orig.id, e.dest.id) for e in E_AG]
        # return Grafo(V_AG, E_AG)

    def get_aresta(self, orig: Vertice, dest: Vertice, direcionado: bool = False) -> Aresta| None:
        """
        Procura uma aresta que tenha a mesma origem e desitno.
        """
        for aresta in self.E:
            if self.sao_incidentes(orig, dest, aresta, direcionado):
                return aresta
        return None

    def get_arestas(self, v: Vertice, direcionado: bool = False) -> List[Aresta]:
        """
        Retorna todas as arestas que partem de um vértice.
        """
        edges: List[Aresta] = []
        if direcionado:
            for e in self.E:
                if v == e.orig:
                    edges.append(e)
        else:
            for e in self.E:
                if v in e.vertices:
                    edges.append(e)
        return edges

    def dijkstra(self, A: Vertice, B: Vertice) -> float:
        """
        Implementação do algoritmo de Dijkstra, retornando o custo de menor caminho do
        vértice A, ao vértice B.
        :param A: Vértice de origem.
        :param B: Vértice de destino.
        :return: Custo do menor de caminho de A até B.
        """
        N: List[Vertice] = [A]  # Nós visitados.
        D: Dict[Vertice, float] = {}  # Custo de A até o nó v.
        # Inicializa o pesos dos vizinhos de A com o peso deles, e os demais com infinito.
        for v in self.V:
            if self.sao_vizinhos(A, v):
                e: Aresta = self.get_aresta(A, v)
                D[v] = e.weight
            else:
                D[v] = float('inf')
        # Define o custo até A como 0.
        D[A] = 0
        while len(N) != len(self.V):
            # Lista os vértices ainda não inseridos em N.
            nao_inseridos = [v for v in D if v not in N]
            # Ordena os vértices com base em D(v).
            nao_inseridos = sorted(nao_inseridos, key=lambda x: D[x])
            # Seleciona o com menor custo.
            w: Vertice = nao_inseridos[0]
            N.append(w)
            # Lista os vizinhos de w.
            vertices = self.get_adj_list(w)
            # Remove os que já estão em n.
            vertices = [v for v in vertices if v not in N]
            # Atualiza os valores de D.
            for v in vertices:
                aresta = self.get_aresta(w, v)
                c: float = aresta.weight
                D[v] = min(D[v], D[w]+c)
        return D[B]

    def floyd_warshall(self, direcionado: bool = True) -> Dict[Vertice, Dict[Vertice, float]]:
        """
        Implementação do algoritmo de Floyd Warshall.
        :return: Matriz com a menor distâcia entre cada vértice.
        """
        C = {v: {} for v in self.V}
        # Inicializa os pesos.
        for orig in self.V:
            for dest in self.V:
                # Trata autocaminhos.
                if orig == dest:
                    C[orig][dest] = 0
                    continue
                # Verifica se há o caminho de orig para dest.
                e: Aresta = self.get_aresta(orig, dest, direcionado)
                # Se e for Nulo, o caminho não existe.
                if e is None:
                    C[orig][dest] = float('inf')
                else:
                    C[orig][dest] = e.weight
        # Atualiza os pesos.
        for vk in self.V:
            for vi in self.V:
                for vj in self.V:
                    C[vi][vj] = min(C[vi][vj], C[vi][vk] + C[vk][vj])
        return C


    def prim(self) -> Grafo:
        v: Vertice = self.V[0]  # Nó atual.
        V_vis: List[Vertice] = [v]  # Vértices visitados.
        E_vis: List[Aresta] = self.get_arestas(v)  # Arestas visitadas.
        E: List[Aresta] = []  # Arestas da AGM.
        while len(V_vis) != len(self.V):
            # Ordena as arestas com base no menor peso.
            E_vis = sorted(E_vis, key=lambda e: e.weight, reverse=True)
            while len(E_vis) != 0:
                e: Aresta = E_vis[0]
                E_vis = E_vis[1:]  # Descarta a aresta nova.
                # Verifica se a aresta adiciona um nó já pertencente à AGM.
                v = e.dest
                if v not in V_vis:
                    break
            V_vis.append(v)
            E_vis.extend(self.get_arestas(v))
            E.append(e)
        G = Grafo(V_vis, E)
        return G