import datetime

import xlrd


class XlsLoader(object):

    @staticmethod
    def load(file, sheet_name=None):
        book = xlrd.open_workbook(file, encoding_override='GBK')

        if sheet_name:
            sh = book.sheet_by_name(sheet_name)
        else:
            sh = book.sheet_by_index(0)

        for rx in range(sh.nrows):
            row = sh.row(rx)
            back_row = []
            for cell in row:
                if cell.ctype == 3:  # xldate
                    back_row.append(datetime.datetime(*xlrd.xldate_as_tuple(cell.value, book.datemode)))
                else:
                    back_row.append(str(cell.value))

            yield back_row
