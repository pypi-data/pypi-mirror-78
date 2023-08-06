from nefertiti.fileout.xlsxout import ExcelFile, ExcelSheet, ExcelHeader


def main():
    excel_file = ExcelFile('a.xlsx')
    row_datas = [['张三', 19],
                 ['李四', 30],
                 ]
    excel_sheet_a = ExcelSheet(excel_file, 'a', [ExcelHeader('姓名', lambda p: p[0]),
                                                 ExcelHeader('年龄', lambda p: p[1])])
    for row_data in row_datas:
        excel_sheet_a.write_excel_row(row_data)

    excel_sheet_a.worksheet.write(excel_sheet_a.row_index, 0,
                                  '平均年龄')
    excel_sheet_a.worksheet.write_formula(excel_sheet_a.row_index, 1,
                                          'SUM(B1:B{i})/COUNT(B1:B{i})'.format(i=len(row_datas) + 1))


if __name__ == '__main__':
    main()
