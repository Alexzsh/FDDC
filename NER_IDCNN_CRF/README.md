

# Chinese Named Entity Recognition using IDCNN/biLSTM+CRF


End to End Chinese Named Entity Recognition by Iterated Dilated Convolution Nerual Networks with Conditional Random Field layer.


Original paper 
[Fast and Accurate Entity Recognition with Iterated Dilated Convolutions](https://arxiv.org/abs/1702.02098)


![](http://crownpku.github.io/images/201708/3.jpg)


![](http://crownpku.github.io/images/201708/4.jpg)




## Usage


### * Training:

- 50/100/200/300 dimensions word embedding
```
中 0.041946 -0.008482 -0.159824 -0.049679 -0.076711 0.167492 0.130599 -0.032046 0.064531 -0.079213 -0.084977 -0.035551 0.019407 0.000105 -0.171212 0.201787 0.128076 0.136759 -0.044008 0.200287 -0.115818 0.067971 -0.315720 0.050931 -0.347787 -0.083768 -0.157677 0.091808 -0.128085 0.041702 0.034292 0.225157 0.063689 -0.048836 0.083003 0.021937 -0.198219 -0.023556 0.073976 -0.015660 0.016165 -0.157838 0.097250 0.158060 -0.042314 -0.037621 -0.233718 -0.159042 -0.133466 0.092469 0.105558 -0.254628 0.227929 -0.054321 -0.237484 0.120614 0.331842 0.085823 0.167086 -0.035319 0.068754 0.029160 -0.000655 -0.214260 0.064539 0.044746 -0.015626 0.322286 -0.064758 0.266979 -0.125578 0.112040 0.165422 0.205051 -0.376889 0.575517 0.034682 -0.043816 0.151417 0.047435 -0.074374 -0.177582 0.064507 -0.045437 -0.114749 -0.105386 0.192751 -0.223745 -0.195398 -0.280018 -0.182222 -0.020006 -0.086166 -0.209321 0.032767 -0.076373 -0.046701 -0.333495 -0.067261 0.180224
```

- pre-defined tag
```
Current sample data includes 3 types of Named Entities, including ORG, PER and LOC
```

- train data
pre-tagged sentence of words and its tag 
```
美 B-LOC
国 I-LOC
政 O
府 O
不 O
想 O
也 O
没 O
有 O
向 O
中 B-LOC
国 I-LOC
转 O
让 O
敏 O
感 O
技 O
术 O 
```

### * Testing:

Give a whole test sentence

string: 公司控股子公司上海同济建设有限公司近日收到南京江宁经济技术开发总公司发出的中标通知书


## Sample Results

```
INFO:tensorflow:Restoring parameters from ckpt_IDCNN/ner.ckpt

{'string': '公司控股子公司上海同济建设有限公司近日收到南京江宁经济技术开发总公司发出的中标通知书 ',
 'entities': 
 [{'word': '公司控股子公司上海同济建设有限公司', 'start': 0, 'end': 17, 'type': 'ORG'},
  {'word': '南京', 'start': 21, 'end': 23, 'type': 'LOC'}, 
  {'word': '江宁经济技术开发总公司', 'start': 23, 'end': 34, 'type': 'ORG'}]}
```

