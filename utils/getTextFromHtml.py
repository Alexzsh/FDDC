# coding=utf8
import os
import re
import tqdm
import collections
import TextUtils
import bs4
from collections import Counter
import jieba
import random
from bs4 import BeautifulSoup
import time
import multiprocessing as mp
import tableParser
import asyncio
from aiofile import AIOFile, Reader, Writer
import aiofiles
jieba.initialize()
re_replace_blank = re.compile('\s+')
BlankCharSet = set([' ', '\n', '\t'])
CommaNumberPattern = re.compile(u'\d{1,3}([,，]\d\d\d)+')
CommaCharInNumberSet = set([',', '，'])
NumberSet = set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])
CommaCharInNumberSet1 = set([',', '.', '。', '，', '!', '?', ':', '：'])


dir_glob = {'dz': 'E:/实验/round1_train_20180518/round1_train_20180518/定增/html/',
       'ht': 'E:/实验/round1_train_20180518/round1_train_20180518/增减持/html/',
       'zjc': 'E:/实验/round1_train_20180518/round1_train_20180518/重大合同/html/'}

# docu_type = 'dz' # {'ht','dz','zjc'}
# dir_name = dir_glob[doc_type]
# text_dir = 'E:/实验/Label/' + doc_type + '/text/'
# train_dir = 'E:/实验/Label/' + doc_type + '/' + doc_type + '.train' # 源数据给的train


class hetong():
    """docu class
    """

    def __init__(self, name, jiaFang, yiFang, projectName, heTong, topLimit, lowerLimit, combination):
        self.name = name
        self.jiaFang = []
        self.jiaFang.append(getDict(jiaFang))
        self.yiFang = []
        self.yiFang.append(getDict(yiFang))
        self.projectName = []
        self.projectName.append(getDict(projectName))
        self.heTong = []
        self.heTong.append(getDict(heTong))
        self.topLimit = []
        self.topLimit.append(getDict(topLimit))
        self.lowerLimit = []
        self.lowerLimit.append(getDict(lowerLimit))
        self.combination = []
        self.combination.append(getDict(combination))


class dingzeng():
    """docu class
    """

    def __init__(self, name, addObj, addType, addNum, addPrice, lockup, buyType):
        self.name = name
        self.addObj = []
        self.addObj.append(getDict(addObj))
        self.addType = []
        self.addType.append(getDict(addType))
        self.addNum = []
        self.addNum.append(getDict(addNum))
        self.addPrice = []
        self.addPrice.append(getDict(addPrice))
        self.lockup = []
        self.lockup.append(getDict(lockup))
        self.buyType = []
        self.buyType.append(getDict(buyType))


class zengjianchi():
    """docu class
    """

    def __init__(self, name, fullName, simpleName, changeDate, changePrice, changeNumber, afterChange, afterRate):
        self.name = name
        self.fullName = []
        self.fullName.append(getDict(fullName))
        self.simpleName = []
        self.simpleName.append(getDict(simpleName))
        self.changeDate = []
        self.changeDate.append(getDict(changeDate))
        self.changePrice = []
        self.changePrice.append(getDict(changePrice))
        self.changeNumber = []
        self.changeNumber.append(getDict(changeNumber))
        self.afterChange = []
        self.afterChange.append(getDict(afterChange))
        self.afterRate = []
        self.afterRate.append(getDict(afterRate))


def getHeTong(train_dir):
    """get all entity object from docu_type dir

    Returns:
        list -- [a list of the entity object]
    """
    # filename = 'E:/实验/Label/ht/hetongtest1.train'
    length, length2, ht = [], [], []
    with open(train_dir, 'r', encoding='utf-8') as fr:
        for line in fr.readlines():
            a = line.split('\t')
            length.append(len(a))
            if len(a) < 8:
                a.extend([''] * (8 - len(a)))
            length2.append(len(a))
            ht.append(hetong(*a))
    return ht


