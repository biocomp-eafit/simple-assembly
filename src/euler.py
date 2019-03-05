import networkx as nx
import operator
import matplotlib.pyplot as plt
from functools import reduce

def has_euler_circuit(graph):
    if not nx.is_strongly_connected(graph):
        return False
    for node in graph.nodes():
        if graph.in_degree(node) != graph.out_degree(node):
            return False
    return True    

def has_euler_path(graph):
    flag = False
    start = None
    end = None
    for n in graph.nodes():
        graph.node[n]['end'] = False
        graph.node[n]['start'] = False
        if graph.degree(n) % 2 != 0:
            if graph.out_degree(n) == graph.in_degree(n) - 1:
                graph.node[n]['end'] = True
                end = n
            elif graph.in_degree(n) == graph.out_degree(n) - 1:
                graph.node[n]['start'] = True
                start = n
            flag = True
    return flag, start, end


def eulerian_random_walk(DBG):
    assembly = []
    for subg in DBG.subgraphs:
        # nx eulerian assumes strong connection for directed graph
        if subg.graph['euler_circuit']:
            a_euler_circuit = list(nx.eulerian_circuit(subg))
            # assembly removed the last edge to source
            assembly.append(make_contig_from_path(a_euler_circuit[:-1]))
        elif subg.graph['euler_path']:
            # add a temp edge here
            subg.add_edge(subg.graph['euler_path_end'],
                          subg.graph['euler_path_start'],
                          seq='[temp_edge]')
            a_euler_path = list(find_eulerian_path(subg,
                                                  subg.graph[
                                                      'euler_path_start']))[:-1]
            #print(a_euler_path)
            assembly.append(make_contig_from_path(a_euler_path))
        else:
            subg.graph['eulerian'] = False
    return assembly

def find_eulerian_path(graph, start):
    if not graph.graph['euler_path']:
        raise RuntimeError('No hay camino eulereano :c #Sad')

    copy_graph = graph.__class__(graph)
    degree = copy_graph.in_degree
    edges = copy_graph.in_edges_iter
    get_node = operator.itemgetter(0)

    stack = [start]
    last_node = None
    while stack:
        current_node = stack[-1]
        # if there is no more edge to explore
        if degree(current_node) == 0:
            if last_node is not None:
                yield (last_node, current_node)
            last_node = current_node
            stack.pop()  # remove [-1]
        else:  # move on and remove the edge through
            random_edge = next(edges(current_node))
            stack.append(get_node(random_edge))
            copy_graph.remove_edge(*random_edge)


def make_contig_from_path(path):
    return reduce(lambda x,y: x+y[-1],[l + r[-1] for l, r in path])
