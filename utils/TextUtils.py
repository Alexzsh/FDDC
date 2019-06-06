#-*- coding: utf-8 -*-

import re


BlankCharSet = set([' ', '\n', '\t'])
CommaNumberPattern = re.compile(u'\d{1,3}([,，]\d\d\d)+')
CommaCharInNumberSet = set(list(',，.。、？》《：”；’-+'))
NumberSet = set(list('0123456789.'))


def clean_text(text):
    return clean_number_in_text(strQ2B(remove_blank_chars(text)))

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
    return ''.join(ss)
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
    """normalized number
    
    Arguments:
        text [string] -- matched number
    
    Returns:
        string -- normalized result data
    """
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
    """normalze date
    
    Returns:
        [string] -- [normalized result date]
    """
    char = re.compile('[年月./]')
    date=date.group(0)
    date = char.sub('-',date)
    if '日' in date:
        date=date.replace('日','')
    return date
def normalize_num_continue(text):
    """normalize number
    
    Returns:
        string -- normalized result data
    """

    text = text.group(0)
    try:
        l,i,r = text.split('.')
        k =1 if len(i)==3 else 2
        i=i[:k]+','+i[k:]
        return '.'.join([l,i,r])
    except:
        print('normalize_num:\t',text)
        return text
def normalize_per(text):
    """normalize percentage 

    Returns:
        [string] -- [normalized result data]
    """
    text=text.group(0)
    try:
        return str(float(text[:-1])/100)
    except:
        print('normalize_per:\t',text)
        changeNumSeq = re.compile(r'([0-9]+\.[0-9]{3,5}\.[0-9]+)')
        text = changeNumSeq.sub(normalize_num_continue, text)
        print('change:\t',text)
        return text

def matchPunc(content):
    res = re.search(r'(^[,，。、？》《：”；’-]*[,，。、？》《：”；’-]$)', content)
    return res
def normalize(content):
    """normalize content's date, number and money data
    
    Returns:
        string -- origin content
    """
    content=clean_text(content)

    date = re.compile(r'\d{4}[-.年](\d{1,2})[-.月](\d{1,2})日?')
    content = date.sub(normalize_date, content)

    money = re.compile(r'\d[\\.|\d]*[亿|万|千|百|元]*')
    content=money.sub(normalize_num,content)

    per = re.compile(r'([0-9\.]+\%)')
    content = per.sub(normalize_per, content)

    changeNumSeq = re.compile(r'([0-9]+\.[0-9]{3,5}\.[0-9]+)')
    content = changeNumSeq.sub(normalize_num_continue, content)

    return content


if __name__ == "__main__":
    text = "Re2014年29月12日gEx总股2000000总价300000000000rwas200067.80100.00%cre12321321.1221.312atedb4868046.4539.20%ygskinner.c----+-;‘,。oeqw__=--m,a"
    # print(text)
    # print(clean_number_in_text(text))

    print(normalize(text))
    # changeNumSeq = re.compile(r'([0-9]+\.[0-9]{3,4}\.[0-9]+)')
    # text = changeNumSeq.sub(normalize_num_continue, text)
    # money = re.compile(r'\d[\\.|\d]*[亿|万|千|百|元]*')
    # text = money.sub(normalize_num, text)
    # date = re.compile(r'\d{4}[-.年](\d{1,2})[-.月](\d{1,2})日?')
    # text = date.sub(normalize_date, text)
    # print(text)
