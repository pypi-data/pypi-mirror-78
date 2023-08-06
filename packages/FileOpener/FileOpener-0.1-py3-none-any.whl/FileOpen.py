import pandas as pd
import xlrd

def data_find(sheet, col):
    '''
    Returns the row the data starts on
    
    Arguments: 
        Sheet (str): 
            Which sheet to look through
        col (): 
            Which column the data starts on

    Return:
        Row (int):
            the row the data starts on
    '''
    for row in range(sheet.nrows):
        if str(sheet.cell(row, col)).split(':')[0] == 'xldate':
            return row

def header_find(sheet):
    '''
    Returns row and column the header starts on
    Returns type of data structures the file it is

    Arguments: 
        Sheet(str): which sheet to look through

    Return:
        Row (int):
            the row the header starts on
        col (int):
            the column the header starts on
        cell (string):
            Tag or Stream
    '''
    for col in range(sheet.ncols):
        for row in range(sheet.nrows):
            cell = str(sheet.cell(row, col)).split(':')[-1]
            if cell.startswith("'Tag") or cell.startswith("'Stream'"):
                return row, col, cell

def header_combine(df):
    '''
    Returns list of strings, of each column of the imported data frame, flattened and seperated by underscores

    Arguments: 
        df (dataframe): 
            which dataframe to flatten

    Returns:
        headers (list):
            list of the flattened headers
    '''
    headers = ['_'.join([str(row) for row in df[col]]) for col in df]
    return headers

def open_xl(sheet, sheet_xlrd, data_file):
    '''
    Returns the dataframe with the data and the header combined into a single dataframe

    Arguments: 
        sheet (str): 
            sheet to look through
        df (dataframe): 
            data file to turn into data frame

    Returns: 
        data_df (dataframe):
            dataframe combining the headers and the data

    '''
    header_data = header_find(sheet_xlrd)
    header_row_start, header_col_start, data_type = header_data

    if data_type.startswith("'Tag"):
        data_row_start = data_find(sheet_xlrd, header_col_start)
        header_df = pd.read_excel(data_file, 
                                sheet_name=sheet, 
                                skiprows=range(header_row_start), 
                                usecols=range(header_col_start, sheet_xlrd.ncols), 
                                nrows=3, 
                                header=None)
        headers=header_combine(header_df)
        data_df = pd.read_excel(data_file, 
                                sheet_name=sheet, 
                                skiprows=range(data_row_start), 
                                usecols=range(header_col_start, sheet_xlrd.ncols), 
                                header=None, 
                                names=headers)

    if data_type == "'Stream'":
        rows = [header_row_start, header_row_start+1]
        data_df = pd.read_excel(data_file, header=rows)
                
    return data_df

def import_file(data_file):
    '''
    Return a dictionary of pandas dataframes extracted from input excel or csv file
    
    Excel files:
        - loop through sheets
        - associate with one of 3 input types
        - find headers: "Tag"...
        - import into pandas data frame

    Arguments: 
        data_file (path):
            path to input file
    
    Returns:
        dfs (dict):
            ouput dictionary: {"excel_sheet_name": pd.DataFrame, 
                               "CSV": pd.DataFrame}
    '''
    dfs = {}
    try:
        #Open Excel File
        workbook = xlrd.open_workbook(data_file)
        sheet_amount = len(workbook.sheet_names())

        for index in range(sheet_amount):
            sheet = workbook.sheet_names()[index]
            sheet_xlrd = workbook.sheet_by_index(index)

            if HeaderFind(sheet_xlrd):
                df = open_xl(sheet, sheet_xlrd, data_file)
                dfs.update({sheet : df})

    except:
        #Open Csv File
        with open(data_file) as csv_file:
            df = pd.read_csv(data_file)
            dfs.update({"CSV" : df})
    
    return dfs
