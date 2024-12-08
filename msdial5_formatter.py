#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2024/01/30

@author: Louis-Félix Nothias
@purpose: to convert the MS-DIAL v5 file into a FBMN diserable format
"""
import pandas as pd
import argparse
import sys
import os

def convert_to_feature_csv(input_filename, output_filename):
    # Read the entire table without treating the first row as headers
    file_extension = os.path.splitext(input_filename)[-1].lower()
    if file_extension == '.csv':
        separator = ','
    elif file_extension == '.tsv' or file_extension == '.txt':
        separator = '\t'
    else:
        raise ValueError("Unsupported file extension. Supported extensions are .csv, .tsv, and .txt")

    input_format = pd.read_csv(input_filename, sep=separator, header=None)

    # Set the first row as the new header
    new_header = input_format.iloc[0]
    input_format.columns = new_header

    # Remove the original first row from the data
    input_format = input_format[1:]
    class_column_position = input_format.columns.get_loc("Class")

    # Keep all columns from the "Class" column position onwards and the first three columns
    columns_to_keep_indices = list(range(3)) + list(range(class_column_position+1, len(input_format.columns)))
    input_format = input_format.iloc[:, columns_to_keep_indices]
    input_format.columns = ['A', 'B', 'C'] + list(input_format.columns[3:])
    
    # Ensure column names are strings to avoid errors when comparing
    input_format.columns = input_format.columns.map(str)

    # Identify columns where the name is 'nan' (as a string)
    nan_columns = [col for col in input_format.columns if col == 'nan']

    # Drop these columns if any are found
    if nan_columns:
        input_format = input_format.drop(columns=nan_columns)
    input_format.columns = input_format.iloc[3]  # Use the third row as header
    input_format = input_format.drop(input_format.index[:4])  # Drop the first three rows

    # Check if "Alignment ID" is in the columns
    if "Alignment ID" not in input_format.columns:
        # If not present, use iloc[2] and index[:3]
        input_format.columns = input_format.iloc[2]  # Use the third row as header
        input_format = input_format.drop(input_format.index[:3])  # Drop the first three rows

    if "Alignment ID" in input_format.columns:
        input_format["Alignment ID"] = input_format["Alignment ID"].astype(int) + 1
    
    rename_map = {
        "Alignment ID": "row ID",
        "Average Rt(min)": "row retention time",
        "Average Mz": "row m/z"
    }
    input_format = input_format.rename(columns=rename_map)
    for col in rename_map.values():
        if col in input_format.columns:
            input_format[col] = input_format[col].astype(str)

        # Append " Peak area" to the remaining column names
    for col in input_format.columns:
        if col not in rename_map.values():
            input_format = input_format.rename(columns={col: col + " Peak area"})

    columns_order = ["row ID", "row m/z", "row retention time"] + [col for col in input_format.columns if col not in ["row ID", "row m/z", "row retention time"]]
    output = input_format[columns_order]

    output.to_csv(output_filename, sep=",", index=False)

    return

def convert_mgf(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        if line.startswith('TITLE='):
            # Searching for 'PEAKID=' in the line
            peakid_parts = [part for part in line.split('|') if part.startswith('PEAKID=')]
            if peakid_parts:
                # Extracting the PEAKID value
                peakid_value = peakid_parts[0].replace('PEAKID=', '').strip()

                # Creating and adding the new SCANS line
                new_lines.append(f'SCANS={int(peakid_value)+1}\n')

            new_lines.append('MSLEVEL=2\n')

        # Skip lines starting with 'TITLE=' or 'Num Peaks:'
        elif not line.startswith('Num Peaks:') and not line.startswith('TITLE='):
            new_lines.append(line)

    with open(output_filename, 'w') as file:
        file.writelines(new_lines)

def help():
    parser = argparse.ArgumentParser(
        description="convert the MS-DIAL v5 file into a FBMN diserable format",
        epilog=(
            "usage example:\n"
            "  python3 msdial5_formatter.py -q input_quant.txt -m input.mgf -Q converted_quant.csv -M converted.mgf"
        ),
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-q", "--input_quant", required=True, help="input quant table from MS-DIAL5")
    parser.add_argument("-m", "--input_mgf", required=True, help="input mgf file from MS-DIAL5")
    parser.add_argument("-Q", "--output_quant", required=True, help="output converted quant table")
    parser.add_argument("-M", "--output_mgf", required=True, help="output converted mgf file")

    args = parser.parse_args()
    return args

if __name__=="__main__":
    args = help()
    convert_mgf(args.input_mgf, args.output_mgf)
    convert_to_feature_csv(args.input_quant, args.output_quant)
