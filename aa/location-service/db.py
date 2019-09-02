import cx_Oracle as orl
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  

def getconn():
    dns = getdns()
    return orl.connect(dns)


def login(user_name, pwd):
    sql = 'select * from users where user_name=:user_name and pwd=:pwd and account_state=1'
    return select(sql, one=False, user_name=user_name, pwd=pwd)


def listtypes():
    sql = 'select * from types'
    return select(sql,False)

def addtype(typename,parentID):
    sql='insert into types(id ,type_name,parent_id) values(:id,:typename,:parentID)'
    id=select('select seq_sequence.nextval from dual')
    if update(sql,id=id,type_name=typename,parent_id=parentID):
        return id,typename,parentID  #当语句有多个返回值时，返回值的形式是元组
    else:
         return None               

def listAllTypes(page,size):
    sql='select * from (select rownum ro,t.* from  (select * from types order by id desc) t \
        where ROWNUM<=:max) where ro>:min'   
    return select(sql,False,max=page*size,min=(page-1)*size)


def delType(id):
    sql='delete from types where id=:id' 
    return update(sql,id=id)

def searchTypes(key):
    sql='select *  from types where type_name=:key'
    return select(sql,False,key=key)

def update(sql,**arg):      #更新数据库
    ok=True
    try:
        conn=getconn()
        cursor=conn.cursor()
        cursor.execute(sql,arg)
        conn.commit()
    except expression as identifier:
        ok=False
        conn.rollback()
        print('error')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return ok                 


def select(sql, one=True, **arg):    #查
    data = None
    try:
        conn = getconn()
        cur = conn.cursor()
        cur.execute(sql, arg)
        if one:
            data = cur.fetchone()
        else:
            data = cur.fetchall()
        conn.commit()
        print(data)
    except Exception as identifier:
        if conn:
            conn.rollback()
        print(identifier)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return data




# def sum(a, b, *c, **d):
#     print(d)
#     result = 0
#     result += (a+b)
#     for i in c:
#         result += i
#     for i in d.keys():
#         result += d.get(i)
#     return result




def getdns():       #ini路径
    path = os.path.dirname(__file__)
    ini = os.path.join(path, 'db.ini')
    file = open(ini, 'r')
    data = file.readline()
    at = data.find('=')
    url= data[at+1::]
    file.close()
    return url

if __name__=='__main__':
    print(getdns())