def getDingZeng(train_dir):
    """get all entity object from docu_type dir

    Returns:
        list -- [a list of the entity object]
    """
    # filename = 'E:/实验/Label/dz/dingzeng.train'

    length, length2, dz = [], [], []
    with open(train_dir, 'r', encoding='utf-8') as fr:
        for line in fr.readlines():
            a = line.split('\t')
            length.append(len(a))
            if len(a) < 7:
                a.extend([''] * (7 - len(a)))
            length2.append(len(a))
            dz.append(dingzeng(*a))
    return dz


def getZengJianChi(train_dir):
    """get all entity object from docu_type dir

    Returns:
        list -- [a list of the entity object]
    """
    # filename = 'E:/实验/Label/zjc/zjctest1.train'
    length, length2, zjc = [], [], []
    with open(train_dir, 'r', encoding='utf-8') as fr:
        for line in fr.readlines():
            a = line.split('\t')
            length.append(len(a))
            if len(a) < 8:
                a.extend([''] * (8 - len(a)))
            length2.append(len(a))
            zjc.append(zengjianchi(*a))
    return zjc


def getDict(name, start=-1, end=-1, sentence=-1):
    """entity struct

    Arguments:
        name {string} -- entity content

    Keyword Arguments:
        start {int} -- entity start position (default: {-1})
        end {int} -- entity end position (default: {-1})
        sentence {string} -- the index of entity in context  (default: {-1})

    Returns:
        [dict] -- [result dict about an entity]
    """
    return {'name': name, 'start': start, 'end': end, 'sentence': sentence}


def getDingZeng_old(filename):
    # test function
    with open(filename, 'r', encoding='utf-8') as fr:
        soup = BeautifulSoup(fr.read(), 'html.parser')
        text = ""
        cutPage = False
        # print((list(soup.contents[0].contents)))
        hidden = soup.findAll('hidden')
        if len(hidden) > 3:
            cutPage = True
            last_hidden = int(int(hidden[-1]['name'][1:])*0.6)
        for child in soup.descendants:
            sentence = ""

            if cutPage and child.name == 'hidden' and int(child['name'][1:]) >= last_hidden:
                print('break in\t', child['name'], '\tall\t', hidden[-1]['name'])
                break
            if child.name == 'tr' or child.name == 'td':
                if not text[-1] in CommaCharInNumberSet1:
                    sentence += ','
            if child.name == 'img':
                continue
            if isinstance(child, bs4.element.Tag) and child.attrs.get('title'):
                if 'title' in child.attrs:
                    sentence = TextUtils.clean_text(TextUtils.normalize(child['title']))

                    if not sentence.endswith(':'):
                        sentence += ':'
            elif isinstance(child, bs4.NavigableString) and len(child.string) > 2:
                sentence = TextUtils.clean_text(TextUtils.normalize(child.string))

            text += sentence
        return text


def getContentFromEveryDiv(filename):
    """ignore table data,get data from every div
    
    Arguments:
        filename {string} -- the filename need to be extracted
    
    Returns:
        text -- result data
    """
    
    with open(filename, 'r', encoding='utf-8') as fr:
        soup = BeautifulSoup(fr.read(), 'html.parser')
        text = ""
        # print((list(soup.contents[0].contents)))
        for child in soup.descendants:
            sentence = ""
            if child.name == 'tr' or child.name == 'td':
                if not text[-1] in CommaCharInNumberSet1:
                    sentence += ','
            if isinstance(child, bs4.element.Tag) and child.attrs.get('title'):
                if 'title' in child.attrs:
                    sentence = TextUtils.clean_text(TextUtils.normalize(child['title']))

                    if not sentence.endswith(':'):
                        sentence += ':'
            elif isinstance(child, bs4.NavigableString) and len(child.string) > 2:
                sentence = TextUtils.clean_text(TextUtils.normalize(child.string))

            text += sentence
        return text


