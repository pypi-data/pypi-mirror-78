import openpyxl


class XlsxLoader(object):

    @staticmethod
    def load(file, sheet_name=None):
        wb = openpyxl.load_workbook(file)
        if sheet_name:
            ws = wb.get_sheet_by_name(sheet_name)
        else:
            ws = wb.active  # 如果没有传入sheet name, 则默认使用第1个
        for row in ws.rows:
            back_row = []
            for cell in row:
                if type(cell) is openpyxl.cell.cell.Cell:
                    back_row.append(str(cell.value) if cell.value else '')
                else:
                    back_row.append(cell)
            yield back_row
        wb.close()
