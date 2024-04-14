import argparse
import pandas as pd
import io

def compare(input_key_original, input_key_new):

    excel_file = open(input_key_original, 'rb').read()
    df = pd.read_excel(io.BytesIO(excel_file))
    df.columns = df.columns.str.strip()
    print(df.columns.tolist())

    excel_file_new = open(input_key_new, 'rb').read()
    df2 = pd.read_excel(io.BytesIO(excel_file_new))
    df2.columns = df2.columns.str.strip()
    print(df2.columns.tolist())

    diff_index = df[df['Version'] != df2['Version']].index
    changed_data = df.loc[diff_index, ['Extension ID', 'Extension Name', 'Version', 'Vulnerability', 'Safety Status', 'Permissions']]

    changelogcsv = 'versions_output.xlsx'
    changed_data.to_excel(changelogcsv, index=True)
    print(f"Comparison complete. Changes saved to {changelogcsv}")

def main():
    parser = argparse.ArgumentParser(description='CLI tool to compare two Excel files.')
    parser.add_argument('input_key_original', type=str, help='The path to the original Excel file.')
    parser.add_argument('input_key_new', type=str, help='The path to the new Excel file.')
    args = parser.parse_args()
    compare(args.input_key_original, args.input_key_new)

if __name__ == "__main__":
    main()