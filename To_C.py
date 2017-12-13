import ctypes
from ctypes import Structure, POINTER
import numpy as np
'''
GSL = ctypes.cdll.LoadLibrary('./后台_01_DLL.dll')
GSL.My_C.argtypes=(POINTER(ctypes.c_float),POINTER(ctypes.c_float),ctypes.c_int,ctypes.c_int)
#只有一个借口，它是函数My_C，GSL是我们姓名首字母的结合
#argtypes=(POINTER(ctypes.c_float),POINTER(ctypes.c_float),ctypes.c_int,ctypes.c_int)定义输入参数类型
#四个参数,两个float指针,两个int，分别代表:节点数组首地址、边数组首地址、节点个数、边个数


# 节点:
#   [0]id,[1]ES，[2]LS
# 边:
#   [0]head,    [1]tail,    [2]duration，
#   [3]ES,      [4]LS,      [5]TF,      [6]Is_Critical_Path,
#   [7]EF,      [8]LF,      [9]FF

#下面生成numpy数组，作为信息源
Py_N=np.array([ [ 1,0,0 ],
                [ 2,0,0 ],
                [ 3,0,0 ],
                [ 5,0,0 ],
                [ 8,0,0 ],
                [ 7,0,0 ],
                [ 9,0,0 ],
                [ 4,0,0 ],
                [ 6,0,0 ] ])		
Py_L=np.array([ [ 1,2,6,0,0,0,0,0,0,0 ],
                [ 1,3,4,0,0,0,0,0,0,0 ],
                [ 1,4,5,0,0,0,0,0,0,0 ] ,
                [ 2,5,1,0,0,0,0,0,0,0 ],
                [ 3,5,1,0,0,0,0,0,0,0 ],
                [ 4,6,3,0,0,0,0,0,0,0 ],
	            [ 5,7,9,0,0,0,0,0,0,0 ],
                [ 5,8,7,0,0,0,0,0,0,0 ],
                [ 6,8,4,0,0,0,0,0,0,0 ],
                [ 7,9,2,0,0,0,0,0,0,0 ],
                [ 8,9,4,0,0,0,0,0,0,0 ] ])

#下面将numpy数组转化为C类型的数组，分别给Py_Nodes与Py_Links
Py_Nodes=np.asarray(Py_N,dtype=np.float32)
Py_Links=np.asarray(Py_L,dtype=np.float32)

#下面得到Py_Nodes与Py_Links的指针
Py_Nodes_P = ctypes.cast(Py_Nodes.ctypes.data, POINTER(ctypes.c_float))
Py_Links_P = ctypes.cast(Py_Links.ctypes.data, POINTER(ctypes.c_float))

#如果Py_Nodes与Py_Links内存不连续，强制转化为连续存储
if not Py_Nodes.flags['C_CONTIGUOUS']:
    Py_Nodes = np.ascontiguous(Py_Nodes, dtype=Py_Nodes.dtype)

if not Py_Links.flags['C_CONTIGUOUS']:
    Py_Links = np.ascontiguous(Py_Links, dtype=Py_Links.dtype)

#调用我的接口，计算时内存中的信息已经发生了变化
GSL.My_C(Py_Nodes_P,Py_Links_P,9,11)

print(Py_Nodes)
print(Py_Links)

#其实我是看了网上的一篇博客，然后想到numpy很强大，以后还会多多使用，或许值得一试
#然后结合ctypes仅有的一点经验，试了一下，然后成功了，好开心啊
#博客网址:http://blog.csdn.net/thesby/article/details/76512629
'''

def Cal(Data):#{'Nodes': ,'Links': }
    Py_N=Data['Nodes']
    Py_L=Data['Links']

    GSL = ctypes.cdll.LoadLibrary('./后台_01_DLL.dll')
    GSL.My_C.argtypes = (POINTER(ctypes.c_float), POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int)
    Py_Nodes = np.asarray(Py_N, dtype=np.float32)
    Py_Links = np.asarray(Py_L, dtype=np.float32)

    Py_Nodes_P = ctypes.cast(Py_Nodes.ctypes.data, POINTER(ctypes.c_float))
    Py_Links_P = ctypes.cast(Py_Links.ctypes.data, POINTER(ctypes.c_float))

    if not Py_Nodes.flags['C_CONTIGUOUS']:
        Py_Nodes = np.ascontiguous(Py_Nodes, dtype=Py_Nodes.dtype)

    if not Py_Links.flags['C_CONTIGUOUS']:
        Py_Links = np.ascontiguous(Py_Links, dtype=Py_Links.dtype)

    GSL.My_C(Py_Nodes_P, Py_Links_P, Py_N.shape[0],Py_L.shape[0] )

    Data2={'Nodes':Py_Nodes,'Links':Py_Links}

    return Data2