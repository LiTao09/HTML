import cx_Oracle as orl
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'   #？？？

def getconn():                      #连接函数，但是要从ini文件取出地址
    return orl.connect(getdns() ) 

def getdns():
    path=os.path.dirname(__file__)  #文件路径
    ini=os.path.join(path,'db.ini') #文件路径下的db.ini名称的文件
    file=open(ini,'r')              #打开文件ini并执行read
    data=file.readline()            #读取文件下第一行
    at=data.find('=')               #找到=位置
    url=data[at+1::]                #url取值=+1后面所有
    file.close()                    #关闭文件
    return url                      #返回url

def login(user_name,pwd):            #开始函数，从形参取sql数值，返给select函数    
    sql='select * from users where user_name=:user_name and pwd=:pwd and account_state=1'
    return select(sql,one=False,user_name=user_name,pwd=pwd)

def listtypes():
    sql='select * from types'
    return select(sql,False)

def select(sql,one=True,**arg):
    print(one)
    data=None
    try:
        conn=getconn()
        cur=conn.cursor()
        cur.execute(sql,arg)     #arg必须是字典，**arg保证{user_name:user_name,pwd:pwd}
        if one:                  #若是one=true,则是单条数据，则取为元组即可   
            data=cur.fetchone()
        else:                    #若是one=false,则是多条数据，则取为字典   
            data=cur.fetchall()       
        conn.commit()            #提交
        print(data)
    except Exception as identifier :    #前面出错则回滚
        if conn :
            conn.rollback()
        print(identifier)
    finally:                 #最后关闭数据库连接
        if cur:
            cur.close()
        if conn:
            conn.close()
    return data
    
if __name__=='__main__':
    print(getdns())