def getDataFromParserThread(filename, file, res):
    '''this function make fasttext data
    
    Arguments:
        filename {string} -- extracted file's name
        file {string} -- extracted file's name
        res {[type]} -- [description]
    '''

    start = time.time()
    print(file, ' start ', '!' * 10)
    sum = 0
    content = tableParser.parseHtmlGetTable.parse_content(os.path.join(filename, file))
    result = '。'.join(content)
    result = TextUtils.clean_text(TextUtils.normalize(result))

    sentences = result.split('。')
    savename = file.split('.')[0]
    for sentence in sentences:
        if sentence == "":
            continue
        label = 0
        sum += 1
        if savename in res.keys():
            field = res.get(savename)
            for v in field[1:]:
                if len(v) > 1 and field[0] in sentence and v in sentence:
                    print('-' * 10, v, sentence.find(field[0]), sentence.find(v), len(sentence))
                    label = 1
                    break

        seg = jieba.cut(sentence)
        res_sentence = " ".join(seg)
        res_sentence = " ".join(res_sentence.split())
        res_sentence += '\t__label__dingzeng\n' if label else '\t__label__useless\n'
        contents.append(res_sentence)
    print(file, ' spend ', time.time()-start, '!'*10)


def getTableFromFaXing(filename, file):
    res = (tableParser.parseHtmlGetTable.parse_content(os.path.join(filename, file)))
    result = '。'.join(res)
    with open('../FDDC/dingzeng/textWithPara/'+file.split('.')[0]+'.txt', 'w') as fw:
        fw.write(result)


def getDataFromParser():
    """
    function to get labeled data or statistical data 
    """

    import pprint
    import threading

    dataFrame = []
    def getTableOther(filename, file, res):
        series = tableParser.parseHtmlGetTable.parse_content(os.path.join(filename, file), res)
        dataFrame.append(series)
    import pandas as pd
    import multiprocessing as mp
    pool = mp.Pool(processes=4)
    dirname = '../FDDC/dingzeng'
    output = 'fasttext.train'
    res = collections.defaultdict(list)
    
    with open(os.path.join(dirname, 'dingzeng.train'), 'r') as trainFr:
        trains = trainFr.readlines()
        for train in trains:
            train = train.replace('\n', '').split('\t')
            train = [i for i in train if i != '']
            res[train[0]].append(train[1:])
    filename = '../FDDC/dingzeng/html'
    print(res['224128'])

    start = time.time()
    for root, dirs, files in os.walk(filename):
        for file in tqdm.tqdm(files[:]):
            if 'html' not in file:
                continue
            # if file == '317510.html':
            # getTableFromFaXing(filename, file)
            # getTableOther(filename, file, res)

            # t = threading.Thread(getTableFromFaXing(filename, file),name='file:'+file)
            # t.start()
            # t.join()
            pool.apply_async(getTableFromFaXing, (filename, file))
        #
        print('<'*20)
        pool.close()
        pool.join()
        print('>'*20)
    # print('thread spend ',time.time()-start)
    global contents
    contents = []
    # import pickle
    # with open('dataFrame.pkl', 'wb') as fw:
    #     pickle.dump(dataFrame,fw)
    # df=pd.DataFrame(dataFrame)
    # df.columns='allSum,allData,id,notFoundSum,notFoundData,otherSum,otherSumData,tableSum,tableSumData'.split(',')
    # df.to_csv('dingzengDataDistribution.csv', header=None, index=None)
        # trueContent = [i for i in contents if i.endswith('\t__label__dingzeng\n')]
        # falseContent = [i for i in contents if i.endswith('\t__label__useless\n')]
        # random.shuffle(falseContent)
        # trueContent.extend(falseContent)#[:len(trueContent)]
        # random.shuffle(trueContent)
        # with open(os.path.join(dirname, output), 'w') as fw:
        #     fw.writelines(trueContent)


