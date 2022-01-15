from flask import request,Flask,render_template,redirect
import pymysql

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='wadrbaw74560',
                     database='huixuanjiasu_test')

# 创建Flask对象app
app = Flask(__name__)

@app.route('/')
def login_form():
    return render_template('user/log_in.html')


# 处理用户登录逻辑
@app.route('/log_in', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(type(username),type(password))

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # 判断用户和密码是否在数据库中
    user_passwd = "SELECT * from user_passwd where `user`='%s' AND `password`=%s" % (str(username),password)
    cursor.execute(user_passwd)
    res_user_passwd = cursor.fetchall()

    # 关闭数据库连接
    db.close()

    #判断登录的用户是否和查询的用户信息一致
    if res_user_passwd[0][0]==username and res_user_passwd[0][1]==int(password):
        #计算器功能

        return redirect('/calculator')

@app.route('/sign_up', methods=['POST'])
def sign_up():
    username = request.form['username']
    password = request.form['password']

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # 判断用户名是否重复
    user_isrepeat = "SELECT user from user_passwd where `password`=%s"%password

    cursor.execute(user_isrepeat)

    res_user = cursor.fetchall()

    if res_user[0][0]==username:
        return render_template('user/sign_up.html', username=username, error='用户名已经存在')
    else:
        # SQL 插入语句
        sql = "INSERT INTO user_passwd(user,password)VALUES ('%s', '%s')" % (username, password)

        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()

        # 关闭数据库连接
        db.close()

        # 注册成功后重定向到登录页面
        return redirect('/')

# 用户注册页面
@app.route('/sign_up_form')
def sign_up_form():
    return render_template('user/sign_up.html')

# 跳回用户登录页面
@app.route('/relog_in')
def relogin_form():
    return render_template('user/log_in.html')


@app.route('/calculator')
def calculator():
    return render_template('calculator/calculator.html')

@app.route('/calculator_jisuan', methods=['POST'])
def calculator_jisuan():
    num1 = request.form['num1']
    num2 = request.form['num2']
    ca = request.form['ca']
    print(num1,num2,ca)
    if ca=="+":
        return str(int(num1)+int(num2))
    elif ca=="-":
        return str(int(num1)-int(num2))
    elif ca=="*":
        return str(int(num1)*int(num2))
    elif ca=="/":
        return str(int(num1)/int(num2))
    else:
        return '运算符号非法输入'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8001')