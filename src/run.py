import argparse

from utils import *
from de_bruijn_graph import *
from euler import eulerian_random_walk

def run(input_fasta, output_file, kmer_length,
        reverse_complement = False, graph = False,
        longest_assembly_only  = False):
    seq_dict = get_seq_from_fasta(input_fasta)
    
    if reverse_complement:
        seq_dict = include_reverse_complement(seq_dict)

    dbg = DeBruijnGraph(seq_dict, int(kmer_length))

    visualize_graph(dbg.G)

    assembly = eulerian_random_walk(dbg)

    if len(assembly) != 0:
        output_assembly(assembly,output_file,longest_assembly_only)
    else:
        print('Epic fail')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfastafile',
                        help=' el fasta que vamos a ensamblar',
                        default='../data/dummy.fa')
    
    parser.add_argument('--reverse_complement', action='store_true',
                        help='¿Incluimos la secuencia complementaria?',
                        default=False)

    parser.add_argument('-k', '--kmerlength',
                       help='la longitud de los kmers',
                       default=6)
    parser.add_argument('-o', '--outputfile',
                        help='el archivo de salida',
                        default='out.txt')
    
    parser.add_argument('--output_longest_assembly', action='store_true',
                        help='¿retornamos solamente la secuencia mas larga?',
                        default=False)
    
    args = parser.parse_args()
    assembly = run(args.inputfastafile, args.outputfile, args.kmerlength,
                   args.reverse_complement, args.output_longest_assembly)
