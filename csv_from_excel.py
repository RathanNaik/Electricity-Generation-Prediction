import xlrd
import csv
import os
from os import sys

def csv_to_excel(path,excel_file):
    workbook = xlrd.open_workbook(excel_file)
    all_worksheets = workbook.sheet_names()
    for worksheet_name in all_worksheets[1:]:
        worksheet = workbook.sheet_by_name(worksheet_name)
        cell = worksheet.cell(0,2)
        #print cell, cell.value
        
        your_csv_file = open(path+''.join([worksheet_name,'.csv']), 'wb')
        wr = csv.writer(your_csv_file, quoting=csv.QUOTE_NONE)
        
        for rownum in xrange(worksheet.nrows):
            #print [str(entry) for entry in worksheet.row_values(rownum)]
            
            wr.writerow([unicode(entry).encode("utf-8").strip() for entry in worksheet.row_values(rownum)])
            
        your_csv_file.close()

if __name__ == "__main__":
    csv_from_excel("./","C:\parikshit\project\District-wise Rainfall data_2004-2010.xls")