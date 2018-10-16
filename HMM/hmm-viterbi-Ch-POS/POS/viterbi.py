# -*- coding:utf-8 -*-

'''
举例
求解最可能的隐状态序列是HMM的三个典型问题之一，通常用维特比算法解决。
维特比算法就是求解HMM上的最短路径（-log(prob)，也即是最大概率）的算法。

稍微用中文讲讲思路，很明显，第一天天晴还是下雨可以算出来：

1、定义V[时间][今天天气] = 概率，注意今天天气指的是，前几天的天气都确定下来了（概率最大）今天天气是X的概率，这里的概率就是一个累乘的概率了。

2、因为第一天我的朋友去散步了，所以第一天下雨的概率V[第一天][下雨] = 初始概率[下雨] * 发射概率[下雨][散步] = 0.6 * 0.1 = 0.06，
同理可得V[第一天][天晴] = 0.24 。从直觉上来看，因为第一天朋友出门了，她一般喜欢在天晴的时候散步，所以第一天天晴的概率比较大，数字与直觉统一了。

3、从第二天开始，对于每种天气Y，都有前一天天气是X的概率 * X转移到Y的概率 * Y天气下朋友进行这天这种活动的概率。
因为前一天天气X有两种可能，所以Y的概率有两个，选取其中较大一个作为V[第二天][天气Y]的概率，同时将今天的天气加入到结果序列中

4、比较V[最后一天][下雨]和[最后一天][天晴]的概率，找出较大的哪一个对应的序列，就是最终结果。
'''

def viterbi(obs, states, start_p, trans_p, emit_p):  # 维特比算法（一种递归算法）
	"""
	:param obs:观测序列
	:param states:隐状态
	:param start_p:初始概率（隐状态）
	:param trans_p:转移概率（隐状态）
	:param emit_p: 发射概率 （隐状态表现为显状态的概率）
	:return:
	"""
	V = [{}]
	path = {}
	for y in states:  # 初始值
		V[0][y] = start_p[y] * emit_p[y].get(obs[0], 0)  # 初始概率[下雨] * 发射概率[下雨][散步]	(t == 0)
		path[y] = [y]
	# 对 t > 0 跑一遍维特比算法
	for t in range(1, len(obs)):
		V.append({})
		newpath = {}
		for y in states:
			# 概率 隐状态 =   前状态是y0的概率 * y0转移到y的概率   *   y表现为当前状态的概率
			(prob, state) = max([(V[t - 1][y0] * trans_p[y0].get(y, 0) * emit_p[y].get(obs[t], 0), y0)
								 for y0 in states if V[t - 1][y0] > 0])
			# 记录最大概率
			V[t][y] = prob
			# 记录路径
			newpath[y] = path[state] + [y]
		path = newpath  # 记录状态序列
	(prob, state) = max([(V[len(obs) - 1][y], y) for y in states])  # 在最后一个位置，以y状态为末尾的状态序列的最大概率
	return (prob, path[state])  # 返回概率和状态序列
