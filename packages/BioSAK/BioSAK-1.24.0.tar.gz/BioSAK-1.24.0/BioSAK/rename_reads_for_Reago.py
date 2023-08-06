import os
import argparse
from Bio import SeqIO


rename_reads_for_Reago_usage = '''
=========================== rename_reads_for_Reago example commands ===========================

BioSAK rename_reads_for_Reago -in Soil_reads_R1.fasta -out Soil_reads_R1_renamed.fasta -d 1
BioSAK rename_reads_for_Reago -in Soil_reads_R2.fasta -out Soil_reads_R2_renamed.fasta -d 2

===============================================================================================
'''


def sep_path_basename_ext(file_in):

    # separate path and file name
    file_path, file_name = os.path.split(file_in)
    if file_path == '':
        file_path = '../My_Python_scripts/scripts_backup'

    # separate file basename and extension
    file_basename, file_extension = os.path.splitext(file_name)

    return file_path, file_basename, file_extension


def rename_reads_for_Reago(args):

    input_file  = args['in']
    output_file = args['out']
    direction   = args['d']

    input_file_path, input_file_basename, input_file_extension = sep_path_basename_ext(input_file)

    output_file_handle = open(output_file, 'w')
    seq_index = 1
    for seq_record in SeqIO.parse(input_file, 'fasta'):
        output_file_handle.write('>%s_%s.%s\n' % (input_file_basename, seq_index, direction))
        output_file_handle.write('%s\n' % seq_record.seq)
        seq_index += 1

    output_file_handle.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='', add_help=False)

    parser.add_argument('-in',  required=True,  type=str, help='input fasta file')
    parser.add_argument('-out', required=True,  type=str, help='renamed fasta file')
    parser.add_argument('-d',   required=True,  type=int, help='chose from 1 (forward) or 2 (reverse)')

    args = vars(parser.parse_args())

    rename_reads_for_Reago(args)


