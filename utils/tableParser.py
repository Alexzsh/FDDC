#coding=utf-8
"""
@version=1.0
@author:zsh
@file:tableParser.py
@time:2018/11/6 09:23
"""
import codecs
from bs4 import BeautifulSoup
import TextUtils
class parseHtmlGetTable:
    def __init__(self, shareholderFullName, shareholderShortName, finishDate, sharePrice, shareNum, shareNumAfterChg, sharePcntAfterChg):
        # 股东
        self.shareholderFullName = shareholderFullName
        # 股东
        self.shareholderShortName = shareholderShortName
        # 结束日期
        self.finishDate = finishDate
        # 增减持股价
        self.sharePrice = sharePrice
        # 增减持股数
        self.shareNum = shareNum
        # 增减持变动后股数
        self.shareNumAfterChg = shareNumAfterChg
        # 增减持变动后持股比例
        self.sharePcntAfterChg = sharePcntAfterChg
        self.table_dict_field_pattern_dict = {}
    @classmethod
    def parse_table(self,html_file_path):
        """
        解析 HTML 中的 table
        返回一个二维表
        :param html_file_path:
        :return:
        """
        rs_list = []
        with codecs.open(html_file_path, encoding='utf-8', mode='r') as fp:
            soup = BeautifulSoup(fp.read(), "html.parser")
            for table in soup.find_all('table'):
                table_dict, is_head_two_rowspan = self.parse_table_to_2d_dict(table)
                row_length = len(table_dict)
                if table_dict is not None:
                    if is_head_two_rowspan and row_length > 2:
                        try:
                            new_table_dict = {}
                            head_row = {}
                            col_length = len(table_dict[0])
                            for col_idx in range(col_length):
                                head_row[col_idx] = table_dict[0][col_idx] + table_dict[1][col_idx]
                            new_table_dict[0] = head_row
                            for row_idx in range(2, row_length):
                                new_table_dict[row_idx - 1] = table_dict[row_idx]
                            rs_list.append(new_table_dict)
                        except KeyError:
                            rs_list.append(table_dict)
                    else:
                        rs_list.append(table_dict)
        return rs_list

    @staticmethod
    def parse_table_to_2d_dict(table):
        rs_dict = {}
        row_index = 0
        is_head_two_rowspan, is_head = False, True
        for tr in table.find_all('tr'):
            col_index, cur_col_index = 0, 0
            for td in tr.find_all('td'):
                rowspan = td.get('rowspan')
                rowspan = int(rowspan) if (rowspan is not None and int(rowspan) > 1) else 1
                colspan = td.get('colspan')
                colspan = int(colspan) if (colspan is not None and int(colspan) > 1) else 1
                if is_head:
                    if rowspan > 1 or colspan > 1:
                        is_head_two_rowspan = True
                    is_head = False
                for r in range(rowspan):
                    if (row_index + r) not in rs_dict:
                        rs_dict[row_index + r] = {}
                    for c in range(colspan):
                        cur_col_index = col_index
                        while cur_col_index in rs_dict[row_index + r]:
                            cur_col_index += 1
                        rs_dict[row_index + r][cur_col_index] = TextUtils.remove_blank_chars(td.text)
                        cur_col_index += 1
                col_index = cur_col_index
            row_index += 1
        return rs_dict, is_head_two_rowspan
    def extract_from_table_dict(self, table_dict):
        rs = []
        if table_dict is None or len(table_dict) <= 0:
            return rs
        row_length = len(table_dict)
        field_col_dict = {}
        skip_row_set = set()
        # 1. 假定第一行是表头部分则尝试进行规则匹配这一列是哪个类型的字段
        # 必须满足 is_match_pattern is True and is_match_col_skip_pattern is False
        head_row = table_dict[0]
        col_length = len(head_row)
        for i in range(col_length):
            text = head_row[i]
            for (field_name, table_dict_field_pattern) in self.table_dict_field_pattern_dict.items():
                if table_dict_field_pattern.is_match_pattern(text) and \
                        not table_dict_field_pattern.is_match_col_skip_pattern(text):
                    if field_name not in field_col_dict:
                        field_col_dict[field_name] = i
                    # 逐行扫描这个字段的取值，如果满足 row_skip_pattern 则丢弃整行 row
                    for j in range(1, row_length):
                        try:
                            text = table_dict[j][i]
                            if table_dict_field_pattern.is_match_row_skip_pattern(text):
                                skip_row_set.add(j)
                        except KeyError:
                            pass
        if len(field_col_dict) <= 0:
            return rs
        # 2. 遍历每个有效行，获取 record
        for row_index in range(1, row_length):
            if row_index in skip_row_set:
                continue
            record = parseHtmlGetTable(None, None, None, None, None, None, None)
            for (field_name, col_index) in field_col_dict.items():
                try:
                    text = table_dict[row_index][col_index]
                    if field_name == 'shareholderFullName':
                        record.shareholderFullName = self.table_dict_field_pattern_dict.get(field_name).convert(text)
                    elif field_name == 'finishDate':
                        record.finishDate = self.table_dict_field_pattern_dict.get(field_name).convert(text)
                    elif field_name == 'sharePrice':
                        record.sharePrice = self.table_dict_field_pattern_dict.get(field_name).convert(text)
                    elif field_name == 'shareNum':
                        record.shareNum = self.table_dict_field_pattern_dict.get(field_name).convert(text)
                    elif field_name == 'shareNumAfterChg':
                        record.shareNumAfterChg = self.table_dict_field_pattern_dict.get(field_name).convert(text)
                    elif field_name == 'sharePcntAfterChg':
                        record.sharePcntAfterChg = self.table_dict_field_pattern_dict.get(field_name).convert(text)
                    else:
                        pass
                except KeyError:
                    pass
            rs.append(record)
        return rs
    def mergeRecord(self, changeRecords, changeAfterRecords):
        if len(changeRecords) == 0 or len(changeAfterRecords) == 0:
            return
        last_record = None
        for record in changeRecords:
            if last_record != None and record.shareholderFullName != last_record.shareholderFullName:
                self.mergeChangeAfterInfo(last_record,changeAfterRecords)
            last_record = record
        self.mergeChangeAfterInfo(last_record,changeAfterRecords)

    def mergeChangeAfterInfo(self, changeRecord, changeAfterRecords):
        for record in changeAfterRecords:
            if record.shareholderFullName == changeRecord.shareholderFullName:
                changeRecord.shareNumAfterChg = record.shareNumAfterChg
                changeRecord.sharePcntAfterChg = record.sharePcntAfterChg
    @classmethod
    def parse_content(self, html_file_path):
        """
        解析 HTML 中的段落文本
        按顺序返回多个 paragraph 构成一个数组，
        每个 paragraph 是一个 content 行构成的数组
        :param html_file_path:
        :return:
        """
        rs = []
        with codecs.open(html_file_path, encoding='utf-8', mode='r') as fp:
            soup = BeautifulSoup(fp.read(), "html.parser")
            paragraphs = []
            for div in soup.find_all('div'):
                div_type = div.get('type')
                if div_type is not None and div_type == 'paragraph':
                    paragraphs.append(div)
            for paragraph_div in paragraphs:
                has_sub_paragraph = False
                for div in paragraph_div.find_all('div'):
                    div_type = div.get('type')
                    if div_type is not None and div_type == 'paragraph':
                        has_sub_paragraph = True
                if has_sub_paragraph:
                    continue
                rs.append([])
                for content_div in paragraph_div.find_all('div'):
                    div_type = content_div.get('type')
                    if div_type is not None and div_type == 'content':
                        rs[-1].append(TextUtils.clean_text(content_div.text))
        paragraphs = []
        for content_list in rs:
            if len(content_list) > 0:
                paragraphs.append(''.join(content_list))
        return paragraphs