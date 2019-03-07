import networkx as nx
import matplotlib.pyplot as plt

def L_spectrum(seq, L):
    spectrum = []
    printable = ['' for i in range(L)]
    for i in range(len(seq) - L + 1):
        printable[i%L] += seq[i:i+L]
        spectrum.append(seq[i:i+L])

    for i, v in enumerate(printable):
        print(' ' * i + v)
    
    print(seq)
    return spectrum

def visualize_graph(graph):
    nx.draw_networkx_labels(graph, pos=nx.circular_layout(graph))
    nx.draw_networkx_edges(graph, pos=nx.circular_layout(graph), alpha=0.5)
    plt.show()

def euler_path(graph):
    g = graph.copy()
    v = seed
    while g.size() > 0:
        n = v
        nbrs = sorted([v for u, v in g.edges(n)])
        for v in nbrs:
            g.remove_edge(n, v)
            bridge = not nx.is_connected(g.to_undirected())
            if bridge:
                g.add_edge(n,v)
            else:
                break
        if bridge:
            g.remove_edge(n, v)
            g.remove_node(n)
        yield (n, v)
