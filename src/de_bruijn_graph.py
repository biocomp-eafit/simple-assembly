import networkx as nx
import matplotlib.pyplot as plt
import datetime
import sys
from euler import *

def visualize_graph(graph):
    nx.draw(graph, with_labels = True, cmap=plt.get_cmap('jet'))
    plt.show()


class Kmer():
    def __init__(self, kmers_str):
        self.kmer_str = kmers_str
        self.k = len(self.kmer_str)
        self.prefix_node = self.kmer_str[:-1]
        self.sufix_node = self.kmer_str[1:]

class DeBruijnGraph():
    def __init__(self, seq_dict, k=3):
        self.sequences = [seq.seq for seq in seq_dict.values()]
        min_len = len(min(self.sequences, key=len))
        if k <= 2:
            raise ValueError('k es muy pequeño, mejor cancele')
        elif k >= min_len:
            raise ValueError('k es mayor que la longitud minima')
        else:
            self.k = k

        self.G = nx.MultiDiGraph()
        self.build_graph() # Construct the graph
        # Check for subgraphs
        self.subgraphs = DeBruijnGraph.extract_directed_subgraph(self.G)
        # check subgraph eulerian features
        self.check_eulerian_features_subgraphs()
        
    def build_graph(self):
        '''
        Este metodo construye el grafo.
        La construccion asume un matching exacto, es decir 
        "secuencias perfectas", en general, esta suposicion
        es bastante fuerte dado que no suele cumplirse, dado
        que en la vida real la secuenciacion esta sujeta a
        errores, lo que se suele hacer es "aflojar" el criterio
        de matcheo.
        '''
        for seq in self.sequences:
            seq = [Kmer(seq[i:i + self.k].upper()) for i in \
                   range(len(seq) - self.k + 1)] # Extract kmer
            for kmer in seq:
                if kmer.prefix_node not in self.G.nodes():
                    self.G.add_node(kmer.prefix_node)
                if kmer.sufix_node not in self.G.nodes():
                    self.G.add_node(kmer.sufix_node)
        if len(self.G.nodes()):
            [self.G.add_edge(L, R) for L in self.G.nodes() for R in \
                    self.G.nodes() if L[1:] == R[:-1]]
        else:
            raise ValueError('no hay grafo por aqui')

    def extract_directed_subgraph(directed_graph):
        return [directed_graph.subgraph(subg) for subg in
                nx.weakly_connected_component_subgraphs(directed_graph)]

    def check_eulerian_features_subgraphs(self):
        for subg in self.subgraphs:
            if has_euler_circuit(subg):
                subg.graph['euler_circuit'] = True
            else:
                subg.graph['euler_circuit'] = False

            # check for Euler Path
            subg.graph.update(dict(zip(['euler_path',
                                        'euler_path_start',
                                        'euler_path_end'],
                                        has_euler_path(subg))))
