import getTextFromHtml

doc_tpye = 'dz' # {'ht','dz','zjc'}

dir = {'dz': 'E:/实验/round1_train_20180518/round1_train_20180518/定增/html/',
       'ht': 'E:/实验/round1_train_20180518/round1_train_20180518/增减持/html/',
       'zjc': 'E:/实验/round1_train_20180518/round1_train_20180518/重大合同/html/'}
dir_name = dir[doc_tpye]
text_dir = 'E:/实验/Label/' + doc_tpye + '/text/'
train_dir = 'E:/实验/Label/' + doc_tpye + '/hetongtest1.train'


def step1():
    '''
    将html文件转化为text
    '''
    filename = '20286416'
    with open(text_dir + filename + '.txt', 'w', encoding='utf-8') as f:
        text = getTextFromHtml.getContentFromEveryDiv(dir_name + filename + '.html')
        f.write(text)
    return


def step2():
    '''
    根据源数据的.train文件获得BIOtext
    :return:
    '''
    getTextFromHtml.makeDingZengBIOData()


def step3():
    '''
    将BIOtext存为 train\dev\test data：
        example.train
        example.test
        example.dev
    :return:
    '''
    getTextFromHtml.saveTrainData(doc_tpye, train_ratio=0.9, test_ratio=0.95)


if __name__ == '__main__':
    print('-------run-------')
    # step1()
    # step2()
    # step3()


