import xlrd
import sys
import json


class XlsxLoader():

    def load_data(self,
                  xlsfile,
                  sheet_name,
                  header_row=0,
                  header_col=0,
                  end_row=None,
                  end_col=None):
        # print("start to load xls: %s, %s" % (xlsfile, sheet_name))
        workbook = xlrd.open_workbook(xlsfile)
        if not sheet_name in workbook.sheet_names():
            print("%s not exist!" % (sheet_name))
            return None

        worksheet = workbook.sheet_by_name(sheet_name)
        data = []
        if end_row is None or end_row > worksheet.nrows:
            end_row = worksheet.nrows
        if end_col is None or end_col > worksheet.ncols:
            end_col = worksheet.ncols
        for row in range(header_row + 1, end_row):
            dataRow = {}
            for col in range(header_col, end_col):
                key = worksheet.cell_value(header_row, col)
                val = worksheet.cell_value(row, col)
                dataRow[key] = str(val)
            data.append(dataRow)
        return data
