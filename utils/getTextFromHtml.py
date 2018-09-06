from bs4 import BeautifulSoup
import os
import re
import tqdm
import html2text
dirname='../FDDC/html'
re_replace_blank=re.compile('\s+')
from bs4 import BeautifulSoup
import bs4
import re


BlankCharSet = set([' ', '\n', '\t'])
CommaNumberPattern = re.compile(u'\d{1,3}([,，]\d\d\d)+')
CommaCharInNumberSet = set([',', '，'])
NumberSet = set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])


def clean_text(text):
    return clean_number_in_text(remove_blank_chars(text))


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

def parse_content(filename):
    """
    解析 HTML 中的段落文本
    按顺序返回多个 paragraph 构成一个数组，
    每个 paragraph 是一个 content 行构成的数组
    :param html_file_path:
    :return:
    """
    rs=[]
    filename = os.path.join(dirname, filename)
    with open(filename, 'r') as fp:
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
                    rs[-1].append(clean_text(content_div.text))
    paragraphs = []
    for content_list in rs:
        if len(content_list) > 0:
            paragraphs.append(''.join(content_list))
    return paragraphs

def strQ2B(ustring):
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
                inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ss

def getContentFromEveryDiv(filename):
    rule=re.compile(r'\s+')
    with open(filename,'r') as fr:
        soup=BeautifulSoup(fr.read(),'html.parser')
        text=""
        for child in soup.descendants:
            if isinstance(child,bs4.element.Tag) and child.attrs.get('title'):
                if 'title' in child.attrs:
                    text+=re.sub(rule,'',(child['title']))
            if isinstance(child,bs4.NavigableString) and len(child.string)>2 :
                text+=re.sub(rule,'',child.string)
        return clean_text(strQ2B(text))


def getContentWithoutTable(filename):
    res_text = ""
    filename=os.path.join(dirname,filename)
    with open(filename, 'r') as fr:
        html = BeautifulSoup(fr.read(), 'lxml')
        for div in html.select('div[type="content"]'):
            if isinstance(div.string, str):
                res_text+=(re.sub(re_replace_blank, '', div.string))

    return res_text

def getContentFromHtml2Text(filename):
    filename = os.path.join(dirname, filename)
    with open(filename, 'r') as fr:
        return html2text.html2text(fr.read())

if __name__ == '__main__':

    text_dirname='../FDDC/textWithParagraph'
    if not os.path.exists(text_dirname):
        os.makedirs(text_dirname)

    # print(list(os.walk(dirname))[0][2][0])
    for filename in tqdm.tqdm(list(os.walk(dirname))[0][2]):
        text_filename=filename[:filename.find('.')]+'.txt'
        filename = os.path.join(dirname, filename)
        with open(os.path.join(text_dirname,text_filename),'w') as fw:
            text=getContentFromEveryDiv(filename)
            fw.write(text)