def process(dirname, file, fasttext_model, docu_type):
    """get data after fasttext model prediction
    
    Arguments:
        file {string} -- filename
        fasttext_model {object} -- fasttext model
    """
    print(dirname, file)
    with open(os.path.join(dirname, 'textWithPara', file), 'r') as fr:
        sentence = fr.read().split('。')
        sentence = [i for i in sentence if i != '']
        label = fasttext_model.predict(sentence)
        label = [i[0] for i in label]
        res = [sentence[index] for index in range(len(sentence)) if label[index] == '__label__' + docu_type]
        print(Counter(label))
    with open(os.path.join(dirname, 'textWithFasttext', file), 'w') as fw:
        fw.writelines(res)


def makeAfterFasttextData(docu_type):
    """multi processes to process different types documents
    
    Arguments:
        docu_type {string} -- dz、ht、zjc
    """ 
    import fasttext
    import multiprocessing as mp
    pool = mp.Pool(processes=4)

    dirname = '../FDDC/'+docu_type
    save_dir = '../FDDC'+docu_type+'/textAfterFasttext'
    fasttext_model = fasttext.load_model('../FDDC/'+docu_type+'/fasttext.bin')

    for root, _, files in os.walk(os.path.join(dirname, 'textWithPara')):
        for file in tqdm.tqdm(files[:]):
            # pool.apply_async(process,(dirname, file, fasttext_model))
            process(dirname, file, fasttext_model, docu_type)
        # print('<' * 20)
        # pool.close()
        # pool.join()
        # print('>' * 20)


def getFasttextData(docu_type):
    '''

    '''
    dirname = '../FDDC/'+docu_type
    output = 'fasttext.train'
    res = collections.defaultdict(list)
    contents = []
    sum = 0
    with open(os.path.join(dirname, docu_type+'.train'), 'r') as trainFr:
        trains = trainFr.readlines()
        for train in trains:
            train = train.replace('\n', '').split('\t')
            train = [i for i in train if i != '']
            res[train[0]].append(train[1:])
    for root, dir, files in os.walk(os.path.join(dirname, 'textWithPara')):
        for file in tqdm.tqdm(files):
            with open(os.path.join(dirname, 'textWithPara', file), 'r') as fr:
                text = fr.read()
                sentences = text.split('。')
                filename = file.split('.')[0]
                for sentence in sentences:
                    if sentence == "":
                        continue
                    label = 0
                    sum += 1
                    if filename in res.keys():
                        f = res.get(filename)
                        for field in f:
                            for v in field[:]:
                                if label == 0 and len(v) > 1 and field[0] in sentence and v in sentence:
                                    print('-'*10, v, sentence.find(field[0]), sentence.find(v), len(sentence))
                                    label = 1
                                    break

                    # seg=jieba.cut(sentence)
                    # res_sentence=" ".join(seg)
                    # res_sentence=" ".join(res_sentence.split())
                    res_sentence = sentence
                    labelStr = '__label__'+docu_type+'\t' if label else '__label__useless\t'
                    res_sentence = labelStr+res_sentence+'\n'
                    contents.append(res_sentence)
    trueContent = [i for i in contents if i.startswith('__label__'+docu_type)]
    falseContent = [i for i in contents if i.startswith('__label__useless')]
    random.shuffle(falseContent)
    trueContent.extend(falseContent)#[:len(trueContent)*2]
    random.shuffle(trueContent)
    with open(os.path.join(dirname, output), 'w') as fw:
        fw.writelines(trueContent)


def fasttextModel(docu_type):
    import fasttext
    filename = '../FDDC/'+docu_type+'/fasttext.train'
    model = fasttext.supervised(filename, os.path.join('../FDDC/'+docu_type, 'fasttext'), label_prefix='__label__')
    result = model.test('../FDDC/'+docu_type+'/fasttext.test')
    print('P@1:', result.precision)
    print('R@1:', result.recall)
    print('Number of examples:', result.nexamples)


