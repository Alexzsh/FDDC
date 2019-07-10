import getTextFromHtml
import tableParser
import os

docu_type = 'ht' # {'ht','dz','zjc'}
train_name = {'dz': 'dingzeng',
              'ht': 'hetong',
              'zjc': 'zengjianchi'}

html_dir = {'dz': 'E:/实验/round1_train_20180518/round1_train_20180518/定增/html/',
            'ht': 'E:/实验/round1_train_20180518/round1_train_20180518/重大合同/html/',
            'zjc': 'E:/实验/round1_train_20180518/round1_train_20180518/增减持/html/'}

dir_name = html_dir[docu_type] # html文件所在位置
text_dir = 'E:/实验/Label/' + docu_type + '/text/'
BIO_dir = 'E:/实验/Label/' + docu_type + '/BIOdata_new/'
example_dir = "E:/实验/Label/"+docu_type+"/example/"
train_dir = 'E:/实验/Label/' + docu_type + '/' + train_name[docu_type] + '.train'


def step1():
    '''
    将html文件转化为text
    '''
    file_list = list(os.walk(dir_name))
    # cl1 = tableParser.parseHtmlGetTable(None, None, None, None, None, None, None)

    # print(file_list[0][2])
    for f in file_list[0][2]:
        filename = f.split('.')[0]
        with open(text_dir + filename + '.txt', 'w', encoding='utf-8') as txtf:
            # text = getTextFromHtml.getDingZeng_old(dir_name + filename + '.html')

            text = getTextFromHtml.getContentFromEveryDiv(dir_name + filename + '.html')
            # text = '。'.join(cl1.parse_content_statistics(dir_name + filename + '.html'))
            # text = '。'.join(cl1.parse_content(dir_name + filename + '.html'))

            txtf.write(text)

    return


def step2():
    '''
    根据源数据的.train文件获得BIOtext
    :return:
    '''
    # getTextFromHtml.makeDingZengBIOData(docu_type, train_dir)
    # getTextFromHtml.makeObjBIOData(docu_type, text_dir, BIO_dir, train_dir)
    getTextFromHtml.makehtBIOData(docu_type, text_dir, BIO_dir, train_dir)

def step3():
    '''
    将BIOtext存为 train\dev\test data：
        example.train
        example.test
        example.dev
    :return:
    '''
    getTextFromHtml.saveTrainData(0.9, 0.95, BIO_dir, example_dir)


if __name__ == '__main__':
    print('-------run-------')
    # step1()
    step2()
    # step3()

