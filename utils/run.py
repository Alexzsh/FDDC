import getTextFromHtml
import tableParser
import os

docu_type = 'dz' # {'ht','dz','zjc'}

dir = {'dz': 'E:/实验/round1_train_20180518/round1_train_20180518/定增/html/',
       'ht': 'E:/实验/round1_train_20180518/round1_train_20180518/增减持/html/',
       'zjc': 'E:/实验/round1_train_20180518/round1_train_20180518/重大合同/html/'}
dir_name = dir[docu_type]
text_dir = 'E:/实验/Label/' + docu_type + '/text3/'
train_dir = 'E:/实验/Label/' + docu_type + '/hetongtest1.train'


def step1():
    '''
    将html文件转化为text
    '''
    file_list = list(os.walk(dir_name))
    cl1 = tableParser.parseHtmlGetTable(None, None, None, None, None, None, None)

    # print(file_list[0][2])
    for f in file_list[0][2]:
        filename = f.split('.')[0]
        with open(text_dir + filename + '.txt', 'w', encoding='utf-8') as txtf:
            print('start')
            # text = getTextFromHtml.getDingZeng_old(dir_name + filename + '.html')

            # text = getTextFromHtml.getContentFromEveryDiv(dir_name + filename + '.html')
            # text = '。'.join(cl1.parse_content_statistics(dir_name + filename + '.html'))
            text = '。'.join(cl1.parse_content(dir_name + filename + '.html'))

            txtf.write(text)

    return


def step2():
    '''
    根据源数据的.train文件获得BIOtext
    :return:
    '''
    getTextFromHtml.makeDingZengBIOData(docu_type)


def step3():
    '''
    将BIOtext存为 train\dev\test data：
        example.train
        example.test
        example.dev
    :return:
    '''
    getTextFromHtml.saveTrainData(docu_type, train_ratio=0.9, test_ratio=0.95)


if __name__ == '__main__':
    print('-------run-------')
    step1()
    # step2()
    # step3()