def testFasttext():

    import fasttext
    modelPath = '../FDDC/dingzeng/fasttext.bin'
    model = fasttext.load_model(modelPath)


    testFilename = '../FDDC/dingzeng/html/'
    content = tableParser.parseHtmlGetTable.parse_content(os.path.join(testFilename, '7880.html'))
    result = '。'.join(content)
    result = TextUtils.clean_text(TextUtils.normalize(result))
    sentence = result.split('。')
    sentence = [i for i in sentence if len(i) > 2]
    labels = model.predict_proba(sentence)
    print(Counter(labels))
    # for index,label in enumerate(labels):
    #     if 'dingzeng' in label:
    #         print(sentence[index],'----->',labels[index])


def makeDingZengBIOData(docu_type, train_dir):
    '''
    make labeled data via multi-process
    '''

    dz = getDingZeng(train_dir)
    pool = mp.Pool(processes=4)
    # dir_name = '../FDDC/dingzeng/data' #原
    text_dir = 'E:/实验/Label/' + docu_type + '/text3' # new

    # if not os.path.exists(dir_name): # 原
    #     os.makedirs(dir_name)
    if not os.path.exists(text_dir):
        os.makedirs(text_dir)

    for file in tqdm.tqdm(
            sorted(list(os.walk(text_dir))[0][2], key=lambda x: int(x.split('.')[0]),
                   reverse=True)[:]):
        name = file.split('.')[0]
        dz_obj = []
        dz_tmp = dz[0]
        while dz_tmp.__dict__['name'] == name and len(dz) > 1:
            dz_obj.append(dz_tmp)
            dz = dz[1:]
            try:
                dz_tmp = dz[0]
            except IndexError:
                print(dz)
                input()
        pool.apply_async(dingZengBIOThread(file, dz_obj))

    print('<' * 20)
    pool.close()
    pool.join()
    print('>' * 20)


