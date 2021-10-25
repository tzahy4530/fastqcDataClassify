#!/usr/bin/python

import pandas as pd
import sys
import io

def readFastqcData(fastqc_path):
    data_string = ''
    read = False
    with open(fastqc_path) as fastqc_data:
        lines = fastqc_data.readlines()
        for line in lines:
            if '>>END_MODULE' in line:
                read = False
            if read:
                data_string += line
            if '>>Overrepresented sequences' in line:
                read = True
    data = io.StringIO(data_string)
    df = pd.read_csv(data, sep="\t")
    return df

def run(inputs, output, fastqc_data, seq_columns, id_column):
    columns_dic = {}
    for path in inputs:
        input_file = pd.read_csv(path, sep='\t')
        for data_index, data_row in fastqc_data.iterrows():
            data_seq = data_row['#Sequence'].upper()
            if data_seq not in columns_dic:
                columns_dic[data_seq] = {'found': False, 'id': 'No Hit'}
            if columns_dic[data_seq]['found']:
                continue

            for input_index, input_row in input_file.iterrows():
                if columns_dic[data_seq]['found']:
                    break;

                for seq_col in seq_columns:
                    input_seq = input_row[seq_col].upper()
                    if data_seq in input_seq:
                        columns_dic[data_seq]['found'] = True
                        columns_dic[data_seq]['id'] = input_row[id_column]
                        break;
                    elif data_seq in input_seq[::-1]:
                        columns_dic[data_seq]['found'] = True
                        columns_dic[data_seq]['id'] = input_row[id_column]
                        break;
    source_array = []
    for key in columns_dic:
        source_array.append(columns_dic[key]['id'])

    fastqc_data['Possible Source'] = source_array
    fastqc_data.to_csv(output)


if __name__ == '__main__':
    inputs = None
    output = None
    seq_columns = None
    id_column = None
    fastqc_data = None

    for i in range(1, len(sys.argv), 2):
        arg = sys.argv[i]
        if arg == '-i':
            inputs = sys.argv[i + 1]
        if arg == '-o':
            output = sys.argv[i + 1]
        if arg == '-f':
            fastqc_data = sys.argv[i + 1]
        if arg == '-sc':
            seq_columns = sys.argv[i + 1]
        if arg == '-idc':
            id_column = sys.argv[i + 1]

        if arg == '--help' or arg == '-h':
            print(f'\nfastqcDataClassify Manual:\n'
                  f' -i <path1,path2,...>:\ncsv file separated by tab, for multiply input files use `,`, all the input files should be in the same format.\n\n'
                  f' -f <path>:\nfastqc_data input path.\n\n' 
                  f' -o <path>:\noutput path.\n\n'
                  f' -sc <column_name1,column_name2,...>:\ncolumn: sequence columns name, columns should include the sequence. for multiply seq columns use `,` .\n\n'
                  f' -idc <column_name>:\n id column name.\n\n')

            sys.exit()

    if not inputs:
        raise ('Input path is required (-i <path1,path2,...>)')
    if not output:
        raise ('Output path is required (-o <path>)')
    if not seq_columns:
        raise ('Seq column name is required (-sc <column_name1,column_name2,...>)')
    if not id_column:
        raise ('Id column name is required (-idc <column_name>)')
    if not fastqc_data:
        raise ('fastqc data is required (-f <path>)')

    fastqc_data = readFastqcData(fastqc_data)
    inputs = inputs.split(',')
    seq_columns = seq_columns.split(',')

    run(inputs, output, fastqc_data, seq_columns, id_column)