import csv


class CsvLoader(object):

    @staticmethod
    def load(file, encoding='GBK'):
        with open(file, encoding=encoding) as f_in:
            reader = csv.reader(f_in)
            for row in reader:
                yield row
