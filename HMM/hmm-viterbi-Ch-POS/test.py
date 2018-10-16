# -*- coding:utf-8 -*-
import util
import numpy as np
from tqdm import tqdm

# str = u'的发地方'
# print str[2]
# print type(str[-4:])
#
#
# '''避免乱码'''
# s='我不知道怎么做'.decode('utf-8')
# ss = s[2]
# print ss
# s.encode('utf-8')
# print s

# i = '多个'
# lenth = len(i) / 3
# print i[-3:]
# print lenth
# if lenth == 1:
# i = i + '/S'
# else:
# i = i.replace(i[0:3], i[0:3] + '/B')
# k = 1
# while k+1 < lenth:
#         i = i.replace(i[3*k:5*k + 3], i[3*k:5*k + 3] + '/M')
#         # i = i[:5 * k + 3] + '/M' + i[5 * k + 3:]
#         k = k + 1
#     i = i.replace(i[-3:], i[-3:] + '/E')
# print i



# def func(a):
#     b = set(a)
#     c = {}
#     for i in b:
#         c[i] = 0
#     for i in a:
#         c[i]+=1
#     for i in c:
#         print i+':'+str(c[i])
#
# import collections
# def func2(a):
#     str = a.split(' ')
#     print "\n各单词出现的次数：\n %s" % collections.Counter(str)
#
# if __name__ == '__main__':
#     a = '中共中央 总书记 、 国家 主席 江 泽民 '
#     # a.decode('gbk')
#     func(a)



# with open('Segment/corpu.txt', 'r') as f:
#     text = f.read()
#     text = text.decode('utf-8')
#     print text[0]


def cal_A(file):
	'''
	Aij = P(Cj|Ci)  =  P(Ci,Cj) / P(Ci) = Count(Ci,Cj) / Count(Ci)
	'''

	lines = util.read_file(file)
	for i in tqdm(range(len(lines))):
		str = lines[i]
		for i in range(0, len(str) - 1):
			if str[i] == 'S':
				Snum = Snum + 1
				if str[i + 1] == 'S': SS = SS + 1
				if str[i + 1] == 'B': SB = SB + 1
			if str[i] == 'B':
				Bnum = Bnum + 1
				if str[i + 1] == 'M': BM = BM + 1
				if str[i + 1] == 'E': BE = BE + 1
			if str[i] == 'M':
				Mnum = Mnum + 1
				if str[i + 1] == 'M': MM = MM + 1
				if str[i + 1] == 'E': ME = ME + 1
			if str[i] == 'E':
				Enum = Enum + 1
				if str[i + 1] == 'S': ES = ES + 1
				if str[i + 1] == 'B': EB = EB + 1

	A = [[0, BM / Bnum, BE / Bnum, 0],
		 [0, MM / Mnum, (ME / Mnum), 0],
		 [EB / Enum, 0, 0, (ES / Enum)],
		 [SB / Snum, 0, 0, (SS / Snum)]]

	print('A计算完毕')
	return np.array(A, dtype=np.float32)


def build_dict(dict_file):
	global seg_dict
	seg_dict = {}
	fin = open(dict_file, "r")
	for line in fin:
		line = line.strip().decode('GBK')
		if not line or line[0] == '#':
			continue
		line_t = line.split()
		if not util.is_zhs(line_t[0]):  # 如果不是中文汉字
			print("SKIP:%s" % (line_t[0]))
			continue
		if (len(line_t[0]) == 1):
			if line_t[0] not in seg_dict.keys():
				seg_dict[line_t[0]] = [line_t[0]]
			else:
				print("EEEEEEEEEEEEEEEEEEEEEE1")
				seg_dict[line_t[0]].append(line_t[0])
				return
		else:
			chr = line_t[0][0]
			if chr not in seg_dict.keys():
				seg_dict[chr] = [line_t[0]]
			else:
				seg_dict[chr].append(line_t[0])
	print(seg_dict)


