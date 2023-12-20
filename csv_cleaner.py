import pandas as pd
import os

# Cleans the excel tables returned by Textract
# Removes unnecessary characters and saves the cleaned excel files with a cleaned- prefix

def save_to_excel_workbook(prefix="cleaned-table-", extension=".csv", output_filename="Cleaned_Tables_Workbook.xlsx"):
    """
    Save all cleaned DataFrames to separate sheets in a single Excel workbook.
    """
    # Get all cleaned CSV file paths
    cleaned_file_paths = get_existing_file_paths(prefix, extension)

    # Create an Excel writer object
    with pd.ExcelWriter(output_filename) as writer:
        for file_path in cleaned_file_paths:
            # Extract sheet name from file path (e.g., "cleaned-table-1" becomes "table-1")
            sheet_name = os.path.basename(file_path).replace(prefix, "")
            df = pd.read_csv(file_path)
            df.to_excel(writer, sheet_name=sheet_name, index=False)


def clean_and_save_dataframes(prefix="table-", extension=".csv"):
    """
    Clean all existing dataframes and save them with a "cleaned-" prefix.
    """
    file_paths = get_existing_file_paths(prefix, extension)
    for file_path in file_paths:
        df = clean_dataframe(file_path)
        output_path = "cleaned-" + file_path
        df.to_csv(output_path, index=False)


def clean_dataframe(file_path):
    """
    Read a CSV file from the given path, clean the data, and return the cleaned DataFrame.
    """
    df = pd.read_csv(file_path)
    
    # Remove columns with names containing "Unnamed"
    remove_unnamed_columns(df)
    
    # Remove apostrophes from headers
    remove_apostrophes_from_headers(df)
    
    # Apply data cleaning transformations
    df = df.map(remove_non_alphanumeric)
    df = df.map(strip_whitespace)
    
    # Format columns as numeric
    format_columns_as_numeric(df)
    
    # Remove rows after "Confidence Scores"
    remove_rows_after_confidence_scores(df)

    return df


def remove_unnamed_columns(df):
    """Drop columns with names containing "Unnamed"."""
    cols_to_drop = [col for col in df.columns if 'Unnamed' in col]
    df.drop(columns=cols_to_drop, inplace=True, errors='ignore')


def remove_non_alphanumeric(value):
    """Remove non-alphanumeric characters from a value, excluding spaces."""
    return ''.join(e for e in str(value) if e.isalnum() or e.isspace())


def strip_whitespace(value):
    """Strip whitespace from a value."""
    return str(value).strip()

def format_columns_as_numeric(df):
    """
    Attempt to format columns in the DataFrame as numeric.
    """
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')
        
def remove_apostrophes_from_headers(df):
    """Remove apostrophes from DataFrame headers."""
    df.columns = df.columns.str.replace("'", "")


def remove_rows_after_confidence_scores(df):
    """Remove rows in the DataFrame after the row containing 'Confidence Scores'."""
    confidence_scores_index = df[df.iloc[:, 0].str.contains('Confidence Scores', na=False)].index
    if not confidence_scores_index.empty:
        df.drop(df.index[confidence_scores_index[0]-1:], inplace=True)

def get_existing_file_paths(prefix="table-", extension=".csv"):
    """
    Return a list of existing file paths with the specified prefix and extension.
    """
    i = 1
    file_paths = []
    while True:
        file_path = f"{prefix}{i}{extension}"
        if os.path.exists(file_path):
            file_paths.append(file_path)
            i += 1
        else:
            break
    return file_paths
