# -*- coding:utf-8 -*-
import util
import sys

'''
π是初始状态概率分布，就是说，对于语料库每个词，初始状态的发生概率
（实际上词中词尾的初始概率就是0）
26个基本词类标记
（名词n、时间词t、处所词s、方位词f、数词m、量词q、区别词b、代词r、动词v、
形容词a、状态词z、副词d、介词p、连词c、助词u、语气词y、叹词e、拟声词o、
成语i、习惯用语l、简称j、前接成分h、后接成分k、语素g、非语素字x、标点符号w）
'''
A_dic = {}  # 转移概率 
B_dic = {}  # 发射概率
Pi_dic = {}
Count_dic = {}  # Count(Ci)
state_list = ['Ag', 'a', 'ad', 'an', 'Bg', 'b', 'c', 'Dg',
			  'd', 'e', 'f', 'h', 'i', 'j', 'k', 'l',
			  'Mg', 'm', 'Ng', 'n', 'nr', 'ns', 'nt', 'nx',
			  'nz', 'o', 'p', 'q', 'Rg', 'r', 's','na',
			  'Tg', 't','u', 'Vg', 'v', 'vd', 'vn','vvn',
			  'w', 'Yg', 'y', 'z']  # 状态集

line_num = -1
word_set = set()
# INPUT_DATA = '../data/corpu.txt'
INPUT_DATA = '../data/corpus_POS.txt'
PROB_TRANS = "matrix\prob_trans_POS.txt"  # 保存转移概率
PROB_EMIT = "matrix\prob_emit_POS.txt"  # 保存发射概率
PROB_START = "matrix\prob_start_POS.txt"


# 初始化字典
def init():
	for state in state_list:
		A_dic[state] = {}
		for state1 in state_list:
			A_dic[state][state1] = 0.0
	for state in state_list:
		Pi_dic[state] = 0.0
		B_dic[state] = {}
		Count_dic[state] = 0


# 计算概率 A B
def get_A_B(dict_path):
	init()
	global word_set  # 初始是set()
	global line_num  # 初始是-1
	with open(dict_path) as ifp:
		for line in ifp:
			line_num += 1
			if line_num % 10000 == 0:
				print(line_num)

			line = line.strip()
			if not line: continue
			# line = line.decode("gbk", "ignore")  # 设置为ignore，会忽略非法字符

			word_list = []
			line_state = []
			lineArr = line.split(" ")
			for item in lineArr:
				ind = item.index('/')
				if '[' in item:
					word = item[1:ind]
				else:
					word = item[:ind]
				if ']' in item:
					ind2 = item.index(']')
					state = item[ind + 1:ind2]
				else:
					state = item[ind + 1:]
				# if state == 'w': print('w')
				word_list.append(word)
				line_state.append(state)

			# # 去除词性标注，只保存词组
			# phrase = line.split("(/[a-z]*\\s{0,})")
			# # 获取语料库中从前往后的所有词组的词性
			# characters = line.split("[0-9|-]*/|\\s{1,}[^a-z]*")
			# word_list.append(phrase)
			# line_state.append(characters)

			if len(word_list) != len(line_state):
				print(sys.stderr, "[line_num = %d][line = %s]" % (line_num, line.endoce("utf-8", 'ignore')))
			else:
				for i in range(len(line_state)):
					if i == 0:
						Pi_dic[line_state[0]] += 1
						Count_dic[line_state[0]] += 1
					else:
						# 用于计算转移概率	Count(Ci,Cj) / Count(Ci)
						A_dic[line_state[i - 1]][line_state[i]] += 1
						Count_dic[line_state[i]] += 1  # B 状态的出现次数 +1

						# 计算发射概率	Count(Oj,Ci)+1 / Count(Ci)
						if word_list[i] not in B_dic[line_state[i]]:
							B_dic[line_state[i]][word_list[i]] = 1.0
						else:  # 如果单词已经在词典中
							B_dic[line_state[i]][word_list[i]] += 1


def Output():  # 输出模型的 AB 到文件
	print("len(word_set) = %s " % (len(word_set)))

	for key in Pi_dic:  # 状态的初始概率
		Pi_dic[key] = Pi_dic[key] * 1.0 / line_num
	print(Pi_dic)

	for key in A_dic:  # 状态转移概率
		for key1 in A_dic[key]:
			if Count_dic[key] == 0: print(key)
			A_dic[key][key1] = A_dic[key][key1] / Count_dic[key]
	print(A_dic)

	for key in B_dic:  # 发射概率(状态->词语的条件概率)
		for word in B_dic[key]:
			B_dic[key][word] = B_dic[key][word] / Count_dic[key]
	print(B_dic)

	with open(PROB_START, 'w') as f:
		f.write(str(Pi_dic))
	with open(PROB_TRANS, 'w') as f:
		f.write(str(A_dic))
	with open(PROB_EMIT, 'w') as f:
		f.write(str(B_dic))


def main():
	get_A_B(INPUT_DATA)
	Output()


if __name__ == '__main__':
	main()
