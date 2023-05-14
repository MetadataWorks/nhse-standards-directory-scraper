
from openpyxl.styles.borders import Border, Side
from openpyxl import Workbook  
from openpyxl.utils.cell import get_column_letter
from openpyxl.styles import Alignment, PatternFill
from datetime import datetime
import pandas as pd


thin_border = Border(left=Side(style='thin'), 
                     right=Side(style='thin'), 
                     top=Side(style='thin'), 
                     bottom=Side(style='thin'))

headers = {'A':"Persistent Identifer", 'B':"Summary", 'N':"Documentation", 'S':"Publisher", 'X':"Document Control", 'AM':"Data Status"}



def create_excel(api_data):

    # filename containing current date and time
    now = datetime.now()
    filename = now.strftime("%d-%m-%Y__%H-%M-%S")


    work_book = Workbook()  
    print('Workbook')

    work_sheet = work_book.active  
    print('worksheet')

    data_header = list(api_data[0].keys())
    data_header_updated = []
    for heading in data_header:
        if 'Publisher ' in heading:
            heading = heading.replace('Publisher ', '')
        data_header_updated.append(heading)


    work_sheet.append(data_header_updated)
    print('inserted headers')

    for col in range(1, 41):
        work_sheet.cell(1, col).alignment = Alignment(horizontal='center',vertical='center', wrap_text=True)

    for x in api_data:
        work_sheet.append(list(x.values()))
    
    print('inserted data')


    dims = {}
    for row in work_sheet.rows:
        for cell in row:
            if cell.value:
                colLetter = get_column_letter(cell.column)
                dims[colLetter] = max((dims.get(colLetter, 0), len(str(cell.value))))    

    for col, value in dims.items():
        if value<10:
            value=10
        work_sheet.column_dimensions[col].width = value

    print('width settled')

    data_comparison_file_format = f'comparison_files/comparison_file_{filename}.xlsx'
    work_book.save(data_comparison_file_format)
    print('no_merged_header_xlsx saved for further comparison purpose')
    

    work_sheet.insert_rows(idx=1)
    work_sheet.insert_rows(idx=1)

    print('new rows inserted')


    # cells to merge  
    work_sheet.merge_cells('A1:A2') 
    work_sheet.merge_cells('B1:M2') 
    work_sheet.merge_cells('N1:R2') 
    work_sheet.merge_cells('S1:W2') 
    work_sheet.merge_cells('X1:AL1')
    work_sheet.merge_cells('X2:AJ2')
    work_sheet.merge_cells('AM1:AN2') 

    print('cells merged')


    for col in ['A', 'B', 'N', 'S', 'X', 'AM']:
        work_sheet[f'{col}1'].alignment = Alignment(horizontal='center',vertical='center', wrap_text=True)
        work_sheet[f'{col}1'].border = thin_border
        work_sheet[f'{col}1'].fill = PatternFill(start_color='f1c232', fill_type='solid')
        work_sheet[f'{col}1'].value = headers[col]
    

    work_sheet['X2'].fill = PatternFill(start_color='f1c232', fill_type='solid')
    work_sheet['X2'].border = thin_border

    work_sheet['AK2'].fill = PatternFill(start_color='e69138', fill_type='solid')
    work_sheet['AK2'].alignment = Alignment(horizontal='center',vertical='center', wrap_text=True)
    work_sheet['AK2'].border = thin_border
    work_sheet['AK2'].value = 'Reviews'


    work_sheet['AL2'].fill = PatternFill(start_color='e69138', fill_type='solid')
    work_sheet['AL2'].alignment = Alignment(horizontal='center',vertical='center', wrap_text=True)
    work_sheet['AL2'].border = thin_border
    work_sheet['AL2'].value = 'Legal Authorities'


    print('rows formatted')

    
    scraped_data_filename = f'scraped_files/NHS_{filename}.xlsx'
    work_book.save(scraped_data_filename)
    print('scraped data saved at: ', scraped_data_filename)

    # try:
    #     ### convert it into csv
    #     read_file = pd.read_excel(scraped_data_filename)
    #     print('xlsx read')

    #     read_file.to_csv(f'nhs_csv_files/NHS_{filename}.csv')
    #     print('csv saved')

    # except:
    #     print('error while converting xlsx file into csv')


    return scraped_data_filename, data_comparison_file_format