# Ci->Cj  转移矩阵
count_trans = {'B': {'B': 0, 'E': 0, 'M': 0, 'S': 0}, 'E': {'B': 0, 'E': 0, 'M': 0, 'S': 0},
			   'M': {'B': 0, 'E': 0, 'M': 0, 'S': 0}, 'S': {'B': 0, 'E': 0, 'M': 0, 'S': 0}}
P_transMatrix = {'B': {'B': 0, 'E': 0, 'M': 0, 'S': 0}, 'E': {'B': 0, 'E': 0, 'M': 0, 'S': 0},
				 'M': {'B': 0, 'E': 0, 'M': 0, 'S': 0}, 'S': {'B': 0, 'E': 0, 'M': 0, 'S': 0}}
# Ci->Oj  混淆矩阵
count_mixed = {'B': {}, 'E': {}, 'M': {}, 'S': {}}
P_mixedMatrix = {'B': {}, 'E': {}, 'M': {}, 'S': {}}


def st_trainMatrix(trainfile):
	with open(trainfile) as fin:
		for line in fin:
			line = line.strip()
			line_items = line.split()
			for item in line_items:
				if util.is_terminator(item) or (len(item) == 1 and util.is_punct(item)):
					line_items.remove(item)
			# whether exists elements
			if not line_items:
				continue
			# BEMS encode
			# line_hits  <-->  line_items
			# 进行字符和处理结果的对应
			line_hits = []  # every char status
			for i_index in range(len(line_items)):
				# line_items[i_index] = line_items[i_index].decode('GBK')
				if len(line_items[i_index]) == 1:
					line_hits += 'S'
				else:
					for j_index in range(len(line_items[i_index])):
						if j_index == 0:
							line_hits += 'B'
						elif j_index == len(line_items[i_index]) - 1:
							line_hits += 'E'
						else:
							line_hits += 'M'
			if len(''.join(line_items)) != len(line_hits):
				print("EEEEEEE %d<->%d" % (len(''.join(line_items)), len(line_hits)))
			# print(''.join(line_items))
			# print(line_hits)
			line_items = ''.join(line_items)

			for i in range(len(line_hits) - 1):
				# for calc trans matrix P[I][J]
				count_trans[line_hits[i]][line_hits[i + 1]] += 1
			for i in range(len(line_hits) - 1):
				# for calc mixed_matrix
				if line_items[i] not in count_mixed[line_hits[i]].keys():
					count_mixed[line_hits[i]][line_items[i]] = 1
				else:
					count_mixed[line_hits[i]][line_items[i]] += 1

	for (k_i, v_i) in count_trans.items():
		count = sum(v_i.values())
		for (k_j, v_j) in v_i.items():
			P_transMatrix[k_i][k_j] = v_j / count

	# for (k_i, v_i) in count_mixed.items():
	#     for item in enumo:
	#         if item not in v_i.keys():
	#             count_mixed[k_i][item] = 1  #针对没有出现的词，将其出现频次设置为1

	for (k_i, v_i) in count_mixed.items():
		count = sum(v_i.values())
		for (k_j, v_j) in v_i.items():
			P_mixedMatrix[k_i][k_j] = (v_j + 1) / count  # 添加1进行平滑

	print(P_mixedMatrix, P_transMatrix)
	return


if __name__ == '__main__':

	def load_model(f_name):
		ifp = open(f_name, 'r')
		return eval(ifp.read())  # eval参数是一个字符串, 可以把这个字符串当成表达式来求值,


	PROB_EMIT = "Segment\matrix\prob_emit.txt"  # 发射概率
	B = load_model(PROB_EMIT)
	print(type(B['S'].get('傲')))

	emit = {'S': {'傲': 5.678774444757828e-06, '琮': 1.8929248149192763e-06}}
	print(emit['S'].get('傲', 0))

	pass
# build_dict('Segment/dict.small.txt')
# st_trainMatrix('Segment/corpu.txt')
