#!/usr/bin/python
#-*-coding:utf-8
import pickle
import numpy as np
def load_model(f_name):
    with open(f_name,'rb') as fr:
        return pickle.load(fr)

prob_start = load_model("prob_start.pkl")
prob_trans = load_model("prob_trans.pkl")
prob_emit = load_model("prob_emit.pkl")



def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}] #tabular
    path = {}
    for y in states:  # init
        V[0][y] = start_p[y] * emit_p[y].get(obs[0], 1e-10)
        path[y] = [y]
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
        for y in states:
            (prob, state) = max([(V[t - 1][y0] * trans_p[y0].get(y, 1e-10) * emit_p[y].get(obs[t], 1e-10), y0) for y0 in states if V[t - 1][y0] > 0])
            V[t][y] = prob
            newpath[y] = path[state] + [y]
        path = newpath
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])

def cut(sentence):
    #pdb.set_trace()
    pos_list =  viterbi(sentence,('B','M','E','S'), prob_start, prob_trans, prob_emit)
    return (pos_list)

if __name__ == "__main__":
    test_str_list=[]
    test_str_list.append( u"长春市长春节讲话。")
    test_str_list.append( u"他说的确实在理.")
    test_str_list.append( u"毛主席万岁。")
    test_str_list.append( u"我有一台电脑。")
    for test_str in test_str_list:
        pos_list = cut(test_str)
        print (test_str)
        print (pos_list)