def dingZengBIOThread(file, dz_obj):
    '''use entity to get reverse labeled data

    Arguments:
        file {string} -- filename
        dz_obj {object} -- entity type
    '''

    with open('E:/实验/Label/dz/text2/' + file, 'r', encoding='utf-8') as fr:
        name = file.split('.')[0]
        sss = ""
        text = fr.readline()
        sentence = text.split('。')
        for index1, i in enumerate(dz_obj):
            i = i.__dict__
            if i['addObj'] == '' or i['addType'] == '':
                continue
            name = i['name']
            i.pop('name')

            addObj_name = i['addObj'][0]['name'] # 增发对象
            addType_name = i['addType'][0]['name'] # 发行方式
            addNum_name = i['addNum'][0]['name'] # 增发数量
            addPrice_name = i['addPrice'][0]['name'] # 增发金额
            lockup_name = i['lockup'][0]['name'] # 锁定期
            buyType_name = i['buyType'][0]['name'] # 认购方式

            # index = 0
            # for num, sen in enumerate(sentence):
            #     addObj_start = sen.find(addObj_name)
            #     # addType_start = sen.find(addType_name)
            #     if addObj_start != -1 :
            #         i['addObj'].append(
            #             getDict(addObj_name, index + addObj_start, index + addObj_start + len(addObj_name), num)
            #         )
            #         # i['addType'].append(
            #         #     getDict(addType_name, index + addType_start, index + addType_start + len(addType_name),
            #         #             num))
            #     index += len(sen) + 1
            index = 0
            for num, sen in enumerate(sentence):
                index_loop = 0
                while index_loop < len(sen):
                    index_loop = sen.find(addObj_name, index_loop)
                    if index_loop == -1:
                        break

                    addObj_start = sen.find(addObj_name)
                    addType_start = sen.find(addType_name)
                    addNum_start = sen.find(addNum_name)
                    addPrice_start = sen.find(addPrice_name)
                    lockup_start = sen.find(lockup_name)
                    buyType_start = sen.find(buyType_name)

                    if addNum_name != '' and addNum_start != -1 and (addObj_start != -1):
                        i['addNum'].append(
                            getDict(addNum_name, index + addNum_start, index + addNum_start + len(addNum_name),
                                    num))
                        i['addObj'].append(
                            getDict(addObj_name, index + addObj_start, index + addObj_start + len(addObj_name),
                                    num))
                        if addType_start != -1:
                            i['addType'].append(
                                getDict(addType_name, index + addType_start, index + addType_start + len(addType_name),
                                        num))
                    if addPrice_name != '' and addPrice_start != -1 and (addObj_start != -1):
                        i['addPrice'].append(
                            getDict(addPrice_name, index + addPrice_start, index + addPrice_start + len(addPrice_name),
                                    num))
                        i['addObj'].append(
                            getDict(addObj_name, index + addObj_start, index + addObj_start + len(addObj_name),
                                    num))
                        if addType_start != -1:
                            i['addType'].append(
                                getDict(addType_name, index + addType_start, index + addType_start + len(addType_name),
                                        num))
                    if lockup_name != '' and lockup_start != -1 and (addObj_start != -1):
                        i['lockup'].append(
                            getDict(lockup_name, index + lockup_start, index + lockup_start + len(lockup_name), num))
                        if addObj_start != -1:
                            i['addObj'].append(
                                getDict(addObj_name, index + addObj_start, index + addObj_start + len(addObj_name),
                                        num))
                        if addType_start != -1:
                            i['addType'].append(
                                getDict(addType_name, index + addType_start, index + addType_start + len(addType_name),
                                        num))
                    if buyType_name != '' and buyType_start != -1 and (addObj_start != -1 or addType_start != -1):
                        i['buyType'].append(
                            getDict(buyType_name, index + buyType_start, index + buyType_start + len(buyType_name),
                                    num))
                        if addObj_start != -1:
                            i['addObj'].append(
                                getDict(addObj_name, index + addObj_start, index + addObj_start + len(addObj_name),
                                        num))
                        if addType_start != -1:
                            i['addType'].append(
                                getDict(addType_name, index + addType_start, index + addType_start + len(addType_name),
                                        num))
                    index_loop += len(addObj_name)
                index += len(sen) + 1
            dz_obj[index1] = i
        li = ['O' for i in text]
        for i in dz_obj:
            for k, v in i.items():
                for item in v:
                    if item['name'] != '' and item['start'] != -1:
                        li[item['start']] = 'B-' + k
                        for i in range(item['start'] + 1, item['end']):
                            li[i] = 'I-' + k
        for j, con in enumerate(li):
            if con != 'O':
                sub_start = j
                break

        for j, con in enumerate(li):
            if li[len(li) - j - 1] != 'O':
                sub_end = len(li) - j - 1
                break
        # li = li[sub_start - 10:sub_end + 10]
        # text = text[sub_start - 10:sub_end + 10]

        for j, con in enumerate(li):
            sss += text[j] + ' ' + con + '\n'

        commonRulu=re.compile(r',+[,|。]')
        sss = commonRulu.sub(lambda x: x.group()[0][-1], sss)
        with open('E:/实验/Label/dz/BIOdata3/'+name + '.txt', 'w', encoding='utf-8') as fw:
            fw.write(sss)


def makeObjBIOData(docu_type, text_dir, BIO_dir, train_dir):
    '''
    make labeled data via multi-process
    '''

    if(docu_type == 'dz'):
        obj = getDingZeng(train_dir)
    elif(docu_type == 'ht'):
        obj =getHeTong(train_dir)
    elif(docu_type == 'zjc'):
        obj = getZengJianChi(train_dir)

    pool = mp.Pool(processes=4)
    # dir_name = '../FDDC/dingzeng/data' #原
    # text_dir = 'E:/实验/Label/' + docu_type + '/text2'  # new

    # if not os.path.exists(dir_name): # 原
    #     os.makedirs(dir_name)
    if not os.path.exists(BIO_dir):
        os.makedirs(BIO_dir)

    for file in tqdm.tqdm(
            sorted(list(os.walk(text_dir))[0][2], key=lambda x: int(x.split('.')[0]),
                   reverse=True)[:]):
        name = file.split('.')[0]
        new_obj = []
        obj_tmp = obj[0]
        while obj_tmp.__dict__['name'] == name and len(obj) > 1:
            new_obj.append(obj_tmp)
            obj = obj[1:]
            try:
                obj_tmp = obj[0]
            except IndexError:
                print(obj)
                input()
        pool.apply_async(objBIOThread(file, docu_type, new_obj, BIO_dir, text_dir))

    print('<' * 20)
    pool.close()
    pool.join()
    print('>' * 20)


