import os
import re
import tqdm
import TextUtils
import bs4
import pprint
import random
from bs4 import BeautifulSoup


import tableParser



dirname='../FDDC/html'
re_replace_blank=re.compile('\s+')
BlankCharSet = set([' ', '\n', '\t'])
CommaNumberPattern = re.compile(u'\d{1,3}([,，]\d\d\d)+')
CommaCharInNumberSet = set([',', '，'])
NumberSet = set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])
CommaCharInNumberSet1 = set([',','.','。','，','!','?',':','：'])



def getDingZeng(filename):
    with open(filename,'r') as fr:
        soup=BeautifulSoup(fr.read(),'html.parser')
        text=""
        cutPage=False
        # print((list(soup.contents[0].contents)))
        hidden = soup.findAll('hidden')
        if len(hidden)>3:
            cutPage=True
            last_hidden = int(int(hidden[-1]['name'][1:])*0.6)
        for child in soup.descendants:
            sentence=""
            if cutPage and child.name=='hidden' and int(child['name'][1:])>=last_hidden:
                print('break in\t',child['name'],'\tall\t',hidden[-1]['name'])
                break
            if child.name=='tr' or child.name=='td':
                if not text[-1] in CommaCharInNumberSet1:
                    sentence+=','
            if isinstance(child,bs4.element.Tag) and child.attrs.get('title'):
                if 'title' in child.attrs:
                    sentence= TextUtils.clean_text(TextUtils.normalize(child['title']))

                    if not sentence.endswith(':'):
                        sentence+=':'
            elif isinstance(child,bs4.NavigableString) and len(child.string)>2:
                sentence= TextUtils.clean_text(TextUtils.normalize(child.string))

            text+=sentence
        return text

def getContentFromEveryDiv(filename):
    with open(filename,'r') as fr:
        soup=BeautifulSoup(fr.read(),'html.parser')
        text=""
        # print((list(soup.contents[0].contents)))
        for child in soup.descendants:
            sentence=""
            if child.name=='tr' or child.name=='td':
                if not text[-1] in CommaCharInNumberSet1:
                    sentence+=','
            if isinstance(child,bs4.element.Tag) and child.attrs.get('title'):
                if 'title' in child.attrs:
                    sentence= TextUtils.clean_text(TextUtils.normalize(child['title']))

                    if not sentence.endswith(':'):
                        sentence+=':'
            elif isinstance(child,bs4.NavigableString) and len(child.string)>2:
                sentence= TextUtils.clean_text(TextUtils.normalize(child.string))

            text+=sentence
        return text


def getContentWithoutTable(filename):
    res_text = ""
    filename=os.path.join(dirname,filename)
    with open(filename, 'r') as fr:
        html = BeautifulSoup(fr.read(), 'lxml')
        for div in html.select('div[type="content"]'):
            if isinstance(div.string, str):
                res_text+=(re.sub(re_replace_blank, '', div.string))

    return res_text

def testTable(filename):
    rule = re.compile(r'\s+')
    with open(filename, 'r') as fr:
        soup = BeautifulSoup(fr.read(), 'lxml')
        text = ""
        for child in soup.descendants:
            if isinstance(child, bs4.element.Tag):
                print(child.name)
            elif isinstance(child, bs4.NavigableString):
                print(child)


def doGetTextFromHtml():
    text_dirname = '../FDDC/dingzeng/dataHalf'
    dirname = '../FDDC/dingzeng/html'
    if not os.path.exists(text_dirname):
        os.makedirs(text_dirname)

    print(list(os.walk(dirname)))
    filename='6927.html'
    for filename in tqdm.tqdm(list(os.walk(dirname))[0][2]):
        # filename=list(os.walk(dirname))[0][2][0]
        text_filename = filename[:filename.find('.')] + '.txt'
        filename = os.path.join(dirname, filename)
        with open(os.path.join(text_dirname, text_filename), 'w') as fw:

            text = getDingZeng(filename)
            fw.write(text)


def doTestGetTableFromHtml():
    filename = '../../NER/round1_train_20180518/增减持/html/6927.html'
    # pprint.pprint(tableParser.parseHtmlGetTable.parse_table(filename))
    print(tableParser.parseHtmlGetTable.parse_table(filename))
    # for table in res:

    # record = tableParser.parseHtmlGetTable(None, None, None, None, None, None, None)
    # rs = []
    # for table_dict in record.parse_table(filename):
    #     rs_table = record.extract_from_table_dict(table_dict)
    #     if len(rs_table) > 0:
    #         if len(rs) > 0:
    #             record.mergeRecord(rs, rs_table)
    #             break
    #         else:
    #             rs.extend(rs_table)
    # pprint.pprint(rs)
def test():
    filename = '../../NER/round1_train_20180518/增减持/html/6927.html'

import jieba
def getFasttextData():
    dirname='../FDDC/dingzeng'
    output='fasttext.train'
    res={}
    contents=[]
    sum=0
    with open(os.path.join(dirname,'dingzeng.train'),'r') as trainFr:
        trains=trainFr.readlines()
        for train in trains:
            train=train.split('\t')
            res[train[0]]=train[1:]
    for root,dir,files in os.walk(os.path.join(dirname,'data')):
        for file in tqdm.tqdm(files):
            with open(os.path.join(dirname,'data',file),'r') as fr:
                text=fr.read()
                sentences=text.split('。')
                filename=file.split('.')[0]
                for sentence in sentences:
                    label=0
                    sum+=1
                    if filename in res.keys():
                        field = res.get(filename)
                        for v in field[1:]:
                            if len(v)>1 and field[0] in sentence and v in sentence:
                                print('-'*10,v,sentence.find(field[0]),sentence.find(v),len(sentence))
                                label=1
                                break

                    seg=jieba.cut(sentence)
                    res_sentence=" ".join(seg)
                    res_sentence=" ".join(res_sentence.split())
                    res_sentence += '\t__label__dingzeng\n' if label else '\t__label__useless\n'
                    contents.append(res_sentence)
    trueContent = [i for i in contents if i.endswith('\t__label__dingzeng\n')]
    falseContent=[i for i in contents if i.endswith('\t__label__useless\n')]
    random.shuffle(falseContent)
    trueContent.extend(falseContent[:len(trueContent)])
    random.shuffle(trueContent)
    with open(os.path.join(dirname,output),'w') as fw:
        fw.writelines(trueContent)
def getDataByPage(filename):
    with open(filename,'r') as fr:
        soup=BeautifulSoup(fr.read())

if __name__ == '__main__':
    doGetTextFromHtml()




