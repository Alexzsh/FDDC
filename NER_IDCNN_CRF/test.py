class testObj(object):
    __slots__= ('__storage__', '__ident_func__')

class oriObj(object):
    pass
print(dir(testObj),'\n',dir(oriObj))
a=testObj()
a.__storage__=1
a.x=2
print(a.x)