def objBIOThread(file, docu_type, new_obj, BIO_dir, text_dir):
    '''use entity to get reverse labeled data

    Arguments:
        file {string} -- filename
        dz_obj {object} -- entity type
    '''

    htlist = ['jiaFang', 'yiFang', 'projectName', 'heTong', 'topLimit', 'lowerLimit', 'combination']
    dzlist = ['addObj', 'addType', 'addNum', 'addPrice', 'lockup', 'buyType']
    zjclist = ['fullName', 'simpleName', 'changeDate', 'changePrice', 'changeNumber', 'afterChange', 'afterRate']
    htNotNull = [1]
    dzNotNull = [0]
    zjcNotNull = [0, 4] # exist questions

    objlist = {'ht': htlist,
               'dz': dzlist,
               'zjc': zjclist}

    notNull_list = {'ht': htNotNull,
               'dz': dzNotNull,
               'zjc': zjcNotNull}

    with open(text_dir + file, 'r', encoding='utf-8') as fr:
        name = file.split('.')[0]
        sss = ""
        text = fr.readline()
        sentence = text.split('。')
        for index1, i in enumerate(new_obj):
            i = i.__dict__

            '''
            # if i['addObj'] == '' or i['addType'] == '': # addType 为空应该不影响吧
            #     continue
            '''
            flag = False
            for notnull in notNull_list[docu_type]:
                if i[objlist[docu_type][notnull]] == '':
                    flag = True
            if flag:
                continue

            name = i['name']
            i.pop('name')

            attrs = []

            for k in range(6):
                attrs.append(i[objlist[docu_type][k]][0]['name'])
            if docu_type != 'dz':
                attrs.append(i[objlist[docu_type][6]][0]['name'])
            # index = 0
            # for num, sen in enumerate(sentence):
            #     addObj_start = sen.find(addObj_name)
            #     # addType_start = sen.find(addType_name)
            #     if addObj_start != -1 :
            #         i['addObj'].append(
            #             getDict(addObj_name, index + addObj_start, index + addObj_start + len(addObj_name), num)
            #         )
            #         # i['addType'].append(
            #         #     getDict(addType_name, index + addType_start, index + addType_start + len(addType_name),
            #         #             num))
            #     index += len(sen) + 1
            index = 0
            for num, sen in enumerate(sentence):
                index_loop = 0
                while index_loop < len(sen):

                    index_loop = sen.find(attrs[notNull_list[docu_type][0]], index_loop) # exit questions

                    if index_loop == -1:
                        break

                    attr_start_list = []
                    for attr in attrs:
                        attr_start_list.append(sen.find(attr))

                    if docu_type != 'dz':
                        attr_start_list.append(sen.find(attrs[6]))

                    for k in range(len(attrs)):
                        if k == notNull_list[docu_type][0]:
                            continue
                        if attrs[k] != '' and attr_start_list[k] != -1 and attr_start_list[notNull_list[docu_type][0]] != -1:
                            i[objlist[docu_type][k]].append(
                                getDict(attrs[k], index + attr_start_list[k], index + attr_start_list[k] + len(attrs[k]),
                                        num))

                            i[objlist[docu_type][notNull_list[docu_type][0]]].append(
                                getDict(attrs[notNull_list[docu_type][0]],
                                        index + attr_start_list[notNull_list[docu_type][0]],
                                        index + attr_start_list[notNull_list[docu_type][0]] + len(attrs[notNull_list[docu_type][0]]),
                                        num))

                    index_loop += len(attrs[notNull_list[docu_type][0]])
                index += len(sen) + 1
            new_obj[index1] = i
        li = ['O' for i in text]
        for i in new_obj:
            for k, v in i.items():
                for item in v:
                    if item['name'] != '' and item['start'] != -1:
                        li[item['start']] = 'B-' + k
                        for i in range(item['start'] + 1, item['end']):
                            li[i] = 'I-' + k
        for j, con in enumerate(li):
            if con != 'O':
                sub_start = j
                break

        for j, con in enumerate(li):
            if li[len(li) - j - 1] != 'O':
                sub_end = len(li) - j - 1
                break
        # li = li[sub_start - 10:sub_end + 10]
        # text = text[sub_start - 10:sub_end + 10]

        for j, con in enumerate(li):
            sss += text[j] + ' ' + con + '\n'

        commonRulu = re.compile(r',+[,|。]')
        sss = commonRulu.sub(lambda x: x.group()[0][-1], sss)
        with open(BIO_dir + name + '.txt', 'w', encoding='utf-8') as fw:
            fw.write(sss)


