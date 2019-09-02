from flask import Flask, render_template, request, session, Response, redirect,jsonify #导入session机制
import db 
from datetime import timedelta  #导入session时间机制
import random   #导入随机数


app = Flask(__name__)

app.config['SECRET_KEY']='123456'   #设置为24位的安全码,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(minutes=60) #设置session的保存时间。
#session是一种机制，持续一段时间内保存用户信息的机制，需要服务器和浏览器相互配合才能实现，服务器端还会开辟一个存储空间，存储用户放的信息

#在客户端体现在一个cookise语言的id号，服务端为内存空间，可以保存getsession的ID，回话不消失则信息保留，除非手动消除，关闭网页
#识别用户，保存数据，但是时间为我们设置的时间，或者浏览器关闭前

@app.route('/', methods=['GET'])
def index():
    code = getcode()                 #定义一个code随机数
    session['code']=code             #在session中加一个code，并将值给他
    return render_template('/login.html', code=code)  #将code带到页面中


@app.route('/main')
def main():
    userInfo = session.get('userInfo')  #取出session中的userInfo的数值
    if userInfo:
        return render_template('/main.html')
    else:
        return redirect('/')

@app.route('/type',methods=['GET'])
def typehtml():
    types = db.listtypes()  
    print(types)
    return render_template('/type.html', types=types)


@app.route('/addtype', methods=['POST'])  #ajax
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
    data=db.addtype(typ,parent) 
    if db.addtype(typ,parent):
        return jsonify({'result':"ok",'typeName':data[1],'id':data[0]})  #返回复杂数据，字典
    else:
        return jsonify({'result':"fald"})

@app.route('/searchTypeList', methods=['POST'])
def searchTypeList():
    key=request.values.get('key')
    page=request.values.get('page')
    size=request.values.get('size')
    data=None
    if key:
        data=db.searchTypes(key)
    else:
        data=db.listAllTypes(int(page),int(size))
    return jsonify(data)


@app.route('/login', methods=['POST'])
def login():
    try:
        code = request.values.get('code')   #取出网页输入的code
        scode = session.get('code')         #取出session中的code，这就是为什么赋值给session的原因
        if code == scode:
            userName = request.values.get('userName')
            pwd = request.values.get('pwd')
            data = db.login(userName, pwd)
            if data:
                session['userInfo']=data  #session字典赋值，将用户信息传给session['userInfo'],取值则用session.get('userInfo')
                return redirect('/main')
            else:
                return render_template('/login.html', msg='登录失败，重试。')
        else:
            code = getcode()        #如果验证码不正确，则在重新定义code随机数
            session['code']=code    #将随机数再存储到session['code']
            return render_template('/login.html', msg='校验码不正确。', code=code)#返回login网页，msg数据，code网页中显示的数值
    except Exception as ex:
        print(ex)
        return 'error'
    
# @app.route('/delType')
# def delType():

#                             #3

def getcode():                           #产生随机数
    ran = random.randint(10000,100000)   #产生int
    return str(ran)                      #返回str字符串


if __name__ == "__main__":
    app.run(debug=True)