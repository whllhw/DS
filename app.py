#coding:utf-8
from flask import  Flask,render_template,url_for,g,request,jsonify,Response,flash,abort
from database import db
import sqlite3

app = Flask(__name__)
db_connect = sqlite3.connect('sqlite.db')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
cur = db_connect.cursor()

@app.route('/')
def home():
    #return render_template('Home.html')
    return render_template('index.html')
@app.route('/tmp')
def test():
    return render_template('temp.html')
@app.route('/input')
def input():
    return render_template('Input.html')

@app.route('/cal')
def cal():
    return render_template('Calculate.html')

@app.route('/result')
def result():
    return render_template('Result.html')

@app.route('/forget')
def forget():
    return render_template('Find_Password.html')

@app.route('/sign')
def sign():
    return  render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/api/nodes',methods=['POST','PUT'])
def addNode():
    if not request.form:
        abort(503)
    data = request.form
    dic = data
    print(dic)
    if request.method == 'PUT':
        try:
            cur.execute('update nodes set name = ? ,note = ? ,uid = ? where id = ?',
                [
                dic['nodeName'],
                dic['note'],
                dic['uid'],
                dic['id']]
                )
            db_connect.commit()
        except IOError:
            pass
        return '',204
    try:
        cur.execute('insert into nodes(uid,name,note) values (?,?,?)',
            [dic['uid'],
            dic['nodeName'],
            dic['note']]
            )
        db_connect.commit()
    except IOError:
        print(e)
        abort(500,str(e))
    return '',204

@app.route('/api/nodes',methods=['GET'])
def getNode():
    temp = []
    orderColumns = request.args['columns['+request.args['order[0][column]']+'][data]'].replace('nodeName','name')
    cur.execute(r"select * from V_nodes where "
                    "id like '%{name}%' or name like '%{name}%'"
                    " or note like '%{name}%' or uid like '%{name}%' "
                    "ORDER BY {column} {d} LIMIT {length} OFFSET {start}".format(
            name=request.args['search[value]'],
            column=orderColumns,
            d=request.args['order[0][dir]'],
            length=request.args['length'],
            start=request.args['start']
        ))
    data = cur.fetchall()
    length = len(data)
    temp = [{'id':i[0],'nodeName':i[1],'note':i[2],'uid':i[3],'ES':'','LS':''} for i in data]

    return jsonify({
        "draw":request.args['draw'],
        "recordsTotal":length,
        "recordsFiltered":length,
        "data":temp})

@app.route('/api/nodes/<string:id>/',methods=['DELETE'])
def removeNode(id):
    try:
        cur.execute('delete from edges where head = ? or tail = ?',[id,id])
        cur.execute('delete from nodes where id = ?',[id])
        db_connect.commit()
    except IOError:
        pass
    return '',204

@app.route('/api/edges',methods=['POST','PUT'])
def addEdge():
    data = request.form
    print(data)
    assert data
    if request.method == 'PUT':
        try:
            cur.execute('update edges set head=?,tail=?,duration=?,note=?,name=? where id=?',
                        [data['head'],
                        data['tail'],
                        data['duration'],
                        data['note'],
                        data['name'],
                        data['id']])
            db_connect.commit()
        except IOError:
            pass
        return '',204
    try:
        cur.execute('insert into edges(head,tail,duration,note,name)'
                    'values (?,?,?,?,?)',
                    [data['head'],
                    data['tail'],
                    data['duration'],
                    data['note'],
                    data['name']])
        db_connect.commit()
    except IOError: # 注意外键约束！！
        pass
    return '',204

@app.route('/api/edges',methods=['GET'])
def getEdge():
    try:
        orderColumns = request.args['columns['+request.args['order[0][column]']+'][data]'].replace('nodeName','name')
        cur.execute(r"select * from V_edges where "
            "duration like '%{name}%' or id like '%{name}%' "
            "or head like '%{name}%' or tail like '%{name}%' "
            "or name like '%{name}%' or note like '%{name}%' "
            "ORDER BY {column} {d} LIMIT {length} OFFSET {start}".format(
            name=request.args['search[value]'],
            column=orderColumns,
            d=request.args['order[0][dir]'],
            length=request.args['length'],
            start=request.args['start']
        ))
        data = cur.fetchall()
        length = len(data)
        temp = [{
                    'id':i[5],
                    'head':i[0],
                    'tail':i[1],
                    'duration':i[2],
                    'note':i[3],
                    'name':i[4],
                    'EF':'',
                    'LF':'',
                    'FF':'',
                    'Is_Critcal_Path':'',
                    'TF':'',
                    'ES':'',
                    'LS':''
                } for i in data]
    except IOError:
        pass
    return jsonify({
        "draw":request.args['draw'],
        "recordsTotal":length,
        "recordsFiltered":length,
        "data":temp
        })

@app.route('/api/edges/<string:id>/',methods=['DELETE'])
def removeEdge(id):
    try:
        cur.execute('delete from edges where id = ?',[
            id])
        db_connect.commit()
    except IOError:
        pass
    return '',204

@app.route('/api/result')
def getResult():
    import database2
    database2.LetGo()

    temp = []
    try:
        orderColumns = request.args['columns['+request.args['order[0][column]']+'][data]'].replace('nodeName','name')
        cur.execute(r"select id,name,note,uid,ES,LS from nodes2 where "
            "id like '%{name}%' or name like '%{name}%' "
            "or note like '%{name}%' or uid like '%{name}%' "
            "ORDER BY {column} {d} LIMIT {length} OFFSET {start}".format(
            name=request.args['search[value]'],
            column=orderColumns,
            d=request.args['order[0][dir]'],
            length=request.args['length'],
            start=request.args['start']
            ))
        # id , name, note ,uid
        data = cur.fetchall()
        length = len(data)
        temp = [{'id':i[0],'nodeName':i[1],'note':i[2],'uid':i[3],'ES':i[4],'LS':i[5]} for i in data]
    except IOError:
        pass

    return jsonify({
        "draw":request.args['draw'],
        "recordsTotal":length,
        "recordsFiltered":length,
        "data":temp
    })

@app.route('/api/resultEdge')
def getResultEdge():
    try:
        orderColumns = request.args['columns['+request.args['order[0][column]']+'][data]'].replace('nodeName','name')
        cur.execute(r"select id,uid,head,tail,duration,"
            "note,name,ES,LS,TF,Is_Critcal_Path,EF"
            ",LF,FF,Cal_ID "
            "from edges2 where "
            "duration like '%{name}%' or id like '%{name}%' "
            "or head like '%{name}%' or tail like '%{name}%' "
            "or name like '%{name}%' or note like '%{name}%' "
            "ORDER BY {column} {d} LIMIT {length} OFFSET {start}".format(
            name=request.args['search[value]'],
            column=orderColumns,
            d=request.args['order[0][dir]'],
            length=request.args['length'],
            start=request.args['start']
        ))
        data = cur.fetchall()
        length = len(data)
        temp = [{
                        'id':i[0],
                        'uid':i[1],
                        'head':i[2],
                        'tail':i[3],
                        'duration':i[4],
                        'note':i[5],
                        'name':i[6],
                        'ES':i[7],
                        'LS':i[8],
                        'TF':i[9],
                        'Is_Critcal_Path':i[10],
                        'EF':i[11],
                        'LF':i[12],
                        'FF':i[13],
                        'Cal_ID':i[14]
                    } for i in data]
    except IOError:
        pass

    return jsonify({
        "draw":request.args['draw'],
        "recordsTotal":length,
        "recordsFiltered":length,
        "data":temp
        })

if __name__=='__main__':

    app.run()
    db_connect.close()