def saveTrainData(train_ratio, test_ratio, BIO_dir, example_dir):
    '''
        save train\dev\test data
    '''

    # dirname = '../FDDC/'+docu_type+'/data' # 原
    # dirname = 'E:/实验/Label/'+docu_type+'/BIOdata'
    # BIO_dir = 'E:/实验/Label/'+docu_type+'/BIOdata'

    files = list(os.walk(BIO_dir))[0][2]
    random.shuffle(files)
    train = example_dir + 'example.train'
    test = example_dir + 'example.test'
    dev = example_dir + 'example.dev'

    saveData = {
        train: files[:int(len(files) * train_ratio)],
        test: files[int(len(files) * train_ratio):int(len(files) * test_ratio)],
        dev: files[int(len(files) * test_ratio):]
    }

    for key, value in saveData.items():
        print(key, len(value))
        with open(key, 'w', encoding='utf-8') as fw:
            for file in value:
                with open(os.path.join(BIO_dir, file), 'r', encoding='utf-8') as fr:
                    fw.writelines(fr.readlines())
                fw.write('\n')


@asyncio.coroutine
async def writeFiles(txt, filename, dirname):
    '''async write files

    Arguments:
        txt {string} -- the content
        filename {string} -- filename
        dirname {string} -- dirname
    '''

    async with AIOFile(os.path.join(dirname, filename), 'wb') as afp:
        writer = Writer(afp)
        await writer(txt)
        await afp.fsync()


def test(filename):
    # filename = 'test.html'
    # pprint.pprint(tableParser.parseHtmlGetTable.parse_table(filename))
    return tableParser.parseHtmlGetTable.parse_content(filename)
    # with open(filename,'r') as fr:
    #     soup = BeautifulSoup(fr.read(),'html.parser')
    #     table = soup.find_all('table')
    #     if table:
    #         tr = soup.find_all('tr')
    #         for r in tr:
    #             td = r.find_all('td')
    #             for d in td:
    #                 print(TextUtils.clean_text(TextUtils.normalize(d.text)))


if __name__ == '__main__':
    # docu_type = 'dingzeng'
    # getFasttextData(docu_type)
    # fasttextModel(docu_type)
    # testFasttext()

    # makeAfterFasttextData(docu_type)
    # func()
    # getDataFromParser()
    # import  pickle
    # with open('dataFrame.pkl','rb') as fr:
    #     res=pickle.load(fr)
    # print(res)
    # makeDingZengBIOData()
    # saveTrainData('dingzeng', 0.9, 0.95)
    # res=test()
    # print(''.join(res))
    # saveTrainData('dingzeng',0.9,0.95)

    # print(getContentFromEveryDiv(''))
    # print(getTableFromFaXing(dirname, filename))
    # getDataFromParser()

    print('ooo')
