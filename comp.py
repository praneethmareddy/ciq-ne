import pandas as pd
import glob

def extract_csv_parameters(csv_folder):
    """Extract all parameter names from CSV files in the given folder"""
    all_parameters = set()
    csv_files = glob.glob(f"{csv_folder}/*.csv")
    
    for file in csv_files:
        with open(file, 'r') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                if lines[i].startswith('@'):
                    # Section line - next line should be parameters
                    if i+1 < len(lines):
                        params = lines[i+1].strip().split(',')
                        all_parameters.update(params)
                    i += 3  # skip section, params, and values lines
                else:
                    i += 1
    return all_parameters

def compare_with_xlsx(csv_folder, xlsx_file):
    # Get parameters from CSV files
    csv_params = extract_csv_parameters(csv_folder)
    
    # Get column names from XLSX
    xlsx_df = pd.read_excel(xlsx_file)
    xlsx_columns = set(xlsx_df.columns)
    
    # Find matches and differences
    matching = csv_params.intersection(xlsx_columns)
    csv_only = csv_params.difference(xlsx_columns)
    xlsx_only = xlsx_columns.difference(csv_params)
    
    return {
        'matching_parameters': sorted(matching),
        'csv_only_parameters': sorted(csv_only),
        'xlsx_only_columns': sorted(xlsx_only)
    }

# Usage example:
results = compare_with_xlsx('path/to/csv/folder', 'path/to/file.xlsx')

print("Matching parameters:", results['matching_parameters'])
print("Parameters only in CSV files:", results['csv_only_parameters'])
print("Columns only in XLSX:", results['xlsx_only_columns'])
