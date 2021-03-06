from Bio import SeqIO
import os.path
import sys

def get_seq_from_fasta(file, include_reverse = True):
    if os.path.isfile(file):
        try:
            rec_dict = SeqIO.to_dict(SeqIO.parse(file, 'fasta'))
            if len(rec_dict) == 0:
                raise RuntimeError('¿y los reads?')
            return rec_dict
        except IOError as err:
            raise err

    else:
        raise RuntimeError('error 404 file not found')

def include_reverse(rec_dict):
    rev_rec_dict = {}
    for seq_id, seq in rec_dict.items():
        rev_rec_dict[seq_id + '_rev'] = seq.reverse_complement()

    rec_dict.update(reversed_record_dict)
    return rec_dict

def output_assembly(sequences, output_file_name="./output.txt",
                    longest_assembly_only=False):
    with open(output_file_name, 'w') as output_handle:
        if longest_assembly_only:
            sequence = max(sequences, key=len)
            output_handle.write(str(sequence) + '\n')
        else:
            for sequence in sorted(sequences,key=len,reverse=True):
                output_handle.write(str(sequence) + '\n')
