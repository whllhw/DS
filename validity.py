import numpy as np
Py_N=np.array([ [ 1,0,0 ],
                [ 2,0,0 ],
                [ 4,0,0 ],
                #[4,0,0 ],
                [ 9,0,0 ],
                [ 8,0,0 ],
                [ 7,0,0 ],
                #[7,0,0 ],
                [ 5,0,0 ],
                [ 3,0,0 ],
                [ 6,0,0 ] ])
Py_L=np.array([ [ 1,2,6,0,0,0,0,0,0,0 ],
                [ 1,3,4,0,0,0,0,0,0,0 ],
                [ 1,4,5,0,0,0,0,0,0,0 ],
                [ 2,5,1,0,0,0,0,0,0,0 ],
                [ 3,5,1,0,0,0,0,0,0,0 ],
                [ 4,6,3,0,0,0,0,0,0,0 ],
	        [ 5,7,9,0,0,0,0,0,0,0 ],
                [ 5,8,7,0,0,0,0,0,0,0 ],
                #[ 5,1,4,0,0,0,0,0,0,0 ],
                [ 6,8,4,0,0,0,0,0,0,0 ],
                [ 7,9,2,0,0,0,0,0,0,0 ],
                [ 8,9,4,0,0,0,0,0,0,0 ] ])
#None无返回值 合法
#不合法，返回一个元组
#返回ID[0]=1 输入了重复的代号（结点） ID[1]为已经删除所有重复结点的Py_N
#ID[0]=2 输入了重复的工作（边）
#ID[0]=3 有多个起点
#ID[0]=4 有多个终点
#ID[0]=5 图中有环
def validity(Py_N,Py_L):
    #判断是否有重复的结点，若有返回（1，Py_N）
    flag=[]
    #不能在循环里动态删除列表
    for i in range(Py_N.shape[0]):
        if list(Py_N[:,0]).count(Py_N[i,0])>1:
            #Py_N=np.delete(Py_N,i,0)
            flag.append(i)
    Py_N=np.delete(Py_N,flag,0)
    if flag:
        return (1,Py_N)
    #判断是否有重复的边
    #创建一个key：前驱结点，value：后继结点的列表
    Next=dict((i,[]) for i in Py_N[:,0])
    for i in range(Py_L.shape[0]):
        Next[Py_L[i,0]].append(Py_L[i,1])
    for i in Py_N[:,0]:
        for j in Next[i]:
            if Next[i].count(j)>1:
                return (2,)
                #print("有重复的边")
    #——————
    InDegree=dict((i,0) for i in Py_N[:,0])
    OutDegree=dict((i,0) for i in Py_N[:,0])
    for i in Py_L[:,1]:
        InDegree[i]+=1
    for i in Py_L[:,0]:
        OutDegree[i]+=1
    #>=1
    if list(InDegree.values()).count(0)>1:
        return (3,)
        #print("有多个起点")
    elif list(OutDegree.values()).count(0)>1:
        return (4,)
        #print("有多个终点")
    #入度为0的顶点<=1或出度为0的顶点<=1
    else:
        #入度为0的结点
        InDegree_0=[i for i in Py_N[:,0] if InDegree[i]==0]
        count=0
        while InDegree_0:
            temp=InDegree_0.pop()
            count+=1
            for i in range(Py_L.shape[0]):
                if Py_L[i,0]==temp:
                    InDegree[Py_L[i,1]]-=1
                    if InDegree[Py_L[i,1]]==0:
                        InDegree_0.append(Py_L[i,1])
        if count<len(Py_N[:,0]):
            return (5,)
            #print("图中有环")

#虚箭线

ID=validity(Py_N,Py_L)
##如果不合法
#if ID:
#    print(ID[0])
#    #如果Py_N发生变化
#    if ID[0]==1:
#        print(ID[1])
