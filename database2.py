import sqlite3
import numpy as np

#如果用户中途退出程序，我的数据库并不会把他输入的信息清空

db_connect = sqlite3.connect('sqlite.db')
cur = db_connect.cursor()

def Init_Data():
    cur.execute('Delete  From nodes')
    cur.execute('Delete From nodes2')
    cur.execute('Delete From edges')
    cur.execute('Delete From edges2')

    cur.executemany('Insert Into nodes(id,name)'
                'Values(?,?)',
                        [   ('1','1'),
                            ('2','2'),
                            ('3','3'),
                            ('5','5'),
                            ('8','8'),
                            ('7','7'),
                            ('9','9'),
                            ('4','4'),
                            ('6','6') ]
                )
    db_connect.commit()

    cur.executemany('Insert Into edges(head, tail,duration)'
                'Values(?,?,?)',
                        [( '1' , '2' , '6' ),
                         ( '1' , '3' , '4' ),
                         ( '1' , '4' , '5' ),
                         ( '2' , '5' , '1' ),
                         ( '3' , '5' , '1' ),
                         ( '4' , '6' , '3' ),
                         ( '5' , '7' , '9' ),
                         ( '5' , '8' , '7' ),
                         ( '6' , '8' , '4' ),
                         ( '7' , '9' , '2' ),
                         ( '8' , '9' , '4' )
                         ]
                )
    db_connect.commit()




#从网页获取信息储存，汉文已经写了
#输入和返回值均为字符串
def Get_Data2Cal(Cal_id='-1'):
    #id name note
    Cal_id2=str(Cal_id)

    cur.execute('Select head,tail,duration From edges '
                'where Cal_ID=?',[Cal_id2])

    Links=cur.fetchall()

    cur.execute('Select name From nodes '
                'where Cal_ID=?',[Cal_id2]
                )
    Nodes=cur.fetchall()

    Datas={'Nodes':Nodes,'Links':Links}

    return Datas

def Put_Result2DB(Datas):
    cur.executemany('Insert Into nodes2(id,name,note,ES,LS)'
                    'Values(?,?,?,?,?)',
                    Datas['Nodes']
                    )
    cur.executemany('Insert Into edges2(id,head,tail,duration,note,name,ES,LS,TF,Is_Critcal_Path,EF,LF,FF)'
                    'Values(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    Datas['Links']
                    )
    pass

def Cal(Datas1):
    Links1 = Datas1['Links']
    Nodes1 = Datas1['Nodes']

    Links_np = np.asarray(Links1, 'float')
    Nodes1_np = np.asarray(Nodes1, 'float')

    LenL = Links_np.shape[0]
    LenN = Nodes1_np.shape[0]

    Links_C = np.zeros((LenL, 10))
    Nodes_C = np.zeros((LenN, 3))

    for i in range(0, 3):
        Links_C[:, i] = Links_np[:, i]

    for i in range(0, 1):
        Nodes_C[:, i] = Nodes1_np[:, i]

    Input = {'Nodes': Nodes_C, 'Links': Links_C}

    import To_C
    Re1 = To_C.Cal(Input)
    Nodes_C2 = Re1['Nodes']
    Links_C2 = Re1['Links']

    Nodes_np = np.asarray(Nodes_C2, '<U1')
    Links_np = np.asarray(Links_C2, '<U1')

    Re2 = {'Nodes': Nodes_C2, 'Links': Links_C2}
    return Re2

def Invalid(Datas1):
    Links1 = Datas1['Links']
    Nodes1 = Datas1['Nodes']

    Links_np = np.asarray(Links1, 'float')
    Nodes1_np = np.asarray(Nodes1, 'float')

    LenL = Links_np.shape[0]
    LenN = Nodes1_np.shape[0]

    Links_C = np.zeros((LenL, 10))
    Nodes_C = np.zeros((LenN, 3))

    for i in range(0, 3):
        Links_C[:, i] = Links_np[:, i]

    for i in range(0, 1):
        Nodes_C[:, i] = Nodes1_np[:, i]

    import validity
    flag=validity.validity(Nodes_C,Links_C)
    return flag

def LetGo():
    Init_Data()
    #Cal_ID2 = str(Cal_ID)
    #cur.execute('Select id From nodes Where Cal_ID=?',[Cal_ID])
    G_Cal_ID=0

    Datas1 = Get_Data2Cal('-1')
    check=Invalid(Datas1)
    if check:
        return check
        pass
    else:
        Data_Re=Cal(Datas1)
        G_Cal_ID=G_Cal_ID+1

#从输入表抽取信息
#准备工作
    cur.execute('Update nodes Set Cal_ID=?'
                'Where Cal_ID=?', [G_Cal_ID,-1])
    db_connect.commit()

    cur.execute('Update edges Set Cal_ID=?'
                'Where Cal_ID=?', [G_Cal_ID,-1])
    db_connect.commit()

#从输入表拷贝信息
# 点
    cur.execute('Select id,uid,name,note,Cal_ID From nodes '
                'where Cal_ID=?',[G_Cal_ID])

    N1=cur.fetchall()
    cur.executemany('Insert Into nodes2(id,uid,name,note,Cal_ID)'
                'Values (?,?,?,?,?)',N1)
    db_connect.commit()


#边
    cur.execute('Select id,uid,head,tail,duration,note,name,Cal_ID From edges '
                'where Cal_ID=?', [G_Cal_ID])

    L1=cur.fetchall()
    cur.executemany('Insert Into edges2(id,uid,head,tail,duration,note,name,Cal_ID)'
                'Values (?,?,?,?,?,?,?,?)',L1)
    db_connect.commit()

#录入计算信息
    Nodes=Data_Re['Nodes']
    Links=Data_Re['Links']

    Up_Nodes=np.zeros(Nodes.shape,'float')
    Up_Links=np.zeros(Links.shape,'float')
    Up_Nodes[:,0]=Nodes[:,1]
    Up_Nodes[:,1]=Nodes[:,2]
    Up_Nodes[:,2]=Nodes[:,0]

    Up_Links[:,0]  = Links[:,3]
    Up_Links[:,1]  = Links[:,4]
    Up_Links[:, 2] = Links[:, 5]
    Up_Links[:, 3] = Links[:, 6]
    Up_Links[:, 4] = Links[:, 7]
    Up_Links[:, 5] = Links[:, 8]
    Up_Links[:, 6] = Links[:, 9]
    Up_Links[:, 7] = Links[:, 2]
    Up_Links[:, 8] = Links[:, 0]
    Up_Links[:, 9] = Links[:, 1]



    cur.executemany('Update nodes2 Set ES=?,LS=?'
                'Where id=?',Up_Nodes.tolist())

    db_connect.commit()


    cur.executemany('Update edges2 Set ES=?,LS=?,TF=?,Is_Critcal_Path=?,EF=?,LF=?,FF=?,duration=?'
                    'where  cast(head as float)=? and cast(tail as float)=?',Up_Links.tolist()
                    )
    db_connect.commit()



#if __name__ == '__main__':
#    pass
