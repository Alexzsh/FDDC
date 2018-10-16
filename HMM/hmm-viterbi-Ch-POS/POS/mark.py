'''
    最大序列的逆推输出和分词实现。
'''

from Segment.viterbi import viterbi


def load_model(f_name):
	ifp = open(f_name, 'r')
	return eval(ifp.read())  # eval参数是一个字符串, 可以把这个字符串当成表达式来求值,


def cut(sentence, P_START, A, B):
	prob, pos_list = viterbi(sentence, state_list, P_START, A, B)
	return (prob, pos_list)


if __name__ == '__main__':
	PROB_EMIT = "matrix\prob_emit_POS.txt"  # 发射概率
	PROB_TRANS = "matrix\prob_trans_POS.txt"  # 转移概率
	PROB_START = "matrix\prob_start_POS.txt"

	state_list = ['Ag', 'a', 'ad', 'an', 'Bg', 'b', 'c', 'Dg',
				  'd', 'e', 'f', 'h', 'i', 'j', 'k', 'l',
				  'Mg', 'm', 'Ng', 'n', 'nr', 'ns', 'nt', 'nx',
				  'nz', 'o', 'p', 'q', 'Rg', 'r', 's', 'na',
				  'Tg', 't', 'u', 'Vg', 'v', 'vd', 'vn', 'vvn',
				  'w', 'Yg', 'y', 'z']  # 状态集

	# 初始状态概率( jieba 的经验值)    
	P_START = load_model(PROB_START)
	A = load_model(PROB_TRANS)	# 转移概率 
	B = load_model(PROB_EMIT)	# 发射概率
	A, B = dict(A), dict(B)

	test_str = u"今天 天气 特别 好"
	prob, pos_list = cut(test_str, P_START, A, B)
	print(test_str)
	print(pos_list)
	# result = ''
	# for id in range(len(pos_list)):
	# 	state = pos_list[id]
	# 	if state == 'B':
	# 		result +=test_str[id]
	# 	elif state == 'M':
	# 		result += test_str[id]
	# 	elif state == 'E':
	# 		result += test_str[id]+'/'
	# 	else:
	# 		result += test_str[id] + '/'
	# print(result)



