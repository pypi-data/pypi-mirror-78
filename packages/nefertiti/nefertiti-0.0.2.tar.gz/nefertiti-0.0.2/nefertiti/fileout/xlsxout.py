import itertools

import xlsxwriter


class ExcelFile(object):

    def __init__(self, file):
        self.workbook = xlsxwriter.Workbook(file)

    def __del__(self):
        self.workbook.close()


class ExcelSheet(object):

    def __init__(self, excel_file, sheet_name, excel_headers, write_header=True, tab_color=None):
        self.workbook = excel_file.workbook
        self.worksheet = self.workbook.add_worksheet(sheet_name)
        if tab_color:
            self.worksheet.set_tab_color(tab_color)
        self.excel_headers = [h.dump for h in excel_headers]
        self.row_index = 0

        # 首行数据
        self.worksheet.freeze_panes(1, 0)
        for excel_header, col_index in zip(self.excel_headers, itertools.count(0)):
            if write_header:
                self.worksheet.write_string(self.row_index, col_index, excel_header['key'])

            if 'format' in excel_header:
                cell_format = self.workbook.add_format(excel_header['format'])
                self.worksheet.set_column(col_index, col_index, excel_header.get('width'), cell_format)

            elif 'width' in excel_header:
                self.worksheet.set_column(col_index, col_index, excel_header['width'])
        self.row_index += 1

    def write_excel_row(self, row_data):
        """输出一行数据到excel"""
        for excel_header, col_index in zip(self.excel_headers, itertools.count(0)):
            if 'field' in excel_header:
                func = excel_header['field']
                value = func(row_data)
                if value is not None:
                    self.worksheet.write(self.row_index, col_index, value)
            elif 'formula' in excel_header:
                func = excel_header['formula']
                value = func(self.row_index + 1)  # 行号从计数 1 开始
                if value is not None:
                    self.worksheet.write_formula(self.row_index, col_index, value)
        self.row_index += 1


class ExcelHeader(object):

    def __init__(self, key, field=None, formula=None, width=None, format=None):
        """

        :param key: excel首行列名
        :param field: lambda object: 将传入的对象解析返回需要的值
        :param formula: lambda row_index: 将传入的行号加工成公式
        :param width: 列宽
        :param format: 格式见 https://xlsxwriter.readthedocs.io/format.html
        """
        self.dump = {
            'key': key,
        }
        if field:
            self.dump['field'] = field
        elif formula:
            self.dump['formula'] = formula
        if width:
            self.dump['width'] = width
        if format:
            self.dump['format'] = format


# 对文本字体颜色灰色显示
format_font_gray = {
    'font_color': '#CCCCCC',
}


# 对数字进行百分比格式化显示
format_percent_blue = {
    'num_format': '0.0%',
    'font_color': 'Cyan',
}
