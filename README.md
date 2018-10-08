<!-- TOC -->

- [整体处理流程](#%E6%95%B4%E4%BD%93%E5%A4%84%E7%90%86%E6%B5%81%E7%A8%8B)
    - [*.html](#html)
    - [*.train](#train)
- [NER log](#ner-log)
    - [Network architecture](#network-architecture)
    - [Network Hyperparameters](#network-hyperparameters)
    - [train.log](#trainlog)
    - [idcnn 目前陷入局部最优解的问题，loss居高不下，正在解决](#idcnn-%E7%9B%AE%E5%89%8D%E9%99%B7%E5%85%A5%E5%B1%80%E9%83%A8%E6%9C%80%E4%BC%98%E8%A7%A3%E7%9A%84%E9%97%AE%E9%A2%98loss%E5%B1%85%E9%AB%98%E4%B8%8D%E4%B8%8B%E6%AD%A3%E5%9C%A8%E8%A7%A3%E5%86%B3)

<!-- /TOC -->



# 整体处理流程
![process](http://aliyuntianchipublic.cn-hangzhou.oss-pub.aliyun-inc.com/public/files/image/1095279116990/1536305290096_p1jAlZgyUb.jpg)
目前实现结构提取-文本预处理-实体识别阶段

## *.html
![dom](http://aliyuntianchipublic.cn-hangzhou.oss-pub.aliyun-inc.com/public/files/image/1095279116990/1536305456472_deP113CdoZ.jpg)
每一份html文件可以根据其dom树提取无结构化数据,dom层级限制说明如图
- 不考虑任何image
- 暂时未对table处理
- 需要提取type标签的子属性title
- hidden标签可以用来帮助判断table是否为跨页table 用于后期整合
  


## *.train

对应每一份文件都由相应的字段提供，根据这些数据进行反标注为BIO格式
**主键在同一句话中才标注、其他字段与主键之一在一句话中才进行标注**
```yaml
1153: 
    - 国家电网公司	
    - 青岛汉缆股份有限公司	
    - 国家电网公司输变电项目哈密南-郑州±800千伏特高压直流输电线路工程导线施工标段(二)导地线招标活动		
    - 169287975.4	
    - 169287975.4
```

# NER log

BiLSTM+CRF

## Network architecture

<img src="https://upload-images.jianshu.io/upload_images/9813147-ad682cb7c4979f33..png?imageMogr2/auto-orient/" width="80%" height="80%" />

<div STYLE="page-break-after: always;"></div>

## Network Hyperparameters
```yaml
{
    "model_type": "bilstm", #model_type
    "num_chars": 3404, #"nums of chars" 
    "char_dim": 100, #"Embedding size for characters",
    "num_tags": 13, #"nums of entities",
    "seg_dim": 20, #"Embedding size for sentence",
    "lstm_dim": 100, #lstm length
    "batch_size": 5, #
    "emb_file": "data\\vec.txt", #pre-trained embedding
    "clip": 5.0, #clip for dimesion explore
    "dropout_keep": 0.5,
    "optimizer": "adam",
    "lr": 0.001,
    "tag_schema": "iobes",
    "pre_emb": true, #Wither use pre-trained embedding
    "zeros": false, #Wither replace digits with zero
    "lower": true #Wither lower case
}
```




## train.log
- 第一次尝试
    - 随意标注，由于机器配置问题，将每句话进行截断处理，尾部直接截断到最后一个字段为止
```text
2018-09-10 10:22:48,610 - log\train.log - INFO - iteration:42 step:190/210, NER loss: 2.333041
2018-09-10 10:25:02,419 - log\train.log - INFO - evaluate:dev
2018-09-10 10:25:23,958 - log\train.log - INFO - processed 463933 tokens with 1493 phrases; found: 1195 phrases; correct: 893.

2018-09-10 10:25:23,959 - log\train.log - INFO - accuracy:  97.17%; precision:  74.73%; recall:  59.81%; FB1:  66.44

2018-09-10 10:25:23,960 - log\train.log - INFO -            hetong: precision:  76.03%; recall:  62.16%; FB1:  68.40  121

2018-09-10 10:25:23,961 - log\train.log - INFO -           jiafang: precision:  70.96%; recall:  67.63%; FB1:  69.26  427

2018-09-10 10:25:23,963 - log\train.log - INFO -           xiangmu: precision:  59.83%; recall:  48.11%; FB1:  53.33  234

2018-09-10 10:25:23,963 - log\train.log - INFO -            yifang: precision:  86.68%; recall:  59.08%; FB1:  70.26  413

2018-09-10 10:25:23,972 - log\train.log - INFO - evaluate:test
2018-09-10 10:25:51,435 - log\train.log - INFO - processed 695432 tokens with 1456 phrases; found: 1435 phrases; correct: 1014.

2018-09-10 10:25:51,436 - log\train.log - INFO - accuracy:  98.14%; precision:  70.66%; recall:  69.64%; FB1:  70.15

2018-09-10 10:25:51,438 - log\train.log - INFO -            hetong: precision:  61.82%; recall:  54.84%; FB1:  58.12  110

2018-09-10 10:25:51,438 - log\train.log - INFO -           jiafang: precision:  64.65%; recall:  69.57%; FB1:  67.02  495

2018-09-10 10:25:51,439 - log\train.log - INFO -           xiangmu: precision:  46.12%; recall:  41.61%; FB1:  43.75  258

2018-09-10 10:25:51,439 - log\train.log - INFO -            yifang: precision:  88.64%; recall:  86.52%; FB1:  87.56  572

```


```yaml
{
  'string': '美尚生态系观股份有限公司(以下简称“公司")于近日收到招标人江苏省无锡惠山经济开发区委员会发来的《中标通知书,通知书确认
公司为“无锡古庄生态农业科技园PPPI项目"(以下器称“本项目”)的中标人', 
  'entities': [
      {'word': '江苏省无锡惠山经济开发区委员会', 'start': 29, 'end': 47, 'type': 'jiafang'}, 
      {'word': '无锡古庄生态农业科技园PPPI项目', 'start': 66, 'end': 83, 'type': 'xiangmu'}
      ]
}

```

epoch|42
:--:|:--:
loss|2.33
test f1|70.15
dev f1|66.44

> 对该句话的测试，从结果可以看到对于这样的截断方式发现了`甲方`以及`项目`，但没有发现`乙方`

<div STYLE="page-break-after: always;"></div>

- 第二次尝试
    - 随意标注，这次通过前后都留十个`O`标注的字符

```text
2018-09-11 03:50:25,074 - log\train.log - INFO - iteration:101 step:0/419, NER loss: 0.351078
processed 84351 tokens with 721 phrases; found: 731 phrases; correct: 602.

2018-09-11 03:50:28,917 - log\train.log - INFO - accuracy:  96.61%; precision:  82.35%; recall:  83.50%; FB1:  82.92

2018-09-11 03:50:28,917 - log\train.log - INFO -            hetong: precision:  94.55%; recall:  91.23%; FB1:  92.86  55

2018-09-11 03:50:28,917 - log\train.log - INFO -           jiafang: precision:  80.87%; recall:  77.18%; FB1:  78.98  230

2018-09-11 03:50:28,917 - log\train.log - INFO -           xiangmu: precision:  65.56%; recall:  75.00%; FB1:  69.96  151

2018-09-11 03:50:28,917 - log\train.log - INFO -            yifang: precision:  89.83%; recall:  91.07%; FB1:  90.44  295

2018-09-11 03:50:28,922 - log\train.log - INFO - evaluate:test
2018-09-11 03:50:36,830 - log\train.log - INFO - processed 178802 tokens with 1449 phrases; found: 1500 phrases; correct: 1208.

2018-09-11 03:50:36,835 - log\train.log - INFO - accuracy:  96.58%; precision:  80.53%; recall:  83.37%; FB1:  81.93

2018-09-11 03:50:36,835 - log\train.log - INFO -            hetong: precision:  88.00%; recall:  88.71%; FB1:  88.35  125

2018-09-11 03:50:36,835 - log\train.log - INFO -           jiafang: precision:  84.57%; recall:  83.66%; FB1:  84.11  460

2018-09-11 03:50:36,835 - log\train.log - INFO -           xiangmu: precision:  61.95%; recall:  71.64%; FB1:  66.44  318

2018-09-11 03:50:36,835 - log\train.log - INFO -            yifang: precision:  85.76%; recall:  87.52%; FB1:  86.63  597
```

```yaml
{
    'string': '美尚生态系观股份有限公司(以下简称“公司")于近日收到招标人江苏省无锡惠山经济开发区委员会发来的《中标通知书,通知书确认 公
司为“无锡古庄生态农业科技园PPPI项目"(以下器称“本项目”)的中标人', 
    'entities': [
        {'word': '江苏省无锡惠山经济开发区委员会', 'start':30, 'end': 45, 'type': 'jiafang'}
        ]
}
```

epoch|101
:--:|:--:
loss|0.35
test f1|81.93
dev f1|82.92

> - 与上次相比，dev与test的f1值更加接近，相对而言更加鲁棒
> - 由于训练次数较多，所以loss相对更小
> - 但是对于这样的截断方式只能识别出甲方

<div STYLE="page-break-after: always;"></div>

- 第三次尝试
    - 主键出现在同一句话中才进行标注，batch_size减为2，相对耗时

```text
2018-09-13 23:58:51,355 - log\train.log - INFO - iteration:44 step:830/840, NER loss: 1.698312
2018-09-13 23:59:37,254 - log\train.log - INFO - evaluate:dev
2018-09-14 00:00:10,623 - log\train.log - INFO - processed 819272 tokens with 2354 phrases; found: 2151 phrases; correct: 1770.

2018-09-14 00:00:10,624 - log\train.log - INFO - accuracy:  98.30%; precision:  82.29%; recall:  75.19%; FB1:  78.58

2018-09-14 00:00:10,625 - log\train.log - INFO -            hetong: precision:  85.09%; recall:  63.13%; FB1:  72.49  161

2018-09-14 00:00:10,626 - log\train.log - INFO -           jiafang: precision:  81.05%; recall:  80.70%; FB1:  80.87  686

2018-09-14 00:00:10,626 - log\train.log - INFO -           xiangmu: precision:  73.39%; recall:  68.23%; FB1:  70.72  436

2018-09-14 00:00:10,626 - log\train.log - INFO -            yifang: precision:  87.21%; recall:  77.32%; FB1:  81.97  868

2018-09-14 00:00:10,641 - log\train.log - INFO - evaluate:test
2018-09-14 00:01:02,448 - log\train.log - INFO - processed 1416367 tokens with 3188 phrases; found: 2953 phrases; correct: 2306.

2018-09-14 00:01:02,449 - log\train.log - INFO - accuracy:  98.42%; precision:  78.09%; recall:  72.33%; FB1:  75.10

2018-09-14 00:01:02,450 - log\train.log - INFO -            hetong: precision:  82.85%; recall:  62.86%; FB1:  71.48  239

2018-09-14 00:01:02,451 - log\train.log - INFO -           jiafang: precision:  78.76%; recall:  78.00%; FB1:  78.38  923

2018-09-14 00:01:02,451 - log\train.log - INFO -           xiangmu: precision:  64.81%; recall:  58.77%; FB1:  61.64  574

2018-09-14 00:01:02,452 - log\train.log - INFO -            yifang: precision:  82.91%; recall:  77.14%; FB1:  79.92  1217

2018-09-14 00:01:02,552 - log\train.log - INFO - new best test f1 score:75.100
2018-09-14 00:04:52,635 - log\train.log - INFO - iteration:45 step:40/840, NER loss: 1.249973

```

```yaml
{
  'string': '美尚生态系观股份有限公司(以下简称“公司")于近日收到招标人江苏省无锡惠山经济开发区委员会发来的《中标通知书,通知书确认 公 司为“
无锡古庄生态农业科技园PPPI项目"(以下器称“本项目”)的中标人', 
  'entities': [
    {'word': '美尚生态系观股份有限公司', 'start': 0, 'end': 12, 'type': 'yifang'},
    {'word': '江苏省无锡惠山经济开发区委员会', 'start': 30, 'end': 45, 'type': 'jiafang'}, 
    {'word': '无锡古庄生态农业科技园PPPI项目', 'start': 66, 'end': 83, 'type': 'xiangmu'}
    ]
}
```

> - 该方式较为耗时但是保留了较多的上下文信息，也识别出了所有的实体
> - 与第一次尝试相比训练44轮，loss 减小到1.6 test与dev的f1也相对提高


## idcnn 目前陷入局部最优解的问题，loss居高不下，正在解决