#-*- coding: utf-8 -*-

import re


BlankCharSet = set([' ', '\n', '\t'])
CommaNumberPattern = re.compile(u'\d{1,3}([,，]\d\d\d)+')
CommaCharInNumberSet = set([',', '，'])
NumberSet = set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])


def clean_text(text):
    return clean_number_in_text(remove_blank_chars(strQ2B(remove_blank_chars(text))))


def clean_number_in_text(text):
    comma_numbers = CommaNumberPattern.finditer(text)
    new_text, start = [], 0
    for comma_number in comma_numbers:
        new_text.append(text[start:comma_number.start()])
        start = comma_number.end()
        new_text.append(remove_comma_in_number(comma_number.group()))
    new_text.append(text[start:])
    return ''.join(new_text)


def remove_blank_chars(text):
    new_text = []
    if text is not None:
        for ch in text:
            if ch not in BlankCharSet:
                new_text.append(ch)
    return ''.join(new_text)


def remove_comma_in_number(text):
    new_text = []
    if text is not None:
        for ch in text:
            if ch not in CommaCharInNumberSet:
                new_text.append(ch)
    return ''.join(new_text)

def extract_number(text):
    new_text = []
    for ch in text:
        if ch in NumberSet:
            new_text.append(ch)
    return ''.join(new_text)

def normalize_num(text):

    text=text.group(0)
    coeff = 1.0
    if '亿' in text:
        coeff *= 100000000
    if '万' in text:
        coeff *= 10000
    if '千' in text or '仟' in text:
        coeff *= 1000
    if '百' in text or '佰' in text:
        coeff *= 100
    if '%' in text:
        coeff *= 0.01
    try:
        number = float(extract_number(text))
        number_text = '%.4f' % (number * coeff)
        if number_text.endswith('.0'):
            return number_text[:-2]
        elif number_text.endswith('.00'):
            return number_text[:-3]
        elif number_text.endswith('.000'):
            return number_text[:-4]
        elif number_text.endswith('.0000'):
            return number_text[:-5]
        else:
            if '.' in number_text:
                idx = len(number_text)
                while idx > 1 and number_text[idx-1] == '0':
                    idx -= 1
                number_text = number_text[:idx]
            return number_text
    except:
        return text
def normalize_date(date):
    char='年月日./'
    date=date.group(0)
    for ch in date:
        if ch in char:
            date.replace(ch,'-')
    return date
def normalize_per(text):
    text=text.group(0)
    try:
        return str(float(text[:-1])/100)
    except:
        print('normalize_per:\t',text)
        return text
def normalize(content):
    content=clean_text(content)
    money = re.compile(r'\d[\\.|\d]*[亿|万|千|百|元]$')
    content=money.sub(normalize_num,content)
    date = re.compile(r'(\d\d\d\d)[-.年](\d{1,2})[-.月](\d{1,2})日?$')
    content=date.sub(normalize_date,content)
    per = re.compile(r'([0-9\.]+\%)')
    content=per.sub(normalize_per,content)
    return content
def strQ2B(ustring):
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in str(s):
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
                inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ss

if __name__ == "__main__":
    text = "总股 200万元 总价 300,000,000,000 元"
    # print(text)
    # print(clean_number_in_text(text))

