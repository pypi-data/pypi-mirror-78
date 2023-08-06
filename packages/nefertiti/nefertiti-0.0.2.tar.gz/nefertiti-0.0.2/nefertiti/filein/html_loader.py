from lxml import etree


htmlparser = etree.HTMLParser()


class HtmlLoader(object):

    """
    要有一定的xpath知识
    for row in self.load(self.source_file, '//table/tr', './td/text()'):
    """

    @staticmethod
    def load(file, row_xpath, col_xpath):
        """使用xpath解析读取xml格式文本

        :param file: 含有table表单亦或者有明确的行列XML标签的文本
        :param row_xpath: 找到行数据的xpath表达式
        :param col_xpath: 基于行数据的寻找列数据的xpath表达式
        :return:
        """
        tree = etree.parse(file, htmlparser)
        for row_ele in tree.xpath(row_xpath):
            row_data = list()
            for col_ele in row_ele.xpath(col_xpath):
                if isinstance(col_ele, etree._Element):
                    row_data.append(col_ele.text)
                else:
                    row_data.append(col_ele)
            yield row_data
