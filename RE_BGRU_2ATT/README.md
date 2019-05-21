
# Chinese Relation Extraction by biGRU with Character and Sentence Attentions


Bi-directional GRU with Word and Sentence Dual Attentions for End-to End Relation Extraction



Original paper 
[Attention-Based Bidirectional Long Short-Term Memory Networks for Relation Classification](http://anthology.aclweb.org/P16-2034)   
[Neural Relation Extraction with Selective Attention over Instances](http://aclweb.org/anthology/P16-1200)  

![](http://www.crownpku.com/images/201708/1.jpg)




## Usage


### * Training:

- 50/100/200/300 dimensions word embedding
```
中 0.041946 -0.008482 -0.159824 -0.049679 -0.076711 0.167492 0.130599 -0.032046 0.064531 -0.079213 -0.084977 -0.035551 0.019407 0.000105 -0.171212 0.201787 0.128076 0.136759 -0.044008 0.200287 -0.115818 0.067971 -0.315720 0.050931 -0.347787 -0.083768 -0.157677 0.091808 -0.128085 0.041702 0.034292 0.225157 0.063689 -0.048836 0.083003 0.021937 -0.198219 -0.023556 0.073976 -0.015660 0.016165 -0.157838 0.097250 0.158060 -0.042314 -0.037621 -0.233718 -0.159042 -0.133466 0.092469 0.105558 -0.254628 0.227929 -0.054321 -0.237484 0.120614 0.331842 0.085823 0.167086 -0.035319 0.068754 0.029160 -0.000655 -0.214260 0.064539 0.044746 -0.015626 0.322286 -0.064758 0.266979 -0.125578 0.112040 0.165422 0.205051 -0.376889 0.575517 0.034682 -0.043816 0.151417 0.047435 -0.074374 -0.177582 0.064507 -0.045437 -0.114749 -0.105386 0.192751 -0.223745 -0.195398 -0.280018 -0.182222 -0.020006 -0.086166 -0.209321 0.032767 -0.076373 -0.046701 -0.333495 -0.067261 0.180224
```
- pre-defined relation 

```
Current sample data includes the following pre-defined relationships:
unknown, 中标, 增发, 增持, 定价, balabala
```
- train data

e1 |e2 |relation|sentence
:---:|:---:|:---:|:---:
上海同济建设有限公司 |南京江宁经济技术开发总公司 |中标|公司控股子公司上海同济建设有限公司近日收到南京江宁经济技术开发总公司发出的中标通知书 

- output

    - the predict relation via softmax  中标 

### * Testing:

Give a test sentence like the training data, but do not include a relational field

e1 |e2 |sentence
:---:|:---:|:---:
上海同济建设有限公司 |南京江宁经济技术开发总公司 |公司控股子公司上海同济建设有限公司近日收到南京江宁经济技术开发总公司发出的中标通知书 

## Sample Results

请输入中文句子，格式为 "name1 name2 sentence":  
实体1: 上海同济建设有限公司  
实体2: 南京江宁经济技术开发总公司  
公司控股子公司上海同济建设有限公司近日收到南京江宁经济技术开发总公司发出的中标通知书  
关系是:  
No.1: unknown, Probability is 0.9999192  
No.2: 父母, Probability is 4.89466e-05  
No.3: 兄弟姐妹, Probability is 1.8887486e-05  


`由于训练数据中没有中标这个关系预定义、故预测关系是unknown`