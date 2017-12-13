import sqlite3

class db():
    _instance = None
    def __init__(self):
        pass
    @property
    def connect(self, *args, **kwargs):
        if not hasattr(self,'db'):
            setattr(self,'db',sqlite3.connect('sqlite.db'))
        return self.db

    @property
    def cursor(self):
        return self.connect.cursor()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(db,cls).__new__(cls,*args,**kwargs)
        return cls._instance
def init():
    b = db()
    connect = b.connect
    cur = b.cursor

    cur.execute('create table nodes ('
                'id integer primary key AUTOINCREMENT,'
                'uid varchar(10) unique,'
                'name text default 0,'
                'note text default 0,'
                'Cal_ID INTEGER default -1 '
                ')')

    cur.execute('create table edges ('
                'id integer primary key AUTOINCREMENT,'
                'uid varchar(10) unique,'
                'head varchar(10) ,'
                'tail varchar(10) ,'
                'duration varchar(10) default 0 ,'
                'note text default 0,'
                'name text default 0,'
                'Cal_ID INTEGER default -1, '
                'foreign key(head) references nodes(id),'
                'foreign key(tail) references nodes(id)'
                ')')

    cur.execute('create table nodes2 ('
                'id integer primary key AUTOINCREMENT,'
                'uid varchar(10) unique,'
                'name text not null,'
                'note text,'
                'ES varchar(10),'
                'LS varchar(10),'
                'Cal_ID INTEGER default -1 '
                ')')
    cur.execute('create table edges2 ('
                'id integer primary key AUTOINCREMENT,'
                'uid varchar(10) unique,'
                'head varchar(10) ,'
                'tail varchar(10) ,'
                'duration varchar(10) default 0 ,'
                'note text,'
                'name text,'
                'ES varchar(10),'
                'LS varchar(10),'
                'TF varchar(10),'
                'Is_Critcal_Path BOOLEAN,'
                'EF varchar(10),'
                'LF varchar(10),'
                'FF varchar(10),'
                'Cal_ID INTEGER default -1, '
                'foreign key(head) references nodes(uid),'
                'foreign key(tail) references nodes(uid)'
                # 'primary key(head,tail)'
                ')')
    cur.execute('create view V_nodes as '
                'select id , name, note, uid '
                'from nodes')
    cur.execute('create view V_edges as '
                'select head,tail,duration,note,name,id,uid '
                'from edges')

    cur.close()
    connect.commit()
    connect.close()

if __name__ == '__main__':
    init()
