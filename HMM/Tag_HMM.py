#coding=utf-8
"""
@version=1.0
@author:zsh
@file:Tag_HMM.py
@time:2018/10/12 19:25
"""
import sys
import pickle
from viterbi import viterbi
import numpy as np

state_M = 4
word_N = 0

A_dic = {}
B_dic = {}
Count_dic = {}
Pi_dic = {}
word_set = set()
state_list = ['B', 'M', 'E', 'S']
line_num = -1
Min_prob = 1e-10

INPUT_DATA = "data/RenMinData.txt_utf8"
PROB_START = "prob_mat/prob_start.pkl"
PROB_EMIT = "prob_mat/prob_emit.pkl"
PROB_TRANS = "prob_mat/prob_trans.pkl"


def init():
    global state_M
    global word_N
    # A_dic=np.zeros([state_M,state_M])
    for state in state_list:
        A_dic[state] = {}
        for state1 in state_list:
            A_dic[state][state1] = 0.0
    for state in state_list:
        Pi_dic[state] = 0.0
        B_dic[state] = {}
        Count_dic[state] = 0


def load_model(f_name):
    with open(f_name, 'rb') as fr:
        return pickle.load(fr)


def getList(input_str):
    outpout_str = []
    if len(input_str) == 1:
        outpout_str.append('S')
    elif len(input_str) == 2:
        outpout_str = ['B', 'E']
    else:
        M_num = len(input_str) - 2
        M_list = ['M'] * M_num
        outpout_str.append('B')
        outpout_str.extend(M_list)
        outpout_str.append('S')
    return outpout_str


def Output():
    print("len(word_set) = %s " % (len(word_set)))
    for key in Pi_dic:
        Pi_dic[key] = Pi_dic[key] * 1.0 / line_num
    with open(PROB_START, 'wb') as fw:
        pickle.dump(Pi_dic, fw)

    for key in A_dic:
        for key1 in A_dic[key]:
            A_dic[key][key1] = A_dic[key][key1] / Count_dic[key]
    with open(PROB_TRANS, 'wb') as fw:
        pickle.dump(A_dic, fw)

    for key in B_dic:
        for word in B_dic[key]:
            B_dic[key][word] = B_dic[key][word] / Count_dic[key]
    with open(PROB_EMIT, 'wb') as fw:
        pickle.dump(B_dic, fw)


def trainTag():
    # sys.argv[1]='RenMinData.txt_utf-8'
    # if len(sys.argv) != 2:
    #     print >> sys.stderr,"Usage [%s] [input_data] " % (sys.argv[0])
    #     sys.exit(0)
    ifp = open('data/RenMinData.txt_utf8', encoding='utf-8')
    init()
    global word_set
    global line_num
    for line in ifp:
        line_num += 1
        if line_num % 10000 == 0:
            print(line_num)

        line = line.strip()
        if not line: continue

        word_list = []
        for i in range(len(line)):
            if line[i] == " ": continue
            word_list.append(line[i])
        word_set = word_set | set(word_list)  # 并集

        lineArr = line.split(" ")
        line_state = []
        for item in lineArr:
            line_state.extend(getList(item))
        # pdb.set_trace()
        if len(word_list) != len(line_state):
            print >> sys.stderr, "[line_num = %d][line = %s]" % (line_num, line.endoce("utf-8", 'ignore'))
        else:
            for i in range(len(line_state)):
                if i == 0:
                    Pi_dic[line_state[0]] += 1
                    Count_dic[line_state[0]] += 1
                else:
                    A_dic[line_state[i - 1]][line_state[i]] += 1
                    Count_dic[line_state[i]] += 1
                    if not (word_list[i]) in B_dic[line_state[i]].keys():
                        B_dic[line_state[i]][word_list[i]] = 0.0
                    else:
                        B_dic[line_state[i]][word_list[i]] += 1

    Output()
    ifp.close()

def testTag():
    prob_start = load_model("prob_mat/prob_start.pkl")
    prob_trans = load_model("prob_mat/prob_trans.pkl")
    prob_emit = load_model("prob_mat/prob_emit.pkl")

    test_str_list = []
    test_str_list.append(u"长春市长春节讲话。")
    test_str_list.append(u"他说的确实在理.")
    test_str_list.append(u"毛主席万岁。")
    test_str_list.append(u"我有一台电脑。")
    for test_str in test_str_list:
        pos_list = viterbi(test_str, ('B', 'M', 'E', 'S'), prob_start, prob_trans, prob_emit)
        print(test_str,'\n',pos_list)

if __name__ == "__main__":
    testTag()

