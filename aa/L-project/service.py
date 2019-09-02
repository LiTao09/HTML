from flask import Flask,render_template,request,session,Response,jsonify,redirect
import sql
from datetime import timedelta
import random

#创建flask应用对象
wu=Flask(__name__)

wu.config['SECRET_KEY']='123456'
wu.config['PERMANENT_SESSION_LIFETIME']=timedelta(minutes=60)
def getcode():
    return str(random.randint(10000,100000))

@wu.route('/',methods=['GET'])
def index():
    code=getcode()
    session['code']=code
    return render_template('/login.html',code=code)

@wu.route('/main')
def main():
    info=session.get('data')
    if info:
        return render_template('/main.html',info=info)
    else:
        return redirect('/')

@wu.route('/type',methods=['GET'])
def typehtml():
    types=sql.listtypes()
    return render_template('/type.html',types=types)

@wu.route('/addtype', methods=['POST'])  #ajax
def addtype():
    typ = request.values.get('type')
    parent = request.values.get('parent')
    if parent:
        array = parent.split(':')   #将parent的数据进行分离，成['xxx','1']
        if array[1]:
            parent = int(array[1])  #取第二个数值并显示为int型
        else:
            parent = None
    else:
        parent = None
    # add to DB
        return jsonify({'result':"ok"})  #返回复杂数据，字典
    

@wu.route('/login',methods=['POST'])
def login():
    try:
        code=request.values.get('code')
        scode=session.get('code')
        if code==scode:
            userName=request.values.get('userName')
            pwd=request.values.get('pwd')
            data=sql.login(userName,pwd)
            if data:
                session['data']=data
                return redirect('/main')
            else:
                return render_template('/login.html',msg='登录失败，请重试')
        else:
            code=getcode()
            session['code']=code
            return render_template('/login.html',msg='验证码错误',code=code)
    except Exception as ex :
        print(ex)
        return 'error'



#入口函数
if __name__ == "__main__":
    wu.run(debug=True,port=80)          #开启调试
